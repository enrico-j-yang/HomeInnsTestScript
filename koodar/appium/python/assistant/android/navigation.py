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

class KoodarAundroidAssistantNavigationAtomTests(unittest.TestCase):
    def __init__(self, testStep):
        self.testStep = testStep
        
    def __common_launch_app(self):
        # launch assistant app if it installed
        self.testStep.launch_app_if_installed('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.startup.SplashActivity')
    
    def __common_login(self):
        # wait for login activity
        if self.testStep.wait_window('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3):
            # input account and password
            self.testStep.input_textbox('com.gexne.car.assistant:id/login_phone_number', u'13824470628')
            self.testStep.input_secure_textbox('com.gexne.car.assistant:id/login_password', u'ygvuhbijn')
            self.testStep.tap_button('com.gexne.car.assistant:id/login_next')
        else:
            logging.info("*****wait for login activity time out*****") 
    
    def common_enter_navigation(self, launch_app=True):
        if launch_app == True:
            self.__common_launch_app()
        
        self.__common_login()
         
        if (self.testStep.current_window()).index("systems.xos.car"):
            while (self.testStep.current_window() != 'systems.xos.car.android.product.companion.MainActivity'):
                self.testStep.driver.keyevent(4)
                sleep(1)
            
        if self.testStep.wait_window('systems.xos.car.android.product.companion.MainActivity', 3):
            self.testStep.swipe_widget_by_direction("com.gexne.car.assistant:id/recyclerView", "up")
            #size = self.testStep.driver.get_window_size()
            #self.testStep.driver.swipe(size['width']/2, size['height'] - 50, size['width']/2, size['height']/2, 500)
            # enter navigation 
            self.testStep.tap_widget("//android.widget.TextView[@text='导航']")
       
        else:
            logging.info("*****wait for main activity time out*****")
            
        
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity')
        
        # in order to close permision widget, here is script to ensure script can deal with MIUI and Huawei system permision widget
        self.testStep.tap_button_if_exist("//android.widget.Button[@text='允许']")
            
        self.testStep.tap_button_if_exist("com.huawei.systemmanager:id/btn_allow")
        
        self.testStep.wait_widget("com.gexne.car.assistant:id/compass_map_btn")
        self.testStep.wait_widget("com.gexne.car.assistant:id/road_map_btn")
        self.testStep.wait_widget("com.gexne.car.assistant:id/locate_map_btn")
        self.testStep.wait_widget("com.gexne.car.assistant:id/zoom_in_map_btn")
        self.testStep.wait_widget("com.gexne.car.assistant:id/zoom_out_map_btn")
        
        
    def navigation_search_and_push_destination(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity')

        # search destination by input name in the search text box
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.tap_button("com.gexne.car.assistant:id/search_btn")
        #self.driver.hide_keyboard()

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.tap_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.tap_button("com.gexne.car.assistant:id/back_btn")
        
    
    def navigation_add_to_favorate(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity')

        # search destination by input name in the search text box
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.tap_button("com.gexne.car.assistant:id/search_btn")
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.tap_widget_if_image_alike("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.ImageButton[1]", RESOURCE_PATH+"not_fav.png", RESOURCE_PATH+"fav.png")
        self.testStep.tap_widget("com.gexne.car.assistant:id/favorite_btn")
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.tap_button("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.view.View[1]/android.widget.ImageButton[1]")
    
    def navigation_delete_from_favorate_list(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity')

        # search destination by input name in the search text box
        self.testStep.tap_widget("com.gexne.car.assistant:id/favorite_btn")
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.long_tap_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.precise_tap_widget("//android.widget.TextView[contains(@text, '广州')]", "middle", 50, 1000, True)
        self.testStep.tap_button("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.view.View[1]/android.widget.ImageButton[1]")
    
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.tap_button("com.gexne.car.assistant:id/search_btn")
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.check_widget_if_image_alike("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.RelativeLayout[1]/android.support.v7.widget.RecyclerView[1]/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.ImageButton[1]", RESOURCE_PATH+"fav.png")
    
    def navigation_not_exist(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity') 
        
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt",u"请问而退藕拍")
        self.testStep.tap_button("com.gexne.car.assistant:id/search_btn")
        
        # TODO toast detection should be done
        # Appium has no API to capture toast so that an alternative way is taking a screenshot and find content by ocr tool 

    def navigation_smart_hints(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity') 
        
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt",u"河")
            
        self.testStep.swipe_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]\
        /android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]", "middle", 530, "middle", 177)#230, 580, 370, 227
        self.testStep.precise_tap_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]\
        /android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]", "middle", 540)
        
        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '河')]")
        
        self.testStep.tap_button("com.gexne.car.assistant:id/star_btn")
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.tap_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.tap_button("com.gexne.car.assistant:id/back_btn")
    
 
    def navigation_search_history(self):
        # wait for map activity
        # gaode version is systems.xos.car.android.product.companion.navigation.MapActivity
        # baidu version is systems.xos.car.android.product.companion.map.MainMapActivity
        self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.map.MainMapActivity') 

        # search destination by input name in the search text box
        self.testStep.input_textbox_uft8("com.gexne.car.assistant:id/search_edt", u"广州")
        self.testStep.tap_button("com.gexne.car.assistant:id/search_btn")
        #self.driver.hide_keyboard()

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '广州')]")
        self.testStep.tap_button("com.gexne.car.assistant:id/back_btn")

        self.common_enter_navigation(False) # enter navigation window without reset app
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/search_edt")
        self.testStep.precise_tap_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]\
        /android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]", "middle", 180)

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '推送到')]")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.tap_button("com.gexne.car.assistant:id/back_btn")
        sleep(self.__think_time)
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_layout")
        self.testStep.tap_button("com.gexne.car.assistant:id/star_btn")
    

    def navigation_choose_destination_on_map(self):
        
        try:
            self.testStep.long_tap_widget("com.gexne.car.assistant:id/parent_view")
        except:
            self.testStep.long_tap_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]")
             

        self.testStep.wait_widget("//android.widget.TextView[contains(@text, '推送到')]")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/get_route_layout")
        
        self.testStep.wait_widget("//android.widget.TextView[@text='耗时']")
        self.testStep.wait_widget("//android.widget.TextView[@text='距离']")
        
        self.testStep.tap_widget("com.gexne.car.assistant:id/push_destination")
        self.testStep.tap_button("com.gexne.car.assistant:id/back_btn")
           
    # atom test function list here for random combination test 
    # make sure all all atom test tunction listed below
    atom_test_list = {'navigation_search_and_push_destination':navigation_search_and_push_destination,
       'navigation_add_to_favorate':navigation_add_to_favorate,
       'navigation_delete_from_favorate_list':navigation_delete_from_favorate_list,
       'navigation_choose_destination_on_map':navigation_choose_destination_on_map,
       'navigation_smart_hints':navigation_smart_hints,
       'navigation_search_history':navigation_search_history,
       'navigation_not_exist':navigation_not_exist}    
    
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
        #    '../../../apps/Assistant_v0.5.0_production.apk'
        #)
        desired_caps['appPackage'] = 'com.gexne.car.assistant'
        desired_caps['appActivity'] = 'systems.xos.car.android.product.companion.startup.SplashActivity'
        desired_caps['autoLaunch'] = 'false'
        desired_caps['unicodeKeyboard'] = 'True'
        desired_caps['resetKeyboard'] = 'True'

        self.testStep.init_appium(desired_caps)
        self.atomTest = KoodarAundroidAssistantNavigationAtomTests(self.testStep)
        self.atomTest.common_enter_navigation()

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        case_function_name = self.id().split(".")[-1]
        self.testStep.deinit_appium(case_function_name)


    @unittest.skip("demostrating skipping")
    def test_random_navigation(self):
        testMethodPrefix = "test_navigation"
        
        # TODO run atom test randomly
                
    #@unittest.skip("demostrating skipping")
    def test_conbination_navigation(self):
        testMethodPrefix = "navigation_"
        
        # run all atom test once
        """Return a sorted sequence of method names found within testCaseClass
        """
        def isTestMethod(attrname, testCaseClass=self.atomTest,
                         prefix=testMethodPrefix):
            return attrname.startswith(prefix) and \
                hasattr(getattr(self.atomTest, attrname), '__call__')
        testFnNames = filter(isTestMethod, dir(self.atomTest))
        logging.debug(testFnNames)
        for i in testFnNames:
            try:
                self.atomTest.atom_test_list[i](self.atomTest)
            except KeyError:
                raise ValueError("invalid input")
            
        
    #@unittest.skip("demostrating skipping")
    def test_navigation_search_and_push_destination(self):
        self.atomTest.navigation_search_and_push_destination()
        
    #@unittest.skip("demostrating skipping")
    def test_navigation_add_to_favorate(self):
        self.atomTest.navigation_add_to_favorate()
        
    #@unittest.skip("demostrating skipping")
    def test_navigation_delete_from_favorate_list(self):
        self.atomTest.navigation_delete_from_favorate_list()
        
    #@unittest.skip("demostrating skipping")    
    def test_navigation_not_exist(self):
        # search destination does not exist
        # AV-4202	Android X助手导航-在搜索框搜索目的地不存在
        self.atomTest.navigation_not_exist()
        
    #@unittest.skip("demostrating skipping")
    def test_navigation_smart_hints(self):    
        # smart.
        # AV-4547	Android 手机助手-导航，智能提词
        self.atomTest.navigation_smart_hints()
    
    #@unittest.skip("demostrating skipping")    
    def test_navigation_search_history(self):
        # history record
        # AV-4545	Android 手机助手-导航，搜索历史
        self.atomTest.navigation_search_history()
        
    #@unittest.skip("demostrating skipping")    
    def test_navigation_choose_destination_on_map(self):
        # select a location on the map
        # AV-4200	Android X助手导航-在地图上选择地点
        self.atomTest.navigation_choose_destination_on_map()
        

      

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAndroidAssistantNavigationTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
