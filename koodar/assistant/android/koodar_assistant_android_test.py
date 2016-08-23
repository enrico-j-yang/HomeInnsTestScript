# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from koodar_android_assistant_login_test import KoodarAndroidAssistantLoginTests
from koodar_android_assistant_navigation_test import KoodarAndroidAssistantNavigationTests
from koodar_android_assistant_my_account_test import KoodarAndroidAssistantMyAccountTests

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')      
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantLoginTests)
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantNavigationTests)
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantMyAccountTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
