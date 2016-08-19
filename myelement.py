# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium.webdriver.webdriver import WebElement
from selenium.webdriver.support.ui import WebDriverWait 
import logging

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')

class MyElement(WebElement):
        
        
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