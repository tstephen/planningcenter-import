"""
test_planning_center_import.py
"""
import os
from urllib.error import HTTPError
#from unittest.mock import MagicMock, patch
import logging
from logging import DEBUG
import os
import re
import ssl
import urllib.error
import urllib.request
from json import loads, load, dump

from planningcenter_import.planningcenter_client import PlanningCenterClient

logger = logging.getLogger(__name__)

import pytest

@pytest.fixture(name="planningcenter", scope="session")
def init_planningcenter_client():
    logging.basicConfig(level=DEBUG)

    application_id:str|None =os.getenv("PC_APP_ID")
    secret = os.getenv("PC_SECRET")
    if application_id is None:
         raise ValueError("must specify environment variable PC_APP_ID")
    if secret is None:
         raise ValueError("must specify environment variable PC_SECRET")

    return PlanningCenterClient(application_id, secret) 

def test_get_organization(planningcenter: PlanningCenterClient):
    """ test can get organization for the account  """
    organization = planningcenter.get_organization()
    if os.getenv("PC_ORG_NAME"):
        assert organization == os.environ["PC_ORG_NAME"]

def test_get_service_types(planningcenter: PlanningCenterClient):
    """ test can get service types  """
    service_types = planningcenter.get_service_types()
    assert len(service_types) > 0
    if os.getenv("PC_SERVICE_TYPE_NAME"):
        service_type = [st for st in service_types
                         if st["attributes"]["name"] == os.environ["PC_SERVICE_TYPE_NAME"]]
        assert len(service_type) == 1
        logger.info("service type id: %s", service_type[0]["id"])

@pytest.mark.skipif("PC_SERVICE_TYPE_NAME" not in os.environ, reason="PC_SERVICE_TYPE_NAME not in environment")
def test_get_plans(planningcenter: PlanningCenterClient):
    """ test can get plan """
    service_types = planningcenter.get_service_types()
    service_type = [st for st in service_types
                     if st["attributes"]["name"] == os.environ["PC_SERVICE_TYPE_NAME"]]
    logger.info("service type id: %s", service_type[0]["id"])
    plans = planningcenter.get_plans_by_service_type(service_type_id=service_type[0]["id"])
    logger.info("available plans: %s", [plan["attributes"]["dates"] for plan in plans])
    print(f"available plans: {[plan['attributes']['dates'] for plan in plans]}")
    assert len(plans) > 0
    if os.getenv("PC_PLAN_DATE"):
        plan = [plan for plan in plans
                         if plan["attributes"]["dates"] == os.environ["PC_PLAN_DATE"]]
        assert len(plan) == 1
        logger.info("plan: %s", plan[0]["id"])

        plan_items = planningcenter.get_plan_items(service_type[0]["id"], plan[0]["id"])
        sort_date = plan[0]['attributes']['sort_date']
        with open(f"{sort_date[0:sort_date.rfind('T')]}.json", 'w') as outfile:
            dump(plan_items, outfile, indent=2)

@pytest.mark.skipif("PC_SONG_ID" not in os.environ, reason="PC_SONG_ID not in environment")
def test_get_song(planningcenter: PlanningCenterClient):
    """ test can get song """
    song = planningcenter.get_song(os.environ["PC_SONG_ID"])
    with open(f"{song['attributes']['title']}.json", 'w') as outfile:
        dump(song, outfile, indent=2)
    song_arrangements = planningcenter.get_song_arrangements(os.environ["PC_SONG_ID"])
    print(song_arrangements)
    with open(f"{song['attributes']['title']}-arramgements.json", 'w') as outfile:
        dump(song_arrangements, outfile, indent=2)
    song_attachments = planningcenter.get_song_attachments(os.environ["PC_SONG_ID"])
    print(song_attachments)
    with open(f"{song['attributes']['title']}-attachments.json", 'w') as outfile:
        dump(song_attachments, outfile, indent=2)