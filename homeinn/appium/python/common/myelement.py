# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium.webdriver.webdriver import WebElement as AppiumWebElement
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException
import logging

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class PositionProperty(object):
    _NONE = 0
    _NEAR = 1
    _LEFT = 2
    _RIGHT = 3
    _ABOVE = 4
    _UNDER = 5
    _IN = 6

    def __init__(self, rect={}, pos=_NONE):
        self._pos = pos
        self._rect = rect
    
    @property
    def rect(self):
        return self._rect
        
    @property
    def pos(self):
        return self._pos

class WebElement(AppiumWebElement):
    wait_duration = 60
    _porsition_property = PositionProperty()
    
    @property
    def position_property(self):
        return self._porsition_property
        
    def set_position_property(self, posPro):
        self._porsition_property = posPro
    
    def calc_distance(self, ref_rect, rect, position):
        return self.parent.calc_distance(ref_rect, rect, position)
        
    def check_string_type(self, string):
        return self.parent.check_string_type(string)
    
    def has_widget(self, string, posprolist=None):
        return self.parent.has_widget(string, posprolist)
        
    def find_element_by_string(self, string):
        return self.parent.find_element_by_string(string)
                    
    def find_elements_by_string(self, string, timeout=wait_duration, interval=1):
        return self.parent.find_elements_by_string(string, timeout, interval)
        
    def get_position_property_of_element_by_visible_text(self, string, position):
        return self.parent.get_position_property_of_element_by_visible_text(string, position)

    def _near(self, string):
        return self.parent._near(string)
            
    def _above(self, string):
        return self.parent._above(string)
        
    def _under(self, string):
        return self.parent._under(string)
    
    def _left(self, string):
        return self.parent._left(string)
    
    def _right(self, string):
        return self.parent._right(string)
    
    def _in(self, string):
        return self.parent._in(string)