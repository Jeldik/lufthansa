import logging as logger
import time
import Common.CommonFuncs.webcommon as webcommon
from behave import *
import config

logger.basicConfig(level="INFO")


@step("I go to the page {page}")
def go_to_page(context, page):
    url = config.URLCONFIG[page]
    webcommon.go_to_page(url, context)


@step('I click on {element}')
def click_on_element(context, element):
    context.driver.find_element(*config.ELEMENTCONFIG[element]).click()
    time.sleep(1)


@then('I Should see text: {text}')
def assert_text(context, text):
    element = config.ELEMENTCONFIG[text]
    webcommon.assert_element_text(context, element, text)


@step("the page title should be {expected_title}")
def verify_homepage_title(context, expected_title):
    time.sleep(1)
    webcommon.assert_page_title(context, expected_title)


@then("the page should be open in new tab with {expected_title} title")
def verify_homepage_title_new_tab(context, expected_title):
    time.sleep(1)
    webcommon.switch_to_new_tab(context)
    webcommon.assert_page_title(context, expected_title)


@step("current url should be {expected_url}")
def verify_current_url(context, expected_url):
    webcommon.assert_current_url(context, expected_url)


@then("{element} should be disabled")
def assert_element_is_disabled(context, element):
    element_class = context.driver.find_element(*config.ELEMENTCONFIG[element]).get_attribute("class")

    assert "disabled" in element_class


@step("I move off the element")
def move_off_element(context):
    webcommon.go_off_the_element(context)


@step("I type {value} into {element} field")
def type_value_into_field(context, value, element):
    field = config.ELEMENTCONFIG[element]
    value = config.DATACONFIG[value]
    webcommon.type_value_in_field(context, value, field)
