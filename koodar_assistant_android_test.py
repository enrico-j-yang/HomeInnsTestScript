import os
import sys
from time import sleep

import unittest

from appium import webdriver

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class KoodarAssistantAndroidTests(unittest.TestCase):
    think_time = 2
    
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
        sleep(self.think_time)
        self.driver.quit()

    def test_login(self):
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
            phone_number.send_keys('13824470628')
            password = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_password')
            self.assertTrue(password)
            password.send_keys(' ') # because send_keys miss first character, so here come one blank as to avoid this problem
            password.send_keys('ygvuhbijn')
            sleep(self.think_time)
            login = self.driver.find_element_by_id('com.gexne.car.assistant:id/login_next')
            self.assertTrue(login)
            login.click()
            sleep(self.think_time)
        else:
            print "*****wait for login activity time out"
            
        # wait for main activity
        if self.driver.wait_activity('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3, 1):
            self.driver.find_elements_by_class_name('android.widget.LinearLayout')[1].click()
            sleep(self.think_time)
            self.driver.back()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
