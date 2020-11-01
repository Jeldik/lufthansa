from datetime import datetime
import time
from behave import *
import logging as logger
import requests

import config
from Common.CommonFuncs import webcommon
from Common.CommonHelpers.awsHelpers import AwsHelpers
from Common.CommonHelpers.bearerAuth import BearerAuth


@given("I connect to broker and get updated data about flights")
def i_connect_to_broker_and_get_updated_data_about_flights(context):
    helper = AwsHelpers(context)
    helper.run()

    assert context.data.code == AwsHelpers.CONNECTED_CODE


@when("I request flight status from API")
def i_request_flight_status_from_api(context):
    full_flight_number = next(iter(context.queue))
    airline = full_flight_number[:2]
    flight_number = int(full_flight_number[2:10])
    flight_number_next = flight_number + 1

    context.flight_number = flight_number

    range = '{}-{}'.format(flight_number, flight_number_next)

    now = datetime.now()
    api_format_date = '{}{}{}'.format(now.strftime("%d"), now.strftime("%b").upper(), now.strftime("%y"))

    queue = context.queue.values()
    queue_iterator = iter(queue)
    event = next(queue_iterator)

    endpoint = 'https://api.lufthansa.com/v1/flight-schedules/flightschedules/passenger?airlines={}&flightNumberRanges={}&startDate={}' \
               '&endDate={}&daysOfOperation=1234567&timeMode=UTC'.format(airline, range, api_format_date, api_format_date)

    response = requests.get(endpoint, auth=BearerAuth(config.APICONFIG['token']))
    logger.info("Response status code = {}", response.status_code)

    if response.status_code == AwsHelpers.SUCCESS_CODE:
        departure_time = response.json()[0]['legs'][0]['aircraftDepartureTimeUTC']
        arrival_time = response.json()[0]['legs'][0]['aircraftArrivalTimeUTC']

        context.api_departure_time = departure_time
        context.api_arrival_time = arrival_time
        context.event = event

    assert response.status_code == AwsHelpers.SUCCESS_CODE


@step("go to lufthansa website")
def go_to_lufthansa_website(context):
    context.driver = webcommon.open_browser(context.config.userdata.get("browser"))
    webcommon.go_to_page(context, config.APICONFIG['lufthansa'])


@step("I click to flight status")
def i_click_to_flight_status(context):
    context.driver.find_element(*config.APICONFIG['flight_status']).click()
    time.sleep(1)


@step("enter data from API")
def enter_data_from_api(context):
    webcommon.type_value_into_field(context, context.flight_number, config.APICONFIG['flight_number_input'])
    context.driver.find_element(*config.APICONFIG['find_button']).click()


@then("data should be the same")
def data_should_be_the_same(context):
    event = context.event[14:]

    if event == 'Arrival':
        scheduled_time = webcommon.get_element_text(context, config.APICONFIG['arrival_time_train'])
        api_time = context.api_arrival_time
    else:
        scheduled_time = webcommon.get_element_text(context, config.APICONFIG['departure_time_train'])
        api_time = context.api_departure_time

    hh = scheduled_time[:2]
    mm = scheduled_time[3:]
    time_in_minutes = int(hh) * 60 + int(mm)

    assert time_in_minutes == api_time


@step("confirm privacy settings")
def confirm_privacy_settings(context):
    webcommon.find_element(context, config.APICONFIG['accept_button']).click()
