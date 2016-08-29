# -*- coding: utf-8 -*-
import unittest
import os
import sys
import logging
from appium import webdriver

from time import sleep


sys.path.append("../..")
from common.common_test_step import CommonTestStep


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
    


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')
                
class KoodarIOSAssistantAccountAtomTests(unittest.TestCase):
    def __init__(self, testStep, platformName):
        self.testStep = testStep
        self.platformName = platformName
        
    def __common_launch_app(self):
        if self.platformName == 'Android':
            # launch assistant app if it installed
            self.testStep.launch_app_if_installed('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        
            self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.startup.SplashActivity')
        elif self.platformName == 'iOS':
            self.testStep.driver.launch_app()
            
    def __common_login(self):
        # wait for login window
        if self.platformName == 'Android':
            if self.testStep.wait_window('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3):
                # input account and password
                self.testStep.input_textbox('com.gexne.car.assistant:id/login_phone_number', u'13824470628')
                self.testStep.input_secure_textbox('com.gexne.car.assistant:id/login_password', u'ygvuhbijn')
                self.testStep.tap_button('com.gexne.car.assistant:id/login_next')
            else:
                logging.info("*****wait for login window time out*****") 
        elif self.platformName == 'iOS':
            if self.testStep.wait_window("//UIAButton[@name='登录']"):
                # input account and password
                self.testStep.input_textbox("//UIATextField", u'13824470628')
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
                self.testStep.input_secure_textbox("//UIASecureTextField[@value='密码']", u'ygvuhbijn')
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
                self.testStep.tap_button("//UIAButton[@name='登录']")
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            else:
                logging.info("*****wait for login window time out*****") 
    
    def account_logout(self):
        #self.__common_launch_app()
        self.__common_login()

        # enter my account 
        self.testStep.wait_widget("//UIACollectionCell[@name='我的账户']")
        #click into Navigation
        self.testStep.tap_widget("//UIACollectionCell[@name='我的账户']")
        
        # wait for my account activity
        self.testStep.wait_widget("//UIATableCell[@name='账户信息']")
        # enter account info
        self.testStep.tap_widget("//UIATableCell[@name='账户信息']")

        # wait for account info activity
        self.testStep.wait_widget("//UIAButton[@name='退出登录']")
        # log out
        self.testStep.tap_widget("//UIAButton[@name='退出登录']")
        # wait for login activity
        self.testStep.wait_and_check_window_show_up("//UIAButton[@name='登录']")
        

    # atom test function list here for random combination test 
    # make sure all all atom test tunction listed below
    atom_test_list = {'account_logout':account_logout
                        }
            
class KoodarIOSAssistantAccountTests(unittest.TestCase):
    think_time = 3

    def setUp(self):
        logging.info("setUp") 
        self.testStep = CommonTestStep()
        
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '9.3'
        desired_caps['deviceName'] = 'iPhone 6s Plus'
        desired_caps['autoLaunch'] = 'False'
        # for eal device
        #desired_caps['app'] = '/Users/enrico/Documents/Work/RD/Avocado/Test Design/koodar/appium/apps/Radish-Debug.ipa'
        #desired_caps['bundleId'] = 'com.gexne.car.assistant'
        #desired_caps['udid'] = '9c3bfe9438fcb01fde3cff021b8cfdff0cf2bc09' 
        # for simulatorr
        # .app for simulator
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        desired_caps['app'] = '/Users/enrico/Documents/Work/RD/Avocado/Test Design/koodar/appium/apps/Radish.app'
        desired_caps['language'] = 'zh-Hans' # for iphone simulator, input method should be force decided
        desired_caps['locale'] = 'zh_CN' # for iphone simulator, locale should be force decided
        
        self.testStep.init_appium(desired_caps, case_function_name = self.id().split(".")[-1])
        self.atomTest = KoodarIOSAssistantAccountAtomTests(self.testStep, desired_caps['platformName'])

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        case_function_name = self.id().split(".")[-1]
        self.testStep.deinit_appium(case_function_name)
        

    def test_account_logout(self):
        self.atomTest.account_logout()
        

    if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantIOSTests)
        unittest.TextTestRunner(verbosity=2).run(suite)


