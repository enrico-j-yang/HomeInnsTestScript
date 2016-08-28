# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
import logging

from myelement import MyElement
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
        
class MyWebDriver(webdriver.Remote):
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):

        super(MyWebDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive)
        
        
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
        logging.debug("string is "+string)
        wait = WebDriverWait(self, timeout, interval)
        #element = MyElement()
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