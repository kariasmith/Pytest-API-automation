from urllib import response
from assertpy import *
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
import utilities.custom_logger as cl
import pytest
import unittest
import logging
from requests.models import Response
from test_steps.forms.form_steps import FormSteps
from test_steps.reports.reports_steps import ReportsSteps
from test_steps.report_analytics.report_analytics_steps import ReportAnalyticsSteps
from test_data import test_data
import pprint
from test_utils import decorate_test
import json
from operator import contains


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class TestReportAnalytics(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.form_steps = FormSteps
        self.report_steps = ReportsSteps
        self.report_analytics_steps = ReportAnalyticsSteps


    """ Test is retrieving the report element Analytics for the survey ID phpSurveyId: 1613771 , report ID phpReportId: 467"""
    @pytest.mark.run(order=1)
    def test_read_report_elements_analytics(self):
        health_check = self.report_analytics_steps.get_report_analytics_health()
        response = self.report_analytics_steps.read_report_elements_analytics()
        statusCode = response.status_code
        response_json = response.json()
        reportElements = response_json["reportElementData"]
        elements = reportElements[0]
        secondElement = reportElements[1]
        thirdElement = reportElements[2]
        reportElementId = elements["reportElementId"]
        secondreportElementId = secondElement["reportElementId"]
        thirdreportElementId = thirdElement["reportElementId"]
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        pprint.pprint(reportElementId)
        pprint.pprint(secondreportElementId)
        pprint.pprint(thirdreportElementId)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert (reportElementId == "e6881705-abcd-1234-abcd-123415c948f8")
        assert (secondreportElementId == "0ea38d40-abcd-1234-abcd-12346adb2f0e")
        assert (thirdreportElementId == "6ee76842-abcd-1234-abcd-1234aaeff9c8")
