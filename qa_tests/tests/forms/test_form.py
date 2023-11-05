# from asserter import assert_true, assert_equal
from assertpy import *
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test
import utilities.custom_logger as cl
import pytest
import unittest
import logging
from requests.models import Response
from test_steps.forms.form_steps import FormSteps
from test_data import test_data
import pprint


@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
class TestForm(unittest.TestCase):
    log = cl.customLogger(logging.DEBUG)
    pp = pprint.PrettyPrinter(indent=4)

    @pytest.fixture(autouse=True)
    def objectSetUp(self, oneTimeSetUp):
        self.form_steps = FormSteps

    @pytest.mark.run(order=1)
    def test_get_form_by_survey_id(self):
        response = self.form_steps.get_form_by_survey_id(survey_id="1561203")
        statusCode = response.status_code
        response_json = response.json()
        customerId = response_json["phpCustomerId"]
        pprint.pprint(response_json)
        pprint.pprint(customerId)
        pprint.pprint(response.headers)
        assert statusCode == 200
        assert customerId == 123456

    @pytest.mark.run(order=2)
    def test_get_form_invalid_survey_id(self):
        response = self.form_steps.get_form_by_survey_id(survey_id="10098023")
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        assert statusCode == 422

    @pytest.mark.run(order=3)
    def test_get_form_by_form_id(self):
        # TODO: form_id needs updated to something in DB.
        response = self.form_steps.get_form_by_form_id(
            form_id="2acc7513-abcd-1234-abcd-12342c967b6c"
        )
        # print("response")
        # print(response)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        pprint.pprint(response.headers)
        assert statusCode == 200

    @pytest.mark.run(order=4)
    def test_get_uuid_by_survey_id(self):
        health_check = self.form_steps.get_form_health()
        form_uuid = self.form_steps.get_uuid(survey_id = test_data.survey_id_1)
        pprint.pprint(form_uuid)
        assert health_check.status_code == 200
        assert form_uuid == test_data.form_id_1

    @pytest.mark.run(order=5)
    def test_get_uuid_and_form_element_type_by_survey_id(self):
        health_check = self.form_steps.get_form_health()
        form_uuid = self.form_steps.get_uuid(survey_id = test_data.survey_id_3)
        pprint.pprint(form_uuid)
        response = self.form_steps.get_form_by_survey_id(survey_id = test_data.survey_id_3)
        statusCode = response.status_code
        response_json = response.json()
        pprint.pprint(response_json)
        form_element_type = response_json['formElements'][0]['formElementType']
        pprint.pprint(form_element_type)
        assert health_check.status_code == 200
        assert form_uuid == test_data.form_id_3
        assert statusCode == 200
        assert form_element_type == 'question'   

    def test_delete_form_200(self):
        self.created_form_post_response = ''
        response = delete_form(self.client, self.form['id'])
        assert_status_code(response, 200)
        assert_max_response_time(response, 1)

    def test_get_deleted_form_404(self):
        delete_form(self.client, self.form['id'])
        response = get_form_by_form_id(self.client, self.form['id'])
        assert_status_code(response, 404)
        assert_max_response_time(response, 1)

    def test_put_form_200(self):
        self.form['name'] = 'NewName'
        response = put_form(self.client, **self.form)
        assert_status_code(response, 200)
        assert_max_response_time(response, 1)
        assert_valid_schema(response.json(), 'form/form.json')
        assert_response_key_value(response, 'id', self.form['id'])
        assert_response_key_value(response, 'name', self.form['name'])
        response = get_form_by_form_id(self.client, self.form['id'])
        assert_response_key_value(response, 'name', self.form['name'])
