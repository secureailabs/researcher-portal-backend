# -------------------------------------------------------------------------------
# Engineering
# decrypt_file.py
# -------------------------------------------------------------------------------
"""Utility to decrypted files encrypted using AES-GCM scheme"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------
from Crypto.Cipher import AES
from base64 import b64decode
from argparse import ArgumentParser


def decrypt_file(decrypt_params):
    # Read a encrypted file
    with open(decrypt_params.encrypted_file, "rb") as f:
        encrypted_data = f.read()

        # Convert the key and nonce to bytes
        key = b64decode(decrypt_params.key)
        nonce = b64decode(decrypt_params.nonce)
        tag = b64decode(decrypt_params.tag)

        # Decrypt
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        decrypted = cipher.decrypt_and_verify(encrypted_data, received_mac_tag=tag)  # type: ignore

        # Write to the output file
        with open(decrypt_params.decrypted_file, "wb") as f:
            f.write(decrypted)


if __name__ == "__main__":
    # Example usage:
    # python3 decrypt_file.py -i data_content.zip -o decrypted.zip -k DhA5lu3lYGnvOIztQn/IGLX6ar1T25AuVaMMuwLuJGs= -n 3YkHgLifydYyXyRW -t 8OXMz8OnsKTmpLrMsYnu9g==
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        dest="encrypted_file",
        required=True,
        help="Encrypted file path",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="decrypted_file",
        required=True,
        help="Decrypted file path",
    )
    parser.add_argument(
        "-k", "--key", dest="key", required=True, help="Base64 encoded key"
    )
    parser.add_argument(
        "-n", "--nonce", dest="nonce", required=True, help="Base64 encoded nonce"
    )
    parser.add_argument(
        "-t", "--tag", dest="tag", required=True, help="Base64 encoded tag"
    )

    args = parser.parse_args()
    decrypt_file(args)
