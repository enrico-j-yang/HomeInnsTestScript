# -*- coding: utf-8 -*-
import unittest
import os
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from time import sleep


class KoodarAssistantIOSTests(unittest.TestCase):
    think_time = 3

    def setUp(self):
        # set up appium
        app = os.path.abspath('apps/Radish.app')
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '9.3',
                'deviceName': 'iPhone 6s Plus'
            })


    def tearDown(self):
        #end the session
        sleep(self.think_time)
        self.driver.quit()
        

    def test_login(self):
        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            self.driver.switch_to_alert().accept()
            sleep(self.think_time)
            self.touchAction = TouchAction(self.driver)
            aMap = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            aMapSize = aMap.size
            print aMapSize

            self.touchAction.press(aMap, aMapSize['width']/2 , 21).release().perform()
            print "y=21"
            #self.touchAction.press(aMap, 10, aMapSize['height']/2 ).release().perform()
            #print "x=5"
            #self.touchAction.press(aMap, 10, 21).release().perform()
            #print "x=5, y=21"         
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]").send_keys("test search")
            sleep(self.think_time)

        finally:
            print "Test failed"
        '''    self.driver.quit()
            if not success:
            raise Exception("Test failed.")
        '''



    if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantIOSTests)
        unittest.TextTestRunner(verbosity=2).run(suite)


