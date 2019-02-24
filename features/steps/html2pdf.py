import io
import os

import PyPDF2
import requests
from behave import *

HERE = os.path.realpath(os.path.dirname(__file__))

use_step_matcher("re")

sent_result: requests.Response


@given("A micro-service up and running")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    result = requests.get('http://localhost:8888/')
    assert result.status_code == 405


@when('I send the content of the page "resources/example.html"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    global sent_result

    file_path = os.path.join(HERE, "resources", "example.html")
    content = open(file_path, 'rt').read()

    files = {"content": content}
    sent_result = requests.post('http://localhost:8888/', files=files)


@then("I receive a valid PDF file")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    with io.BytesIO(bytes(sent_result.content)) as stream:
        PyPDF2.PdfFileReader(stream)
