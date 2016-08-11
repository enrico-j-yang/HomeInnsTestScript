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
        desired_caps['deviceName'] = 'Android HUD'
        #desired_caps['app'] = PATH(
        #    'apps/Assistant_v0.4.1_production.apk'
        #)
        desired_caps['appPackage'] = 'com.gexne.car.assistant'
        desired_caps['appActivity'] = 'systems.xos.car.android.product.companion.startup.SplashActivity'
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


    def __common_login(self):
        print "__common_login"
        # launch assistant app if it installed
        el = self.driver.is_app_installed('com.gexne.car.assistant')
        self.assertTrue(el)
        el = self.driver.start_activity('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        self.assertTrue(el)
        # wait for login activity
        if self.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3, 1):
            # input account and password
            phone_number = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_phone_number')
            self.assertTrue(phone_number)
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            for i in [1, len(imes)]:
                if imes[i - 1] != "io.appium.android.ime/.UnicodeIME":
                    self.driver.activate_ime_engine(imes[i - 1])
            phone_number.send_keys(u"13824470628")
            password = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_password')
            self.assertTrue(password)
            self.touchAction.press(password).release().perform() # because send_keys miss first character, so here come one blank as to avoid this problem
            password.send_keys(u"ygvuhbijn")
            sleep(self.__think_time)
            login = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_next')
            self.assertTrue(login)
            self.touchAction.press(login).release().perform()
        else:
            print "*****wait for login activity time out*****"
                
            
    #@unittest.skip("demostrating skipping")
    def test_login(self):
        print "test_login"

        # launch assistant app if it installed
        el = self.driver.is_app_installed('com.gexne.car.assistant')
        self.assertTrue(el)
        el = self.driver.start_activity('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        self.assertTrue(el)
        # wait for login activity
        if self.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3, 1):
            print "*****login activity OK*****"
        else:
            print "*****wait for login activity time out*****"

        self.assertTrue('systems.xos.car.android.product.companion.startup.login.LoginActivity' == self.driver.current_activity)
        # input account and password
        try:
            phone_number = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_phone_number')
            self.assertTrue(phone_number)
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            for i in [1, len(imes)]:
                if imes[i - 1] != "io.appium.android.ime/.UnicodeIME":
                    self.driver.activate_ime_engine(imes[i - 1])
            phone_number.send_keys(u'13824470628')
            password = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_password')
            self.assertTrue(password)
            self.touchAction.press(password).release().perform() # because send_keys miss first character, so here come one blank as to avoid this problem
            password.send_keys(u'ygvuhbijn')
            sleep(self.__think_time)
            login = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_next')
            self.assertTrue(login)
            self.touchAction.press(login).release().perform()
        except Exception as e:
            print e
        
        # wait for main activity
        if self.driver.wait_activity('systems.xos.car.android.product.companion.MainActivity', 3, 1):
            print "*****main activity OK*****"
        else:
            print "*****wait for main activity time out*****"
        
        self.assertTrue('systems.xos.car.android.product.companion.MainActivity' == self.driver.current_activity)
            
    
    #@unittest.skip("demostrating skipping")
    def test_logout(self):
        print "test_logout"
        self.__common_login()
        if self.driver.wait_activity('systems.xos.car.android.product.companion.MainActivity', 3, 1):
            print "*****main activity OK*****"
        else:
            print "*****wait for main activity time out*****"
            
        self.assertTrue('systems.xos.car.android.product.companion.MainActivity' == self.driver.current_activity)
        # enter my account 
        navigation = self.driver.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]\
        /android.widget.FrameLayout[1]/android.view.View[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[5]")
        self.assertTrue(navigation)
        self.touchAction.press(navigation).release().perform()
        # enter account info
        account = self.driver.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]\
        /android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[1]")
        #xpath //android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[1]
        self.assertTrue(account)
        self.touchAction.press(account).release().perform()
        # log out
        logout = self.driver.find_element_by_id("com.gexne.car.assistant:id/account_info_logout")
        self.assertTrue(logout)
        self.touchAction.press(logout).release().perform()
        # confirm log out
        confirm = self.driver.find_element_by_id("android:id/button1")
        self.assertTrue(confirm)
        self.touchAction.press(confirm).release().perform()
        
        # wait for login activity
        if self.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3, 1):
            print "*****login activity OK*****"
        else:
            print "*****wait for login activity time out*****"

        self.assertTrue('systems.xos.car.android.product.companion.startup.login.LoginActivity' == self.driver.current_activity)
                
    @unittest.skip("demostrating skipping")
    def test_navigation(self):
        print "test_navigation"
        self.__common_login()
        if self.driver.wait_activity('systems.xos.car.android.product.companion.MainActivity', 3, 1):
            print "*****main activity OK*****"
        else:
            print "*****wait for main activity time out*****"
            
        self.assertTrue('systems.xos.car.android.product.companion.MainActivity' == self.driver.current_activity)
        # enter navigation 
        navigation = self.driver.find_element_by_xpath("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]\
        /android.widget.FrameLayout[1]/android.view.View[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[2]")
        self.assertTrue(navigation)
        self.touchAction.press(navigation).release().perform()
        # wait for map activity    
        el = self.driver.wait_activity('systems.xos.car.android.product.companion.navigation.MapActivity', 3, 1)
        self.assertTrue(el)
        # search destination by input name in the search text box
        search_edit = self.driver.find_element_by_id("com.gexne.car.assistant:id/search_edt")
        self.assertTrue(search_edit)
        self.touchAction.tap(search_edit)
        self.driver.activate_ime_engine("io.appium.android.ime/.UnicodeIME")
        search_edit.send_keys(u"广州")
        search_btn = self.driver.find_element_by_id("com.gexne.car.assistant:id/search_btn")
        self.assertTrue(search_btn)
        self.touchAction.press(search_btn).release().perform()
        #self.driver.hide_keyboard()
        sleep(self.__think_time)
        


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
