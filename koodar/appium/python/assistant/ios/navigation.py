# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest


from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
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
                
                
class KoodarAssistantIOSTests(unittest.TestCase):
    think_time = 3

    def setUp(self):
        logging.info("setUp") 
        self.testStep = CommonTestStep()
        
        desired_caps = {}
        desired_caps['platformName'] = 'iOS'
        desired_caps['platformVersion'] = '9.3'
        desired_caps['deviceName'] = 'iPhone 6s Plus'
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'
        desired_caps['language'] = 'zh-Hans'
        desired_caps['locale'] = 'zh_CN'
        #desired_caps['udid'] = '4be7ab31bff7d81b6b8ad849ca47e42fc857c7e9'

        self.testStep.init_appium(desired_caps)
        #self.atomTest = KoodarAndroidAssistantNavigationAtomTests(self.testStep)
        #self.atomTest.common_enter_navigation()

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        case_function_name = self.id().split(".")[-1]
        self.testStep.deinit_appium(case_function_name)
        
    #@unittest.skip("demostrating skipping")
    def test_login_intelligentWord(self):

        try: 
            self.testStep.wait_widget("//UIAButton[@name='登录']")
            # input account and password
            self.testStep.input_textbox("//UIATextField", u'13726260108')
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
            self.testStep.input_secure_textbox("//UIASecureTextField[@value='密码']", u'12345678')
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
            self.testStep.tap_button("//UIAButton[@name='登录']")
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()

            self.testStep.wait_widget("//UIACollectionCell[@name='导航']")
            #click into Navigation
            self.testStep.tap_widget("//UIACollectionCell[@name='导航']")

            self.testStep.tap_permision_widget("accept")
            # wait for map window
            # gaode version is //UIAApplication[1]/UIAWindow[1]/UIAMapView[1]
            # baidu version is //UIAApplication[1]/UIAWindow[1]
            
            #self.testStep.wait_window("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            self.testStep.wait_widget("//UIASearchBar[@label='输入地址进行搜索']")


            # search destination by input name in the search text box
            self.testStep.input_textbox_uft8("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]", u"广州", "guangzhou")
            '''''
            # for V0.5.0 gaode version can not locate search bar element, script below tap map widget 21 pixel below top of widget
            # it is a hard code here due to appium limitation
            #get the scream size
            self.testStep.touchAction = TouchAction(self.testStep.driver)
            aMap = self.testStep.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            aMapSize = aMap.size
            print aMapSize
            #touch the searchBox 
            self.testStep.touchAction.press(aMap, aMapSize['width']/2 , 21).release().perform()
            print "y=21"
            #self.touchAction.press(aMap, 10, aMapSize['height']/2 ).release().perform()
            #print "x=5"
            #self.touchAction.press(aMap, 10, 21).release().perform()
            #print "x=5, y=21"         
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()
            self.testStep.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]").send_keys(u"广州")
            '''
            
            self.testStep.tap_widget("//UIAButton[@label='搜索']")
            
            #wait for the element loading
            self.testStep.wait_widget("//UIACollectionView/UIACollectionCell/UIAStaticText[contains(@label, '广州')]")
        
            #push into koodar
            self.testStep.tap_widget("//UIAButton[@label='推送到 Koodar']")
            self.testStep.driver.switch_to_alert().accept()

            
            #check the way
            self.testStep.tap_widget("//UIAButton[@label='查看路线']")
        
            self.testStep.wait_widget("//UIAStaticText[@label='需要']")
            self.testStep.wait_widget("//UIAStaticText[@label='一共']")
        
            self.testStep.tap_widget("//UIAButton[@label='btn send']")
            self.testStep.driver.switch_to_alert().accept()

            #back
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIANavigationBar[1]/UIAButton[1]").click()

            self.testStep.tap_button("//UIAButton[@label='btn cancel']")
            sleep(self.think_time)
       
        finally:
            print "Test finsh"
            #self.driver.quit()
            #if not success:
            #raise Exception("Test failed.")
            
        
        
    #@unittest.skip("demostrating skipping")
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


    #@unittest.skip("demostrating skipping")
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



    #@unittest.skip("demostrating skipping")
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


