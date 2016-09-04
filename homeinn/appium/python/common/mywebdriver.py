# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException

from myelement import WebElement as MyElement
from myelement import PositionProperty

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')




class UnknownStringException(Exception):
    def __init__(self, value=None):
        self.value = value
        
class WebDriver(webdriver.Remote):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):

        super(WebDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive)
        


    def create_web_element(self, element_id):
        """
        Creates a web element with the specified element_id.
        Overrides method in Selenium WebDriver in order to always give them
        Appium WebElement
        """
        return MyElement(self, element_id)
            
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
            
    # implicit wait element before find it
    # find element by id and xpath with input string parsing
    #
    def find_element_by_string(self, string, timeout=10, interval=1):
        logging.debug("string is %s"+string)
        wait = WebDriverWait(self, timeout, interval)
        #logging.debug("element is %s", element)
        if (self.check_string_type(string) == "id"):
            logging.debug("string is id")
            #wait.until(lambda dr: dr.find_element_by_id(string).is_displayed())
            element = self.find_element_by_id(string)
        elif (self.check_string_type(string) == "xpath"):
            logging.debug("string is xpath")
            #wait.until(lambda dr: dr.find_element_by_xpath(string).is_displayed())
            element = self.find_element_by_xpath(string)
        else:
            logging.error("string is unknown")
            raise UnknownStringException

        logging.debug("element is %s", element)
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