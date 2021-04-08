import logging
import time
from typing import Dict, List, Optional, Tuple, Union

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from .web_element_wrapper import WebElementWrapper


class WebDriverWrapper:
    """
    This class provides information about the page the driver is connected to, e.g. the size of the page,
    or the information about parents and children of a given element.
    """
    _driver: WebDriver
    _page_rect: Optional[Dict[str, float]]
    _page_size: Optional[float]
    _url: Optional[str]

    def __init__(self, driver: WebDriver):
        self._driver = driver
        self._page_rect = None
        self._page_size = None
        self._url = None

    def __del__(self):
        self.close_driver()

    def _reset(self) -> None:
        self._page_rect = None
        self._page_size = None
        self._url = None

    def close_driver(self):
        try:
            self._driver.close()
            self._driver.quit()
        except:
            pass

    def get(self, url: str, wait_time: int = 0, close_alert=False) -> bool:
        """
        Load page and check if page is accessible
        :param url: url to load
        :param wait_time: Time to wait after page load, e.g. to load dynamic content
        :param close_alert: If True possible alert windows on the page are automatically accepted.
        :return: True if page could be loaded, False otherwise
        """
        self._reset()
        self._url = url
        try:
            if not url.startswith("http"):
                if not url.startswith("www"):
                    url = f"www.{url}"
                url = f"http://{url}"
            self._driver.get(url)
            time.sleep(wait_time)
            self._driver.find_element_by_css_selector("body")
            if close_alert:
                def close_alert_helper():
                    alert = self._driver.switch_to.alert
                    if alert:
                        alert.dismiss()
                try:
                    WebDriverWait(self._driver, timeout=1).until(close_alert_helper())
                except:
                    pass
            return True
        except:
            logging.info(f"{url} failed to load.")
            return False

    @property
    def url(self) -> str:
        return self._url

    @property
    def page_rect(self) -> Dict[str, float]:
        if not self._page_rect:
            self._page_rect = self._driver.find_element_by_css_selector("body").rect
        return self._page_rect

    @property
    def page_size(self) -> float:
        if not self._page_size:
            page_rect = self.page_rect
            self._page_size = page_rect["height"] * page_rect["width"]
        return self._page_size

    @property
    def page_source(self) -> Union[int, List[Union[int, str]]]:
        """
        :return: HTML text of the current web page
        """
        return self._driver.page_source

    @property
    def window_rect(self) -> Dict:
        return self.get_window_rect()

    @property
    def domain(self) -> str:
        return self._driver.execute_script("return document.domain;")

    def execute_script(self, script: str, *args):
        return self._driver.execute_script(script, *args)

    def execute_script_from_file(self, file: str, *args):
        with open(file, "r") as f:
            script = f.read()
        return self.execute_script(script, *args)

    def find_element_by_xpath(self, xpath: str) -> WebElementWrapper:
        return WebElementWrapper(self._driver.find_element_by_xpath(xpath))

    def find_elements_by_xpath(self, xpath: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._driver.find_elements_by_xpath(xpath)]

    def find_element_by_css_selector(self, css_selector: str) -> WebElementWrapper:
        return WebElementWrapper(self._driver.find_element_by_css_selector(css_selector))

    def find_elements_by_css_selector(self, css_selector: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._driver.find_elements_by_css_selector(css_selector)]

    def find_element_by_class_name(self, name: str) -> WebElementWrapper:
        return WebElementWrapper(self._driver.find_element_by_class_name(name))

    def find_elements_by_class_name(self, name: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._driver.find_elements_by_class_name(name)]

    def find_element_by_id(self, name: str) -> WebElementWrapper:
        return WebElementWrapper(self._driver.find_element_by_id(name))

    def find_elements_by_id(self, name: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._driver.find_elements_by_id(name)]

    def find_element_by_tag_name(self, name: str) -> WebElementWrapper:
        return WebElementWrapper(self._driver.find_element_by_tag_name(name))

    def find_elements_by_tag_name(self, name: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._driver.find_elements_by_tag_name(name)]

    def get_window_rect(self) -> Dict:
        return self._driver.get_window_rect()

    def get_window_size(self) -> Dict:
        return self._driver.get_window_size()

    def set_window_size(self, width: float, height: float) -> None:
        self._driver.set_window_size(width, height)

    def get_window_position(self) -> Dict:
        return self._driver.get_window_position()

    def get_viewport_rect(self) -> Dict:
        """ This returns only the actual content rect of the page that is visible to the user.
            Ignores for example header of the window."""
        return self._driver.execute_script("return {\"width\": window.innerWidth, \"height\": window.innerHeight};")

    def get_viewport_size(self) -> float:
        viewport = self.get_viewport_rect()
        return float(viewport["height"] * viewport["width"])

    def fullscreen_window(self, wait_time: float) -> None:
        self._driver.fullscreen_window()
        time.sleep(wait_time)

    def get_screenshot_as_file(self, filename: str) -> None:
        self._driver.get_screenshot_as_file(filename)

    def get_screenshot_whole_page(self, filename: str) -> None:
        current = self.get_window_size()
        width = self.execute_script("return document.body.parentNode.scrollWidth")
        height = self.execute_script("return document.body.parentNode.scrollHeight")
        self.set_window_size(width, height)
        self.find_element_by_tag_name("body").get_screenshot_as_file(filename)
        self.set_window_size(current["width"], current["height"])

    def relative_size_of_element(self, element: WebElementWrapper) -> float:
        return element.size / self.page_size

    def element_size_is_larger_than_fraction_of_window_size(self, element: WebElementWrapper, ratio: float) -> bool:
        window_size = self.get_window_size()
        if element.size >= ratio * window_size["height"] * window_size["width"]:
            return True
        return False

    def check_ancestry(self, child: WebElementWrapper, ancestor: WebElementWrapper) -> bool:
        """
        check if ancestor is ancestor of child
        :param child: child node
        :param ancestor: possible ancestor
        :return: bool
        """
        # If both elements are the same, return False
        if child == ancestor:
            return False

        try:
            script = "return arguments[1].contains(arguments[0]);"
            return self._driver.execute_script(script, child.raw_element, ancestor.raw_element)
        except:
            return False

    def check_if_element_is_ancestor_of_multiple_elements(self, ancestor: WebElementWrapper,
                                                          childs: List[WebElementWrapper]):
        return all([self.check_ancestry(child, ancestor) for child in childs])

    def get_common_ancestor(self, elements: List[WebElementWrapper]) -> WebElementWrapper:
        if len(elements) == 0:
            logging.error("Empty list provided for WebDriverWrapper.get_common_ancestor")

        common_ancestor = elements[0]

        if len(elements) != 1:
            common_ancestor = common_ancestor.parent
            while not self.check_if_element_is_ancestor_of_multiple_elements(common_ancestor, elements[1:]):
                common_ancestor = common_ancestor.parent

        return common_ancestor

    def mark_elements(self, elements: Union[WebElementWrapper, List[WebElementWrapper], Tuple[WebElementWrapper]],
                      color: str = "red", border_width: str = "6px", border_style: str = "solid") -> None:
        """
        Marks elements on a page by setting a border.
        :param elements: List of elements to be marked.
        :param color: The color, valid strings are, e.g., red, blue, green, orange, ...
        :param border_width: Border width in pixels
        :param border_style: Different styles allowed by css
        """
        if not elements:
            return

        if isinstance(elements, WebElementWrapper):
            elements = [elements]

        for el in elements:
            self._driver.execute_script(
                f"arguments[0].style.borderColor = '{color}';"
                f"arguments[0].style.borderWidth = '{border_width}';"
                f"arguments[0].style.borderStyle = '{border_style}';",
                el.raw_element
            )

    def change_element_text(self, element: WebElementWrapper, text: str) -> None:
        self._driver.execute_script(
            f"arguments[0].textContent=\"{text}\";",
            element.raw_element
        )

    def draw_rectangle_around_elements(self, elements: Union[WebElementWrapper, List[WebElementWrapper],
                                                             Tuple[WebElementWrapper, ...]],
                                       container: WebElementWrapper,
                                       color: str = "red", border_width: str = "2px", border_style: str = "dashed") \
            -> None:
        if not elements:
            return

        if isinstance(elements, WebElementWrapper):
            elements = [elements]

        x = min([el.rect["x"] for el in elements]) - 5
        y = min([el.rect["y"] for el in elements]) - 5
        width = max([el.rect["x"] + el.rect["width"] for el in elements]) - x + 5
        height = max([el.rect["y"] + el.rect["height"] for el in elements]) - y + 5

        self._driver.execute_script(
            f"let body = document.getElementsByTagName(\"body\")[0];"
            f"let tag = document.createElement(\"dapda_info\");"
            f"let zInd = document.defaultView.getComputedStyle(arguments[0]).getPropertyValue(\"z-index\");"
            f"console.log(parent);"
            f"tag.style.cssText = \"position:absolute;"
            f"                      top:{y-container.raw_element.rect['y']}px;"
            f"                      left:{x-container.raw_element.rect['x']}px;"
            f"                      width:{width}px;"
            f"                      height:{height}px;"
            f"                      border: {border_width} {border_style} {color};"
            f"                      z-index: zInd + 1;\";"
            f"arguments[0].insertBefore(tag, arguments[0].firstChild);",
            container.raw_element
        )

    def mark_common_ancestor(self, elements: Union[WebElementWrapper, List[WebElementWrapper],
                                                   Tuple[WebElementWrapper, ...]],
                             color: str = "red", border_width: str = "2px", border_style: str = "dashed") -> None:
        if not elements:
            return

        if isinstance(elements, WebElementWrapper):
            elements = [elements]

        common_ancestor = self.get_common_ancestor(elements)

        self.mark_elements(common_ancestor, color, border_width, border_style)

    def switch_to_main_frame(self) -> None:
        self._driver.switch_to.default_content()

    def switch_to_frame(self, element: WebElementWrapper):
        self._driver.switch_to.frame(element.raw_element)
