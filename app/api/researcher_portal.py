# -------------------------------------------------------------------------------
# Engineering
# dataset_upload.py
# -------------------------------------------------------------------------------
"""APIs to encrypt and upload dataset to azure file share"""
# -------------------------------------------------------------------------------
# Copyright (C) 2022 Secure Ai Labs, Inc. All Rights Reserved.
# Private and Confidential. Internal Use Only.
#     This software contains proprietary information which shall not
#     be reproduced or transferred to other documents and shall not
#     be disclosed to others for any purpose without
#     prior written permission of Secure Ai Labs, Inc.
# -------------------------------------------------------------------------------

import base64
import json
import os
import shutil
import pandas as pd

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile, status
from app.utils.analysis import run_analysis

from app.utils.cohort_filter import filtered_cohort

router = APIRouter()

# temp code to load the data frame
file_path_0 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_0.csv"
file_path_1 = os.path.dirname(os.path.realpath(__file__)) + "/data_frame_1.csv"
df1 = pd.read_csv(file_path_0)
df2 = pd.read_csv(file_path_1)
df = pd.concat([df1, df2])

@router.get("/demo/test")
async def test() -> dict:
    return {"status": True, "data": "Hello World", "message": "Test passed"}

@router.post(
    path="/analysis",
    tags=["researcher_portal"],
    description="Upload a dataset to the Azure File Share",
    status_code=status.HTTP_200_OK,
)
def analysis(
    cohort : dict,
    analysis : dict,
):
    filtered_df = filtered_cohort(df, cohort)
    analysis =  run_analysis(filtered_df, analysis)

    return {"status": True, "data": analysis, "message": "Analysis completed"}
