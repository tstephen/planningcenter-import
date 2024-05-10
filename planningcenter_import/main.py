"""
__main__.py
"""
import logging
import os
import sys
from typing import Dict, List

from planningcenter_import.freeshow import FreeShow
from planningcenter_import.planningcenter_client import PlanningCenterClient, PlanningCenterOptions

logger = logging.getLogger(__name__)

def main():
    try:
        options = get_planning_center_options()
        pc = PlanningCenterClient(options)
        print(f"Successfully connected to {pc.get_organization()}")
    except ValueError as err:
        print("Environment variales for PC_APP_ID and PC_SECRET are needed to connect to PlanningCenter")
        sys.exit(0)

    service_types = read_service_types(pc)
    index = get_user_selection(service_types)
    service_type_id = service_types[index]["service_type_id"]
    print(service_type_id)
    plans = read_plans(pc, service_type_id)
    plan_id = plans[get_user_selection(plans)]["plan_id"]
    print(plan_id)
    
    freeshow = FreeShow(options)
    print(freeshow.get_plan_from_planning_center(service_type_id, plan_id))

def get_planning_center_options() -> PlanningCenterClient:
    application_id:str|None = os.getenv("PC_APP_ID")
    secret = os.getenv("PC_SECRET")
    if application_id is None:
         raise ValueError("must specify environment variable PC_APP_ID")
    if secret is None:
         raise ValueError("must specify environment variable PC_SECRET")

    return PlanningCenterOptions()

def get_user_selection(options) -> int:
    for option in options:
        print(f'{option["id"]}: {option["description"]}')
    user_input = int(input("Enter the option number: "))
    logger.info('User selected option: %s', user_input)
    return user_input

def read_service_types(pc: PlanningCenterClient) -> List[Dict[int, str]]:
    service_types = [ {"id": f"{idx}",
                       "description": f"{st['attributes']['name']}",
                       "service_type_id": f"{st['id']}"}
                     for idx, st in enumerate(pc.get_service_types())]    
    logger.debug("  read service types: %s", service_types)
    return service_types

def read_plans(pc: PlanningCenterClient, service_type_id: int):
    plans = [ {"id": f"{idx}",
                       "description": f"{st['attributes']['dates']}",
                       "plan_id": f"{st['id']}"}
                     for idx, st in enumerate(pc.get_plans_by_service_type(service_type_id))]    
    logger.debug("  read plans: %s", plans)
    return plans

if __name__ == "__main__":
    main()
