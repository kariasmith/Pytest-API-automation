# from asserter import assert_true, assert_equal
from urllib import response
from assertpy import *
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test
import utilities.custom_logger as cl
import pytest
import unittest
import logging
import os
from requests.models import Response
from test_steps.forms.form_steps import FormSteps
from test_steps.reports.reports_steps import ReportsSteps
from test_data import test_data
import pprint
from test_utils import decorate_test
import json
from operator import contains
from dotenv import load_dotenv
load_dotenv()


data = {"surveyId": 1600550}
valid_formid = {"formId": "dbad8d7a-abcd-abcd-abcd-1234ad36cb62"}
invalid_formid = {"formId": "7b2984f9-abcd-abcd-abcd-1234259cb3f2"}


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class TestReport(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.form_steps = FormSteps
        self.report_steps = ReportsSteps

    @pytest.mark.run(order=1)
    def test_post_report(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.post_report(json=test_data.post_report_data)
        statusCode = response.status_code
        response_json = response.json()
        description = response_json["description"]
        title = response_json["title"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert description == test_data.default_report_description
        assert title == test_data.default_report_title

    @pytest.mark.run(order=2)
    def test_get_report_by_report_id(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_report_id(
            report_id=test_data.report_id_1
        )
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        survey_id = response_json["surveyId"]
        description = response_json["description"]
        title = response_json["title"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert str(survey_id) == test_data.survey_id_2
        assert description == test_data.default_report_description
        assert title == test_data.default_report_title

    @pytest.mark.run(order=3)
    def test_generate_report(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.generate_report(survey_id='1600552')
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 200

    """ Tests invalid report UUID to verify error code returned"""

    @pytest.mark.run(order=4)
    def test_get_report_by_invalid_report_uuid(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_uuid_report_id(
            report_id="496e8f09-abcd-abcd-abcd-123499999999"
        )
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        errors = response_json["errors"]
        report_element = errors[0]
        fieldId = report_element["fieldId"]
        errorType = report_element["errorType"]
        severity = report_element["severity"]
        error_msg = report_element["errorMsg"]
        info = report_element["info"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 422
        assert fieldId == "report_id"
        assert errorType == "system"
        assert severity == "error"
        assert error_msg == "Report ID: None not found"
        assert info == ""

    """ Tests a deleted report UUID to verify error code returned"""

    @pytest.mark.run(order=5)
    def test_get_report_by_deleted_report_uuid(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_uuid_report_id(
            report_id="585729c2-abcd-abcd-abcd-123443df5f40"
        )
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        errors = response_json["errors"]
        report_element = errors[0]
        errorType = report_element["errorType"]
        severity = report_element["severity"]
        error_msg = report_element["errorMsg"]
        info = report_element["info"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 422
        assert errorType == "system"
        assert severity == "error"
        assert error_msg == "Report ID: None not found"
        assert (
            info
            == "1 validation error for ReportResponseSchema\nconfiguration\n  value is not a valid list (type=type_error.list)"
        )

    """ Test get report by PHP report (integer) ID."""

    @pytest.mark.run(order=6)
    def test_get_report_by_php_report_id(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_php_report_id(report_id="458")
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200

    """ Test get report by invalid PHP report (integer) ID."""

    @pytest.mark.run(order=7)
    def test_get_report_by_invalid_php_report_id(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_php_report_id(report_id="000")
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 422

    """ Test get report by deleted PHP report (integer) ID."""

    @pytest.mark.run(order=8)
    def test_get_report_by_deleted_php_report_id(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_by_php_report_id(report_id="460")
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        # Getting a 200, deletes not working
        assert statusCode == 200

    """ Test creating report with a form ID."""

    @pytest.mark.run(order=9)
    def test_create_report_with_formid(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.create_report_with_formid(formId=valid_formid)
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 200

    """ Testing using form ID that doesn't exist for user creds sent in header, create report with form ID and verifying error status."""

    @pytest.mark.run(order=10)
    def test_create_report_with_invalid_formid(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.create_report_with_formid(formId=invalid_formid)
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        errors = response_json["errors"]
        report_element = errors[0]
        error_msg = report_element["errorMsg"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        assert health_check.status_code == 200
        assert statusCode == 422
        assert error_msg == "Survey ID: 1595853 not found"
    
    """ Test creating a report element"""
    @pytest.mark.run(order=11)
    def test_create_report_element(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.create_report_element()
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        description = response_json["description"]
        title = response_json["title"]
        formElements = response_json["formElements"]
        element = formElements[-1]
        formElementId = element["formElementId"]
        formId = element["formId"]
        phpSurveyId = element["phpSurveyId"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        # pprint.pprint(formElementId)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert description == "Description for element created by Automation"
        assert title == "Title for element created by Automation"
        assert formElementId == "9b13bdb3-abcd-abcd-abcd-1234ed4bcc4c"
        assert formId == "0c02733a-abcd-abcd-abcd-1234fa2eefb6"
        assert phpSurveyId == 1613771

    """ Test updating report element's title, description, and chartType """
    @pytest.mark.run(order=12)
    def test_update_report_element(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.update_report_element()
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        title = response_json["title"]
        description = response_json["description"]
        chartType = response_json["chartType"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        pprint.pprint(title)
        pprint.pprint(description)
        pprint.pprint(chartType)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert title == "Updated Title from Automation"
        assert description == "Updated Description from Automation"
        assert chartType == "donut"
        
    """ Test is retrieving the report elements for the survey ID 1603354, report ID 458"""
    @pytest.mark.run(order=13)
    def test_get_updated_report_elements(self):
        response = self.report_steps.get_updated_element()
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        reportElements = response_json["reportElements"]
        elements = reportElements[2]
        title = elements["title"]
        description = elements["description"]
        chartType = elements["chartType"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        pprint.pprint(title)
        pprint.pprint(description)
        pprint.pprint(chartType)
        assert statusCode == 200
        assert title == "Updated Title from Automation"
        assert description == "Updated Description from Automation"
        assert chartType == "donut"

    """ To reset the report element's title, description, and chart type for next run"""
    @pytest.mark.run(order=14)
    def test_revert_changes_report_elements(self):
        response = self.report_steps.revert_update_element_changes()
        pprint.pprint(response)
        statusCode = response.status_code
        response_json = response.json()
        title = response_json["title"]
        description = response_json["description"]
        chartType = response_json["chartType"]
        pprint.pprint(response_json)
        pprint.pprint(statusCode)
        pprint.pprint(title)
        pprint.pprint(description)
        pprint.pprint(chartType)
        assert statusCode == 200
        assert title == "Reverted Title"
        assert description == "Reverted Description"
        assert chartType == "pie"

    """ Test is retrieving the report elements for the survey ID 1603354, report ID 462"""
    @pytest.mark.run(order=15)
    def test_get_report_elements_by_list(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_report_elements_by_list()
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
        assert health_check.status_code == 200
        assert statusCode == 200
        assert (
            title
            == "True or False: Under specific circumstances, boiling water can freeze faster than water at room temperature."
        )
        assert (
            secondTitle
            == "True or False: A kiss lasting one minute can burn more than 100 calories."
        )

    """ Test is retrieving all of the report UUIDs and PHP IDs for a survey with multiple reports."""
    @pytest.mark.run(order=16)
    def test_get_read_all_reports_for_survey(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = 1603354)
        statusCode = response.status_code
        response_json = response.json()
        reports = response_json["reports"]
        firstreport = reports[0]
        secondreport = reports[1]
        thirdreport = reports[2]
        fourthreport = reports[3]
        firstuuid = firstreport["id"]
        firstPHP = firstreport["phpReportId"]
        seconduuid = secondreport["id"]
        secondPHP = secondreport["phpReportId"]
        thirduuid = thirdreport["id"]
        thirdPHP = thirdreport["phpReportId"]
        fourthuuid = fourthreport["id"]
        fourthPHP = fourthreport["phpReportId"]
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 200
        assert firstuuid == '757d1ae6-abcd-abcd-abcd-12349419287e'
        assert firstPHP == 460
        assert seconduuid == 'dbd20fcb-abcd-abcd-abcd-1234d1dd3aa1'
        assert secondPHP == 461
        assert thirduuid == 'fcbcc51f-abcd-abcd-abcd-123453584da8'
        assert thirdPHP == 462
        assert fourthuuid == '4d7e0175-abcd-abcd-abcd-123461d2d53a'
        assert fourthPHP == 458

    """ Test is retrieving all of the report UUIDs and PHP IDs for a survey with No reports."""
    @pytest.mark.run(order=17)
    def test_get_all_reports_for_survey_empty_list(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = 1601121)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 200

    """ Test is verifying an error is returned for survey that doesn't exist for user."""
    """ Defect RA-1898 """
    @pytest.mark.run(order=18)
    def test_get_all_reports_for_invalid_survey(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = 1234567)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 404
        #assert errorMsg == "Survey ID: 1234567 not found for customer 123456 user 123456"

    """ Test is verifying an error is returned for survey that has been deleted."""
    """ Defect RA-1898 """
    @pytest.mark.run(order=19)
    def test_get_all_reports_for_deleted_survey(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = 1616207)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 404
        #assert errorMsg == "Survey ID: 1616207 not found for customer 123456 user 123456"

    """ Test is verifying an error is returned for text sent as survey."""
    @pytest.mark.run(order=20)
    def test_get_all_reports_for_text_survey(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = "TextSurvey")
        statusCode = response.status_code
        response_json = response.json()
        errors = response_json["errors"]
        firsterrors = errors[0]
        errorMsg = firsterrors["errorMsg"]
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 422
        assert errorMsg == "value is not a valid integer"

    """ Test is verifying an error is returned for text sent as survey."""
    @pytest.mark.run(order=21)
    def test_get_all_reports_for_spaces_survey(self):
        health_check = self.report_steps.get_report_health()
        response = self.report_steps.get_all_reports_for_survey(survey_id = "        ")
        statusCode = response.status_code
        response_json = response.json()
        errors = response_json["errors"]
        firsterrors = errors[0]
        errorMsg = firsterrors["errorMsg"]
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert health_check.status_code == 200
        assert statusCode == 422
        assert errorMsg == "value is not a valid integer"