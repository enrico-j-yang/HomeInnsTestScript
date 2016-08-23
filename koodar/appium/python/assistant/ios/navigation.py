# -*- coding: utf-8 -*-
import unittest
import os


from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from time import sleep


class KoodarAssistantIOSTests(unittest.TestCase):
    think_time = 3

    def setUp(self):
        app = os.path.abspath('/Users/christine/Desktop/Radish.app')
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '9.3'
        desired_caps['deviceName'] = 'iPhone 6s Plus'
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        #desired_caps['udid'] = '4be7ab31bff7d81b6b8ad849ca47e42fc857c7e9'
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.touchAction = TouchAction(self.driver)


    def tearDown(self):
        #end the session
        sleep(self.think_time)
        self.driver.quit()
        
    @unittest.skip("demostrating skipping")
    def test_login_intelligentWord(self):

        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()

            self.driver.switch_to_alert().accept()
            sleep(self.think_time)

            #get the scream size
            self.touchAction = TouchAction(self.driver)
            aMap = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            aMapSize = aMap.size
            print aMapSize

            #touch the searchBox 
            self.touchAction.press(aMap, aMapSize['width']/2 , 21).release().perform()
            print "y=21"
            #self.touchAction.press(aMap, 10, aMapSize['height']/2 ).release().perform()
            #print "x=5"
            #self.touchAction.press(aMap, 10, 21).release().perform()
            #print "x=5, y=21"         
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]").send_keys(u"广州")


            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]')))
            #click into the first option
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]").click()
            
            #push into koodar
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]')))
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]").click()
            self.driver.switch_to_alert().accept()

            
            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]')))
            #check the way
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]").click()
            #wait for the element loading
            #currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')))
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[2]").click()
            #self.driver.switch_to_alert().accept()

            #back
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            
            sleep(self.think_time)

        finally:
            print "Test finsh"
            #self.driver.quit()
            #if not success:
            #raise Exception("Test failed.")
            
        
        
    @unittest.skip("demostrating skipping")
    def test_login_collect(self):
        
        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            sleep(self.think_time)
            self.driver.switch_to_alert().accept()
            sleep(self.think_time)

            #click into collect
            favorite_list = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[3]")
            self.assertTrue(favorite_list)
            self.touchAction.press(favorite_list).release().perform()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]')))
            #click into the first option
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[2]").click()

            #push into koodar
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]')))
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]").click()
            self.driver.switch_to_alert().accept()

            #view route
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]')))
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]").click()
            sleep(self.think_time)
            #currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')))
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[2]").click()
            #self.driver.switch_to_alert().accept()
            #sleep(self.think_time)

        finally:
            print "Test finsh"


    @unittest.skip("demostrating skipping")
    def test_login_longPress(self):
        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            sleep(self.think_time)
            self.driver.switch_to_alert().accept()
            sleep(self.think_time)

            # select a location on the map
            self.touchAction = TouchAction(self.driver)
            aMap = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            aMapSize = aMap.size
            print aMapSize

            #self.assertTrue(map)
            self.touchAction.press(aMap, aMapSize['width']/2 , 66).wait(10000).release().perform()

            #push into koodar
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]')))
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[2]").click()
            self.driver.switch_to_alert().accept()

            # view route
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]')))
            get_route_layout = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[3]")
            self.touchAction.press(get_route_layout).release().perform()
            sleep(self.think_time)
            #currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIAButton[2]')))
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[2]").click()
            #self.driver.switch_to_alert().accept()
            #sleep(self.think_time)

        finally:
            print "Test finsh"



    @unittest.skip("demostrating skipping")
    def test_login_enlarge(self):
        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            sleep(self.think_time)
            self.driver.switch_to_alert().accept()
            sleep(self.think_time)

            #enlarge the map(wrong)
            pinch(self, self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]"), percent=200, steps=50)

        finally:
            print "Test finsh"



    #@unittest.skip("demostrating skipping")
    def test_login_history(self):
        wd = self.driver
        wait = WebDriverWait(wd, 10)

        try: 
            # input account and password
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            sleep(self.think_time)

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            sleep(self.think_time)
            self.driver.switch_to_alert().accept()
            sleep(self.think_time)

            #get the scream size
            self.touchAction = TouchAction(self.driver)
            aMap = self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            aMapSize = aMap.size
            print aMapSize

            #touch the searchBox 
            self.touchAction.press(aMap, aMapSize['width']/2 , 21).release().perform()
            print "y=21"
            #self.touchAction.press(aMap, 10, aMapSize['height']/2 ).release().perform()
            #print "x=5"
            #self.touchAction.press(aMap, 10, 21).release().perform()
            #print "x=5, y=21"         
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]").send_keys(u"广州")


            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]')))
            #click into the first option
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATableView[1]/UIATableCell[1]/UIAStaticText[1]").click()
            #back
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()

            #wait for the element loading
            currently_waiting_for = wait.until(EC.element_to_be_clickable((By.XPATH,'//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]')))
            #click into Navigation
            self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]").click()
            self.touchAction.press(aMap, aMapSize['width']/2 , 21).release().perform()
            sleep(self.think_time)

        finally:
            print "Test finsh"         




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


