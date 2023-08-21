#!/bin/bash
set -e
imageName="researcher-portal-backend"

# cd /app || exit

# Start the nginx server
# nginx -g 'daemon off;' 2>&1 | tee /nginx.log &

# mv /decrypt_file.py ./decrypt_file.py

# Use the InitializationVector to get the connection string of the dataset
datasetStoragePassword=$(cat InitializationVector.json | jq -r '.dataset_storage_password')
storageAccountName=$(cat InitializationVector.json | jq -r '.storage_account_name')

# Use the InitializationVector to populate the IP address of the audit services
auditIP=$(cat InitializationVector.json | jq -r '.audit_service_ip')

mountDir="/mnt/azure"
sudo mkdir -p $mountDir

if [ ! -d "/etc/smbcredentials" ]; then
    sudo mkdir /etc/smbcredentials
fi

if [ ! -f "/etc/smbcredentials/$storageAccountName.cred" ]; then
    echo "username=$storageAccountName" | sudo tee -a /etc/smbcredentials/$storageAccountName.cred
    echo "password=$datasetStoragePassword" | sudo tee -a /etc/smbcredentials/$storageAccountName.cred
fi

sudo chmod 600 /etc/smbcredentials/$storageAccountName.cred

# Function that takes in the dataset id, version id and key as arguments and mounts the dataset
mount_datasets() {
  datasetId="$1"
  datasetVersionId="$2"
  datasetKey="$3"
  datasetDir="/data/$datasetId"

  echo "id: $datasetId, version_id: $datasetVersionId"

  echo "//$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir cifs nofail,credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30" | sudo tee -a /etc/fstab
  sudo mount -t cifs //$storageAccountName.file.core.windows.net/$datasetId/$datasetVersionId $mountDir -o credentials=/etc/smbcredentials/$storageAccountName.cred,dir_mode=0777,file_mode=0777,serverino,nosharesock,actimeo=30

  # Create a folder for the dataset
  sudo mkdir -p $datasetDir

  # Unzip the dataset_{dataset_version_id} file
  sudo unzip $mountDir/dataset_$datasetVersionId -d $datasetDir

  # Decrypt the dataset_content file
  aesTag=$(sudo cat $datasetDir/dataset_header.json | jq -r '.aes_tag')
  aesNonce=$(sudo cat $datasetDir/dataset_header.json | jq -r '.aes_nonce')

  sudo python3 decrypt_file.py -i $datasetDir/data_content.zip -o $datasetDir/data_content.zip -k $datasetKey -n $aesNonce -t $aesTag
}

# get list of datasets in the InitializationVector
jq -r '.datasets[] | "\(.id) \(.version_id) \(.key)"' < InitializationVector.json |
while read -r id version_id key; do
  # Call the get_data function with the id and version_id values as arguments
  mount_datasets "$id" "$version_id" "$key"
done

sudo chmod 744 /data

# Start the Public API Server
uvicorn app.main:server --host 0.0.0.0 --port 8000

# To keep the container running
tail -f /dev/null