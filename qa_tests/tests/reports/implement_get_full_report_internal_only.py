import json
from operator import contains
from qa_tests.session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from qa_tests.test_utils import decorate_test
import qa_tests.utilities.custom_logger as cl
import pytest
import unittest
import logging
from requests.models import Response
from qa_tests.test_steps.reports.reports_steps import ReportsSteps
import pprint
import assertpy


"""
This test is posting call to retrieve a full internal report.
The user created & used for this testing is test@email.com
Testing the ticket RA-1452
"""


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class Testreport(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.reports_steps = ReportsSteps

    #
    # Test 1 is a POST call to retrieve full Internal report, also a 200 status.
    #

    @pytest.mark.run(order=1)
    def test_post_internal_report_with_elements(self):
        response = self.reports_steps.post_report_internal()
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        reportElements = response_json["reportElements"]
        elements = reportElements[0]
        secondQuestion = reportElements[1]
        title = elements["title"]
        secondTitle = secondQuestion["title"]
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        pprint.pprint(title)
        pprint.pprint(secondTitle)
        assert statusCode == 200
        assert (
            title
            == "True or False: Under specific circumstances, boiling water can freeze faster than water at room temperature."
        )
        assert (
            secondTitle
            == "True or False: A kiss lasting one minute can burn more than 100 calories."
        )
