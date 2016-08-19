# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait  

from common_test_step import CommonTestStep

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')      

class KoodarAndroidAssistantNavigationTests(unittest.TestCase):
    __think_time = 2
    
    @classmethod
    def setUpClass(KoodarAssistantAndroidTests):
        logging.info("setUpClass") 
    
    @classmethod   
    def tearDownClass(KoodarAssistantAndroidTests):
        logging.info("tearDownClass") 
        
    def setUp(self):
        logging.info("setUp") 
        self.testStep = CommonTestStep()
        
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        desired_caps['deviceName'] = 'Android HUD'
        #desired_caps['app'] = PATH(
        #    'apps/Assistant_v0.4.1_production.apk'
        #)
        desired_caps['appPackage'] = 'com.gexne.car.assistant'
        desired_caps['appActivity'] = 'systems.xos.car.android.product.companion.startup.SplashActivity'
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'

        self.testStep.init_appium(desired_caps, True)
        

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        case_function_name = self.id().split(".")[-1]
        self.testStep.deinit_appium(case_function_name)

    def _common_login(self):
        # launch assistant app if it installed
        self.testStep.launch_app_if_installed('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        # wait for login activity
        if self.testStep.wait_window('systems.xos.car.android.product.companion.startup.login.LoginActivity'):
            # input account and password
            self.testStep.input_textbox('com.gexne.car.assistant:id/login_phone_number', u'13824470628')
            self.testStep.input_secure_textbox('com.gexne.car.assistant:id/login_password', u'ygvuhbijn')
            self.testStep.press_button('com.gexne.car.assistant:id/login_next')
        else:
            logging.info("*****wait for login activity time out*****") 
    
    def _common_enter_navigation(self):
        self._common_login()
        if self.testStep.wait_window('systems.xos.car.android.product.companion.MainActivity'):
            # enter navigation 
            self.testStep.press_widget("//android.widget.TextView[@text='导航']")
       
        else:
            logging.info("*****wait for main activity time out*****")
            
        
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity')
        
        
        self.testStep.press_button_if_exist("//android.widget.Button[@text='允许']")
            
        self.testStep.press_button_if_exist("com.huawei.systemmanager:id/btn_allow")
            
        
    #@unittest.skip("demostrating skipping")
    def test_navigation(self):
        self.test_navigation_search_and_push_destination()
        self.test_navigation_add_to_favorate()
        self.test_navigation_choose_destination_on_map()
        self.test_navigation_smart_hints()
        self.test_navigation_search_history()
        self.test_navigation_not_exist()
        
    def test_navigation_search_and_push_destination(self):
        self._common_enter_navigation()

        # search destination by input name in the search text box
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.press_button("com.gexne.car.assistant:id/search_btn")
        #self.driver.hide_keyboard()

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.press_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.press_button("com.gexne.car.assistant:id/back_btn")
    
    def test_navigation_add_to_favorate(self):
        self._common_enter_navigation()
        # search destination by input name in the search text box
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.press_button("com.gexne.car.assistant:id/search_btn")
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.press_button_sibling_widget("com.gexne.car.assistant:id/star_btn", "//android.widget.TextView[@text='1. 广州市']")
        
    #@unittest.skip("demostrating skipping")    
    def test_navigation_not_exist(self):
        # search destination does not exist
        # AV-4202	Android X助手导航-在搜索框搜索目的地不存在
        self._common_enter_navigation()
        
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt",u"请问而退藕拍")
        self.testStep.press_button("com.gexne.car.assistant:id/search_btn")
        
        # TODO toast detection should be done
        # Appium has no API to capture toast so that an alternative way is taking a screenshot and find content by ocr tool
        
    #@unittest.skip("demostrating skipping")
    def test_navigation_smart_hints(self):    
        # smart.
        # AV-4547	Android 手机助手-导航，智能提词
        self._common_enter_navigation()
        
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt",u"河")
        self.testStep.press_widget_tap("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]")
        
        
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '河')]")
        self.testStep.press_button("com.gexne.car.assistant:id/star_btn")
        self.testStep.press_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.press_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.press_button("com.gexne.car.assistant:id/back_btn")
    #@unittest.skip("demostrating skipping")    
    def test_navigation_search_history(self):
        # history record
        # AV-4545	Android 手机助手-导航，搜索历史
        self._common_enter_navigation()
        
        self.testStep.press_button("com.gexne.car.assistant:id/clear_btn")
        self.testStep.press_widget_tap("com.gexne.car.assistant:id/parent_view")
        self.testStep.press_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.press_button("com.gexne.car.assistant:id/back_btn")
        sleep(self.__think_time)
        self.testStep.press_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.press_button("com.gexne.car.assistant:id/star_btn")
    #@unittest.skip("demostrating skipping")    
    def test_navigation_choose_destination_on_map(self):
        # select a location on the map
        # AV-4200	Android X助手导航-在地图上选择地点
        self._common_enter_navigation()
        
        #self.testStep.press_widget_tap("com.gexne.car.assistant:id/parent_view")
        self.testStep.press_widget_tap("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]")

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '推送到')]")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.press_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.press_button("com.gexne.car.assistant:id/back_btn")
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantNavigationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
