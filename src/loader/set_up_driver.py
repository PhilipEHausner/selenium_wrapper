import os
import sys

from selenium import webdriver

from wrapper.web_driver_wrapper import WebDriverWrapper


def get_firefox_driver(headless: bool = False) -> WebDriverWrapper:
    options = webdriver.firefox.options.Options()
    options.headless = headless
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/81.0.4044.141 Safari/537.36")
    options.add_argument("--lang=de-DE")

    file_path = os.path.dirname(os.path.realpath(__file__))
    if sys.platform == "win32":
        path = os.path.join(file_path, "..", "driver", "windows", "geckodriver.exe")
    else:  # Linux
        print(os.path.join(file_path, "..", "driver", "linux", "geckodriver"))
        path = os.path.join(file_path, "..", "driver", "linux", "geckodriver")
    driver = webdriver.Firefox(executable_path=path, options=options)
    driver.set_script_timeout(5)

    return WebDriverWrapper(driver)
