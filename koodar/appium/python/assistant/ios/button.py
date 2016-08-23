# -*- coding: utf-8 -*-
import unittest
import os
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from time import sleep


class KoodarAssistantIOSTests(unittest.TestCase):
    think_time = 8

    def setUp(self):
        # set up appium
        app = os.path.abspath('/Users/christine/Desktop/Radish.app')
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

        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[2]')))
            #click into Virtual button
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[2]").click()
            #there will have a switch need to handle
            sleep(10)
            self.driver.switch_to_alert().accept()
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]')))
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            sleep(self.think_time)

        finally:
            print "Test finsh"
        '''    self.driver.quit()
            if not success:
            raise Exception("Test failed.")
        '''


    if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantIOSTests)
        unittest.TextTestRunner(verbosity=2).run(suite)


