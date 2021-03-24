from __future__ import annotations

from typing import Optional, Dict, List

from selenium.webdriver.remote.webelement import WebElement


class WebElementWrapper:
    _element: WebElement
    _parent: Optional[WebElementWrapper]
    _css: Dict

    def __init__(self, element: WebElement):
        self._element = element
        self._parent = None
        self._css = {}

    def __repr__(self):
        return f"WebElementWrapper({self._element!r})"

    def __hash__(self):
        return hash(self._element)

    def __eq__(self, other):
        return self._element == other.raw_element

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def raw_element(self) -> WebElement:
        return self._element

    def find_element_by_xpath(self, xpath: str) -> WebElementWrapper:
        return WebElementWrapper(self._element.find_element_by_xpath(xpath))

    def find_elements_by_xpath(self, xpath: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._element.find_elements_by_xpath(xpath)]

    def find_element_by_css_selector(self, css_selector: str) -> WebElementWrapper:
        return WebElementWrapper(self._element.find_element_by_css_selector(css_selector))

    def find_elements_by_css_selector(self, css_selector: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._element.find_elements_by_css_selector(css_selector)]

    def find_element_by_class_name(self, name: str) -> WebElementWrapper:
        return WebElementWrapper(self._element.find_element_by_class_name(name))

    def find_elements_by_class_name(self, name: str) -> List[WebElementWrapper]:
        return [WebElementWrapper(el) for el in self._element.find_elements_by_class_name(name)]

    def get_attribute(self, name):
        return self._element.get_attribute(name)

    def value_of_css_property(self, property_name: str) -> str:
        return self.raw_element.value_of_css_property(property_name)

    @property
    def rect(self) -> Dict[str, float]:
        return self._element.rect

    @property
    def size(self) -> float:
        rect = self.rect
        return rect["height"] * rect["width"]

    def has_width_or_height(self) -> bool:
        if (rect := self.rect)["width"] > 0 or rect["height"] > 0:
            return True
        return False

    @property
    def parent(self) -> WebElementWrapper:
        if not self._parent:
            self._parent = WebElementWrapper(self._element.find_element_by_xpath("./.."))
        return self._parent

    @property
    def children(self) -> List[WebElementWrapper]:
        return [WebElementWrapper(child) for child in self._element.find_elements_by_xpath("./child::*")]

    @property
    def tag_name(self) -> str:
        return self._element.tag_name

    @property
    def text(self) -> str:
        text = self._element.text.strip()
        if not text:
            if self.raw_element.tag_name == "input":
                try:
                    text = self.raw_element.get_attribute("value").strip()
                except:
                    pass
        return text

    @property
    def css(self) -> Dict:
        return self._css

    @css.setter
    def css(self, new_value: Dict) -> None:
        self._css = new_value

    def is_displayed(self) -> bool:
        return self._element.is_displayed()

    def get_screenshot_as_file(self, filename: str) -> None:
        self._element.screenshot(filename)

    def is_in_window_or_has_size(self) -> bool:
        """
        Checks if element is in window (right bottom of element has non-negative x and y)
        or elements height and width are greater than 0.
        :return: True if element is (potentially) visible, otherwise False.
        """
        if ((self._element.rect["x"] + self._element.rect["width"]) >= 0
            and (self._element.rect["y"] + self._element.rect["height"]) >= 0) \
                or (self._element.rect["height"] > 0 and self._element.rect["width"] > 0):
            return True
        return False

    def visually_contains(self, other: WebElementWrapper) -> bool:
        """
        Check if this element contains other by comparing left upper and right lower bounding box points.
        :param other: Another WebElementWrapper
        :return: bool
        """
        if other.rect["x"] < self.rect["x"] or other.rect["y"] < self.rect["y"]:
            return False
        if other.rect["x"] + other.rect["width"] > self.rect["x"] + self.rect["width"]:
            return False
        if other.rect["y"] + other.rect["height"] > self.rect["y"] + self.rect["height"]:
            return False
        return True
