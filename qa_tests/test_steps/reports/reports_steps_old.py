from dotenv import load_dotenv  # for python-dotenv method

load_dotenv()  # for python-dotenv method

import os
import requests
import ssl
import webbrowser

ssl._create_default_https_context = ssl._create_unverified_context


base_url = "http://localhost:8004"
headers = os.environ.get("HEADERS")
app_env = os.environ.get("APP_ENV")
api_token = os.environ.get("API_TOKEN")
api_token_secret = os.environ.get("API_TOKEN_SECRET")
report_id = os.environ.get("REPORTID")
# report_element_ids = os.environ.get("REPORTELEMENTIDS")
report_element_ids = {
    "reportElementIds": [
        "cd86e55d-abcd-1234-abcd-123482013989",
        "a107ef9e-abcd-1234-abcd-1234846f4f9c",
    ]
}


class ReportsSteps:
    def __init__(self):
        pass

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

    # http://localhost:8004/report/report/496e8f09-abcd-1234-abcd-12346e3ba49c/internal
