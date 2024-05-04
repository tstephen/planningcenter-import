"""
test_freeshow.py
"""
import json
import logging
import os

import pytest

from planningcenter_import.freeshow import FreeShow, FreeShowOptions

@pytest.fixture(name="freeshow", scope="session")
def init_freeshow():
    logging.basicConfig(level=logging.DEBUG)

    application_id:str|None = os.getenv("PC_APP_ID")
    secret = os.getenv("PC_SECRET")
    if application_id is None:
         raise ValueError("must specify environment variable PC_APP_ID")
    if secret is None:
         raise ValueError("must specify environment variable PC_SECRET")
    return FreeShow(FreeShowOptions(application_id=application_id,
                                    secret=secret,
                                    verbose="DEBUG"))

def test_freeshow_import_plan(freeshow: FreeShow):
    """
    create a freeshow project based on files previously extract from
    planningcenter based on the following data:
    
    service_type_name = "Neston Sunday Service"
    plan_date = "28 April 2024"
    """
    with open("tests/resources/2024-04-28/plan-2024-04-28-inc-songs.json", 'r') as file:
        plan = json.load(file)
        # plan = plan if type(plan) == "dict" else plan[0]

    file_name = freeshow.transform_plan_to_project(plan)
    print(f"produced file: {file_name}")
