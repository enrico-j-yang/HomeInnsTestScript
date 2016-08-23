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
    
    def setUp(self):
        print "\nsetUp"
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'Android HUD'
        #desired_caps['app'] = PATH(
        #    'apps/Assistant_v0.4.1_production.apk'
        #)
        desired_caps['appPackage'] = 'com.gexne.car.carhome'
        desired_caps['appActivity'] = 'systems.xos.car.carhome.home.car.CarActivity'
        desired_caps['autoLaunch'] = 'false'
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        touchAction = TouchAction(self.driver)
        

    def tearDown(self):
        print "tearDown" 
        # end the session
        
        sleep(self.__think_time)
        self.driver.quit()
		
    def testNavigation(self):
        self.driver.launch_app()
        # wait for car activity
        if self.driver.wait_activity('systems.xos.car.carhome.home.car.CarActivity', 10, 1):
            print "*****car activity OK*****"
        else:
            print "*****car for main activity time out*****"
        
        self.assertTrue('systems.xos.car.carhome.home.car.CarActivity' == self.driver.current_activity)
        
        #print self.driver.find_element_by_id("com.gexne.car.carhome:id/signalView").is_displayed()
        #print self.driver.find_element_by_id("com.gexne.car.carhome:id/gpsView").is_displayed()
        #print self.driver.find_element_by_id("com.gexne.car.carhome:id/knobBatteryView").is_displayed()
        #print self.driver.find_element_by_id("com.gexne.car.carhome:id/obdView").is_displayed()
        #print self.driver.find_element_by_id("com.gexne.car.carhome:id/navigationView").is_displayed()
        self.driver.press_keycode(66)
        
        # wait for applist activity
        if self.driver.wait_activity('systems.xos.car.carhome.home.car.applist.AppListActivity', 10, 1):
            print "*****applist activity OK*****"
        else:
            print "*****applist for main activity time out*****"
        
        self.assertTrue('systems.xos.car.carhome.home.car.applist.AppListActivity' == self.driver.current_activity)
        
        bingoFlag = False
        while (self.driver.find_element_by_id("systems.xos.car.xsdk:id/current_name").text != u"导航"):
            self.driver.press_keycode(22)
        
        #print self.driver.find_element_by_id("systems.xos.car.xsdk:id/current_name").text
        self.driver.press_keycode(66)
        
        # wait for com.gexne.car.navigation/systems.xos.car.navigation.MapActivity activity
        finish = False
        timeout = 3
        while not (finish and timeout>0):
            try:
                self.driver.find_element_by_id("com.gexne.car.navigation:id/map_view")
            except Exception:
                sleep(1)
                timeout = timeout - 1
            else:
                finish = True
        
        if timeout > 0:
            print "*****map activity OK*****"
        else:
            print "*****wait for map activity time out*****"
        
        #self.assertTrue('systems.xos.car.navigation.MapActivity' == self.driver.current_activity)
        
        
        self.driver.press_keycode(66)
        
        sleep(10)
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
