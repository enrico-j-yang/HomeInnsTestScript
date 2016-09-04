
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep

from behave import *
from behave.log_capture import capture

#from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction 

sys.path.append("../..")
from common.common_test_step import CommonTestStep
from common.mywebdriver import WebDriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

try:
    PATH.find("assistant/android/")
except:
    RESOURCE_PATH = "../resource/"
else:
    RESOURCE_PATH = "assistant/resource/"
    
def before_all(context):
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)
    
def after_all(context):
    context = context
    
def before_feature(context, feature):
    context = context

def after_feature(context, feature):
    context = context
    
def before_scenario(context, scenario):
    context.testStep = CommonTestStep()
    
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '5.1'
    desired_caps['deviceName'] = 'Android'
    desired_caps['appPackage'] = 'com.ziipin.homeinn'
    desired_caps['appActivity'] = '.activity.SplashActivity'
    desired_caps['autoLaunch'] = 'false'
    desired_caps['unicodeKeyboard'] = 'True'
    desired_caps['resetKeyboard'] = 'True'

    context.testStep.init_appium(desired_caps)
    context.touchAction = TouchAction(context.testStep.driver)
    
def after_scenario(context, scenario):
    case_function_name = scenario.name
    context.testStep.deinit_appium(case_function_name)