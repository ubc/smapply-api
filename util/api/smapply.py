from . import *
from http.client import HTTPResponse
from urllib.error import HTTPError
from configparser import ConfigParser

class SMApplyInstance(APIInstance):

    @property
    def default_program_id(self):
        return self._default_program_id
    
    def __init__(self, env=None):
        if not env:
            from .. import _ENV
            env = _ENV
        APIInstance.__init__(self, filename="config/smapply.cfg", env=env)
        if  self._base_url and 'api' not in self._base_url:
            self._base_url = self._base_url + "/api"
        self._urlencode=False
        config = ConfigParser()
        config.read("config/smapply.cfg")
        self._default_program_id = config[env]['default_program_id']

    def call_api(self, url, is_url_absolute=False, method="GET", post_fields=None, all_pages=True, content_type="application/json"):

        response = super().call_api(url,is_url_absolute,method,post_fields,content_type)

        if type(response) == HTTPError:
            logging.debug(response)
            logging.debug("message: {}".format(response.read().decode("utf-8")))
            return

        
        if not all_pages or method=="POST":
            return get_response_body(response)

        more_pages = True
        collector = []
        while more_pages:
            response_body = get_response_body(response)
            if "results" not in response_body:
                break
            collector = collector + response_body['results']
            if response_body['next']:
                response = super().call_api(response_body['next'],
                                            is_url_absolute=True,
                                            method=method,
                                            post_fields=post_fields,
                                            content_type=content_type)
            else:
                more_pages = False
        return collector
