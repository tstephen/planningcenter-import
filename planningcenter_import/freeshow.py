"""
freeshow.py
"""
import json
import logging

from jinja2 import Template
from pydantic import BaseModel

from planningcenter_import.planningcenter_client import PlanningCenterClient, PlanningCenterOptions

logger = logging.getLogger(__name__)

class FreeShow:

    def __init__(self, options: PlanningCenterOptions) -> None:
        self.options = options
        self.planningcenter =  PlanningCenterClient(options)

    def get_plan_from_planning_center(self, service_type_id: int, plan_id: int) -> str:
        return self.transform_plan_to_project(
            self.planningcenter.get_plan_by_service_type_id_and_plan_id(service_type_id, plan_id))

    def transform_plan_to_project(self, plan):
        with open('planningcenter_import/templates/planningcenter2freeshow.j2', 'r') as template_file:
            template_str = template_file.read()

        plan_name = plan["attributes"]["sort_date"][:16].replace('T', ' ')
        template = Template(template_str)
        try:
            transformed_data = json.loads(template.render(plan_name=plan_name, plan=plan))
            ret_val = f"{plan_name.replace(' ','-')}.project"
            with open(ret_val, 'w') as file:
                json.dump(transformed_data, file, indent=2)
            return ret_val
        except json.decoder.JSONDecodeError as err:
            logger.error("produced invalid json, %s", err.msg)
            transformed_data = template.render(plan_name=plan_name, plan=plan)
            ret_val = f"{plan_name.replace(' ','-')}.debug"
            with open(ret_val, 'w') as file:
                file.write(transformed_data)
            return ret_val



    # def get_plan_from_planning_center(self):
    #     service_types = self.planningcenter.get_service_types()
    #     service_type = [st for st in service_types
    #                     if st["attributes"]["name"] == 
    #     logger.info("service type id: %s", service_type[0]["id"])
    #     plans = self.planningcenter.get_plans_by_service_type(service_type_id=service_type[0]["id"])
    #     logger.info("available plans: %s", [plan["attributes"]["dates"] for plan in plans])
    #     print(f"available plans: {[plan['attributes']['dates'] for plan in plans]}")
    #     assert len(plans) > 0
    #     plan = [plan for plan in plans
    #                     if plan["attributes"]["dates"] == os.environ["PC_PLAN_DATE"]]
    #     assert len(plan) == 1
    #     logger.info("plan: %s", plan[0]["id"])

    #     plan_items = self.planningcenter.get_plan_items(service_type[0]["id"], plan[0]["id"])
    #     sort_date = plan[0]['attributes']['sort_date']
    #     with open(f"{sort_date[0:sort_date.rfind('T')]}.json", 'w') as outfile:
    #         json.dump(plan_items, outfile, indent=2) 