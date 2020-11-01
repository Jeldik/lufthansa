from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import logging as logger


def open_browser(browser=None):
    if not browser or browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome()
    elif browser.lower() == "headless":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox()
    elif browser.lower() == "ie":
        driver = webdriver.Ie()
    elif browser.lower() == "opera":
        driver = webdriver.Opera()
    elif browser.lower() == "safari":
        driver = webdriver.Safari()
    else:
        raise Exception("The browser type '{}' is not supported. Try from: chrome, firefox, IE, opera and safari"
                        .format(browser))

    driver.implicitly_wait(30)
    driver.delete_all_cookies()

    return driver


def go_to_page(context, url):
    context.driver.get(url)


def assert_text_visible(context, expected_text, element):
    element = find_element(context, element)

    return element.text == expected_text


def assert_element_visible(context, element):
    assert WebDriverWait(context.driver, 5).until(expected_conditions.presence_of_element_located(element))


def assert_page_title(context, expected_title):
    actual_title = context.driver.title

    assert expected_title == actual_title, "The title is not as expected." \
                                           " Expected: {}, Actual: {}".format(expected_title, actual_title)


def assert_current_url(context, expected_url):
    current_url = context.driver.url

    assert expected_url == current_url, "The current url is not as expected." \
                                        " Expected: {}, Actual: {}".format(expected_url, current_url)


def assert_url_contains(context, text):
    contains = url_contains(context, text)

    assert contains, f"Current url '{context.driver.current_url}' does not contains '{text}'."


def url_contains(context, text):
    current_url = context.driver.current_url
    if text in current_url:
        return True
    else:
        return False


def assert_element_text(context, element, text):
    element = context.driver.find_element(*element)

    # TODO Odebrat
    logger.info("text = " + text)
    logger.info("element = " + element.text.lower())

    assert text.lower() == element.text.lower(), f"Expected text is not on the page!"


def find_element(context, element):
    return context.driver.find_element(*element)


def get_element_text(context, element):
    return find_element(context, element).text


def find_elements(context, elements):
    return context.driver.find_elements(*elements)


def go_off_the_element(context):
    actions = ActionChains(context.driver)
    actions.send_keys(Keys.TAB)
    actions.perform()


def type_value_into_field(context, value, element):
    context.driver.find_element(*element).send_keys(value)


def switch_to_new_tab(context):
    # context.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    window_after = context.driver.window_handles[1]
    context.driver.switch_to_window(window_after)
