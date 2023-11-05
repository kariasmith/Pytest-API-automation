import json
import os
from operator import contains
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test
import utilities.custom_logger as cl
import pytest
import unittest
import logging
import ast
from requests.models import Response
from test_steps.reports.reports_steps import ReportsSteps

from test_data import test_data
import pprint
from dotenv import load_dotenv
from environs import Env
load_dotenv()

# env = Env()
# env.read_env()
# request_body = env.dict('request_body', subcast=str)
# request_body_update_config = os.environ.get("request_body_update_config")
# request_body =  ast.literal_eval(os.environ.get["request_body"])


"""
This test is a PUT call to update a report.
Testing the ticket RA-1450
"""


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class TestReportUpdate(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.reports_steps = ReportsSteps
        

    @pytest.mark.run(order=1)
    def test_update_report_title_and_description(self):
        health_check = self.reports_steps.get_report_health()
        response = self.reports_steps.update_report_by_report_id(report_id=test_data.report_id_1,
                                                                 data=json.dumps(test_data.request_body))
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)

        description = response_json['description']
        title = response_json['title']
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert title == "Newly Updated Title"
        assert description == "Newly Updated Description"
        
       
    @pytest.mark.run(order=2)
    def test_update_report_title_and_description_2(self):
        health_check = self.reports_steps.get_report_health()
        response = self.reports_steps.update_report_by_report_id(report_id=test_data.report_id_1,
                                                                 data=json.dumps(test_data.request_body_default))
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        description = response_json['description']
        title = response_json['title']
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert title == "Default Title Comes with Report"
        assert description == "Default Description"


    @pytest.mark.run(order=3)
    def test_update_report_configuration(self):
        health_check = self.reports_steps.get_report_health()
        response = self.reports_steps.update_report_by_report_id(report_id=test_data.report_id_1,
                                                                 json=test_data.request_body_update_config)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        description = response_json['description']
        title = response_json['title']
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert title == "Newly Updated Title"
        assert description == "Newly Updated Description"


    @pytest.mark.run(order=4)
    def test_update_report_invalid_report_id(self):
        health_check = self.reports_steps.get_report_health()
        response = self.reports_steps.update_report_by_report_id(report_id=test_data.invalid_report_id,
                                                                 json=test_data.request_body)
        statusCode = response.status_code
        assert health_check.status_code == 200
        assert statusCode == 500


    @pytest.mark.run(order=5)
    def test_update_report_update_report_elements(self):
        health_check = self.reports_steps.get_report_health()
        response = self.reports_steps.update_report_by_report_id(report_id=test_data.report_id_1,
                                                                 json=test_data.request_body_updated_report_elements)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)

        description = response_json['description']
        report_element_1 = response_json['reportElements'][0]
        report_element_2 = response_json['reportElements'][1]
        pprint.pprint(statusCode)
        pprint.pprint(report_element_1)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert report_element_1 == '3277abe6-abcd-abcd-abcd-1234e8ecae84'
        assert report_element_2 == '2877abe6-abcd-abcd-abcd-1234e8ecae84'