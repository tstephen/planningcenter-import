"""
Wraps Planning Center Online API v2
"""
import logging
from urllib import error, request
from json import loads, load, dump

logger = logging.getLogger(__name__)


class PlanningCenterClient:
    BASE_API_URL = "https://api.planningcenteronline.com/services/v2/"
    """
    wraps Planning Center Online API v2
    """
    def __init__(self, application_id, secret):
        """
        Initialize client with authentication and authorization info.

        :param application_id: Application id from Planning Center Online
        :param secret: Secret from Planning Center Online
        """
        self.application_id = application_id
        self.secret = secret
        logging.basicConfig(level=logging.DEBUG)

    def do_api_call(self, url_suffix):
        """
        calls the API with the provided url_suffix returning the parsed response.

        :param url_suffix: the query part of the URL. Appended to self.API_URL.
        """
        password_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(realm=None, uri=self.BASE_API_URL,
                                  user=self.application_id, passwd=self.secret)
        handler = request.HTTPBasicAuthHandler(password_mgr)
        opener = request.build_opener(handler)
        opener.open(f"{self.BASE_API_URL}{url_suffix}")
        request.install_opener(opener)
        api_response_string = request.urlopen(f"{self.BASE_API_URL}{url_suffix}", timeout=30) \
                                            .read()
        api_response_object = loads(api_response_string.decode("utf-8"))
        if logger.isEnabledFor(logging.DEBUG):
            with open(f"{url_suffix}.json", 'w') as outfile:
                dump(api_response_object, outfile)
        return api_response_object

    def get_organization(self):
        """
        returns the name of the organization for the Planning Center Online account
        invoke this first to check credentials
        """
        try:
            response = self.do_api_call('')
            organization = response['data']['attributes']['name']
            return organization
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise

    def get_service_types(self):
        """
        return list of service types including named and importantly ids to use in further queries
        """
        service_types = self.do_api_call('service_types')
        return service_types['data']

    def get_plans_by_service_type(self, service_type_id: str, page_size: int = 10):
        """
        returns a list of plans available for a given service_type_id.

        :param service_type_id: The id of the service_type
        :param page_size: defaults to 10 for both future and past plans. 
        """
        try:
            future_plans_query = f"service_types/{service_type_id}/plans?filter=future&per_page={page_size}&order=sort_date"
            future_plans = self.do_api_call(future_plans_query)
            past_plans_query = f"service_types/{service_type_id}/plans?filter=past&per_page={page_size}&order=-sort_date"
            past_plans = self.do_api_call(past_plans_query)
            return list(reversed(future_plans['data'])) + past_plans['data']
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise

    def get_plan_items(self, service_type_id: str, plan_id: str):
        """
        return all items for a given plan id

        :param service_type_id: The id of the service_type
        :param plan_id: The id of the Plan from which to query all Plan Items.
        """
        try:
            item_query = f"service_types/{service_type_id}/plans/{plan_id}/items?include=song,arrangement&per_page=100"
            return self.do_api_call(item_query)["data"]
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise

    def get_song(self, song_id: str):
        """
        return the specified song

        :param song_id: The id of the song
        """
        try:
            song_query = f"songs/{song_id}"
            return self.do_api_call(song_query)["data"]
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise

    def get_song_arrangements(self, song_id: str):
        """
        return attachments for the specified song

        :param song_id: The id of the song
        """
        try:
            song_query = f"songs/{song_id}/arrangements"
            return self.do_api_call(song_query)["data"]
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise


    def get_song_attachments(self, song_id: str):
        """
        return attachments for the specified song

        :param song_id: The id of the song
        """
        try:
            song_query = f"songs/{song_id}/attachments"
            return self.do_api_call(song_query)["data"]
        except error.HTTPError as error:
            logger.error("%s:%s", error.code, error.reason)
            raise
