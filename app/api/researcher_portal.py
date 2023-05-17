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

from fastapi import (
    APIRouter,
    Body,
    status,
)
from app.models.cohort import Cohort
from app.utils.cohort_filter import filtered_cohort
from app.utils.analysis import analysis_function_list, run_analysis

router = APIRouter()


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
    type: str = Body(..., description="Type of analysis"),
    analysis_parameter: dict = Body(..., description="Analysis parameter"),
):
    analysis = run_analysis(type, analysis_parameter)
    return {
        "status": True,
        "data": analysis,
        "message": "Analysis result",
    }


@router.get(
    path="/analysis-functions-list",
    tags=["researcher_portal"],
    description="Get the list of analysis functions",
    status_code=status.HTTP_200_OK,
)
def analysis_functions_list():
    return {
        "status": True,
        "data": analysis_function_list,
        "message": "Analysis functions list",
    }
