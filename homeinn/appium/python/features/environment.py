
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep
import getpass
from simplecrypt import encrypt, decrypt

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
    usr = raw_input("Please input your HomeInn account:")
    if not usr=="":
        context.usr = encrypt("beHome", usr)
    auth = getpass.getpass("Please input your HomeInn password:")
    if not auth=="":
        context.auth = encrypt("beHome", auth)
    
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
    #desired_caps['udid'] = '022MWW1465012734'#Huawei P7
    #desired_caps['udid'] = '50da53b57d32'#Xiaomi Hongmi 2
    #desired_caps['udid'] = '8627d0e6' #Yan's Oppo

    context.testStep.init_appium(desired_caps)
    #if not context.config.log_capture:
    #    logging.basicConfig(level=logging.DEBUG)
    

    
def after_all(context):
    context.testStep.deinit_appium()
    
def before_feature(context, feature):
    context = context

def after_feature(context, feature):
    #case_function_name = feature.name
    context = context

def before_scenario(context, scenario):
    context = context
    
    #context.testStep.take_screen_shot_at_every_step(scenario.name.encode('utf8'))
    #context.testStep.driver.launch_app()
    
def after_scenario(context, scenario):
    #context = context
    screenshotname = "./" + scenario.name + ".png"
    sleep(1)
    context.testStep.driver.get_screenshot_as_file(screenshotname)
    if (scenario.status=='failed'):
        context.testStep.driver.close_app()