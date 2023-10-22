import json
import requests
from requests import RequestException
from qa_tests.logger import Logger
# from qa_tests.logger import Logger


class HTTPSession:
    URL = ''

    @staticmethod
    def send_request(request_type, endpoint, params):
        do_logging = params.pop('do_logging', True)
        try:
            response = request_type(endpoint, params)
            if do_logging:
                Logger.log_request(request_type, endpoint, params, response.status_code)
            return response.status_code, json.loads(response.text)
        except RequestException as e:
            Logger.log('Could not send {} request due to exception: {}'.format(request_type, e))


class RequestTypes:
    GET = requests.get


class Endpoints:
    STATIONS = HTTPSession.URL + 'stations'


class StatusCodes:
    STATUS_200 = '200'
