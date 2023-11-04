from email.base64mime import body_decode
from pprint import pprint
from dotenv import load_dotenv  # for python-dotenv method

load_dotenv()  # for python-dotenv method

from test_data import test_data

import os
import requests
import ssl
import webbrowser
import pprint
import json

ssl._create_default_https_context = ssl._create_unverified_context


base_url = "http://localhost:8004"
headers = os.environ.get("HEADERS")
headers = {
    "Customer-Id": "999999",
    "User-Id": "999999",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
app_env = os.environ.get("APP_ENV")
api_token = os.environ.get("API_TOKEN")
api_token_secret = os.environ.get("API_TOKEN_SECRET")
report_id = os.environ.get("REPORTID")
updated_report_id = os.environ.get("REPORTID2")
survey_id = os.environ.get("SURVEY_ID")
report_element_id = os.environ.get("REPORTELEMENTID")
report_add_element = os.environ.get("REPORTID3")
report_element_ids = {
    "reportElementIds": [
        "84fb02f7-abcd-1234-abcd-12346f729046",
        "415b3a18-abcd-1234-abcd-123432cafe37",
    ]
}
report_elements = {
    "reportElements": [
        "84fb02f7-abcd-1234-abcd-12346f729046",
        "415b3a18-abcd-1234-abcd-123432cafe37",
    ]
}
element_updated = {
    "reportElements": [
        "48da6a4e-abcd-1234-abcd-1234cbf0b0c0",
        "14a3d2df-abcd-1234-abcd-123479542b7d",
        "7a87aae9-abcd-1234-abcd-1234c6eb5f23"
    ]
}
formElementId = {
    "formElementId": "9b13bdb3-abcd-1234-abcd-1234ed4bcc4c",
    "title": "Title for element created by Automation",
    "description": "Description for element created by Automation",
    "elementType": "chart",
    "chartType": "pie",
}
update_element = {"title": "Updated Title from Automation","description": "Updated Description from Automation","elementType": "chart","chartType": "donut"}
revert_element = {"title": "Reverted Title","description": "Reverted Description","elementType": "chart","chartType": "pie"}
request_body_update_config = os.environ.get("request_body_update_config")
request_body = {}


class ReportsSteps:
    def __init__(self):
        pass

    def get_report_health(**data):

        """
        GETs /report/health
        :param client: Rest Client with auth credentials
        """
        response = requests.get(f"{base_url}/report/health", headers=headers, **data)
        return response

    def post_report_internal(**data):
        """
        POSTs /report/report/{report_id}/internal
        providing report elements in request
        :param client: Rest Client with auth credentials
        """
        return requests.post(
            f"{base_url}/report/report/{report_id}/internal",
            headers=headers,
            json=report_element_ids,
            **data,
        )

    def get_report_by_report_id(report_id, **data):
        """
        GETs /report/report
        :param client: Rest Client with auth credentials
        :param report_id: report ID
        """
        response = requests.get(
            f"{base_url}/report/report/{report_id}", headers=headers, **data
        )
        return response

    def post_report(**data):
        """
        POSTs /report/report
        :param client: Rest Client with auth credentials
        """
        return requests.post(f"{base_url}/report/report", **data)

    def update_report_by_report_id(report_id, **data):
        """
        PUTs /report/report/{report_id}
        :param client: Rest Client with auth credentials
        """
        return requests.put(f"{base_url}/report/report/{report_id}", **data)

    def generate_report(survey_id) -> dict:
        report = {
            "id": survey_id,
        }
        return report


    def get_report_by_uuid_report_id(report_id, **data):

        """
        GETs /report/report
        :param client: Rest Client with auth credentials
        :param report_id: UUID report ID
        """
        response = requests.get(
            f"{base_url}/report/report/{report_id}", headers=headers, **data
        )
        return response

    def get_report_by_php_report_id(report_id, **data):

        """
        GETs /report/report/php-report-id/
        :param client: Rest Client with auth credentials
        :param report_id: PHP report ID
        """
        response = requests.get(
            f"{base_url}/report/report/survey-id/{survey_id}/php-report-id/{report_id}",
            headers=headers,
            **data,
        )
        return response

    def create_report_with_formid(formId):
        """
        POST /report/report
        :param client: Rest Client with auth credentials
        :param formid: form ID
        """
        response = requests.post(
            f"{base_url}/report/report", headers=headers, data=formId
        )
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
        return response

    def create_report_element():
        """
        POST /report/report/{report_id}/report-element
        :param client: Rest Client with auth credentials
        :param report_id: report ID (UUID)
        :param formElementId: form element id (UUID)
        """
        response = requests.post(
            f"{base_url}/report/report/{report_add_element}/report-element",
            headers=headers,
            json=formElementId,
        )
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
        return response

    def update_report_element():
        """
        PUT /report/report/{report_id}/report-element/{report_element_id}
        :param client: Rest Client with auth credentials
        :param report_id: report ID (UUID)
        :param report_element_id: report element id (UUID)
        """
        response = requests.put(
            f"{base_url}/report/report/{updated_report_id}/report-element/{report_element_id}",
            headers=headers,
            json=update_element
        )
        
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
        return response

        # method = 'post', url = 'http://localhost:8004/report/report', kwargs = {'body': None, 'data': None, 'headers': None, 'json': None}

    def generate_report(survey_id) -> dict:
        report = {
            "id": survey_id,
        }
        return report
        
    def get_updated_element():
        whatchamacallit = requests.post(
            f"{base_url}/report/report/{updated_report_id}/report-elements",
            headers=headers,
            json=element_updated
            )
        print(whatchamacallit.request.url)
        print(whatchamacallit.request.body)
        print(whatchamacallit.request.headers)
        return whatchamacallit

    def revert_update_element_changes():
        """
        PUT /report/report/{report_id}/report-element/{report_element_id}
        :param client: Rest Client with auth credentials
        :param report_id: report ID (UUID)
        :param report_element_id: report element id (UUID)
        """
        response = requests.put(
            f"{base_url}/report/report/{updated_report_id}/report-element/{report_element_id}",
            headers=headers,
            json=revert_element
        )
        print(response.request.url)
        print(response.request.body)
        print(response.request.headers)
        return response

    def get_report_elements_by_list(**data):
        """
        POSTs /report/report/{report_id}/report-elements
        providing report elements in request
        :param client: Rest Client with auth credentials
        """
        return requests.post(
            f"{base_url}/report/report/{report_id}/report-elements",
            headers=headers,
            json=report_elements,
            **data,
        )

    def get_all_reports_for_survey(survey_id, **data):
        """
        GETs /report/report/survey-id/{survey_id}/all
        :param client: Rest Client with auth credentials
        :param report_id: integer survey ID
        """
        response = requests.get(
            f"{base_url}/report/report/survey-id/{survey_id}/all",
            headers=headers,
            **data,
        )
        return response
