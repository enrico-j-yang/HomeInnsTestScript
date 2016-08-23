# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from common_test_step import CommonTestStep

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')      

class KoodarAndroidAssistantMyAccountTests(unittest.TestCase):
    __think_time = 2
    
    @classmethod
    def setUpClass(KoodarAssistantAndroidTests):
        logging.info("setUpClass") 
    
    @classmethod   
    def tearDownClass(KoodarAssistantAndroidTests):
        logging.info("tearDownClass") 
        
    def setUp(self):
        logging.info("setUp") 
        self.testStep = CommonTestStep()
        
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android HUD'
        #desired_caps['app'] = PATH(
        #    'apps/Assistant_v0.4.1_production.apk'
        #)
        desired_caps['appPackage'] = 'com.gexne.car.assistant'
        desired_caps['appActivity'] = 'systems.xos.car.android.product.companion.startup.SplashActivity'
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'

        self.testStep.init_appium(desired_caps)
        

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        
        sleep(self.__think_time)
        self.testStep.deinit_appium()


    def _common_login(self):
        logging.info("_common_login") 
        # launch assistant app if it installed
        self.testStep.launch_app_if_installed('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        # wait for login activity
        if self.testStep.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 5, 1):
            # input account and password
            self.testStep.input_textbox('com.gexne.car.assistant:id/login_phone_number', u'13824470628')
            self.testStep.input_secure_textbox('com.gexne.car.assistant:id/login_password', u'ygvuhbijn')
            sleep(self.__think_time)
            self.testStep.press_button('com.gexne.car.assistant:id/login_next')
        else:
            logging.info("*****wait for login activity time out*****") 
     
    #@unittest.skip("demostrating skipping")
    def test_logout(self):
        logging.info("test_logout") 
        self._common_login()
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.MainActivity', 5, 1)

        # enter my account 
        self.testStep.press_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]\
        /android.widget.FrameLayout[1]/android.view.View[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[6]")
        
        # wait for my account activity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.account.MyAccountActivity', 5, 1)
        
        # enter account info
        self.testStep.press_widget("//android.widget.TextView[@text='账户信息']")

        # wait for account info activity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.account.AccountInfoActivity', 5, 1)

        # log out
        self.testStep.press_widget("//android.widget.TextView[@text='退出登录']")
        # confirm log out
        self.testStep.press_button("android:id/button1")
        # wait for login activity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.startup.login.LoginActivity', 5, 1)
    


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantMyAccountTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
