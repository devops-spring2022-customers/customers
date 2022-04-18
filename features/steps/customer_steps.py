import os 
import requests
from behave import given, when, then

@given(u'the server is started')
def step_impl(context):
    context.base_url = os.getenv(
        'BASE_URL',
        'http://localhost:8080'
    )
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200

@when(u'I visit the "home page"')
def step_impl(context):
    context.resp = requests.get(context.base_url + '/')
    assert context.resp.status_code == 200


@then(u'I should see "{message}"')
def step_impl(context, message):
    assert message in str(context.resp.text)


@then(u'I should not see "{message}"')
def step_impl(context, message):
    assert message not in str(context.resp.text)