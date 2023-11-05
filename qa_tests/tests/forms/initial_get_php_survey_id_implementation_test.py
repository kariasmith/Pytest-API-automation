import json
from operator import contains
from qa_tests.session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from qa_tests.test_utils import decorate_test
import qa_tests.utilities.custom_logger as cl
import pytest
import unittest
import logging
from requests.models import Response
from qa_tests.test_steps.forms.form_steps import FormSteps
import pprint
import assertpy


"""
These tests are for the initial GET calls for the survey ID and Form ID from PHP to the Form.
The user created & used for this testing is test@email.com
Testing the ticket RA-1099
"""


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class Testform(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.form_steps = FormSteps

    #
    # Test 1 is a GET call on valid survey ID and verifying that the phpCustomerId is correct in the json, also a 200 status.
    #

    @pytest.mark.run(order=1)
    def test_get_form_by_survey_id(self):
        response = self.form_steps.get_form_by_survey_id(survey_id="1597665")
        statusCode = response.status_code
        response_json = response.json()
        customerId = response_json["phpCustomerId"]
        pprint.pprint(response_json)
        pprint.pprint(customerId)
        pprint.pprint(response.headers)
        assert statusCode == 200
        assert customerId == 123456

    #
    # Test 2 is submitting an invalid survey ID and verifying status returns 422.
    #

    @pytest.mark.run(order=2)
    def test_get_form_invalid_survey_id(self):
        response = self.form_steps.get_form_by_survey_id(survey_id="10098023")
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        assert statusCode == 422

    #
    # Test 3 is a GET call on the Form ID and verifying status is 200.
    #

    @pytest.mark.run(order=3)
    def test_get_form_by_form_id(self):
        response = self.form_steps.get_form_by_form_id(
            form_id="e6059f7f-abcd-1234-abcd-12343b22da60"
        )
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert statusCode == 200

    #
    # Test 4 is adding a question to an existing survey and verifying the API call's status is 200.
    # Then verifying the new question is listed in the form's json.
    # SID 1234567 (Add question to survey), grabbing the last element created in json.
    #

    @pytest.mark.run(order=4)
    def test_add_question_to_form_by_survey_id(self):
        # Adding question to the survey and verify status is 200
        add_question = self.form_steps.put_add_question_by_survey_id(
            survey_id="1601048"
        )
        api_status = add_question.status_code
        api_json = add_question.json()
        pprint.pprint("results from add API call")
        pprint.pprint(api_status)
        pprint.pprint(api_json)
        assert api_status == 200
        # Get the form by survey ID and verify status is 200, and json shows the question added
        response = self.form_steps.get_form_by_survey_id(survey_id="1601048")
        statusCode = response.status_code
        response_json = response.json()
        customerId = response_json["phpCustomerId"]
        formElements = response_json["formElements"]
        # This snippet is used for any troubleshooting of the json response returned.
        # if "title" in formElements[-1]:
        #     pprint.pprint("formElements found in json")
        #     pprint.pprint(formElements[-1])
        # else:
        #     pprint.pprint("formElements not found in json")
        # for key in formElements[-1]:
        #     pprint.pprint(key)
        lastForm = formElements[-1]
        title = lastForm["title"]
        active_flag = lastForm["isDeleted"]
        question_id = lastForm["phpQuestionId"]
        pprint.pprint(title)
        pprint.pprint("results from Form by survey ID")
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        # Deleting the newly added question to prep for the next automation run.
        remove_question = self.form_steps.remove_new_added_question_by_survey_id(
            survey_id="1601048", qid=question_id
        )
        assert title == "Question that was added. :-)"
        assert active_flag == 0
        assert statusCode == 200
        assert customerId == 123456

    #
    # Test 5 is updating the question from previous survey and verifying that status is 200.
    # Also verifying the updated question's title is listed in the form's json.
    # SID 1234567 (Add question to survey), question ID 2 for API call, and first element in dict for json.
    #

    @pytest.mark.run(order=5)
    def test_update_question_to_form_by_survey_id(self):
        # Updating question in the survey and verify status is 200
        updated_question = self.form_steps.post_update_question_by_survey_id(
            survey_id="1601048"
        )
        api_status = updated_question.status_code
        api_json = updated_question.json()
        pprint.pprint("results from update API call")
        pprint.pprint(api_status)
        pprint.pprint(api_json)
        assert api_status == 200
        # Get the form by survey ID and verify status is 200, and json shows the question updated
        # defect RA-1556  is currently open on the update not working
        response = self.form_steps.get_form_by_survey_id(survey_id="1601048")
        statusCode = response.status_code
        response_json = response.json()
        customerId = response_json["phpCustomerId"]
        formElements = response_json["formElements"]
        firstForm = formElements[0]
        title = firstForm["title"]
        active_flag = firstForm["isDeleted"]
        pprint.pprint("results from Form by survey ID")
        pprint.pprint(formElements[0])
        pprint.pprint(title)
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert (
            title == "Updated question title"
        )  # when defect is fixed this line should pass, currently failing
        assert active_flag == 0
        assert statusCode == 200
        assert customerId == 123456
        # Reset title of Question for next automation run
        revert_question = self.form_steps.revert_question_title_update(
            survey_id="1601048"
        )

    #
    # Test 6 is deleting a question in the survey and verifying that status is 200.
    # Verifying the question's isDeleted flag is listed as deleted in the form's json.
    # SID 1234567 (Forms get ID), question ID is 6 for API call, and the 4th element that shows up in json.
    #

    @pytest.mark.run(order=6)
    def test_delete_question_to_form_by_survey_id(self):
        # Deleting question in the survey and verifying API call status is 200
        delete_question = self.form_steps.delete_question_by_survey_id(
            survey_id="1597665"
        )
        api_status = delete_question.status_code
        api_json = delete_question.json()
        pprint.pprint("results from delete API call")
        pprint.pprint(api_status)
        pprint.pprint(api_json)
        assert api_status == 200
        # Get the form by survey ID and verify status is 200, and json shows the question is deleted
        response = self.form_steps.get_form_by_survey_id(survey_id="1597665")
        statusCode = response.status_code
        response_json = response.json()
        customerId = response_json["phpCustomerId"]
        formElements = response_json["formElements"]
        fourthForm = formElements[4]
        title = fourthForm["title"]
        active_flag = fourthForm["isDeleted"]
        pprint.pprint("results from Form by survey ID")
        pprint.pprint(formElements[4])
        pprint.pprint(title)
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert active_flag == 1
        assert title == "Question to be deleted :-)"
        assert statusCode == 200
        assert customerId == 123456
        # Test above sets the isDeleted flag to 1 for deleted.
        # Need to reset the isDeleted flag back to 0 for future runs to pass.
        restore_question = self.form_steps.restore_question_by_survey_id(
            survey_id="1597665"
        )

    #
    # Test 7 Providing an invalid form ID and verifying status returns 422
    #

    @pytest.mark.run(order=7)
    def test_get_form_invalid_form_id(self):
        response = self.form_steps.get_form_by_form_id(
            form_id="e6059f7f-9999-9999-9999-99993b999999"
        )
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        assert statusCode == 422

    #
    # Test 8 is making a GET call with an empty survey that exists and verifying a 500 status is returned.
    # SID 1234567 (Empty survey [Please don't add any questions! Leave empty])
    #
    @pytest.mark.run(order=8)
    def test_empty_survey_by_survey_id(self):
        response = self.form_steps.get_form_by_survey_id(survey_id="1601121")
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint("results from Form by survey ID")
        pprint.pprint(statusCode)
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert statusCode == 500
