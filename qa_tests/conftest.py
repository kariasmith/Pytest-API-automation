import pytest
import os
from _pytest.runner import runtestprotocol
import logging
import qa_tests.utilities.custom_logger as cl


@pytest.fixture(scope="function", autouse=True)
def setUp(request):
    print(":::::::::::::::::::::: Running method level setUp :::::::::::::::::::::::")
    yield
    print(":::::::::::::::::::::: Running method level tearDown :::::::::::::::::::::")


@pytest.fixture(scope="function") # scope = class
def oneTimeSetUp(request, browser):
    print("::::::::::::::::::::::::: Running one time setUp ::::::::::::::::::::::::::")
    log = cl.customLogger(logging.DEBUG)
    log.info("*****" * 25)
    log.info("SetUp Method")
    log.info("Initializing API Tests")
    log.info("*****" * 25)

    # if request.cls is not None:
    #     request.cls.driver = driver
    # yield driver
    # log.info("...................Teardown method............................")
    # driver.quit()
    # print("::::::::::::::::::::: Running one time tearDown :::::::::::::::::::::::::")


def pytest_addoption(parser):
    parser.addoption("--browser", help="Type of the browser")
    parser.addoption("--osType", help="Type of the operating system")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")


