"""
Simple iOS tests, showing accessing elements and getting/setting text from them.
"""
import unittest
import os
from random import randint
from appium import webdriver
from time import sleep

class SimpleIOSTests(unittest.TestCase):

    def setUp(self):
        # set up appium
        app = os.path.abspath('apps/Radish.app')
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '9.3',
                'deviceName': 'iPhone 6s Plus',
                #'udid': '4be7ab31bff7d81b6b8ad849ca47e42fc857c7e9'
            })

    def tearDown(self):
        self.driver.quit()

    def testLogin(self):
        # launch assistant app if it installed
        el = self.driver.is_app_installed('com.gexne.car.assistant')
        self.assertTrue(el)
        el = self.driver.launch_app()
        self.assertTrue(el)
        # wait for login activity
    	self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13824470628")
    	self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("ygvuhbijn")
    	self.driver.find_element_by_name("登录").click()
        # input account and password
        
        # wait for main activity
        
        sleep(100)
        print "done"

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
