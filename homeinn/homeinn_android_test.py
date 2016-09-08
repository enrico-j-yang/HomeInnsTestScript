# -*- coding: utf-8 -*-

import os
import sys
from time import sleep

import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class KoodarAssistantAndroidTests(unittest.TestCase):
    __think_time = 2
    
    @classmethod
    def setUpClass(KoodarAssistantAndroidTests):
        print "\nsetUpClass"
    
    @classmethod   
    def tearDownClass(KoodarAssistantAndroidTests):
        print "\ntearDownClass"
        
    def setUp(self):
        print "\nsetUp"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android'
        desired_caps['appPackage'] = 'com.ziipin.homeinn'
        desired_caps['appActivity'] = '.activity.SplashActivity'
        
        #desired_caps['app'] = PATH(
        #    '/Users/enrico/Desktop/掌上如家_1470885797659.apk'
        #)
        
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.touchAction = TouchAction(self.driver)
        

    def tearDown(self):
        print "tearDown"
        # end the session
        
        sleep(self.__think_time)
        self.driver.quit()


    #@unittest.skip("demostrating skipping")
    def test_first_launch(self):
        print "test_first_launch"

        # remove and reinstall app to ensure first time open app circustance
        if self.driver.is_app_installed('com.ziipin.homeinn'):
            print "remove app"
            self.driver.remove_app('com.ziipin.homeinn')
        
        self.driver.install_app('/Users/enrico/Desktop/掌上如家_1470885797659.apk')
        self.assertTrue(self.driver.is_app_installed('com.ziipin.homeinn'))
        print "app installed"
            
        # launch app if it installed
        el = self.driver.start_activity('com.ziipin.homeinn', '.activity.SplashActivity')
        self.assertTrue(el)
        self.driver.wait_activity('.activity.SplashActivity', 5, 1)
        # wait for startshow activity
        if self.driver.wait_activity('.activity.StartShowActivity', 30, 1):
            print "*****startshow activity OK*****"
        else:
            print "*****wait for startshow activity time out*****"
            
        self.assertTrue('.activity.StartShowActivity' == self.driver.current_activity)
        
        finish = False
        while not (finish):
            try:
                self.driver.find_element_by_id("com.ziipin.homeinn:id/start_use_btn")
            except Exception:
                self.driver.swipe(600,486, 98,489, 500)
            else:
                finish = True
            
        start = self.driver.find_element_by_id("com.ziipin.homeinn:id/start_use_btn")
        self.assertTrue(start)
        self.touchAction.press(start).release().perform()    
        
        # wait for main activity
        if self.driver.wait_activity('.activity.MainActivity', 3, 1):
            print "*****main activity OK*****"
        else:
            print "*****wait for main activity time out*****"

        self.assertTrue('.activity.MainActivity' == self.driver.current_activity)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)