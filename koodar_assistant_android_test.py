import os
from time import sleep

import unittest

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class KoodarAssistantAndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH(
            '/Users/enrico/Documents/Work/Tools/Appium/sample-code/sample-code/apps/ApiDemos/bin/ApiDemos-debug.apk'
        )
        #desired_caps['appPackage'] = 'com.android.calculator2'
        #desired_caps['appActivity'] = '.Calculator'
        desired_caps['autoLaunch'] = 'false'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        # end the session
        self.driver.quit()

    def test_login(self):
        #self.wait = webdriver.wait.new()
        
        el = self.driver.is_app_installed('com.gexne.car.assistant')
        self.assertTrue(el)
        el = self.driver.start_activity('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        self.assertTrue(el)
        self.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3, 1)
        self.assertTrue(el)
        phone_number = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_phone_number')
        self.assertTrue(phone_number)
        phone_number.send_keys('13824470628')
        password = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_password')
        self.assertTrue(password)
        password.send_keys('ygvuhbijn')
        sleep(2)
        login = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_next')
        self.assertTrue(login)
        print login
        login.click
        sleep(2)
        print "succeed"  


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
