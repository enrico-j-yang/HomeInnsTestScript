# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium.webdriver.webdriver import WebElement as AppiumWebElement
from selenium.webdriver.support.ui import WebDriverWait 
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

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')

class WebElement(AppiumWebElement):
    _porsition_property = PositionProperty()
    
    @property
    def position_property(self):
        return self._porsition_property
        
    def set_position_property(self, posPro):
        self._porsition_property = posPro
        
    def check_string_type(self, string):
        logging.debug("string is "+string)
        
        try:
            # id string?
            pos = string.index(":id/")
            logging.debug("pos is "+str(pos))
        except:
            try:
                # xpath string?
                pos = string.index("//")
                logging.debug("pos is "+str(pos))
            except:
                return "unknown"
            else:
                if pos == 0:
                    return "xpath"
        else:
            return "id"
            
    def find_element_by_string(self, string):
        logging.debug("string is "+string)
        if (self.check_string_type(string) == "id"):
            logging.debug("string is id")
            element = self.find_element_by_id(string)
        elif (self.check_string_type(string) == "xpath"):
            logging.debug("string is xpath")
            element = self.find_element_by_xpath(string)
        else:
            logging.error("string is unknown")
            raise UnknownStringException
        return element
        
        

    def find_elements_by_string(self, string, timeout=10, interval=1):
        logging.debug("string is %s"+string)
        wait = WebDriverWait(self, timeout, interval)
        #logging.debug("element is %s", element)
        if (self.check_string_type(string) == "id"):
            logging.debug("string is id")
            #wait.until(lambda dr: dr.find_element_by_id(string).is_displayed())
            elements = self.find_elements_by_id(string)
        elif (self.check_string_type(string) == "xpath"):
            logging.debug("string is xpath")
            #wait.until(lambda dr: dr.find_element_by_xpath(string).is_displayed())
            elements = self.find_elements_by_xpath(string)
        else:
            logging.error("string is unknown")
            raise UnknownStringException

        logging.debug("elements is %s", elements)
        return elements
    
    def get_position_property_of_element_by_visible_text(self, string, position):
        try:
            element = self.find_element_by_string("//*[contains(@text, '"+string+"')]")
        except NoSuchElementException:
            try:
                element = self.find_element_by_string("//*[contains(@label, '"+string+"')]")
            except NoSuchElementException:
                try:
                    element = self.find_element_by_string("//*[contains(@name, '"+string+"')]")
                except NoSuchElementException:
                    raise NoSuchElementException
                    
        rect = {'leftside': element.location.get('x'), 
                'topside': element.location.get('y'),
                'rightside': element.location.get('x')+element.size['width'], 
                'bottomside': element.location.get('y')+element.size['height']}
        posPro = PositionProperty(rect, position)
        #element.set_position_property(posPro)
        return posPro


        
    def near(self, string):
        posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._NEAR)
        posprolist = (posPro,);
        return posprolist
            
    def above(self, string):
        posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._ABOVE)
        posprolist = (posPro,);
        return posprolist
        
    def under(self, string):
        posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._UNDER)
        posprolist = (posPro,);
        return posprolist
    
    def left(sel, string):
        posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._LEFT)
        posprolist = (posPro,);
        return posprolist
    
    def right(sel, string):
        posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._RIGHT)
        posprolist = (posPro,);
        return posprolist