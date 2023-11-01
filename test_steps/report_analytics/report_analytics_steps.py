from dotenv import load_dotenv  # for python-dotenv method

load_dotenv()  # for python-dotenv method

import os
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


base_url = "http://localhost:8003"
headers = {
    "Customer-Id": "999999",
    "User-Id": "999999",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
report_id3 = os.environ.get("REPORTID3")
# Pie, Arc, Spider, Donut, Stacked Vertical, Stacked Horizontal
report_element_ids = {
    "reportElementIds": [
        "e6881705-a1bc-2de3-f45g-6h7i8jk9d0d7",
        "0ea38d40-a1bc-2de3-f45g-6h7i8jk92f0e",
        "6ee76842-a1bc-2de3-f45g-6h7i8jk9f9c8",
        "a84bc3bc-a1bc-2de3-f45g-6h7i8jk9fdc4",
        "5e283cb0-a1bc-2de3-f45g-6h7i8jk94c65",
        "0dcf2318-a1bc-2de3-f45g-6h7i8jk9d1f9"
    ]
}
""" "value is not a valid enumeration member; permitted: 'arc', 'area', 'area_spline', 'donut', 'hbar', 
'histogram', 'line', 'longitudinal-area', 'longitudinal-area_spline', 'longitudinal-line', 'longitudinal-spline', 
'longitudinal-stack_area', 'longitudinal-stack_area_spline', 'longitudinal-stack_vbar', 'longitudinal-vbar', 'nps', 
'pie', 'responsemetrics', 'scatter', 'spiderweb', 'spline', 'stack_area', 'stack_area_spline', 'stack_hbar', 'stack_vbar', 
'table', 'vbar', 'wordcloud'","""


class ReportAnalyticsSteps:
    def __init__(self):
        pass

    def get_report_analytics_health(**data):

        """
        GETs /report-analytic/health
        """
        response = requests.get(f"{base_url}/report-analytic/health", headers=headers, **data)
        return response


    def read_report_elements_analytics(**data):
        """
        POSTs /report-analytic/report-analytic/{report_id}
        providing report elements in request
        :param client: Rest Client with auth credentials
        """
        return requests.post(
            f"{base_url}/report-analytic/report-analytic/{report_id3}",
            headers=headers,
            json=report_element_ids,
            **data,
        )
