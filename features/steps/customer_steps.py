import os 
import json
import requests
from behave import given, when, then
import logging
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions
import time

ID_PREFIX = 'customer_'

@when(u'I visit the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)


@then('I should see "{message}" in the title')
def step_impl(context, message):
    expect(context.driver.title).to_contain(message)


@then(u'I should not see "{message}"')
def step_impl(context, message):
    elements = context.driver.find_elements(By.TAG_NAME, 'body')
    body = elements[0].text
    error_msg = "I should not see '%s' in '%s'" % (message, body)
    ensure(message in body, False, error_msg)


@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element_by_id(element_id)
    element.clear()
    element.send_keys(text_string)

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, element_id),
            ''
        )
    )
    expect(found).to_be(True)
    #element = context.driver.find_element_by_id(element_id)
    #expect(element.get_attribute('value')).to_be(u'')

@then('the "{element_name}" field should be empty from the "{model}" form')
def step_impl(context, element_name, model):
    element_id = ID_PREFIX + model.lower() + '_' + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, element_id),
            ''
        )
    )
    expect(found).to_be(True)
    #element = context.driver.find_element_by_id(element_id)
    #expect(element.get_attribute('value')).to_be(u'')


# ##################################################################
# # This code works because of the following naming convention:
# # The buttons have an id in the html hat is the button text
# # in lowercase followed by '-btn' so the Clean button has an id of
# # id='clear-btn'. That allows us to lowercase the name and add '-btn'
# # to get the element id of any button
# ##################################################################

@when('I press the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@when(u'I press the "{button}" button from the "{model}" form')
def step_impl(context, button, model):
    button_id = button.lower() + '-' + model.lower() + '-btn'
    context.driver.find_element_by_id(button_id).click()

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    expect(found).to_be(True)

@then('I should see "{name}" in the results for "{model}"')
def step_impl(context, name, model):
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results_address'),
            name
        )
    )
    expect(found).to_be(True)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element_by_id('search_results')
    error_msg = "I should not see '%s' in '%s'" % (name, element.text)
    ensure(name in element.text, False, error_msg)

@then('I should see the message "{message}"')
def step_impl(context, message):
    msg = "I should see '%s' in '%s'" % (message, context.resp.text)
    ensure(message in context.resp.text, False, msg)


# ##################################################################
# # These two function simulate copy and paste
# ##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I copy the "{element_name}" field from the "{model}" form')
def step_impl(context, element_name, model):
    element_id = ID_PREFIX + model.lower() + "_" + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

@when('I paste the "{element_name}" field to "{element_name_form}"')
def step_impl(context, element_name, element_name_form):
    element_id = element_name_form.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

# ##################################################################
# # This code works because of the following naming convention:
# # The id field for text input in the html is the element name
# # prefixed by ID_PREFIX so the Name field has an id='pet_name'
# # We can then lowercase the name and prefix with pet_ to get the id
# ##################################################################

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.text_to_be_present_in_element_value(
            (By.ID, element_id),
            text_string
        )
    )
    expect(found).to_be(True)

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@given('the following customers')
def step_impl(context):
    """ Delete all Customers and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the customers and delete them one by one
    context.resp = requests.get(context.base_url + '/customers')
    expect(context.resp.status_code).to_equal(200)
    for customer in context.resp.json():
        context.resp = requests.delete(context.base_url + '/customers/' + str(customer["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new customers
    create_url = context.base_url + '/customers'
    for row in context.table:
        data = {
            "first_name": row['first_name'],
            "last_name": row['last_name'],
            "userid": row['userid'],
            "password": row['password'],
            "addresses": []
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)