from multiprocessing.connection import wait
from dotenv import load_dotenv  # for python-dotenv method

load_dotenv()  # for python-dotenv method

import os
import allure
import requests
import ssl
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

ssl._create_default_https_context = ssl._create_unverified_context


base_url = "http://localhost:8005"
# headers = os.environ.get("HEADERS")
headers = {"Customer-Id": "999999", "User-Id": "999999"}
app_env = os.environ.get("APP_ENV")
api_token = os.environ.get("API_TOKEN")
api_token_secret = os.environ.get("API_TOKEN_SECRET")
form_id = os.environ.get("FORM_ID")
username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


class FormSteps:
    def __init__(self):
        pass

    @allure.step('GET /form/health')
    def get_form_health(**data):
        """
        GETs /form/health
        :param client: Rest Client with auth credentials
        """
        response = requests.get(f'{base_url}/form/health', headers=headers, **data)
        return response

    @allure.step("GET /form/form/form-id/{form_id}")
    def get_form_by_form_id(form_id, **data):
        """
        GETs /form/form
        :param client: Rest Client with auth credentials
        :param form_id: Survey Form ID
        """
        return requests.get(
            f"{base_url}/form/form/form-id/{form_id}", headers=headers, **data
        )

    @allure.step("GET /form/form/survey-id/{survey_id}")
    def get_form_by_survey_id(survey_id, **data):
        """
        GETs /form/form
        :param client: Rest Client with auth credentials
        :param survey_id: Survey Survey ID
        """
        return requests.get(
            f"{base_url}/form/form/survey-id/{survey_id}", headers=headers, **data
        )

    @allure.step("POST /form/form")
    def post_form(**data):
        """
        POSTs /form/form
        :param client: Rest Client with auth credentials
        """
        return requests.post(f"{base_url}/form/form", headers=headers, **data)

    @allure.step("PUT /form/form")
    def put_form(**data):
        """
        PUTs /form/form
        :param client: Rest Client with auth credentials
        """
        return requests.put(f"{base_url}/form/form", **data)
    def get_uuid(survey_id, **data):
            """
            GETs /form/form
            :param survey_id: Survey Survey ID
            """
            response =  requests.get(f'{base_url}/form/form/survey-id/{survey_id}', **data)
            response_json = response.json()
            uuid = response_json['id']
            return uuid

    def put_add_question_by_survey_id(survey_id, **data):
        """
        PUTs API call to add question to survey
        :param client: Rest Client with auth credentials
        """
        return requests.put(
            f"http://{app_env}/v5/survey/{survey_id}/surveypage/1/surveyquestion?api_token={api_token}&api_token_secret={api_token_secret}&_method=PUT&title=Question that was added. :-)&base_type=Question&type=RADIO",
            **data,
        )

    def post_update_question_by_survey_id(survey_id, **data):
        """
        POSTs API call to update question in survey
        :param client: Rest Client with auth credentials
        """
        return requests.post(
            f"http://{app_env}/v5/survey/{survey_id}/surveypage/1/surveyquestion/2?api_token={api_token}&api_token_secret={api_token_secret}&_method=POST&title=Updated question title",
            **data,
        )
        # Updating question with ID 2

    def delete_question_by_survey_id(survey_id, **data):
        """
         API call to delete question in survey
        :param client: Rest Client with auth credentials
        """
        return requests.get(
            f"http://{app_env}/v5/survey/{survey_id}/surveypage/1/surveyquestion/6?api_token={api_token}&api_token_secret={api_token_secret}&_method=DELETE",
            **data,
        )
        # Deleting question ID 6

    def remove_new_added_question_by_survey_id(survey_id, qid, **data):
        """
         API call to delete the newly added question in survey for clean up.
        :param client: Rest Client with auth credentials
        """
        return requests.get(
            f"http://{app_env}/v5/survey/{survey_id}/surveypage/1/surveyquestion/{qid}?api_token={api_token}&api_token_secret={api_token_secret}&_method=DELETE",
            **data,
        )

    def restore_question_by_survey_id(survey_id, **data):
        """
        HTML call to open browser and login
        HTML call to restore deleted question to survey
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        # driver = webdriver.Chrome(options=options)
        driver = webdriver.Chrome(
            "/usr/local/selenium/drivers/chromedriver", options=options
        )
        # driver = self.driver
        driver.get("https://app.ksmith.dev.al2.test.us/login/v1")
        email = driver.find_element(By.NAME, "USERNAME")
        email.send_keys(username)
        passw = driver.find_element(By.NAME, "PASS")
        passw.send_keys(password)
        email.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)
        driver.get(
            f"https://app.ksmith.dev.al2.test.us/builder/restore-deleted-question/id/{survey_id}/pid/1/qid/6",
            **data,
        )
        driver.implicitly_wait(5)
        driver.close()
        # Restoring question ID 6 from deleted status webbrowser.open_new_tab('GFG.html')

    def revert_question_title_update(survey_id, **data):
        """
        API call to revert the question's title for next automation run
        """
        return requests.post(
            f"http://{app_env}/v5/survey/{survey_id}/surveypage/1/surveyquestion/2?api_token={api_token}&api_token_secret={api_token_secret}&_method=POST&title=Howdy Ho Hanky the Xmas poo",
            **data,
        )
        # Updating question with ID 2

    def generate_form() -> dict:
        form = {
            "id": "be6fc084-a1bc-2de3-f45g-6h7i8jk9d0d7",
            "phpSurveyId": 1234,
            "phpCustomerId": 99999,
            "formElements": [
                {
                    "id": "dfbff334-a1bc-2de3-f45g-6h7i8jk9d0d7",
                    "phpQuestionId": 1,
                    "formElementType": "question",
                    "questionType": "radio",
                    "title": "Can we add title & question_type to this object?",
                }
            ],
        }
        return form
