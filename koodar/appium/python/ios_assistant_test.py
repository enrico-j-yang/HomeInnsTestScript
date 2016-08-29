# -*- coding: utf-8 -*-cd

"""
Simple iOS tests, showing accessing elements and getting/setting text from them.
"""
import unittest
import os
import logging
from appium import webdriver
#from assistant.ios.login import KoodarAndroidAssistantLoginTests
from assistant.ios.navigation import KoodarIOSAssistantNavigationTests
from assistant.ios.button import KoodarIOSAssistantButtonTests
from assistant.ios.help import KoodarIOSAssistantHelpTests
from assistant.ios.account import KoodarIOSAssistantAccountTests

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
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarIOSAssistantNavigationTests)
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarIOSAssistantButtonTests)
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarIOSAssistantHelpTests)
    #suite = unittest.TestLoader().loadTestsFromTestCase(KoodarIOSAssistantMyAccountTests)
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarIOSAssistantAccountTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
