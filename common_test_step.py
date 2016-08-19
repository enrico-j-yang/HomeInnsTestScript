# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support.ui import WebDriverWait  

from mywebdriver import MyWebDriver

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
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def test_step_info(func):
    def _func(*args, **kw):
        objPtr = args[0]
        objPtr.step = objPtr.step + 1
        logging.info("test step %d %s", objPtr.step, func.__name__)
        result=func(*args, **kw)

        if  objPtr.step_screen_shot == True:
            # take screen shot after every step function
            # it will slow down the test and use much more storage space
            case_function_name = func.__name__
            screenshotname = "./step " + str(objPtr.step) + " "+ case_function_name + ".png"
            objPtr.driver.get_screenshot_as_file(screenshotname)
                
        return result
    return _func


class CommonTestStep(unittest.TestCase):
    def __init__(self):
        self.step = 0
        
        
    #@test_step_info
    def init_appium(self, desired_caps, step_screen_shot=False):
        self.step_screen_shot = step_screen_shot
        self.driver = MyWebDriver('http://localhost:4723/wd/hub', desired_caps)
        self.touchAction = TouchAction(self.driver)
        
        self.ime = self.driver.active_ime_engine
        logging.debug("self.ime is %s", self.ime)
        if self.ime == u"io.appium.android.ime/.UnicodeIME":
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            imes = self.driver.available_ime_engines
            for i in [1, len(imes)]:
                if imes[i - 1] != u"io.appium.android.ime/.UnicodeIME":
                    self.driver.activate_ime_engine(imes[i - 1])
                    self.ime = imes[i - 1]
                    logging.debug("self.ime is %s", self.ime)
                    
    #@test_step_info    
    def deinit_appium(self, screen_shot_file):
        screenshotname = "./" + screen_shot_file + ".png"
        sleep(1)
        self.driver.get_screenshot_as_file(screenshotname)
        self.driver.quit()
        
    @test_step_info
    def wait_window(self, window, timeout=10, interval=1):
        return self.driver.wait_activity(window, timeout, interval)
        
    @test_step_info    
    def wait_window_show_up(self, activity, timeout=10, interval=1):
        el = self.driver.wait_activity(activity, timeout, interval)
        self.assertTrue(el)

    # function wait for act activity and check it show up or not within duration specified by parameter timeout
    # checking interval is specified by parameter interval 
    @test_step_info
    def wait_and_check_window_show_up(self, activity, timeout=10, interval=1):
        if self.driver.wait_activity(activity, timeout, interval):
           logging.info("*****"+activity+" OK*****") 
        else:
           logging.error("*****wait for "+activity+" time out*****") 
   
        self.assertTrue(activity == self.driver.current_activity)
        
    @test_step_info
    def wait_widget(self, string, timeout=10, interval=1): 
        wait = WebDriverWait(self.driver, timeout, interval)
        wait.until(lambda dr: dr.find_element_by_string(string).is_displayed())

    @test_step_info
    def launch_app_if_installed(self, package, activity):
        el = self.driver.is_app_installed(package)
        self.assertTrue(el)
        el = self.driver.start_activity(package, activity)
        self.assertTrue(el)
    
    @test_step_info    
    def input_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        self.assertTrue(textbox)
        # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
        # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)

        self.touchAction.press(textbox).release().perform()
        textbox.send_keys(text)
    
    @test_step_info    
    def input_secure_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        self.assertTrue(textbox)
        
        # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
        # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)
        
        self.touchAction.press(textbox).release().perform() # because send_keys miss first character, so here come one blank as to avoid this problem
        textbox.send_keys(text)
    
    @test_step_info
    def input_textbox_uft8(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(u"io.appium.android.ime/.UnicodeIME")
        logging.debug("ime is %s", self.driver.active_ime_engine)
        textbox.send_keys(text)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)
    
    @test_step_info    
    def press_button(self, string):
        button = self.driver.find_element_by_string(string)
        self.assertTrue(button)
        self.touchAction.press(button).release().perform()
    
    @test_step_info    
    def press_widget(self, string):
        widget = self.driver.find_element_by_string(string)
        self.assertTrue(widget)
        self.touchAction.press(widget).release().perform()
        
    @test_step_info
    def press_button_sibling_widget(self, button_string, widget_string):
        widget = self.driver.find_element_by_string(widget_string)
        self.assertTrue(widget)
        
        if (self.driver.check_string_type(button_string) == "id"):
            logging.debug("string is id")
            button = widget.parent.find_element_by_id(button_string)
        elif (self.driver.check_string_type(button_string) == "xpath"):
            logging.debug("string is xpath")
            button = widget.parent.find_element_by_xpath(button_string)
        else:
            logging.error("string is unknown")
            raise UnknownStringException
            
        self.assertTrue(button)
        self.touchAction.press(button).release().perform()

    @test_step_info
    def press_widget_tap(self, string, x=0, y=0, duration=1000):
        self.touchAction = TouchAction(self.driver)
        widget = self.driver.find_element_by_string(string)
        
        if x==0 and y==0:
            size = widget.size
            x = size["width"] / 2
            y = size["height"]/ 2  + 50
            print size, x , y
        
        self.touchAction.long_press(widget, x, y, duration).release().perform()
        
    @test_step_info
    def ensure_checkbox_checked(self, string):
        checkbox = self.driver.find_element_by_string(string)
        self.assertTrue(checkbox)
        print checkbox.checked
        if not (checkbox.is_selected()):
            self.touchAction.press(checkbox).release().perform()
            print checkbox.checked
    
    @test_step_info
    def press_button_if_exist(self, string):
        try:
            button = self.driver.find_element_by_string(string)        
            self.touchAction.press(button).release().perform()
            logging.debug("%s button exists", string)
        except:
            logging.debug("%s button not exist", string)