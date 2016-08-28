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

class KoodarIOSAssistantNavigationAtomTests(unittest.TestCase):
    def __init__(self, testStep, platformName):
        self.testStep = testStep
        self.platformName = platformName
        
    def __common_launch_app(self):
        if self.platformName == 'Android':
            # launch assistant app if it installed
            self.testStep.launch_app_if_installed('com.gexne.car.assistant', 'systems.xos.car.android.product.companion.startup.SplashActivity')
        
            self.testStep.wait_and_check_window_show_up('systems.xos.car.android.product.companion.startup.SplashActivity')
    
    def __common_login(self):
        # wait for login window
        if self.platformName == 'Android':
            if self.testStep.wait_window('systems.xos.car.android.product.companion.startup.login.LoginActivity', 3):
                # input account and password
                self.testStep.input_textbox('com.gexne.car.assistant:id/login_phone_number', u'13824470628')
                self.testStep.input_secure_textbox('com.gexne.car.assistant:id/login_password', u'ygvuhbijn')
                self.testStep.tap_button('com.gexne.car.assistant:id/login_next')
            else:
                logging.info("*****wait for login window time out*****") 
        elif self.platformName == 'iOS':
            try:
                self.testStep.wait_window("//UIAButton[@name='登录']", 3)
                # input account and password
                self.testStep.input_textbox("//UIATextField", u'13824470628')
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIATextField[1]").send_keys("13726260108")
                self.testStep.input_secure_textbox("//UIASecureTextField[@value='密码']", u'ygvuhbijn')
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIASecureTextField[1]").send_keys("12345678")
                self.testStep.tap_button("//UIAButton[@name='登录']")
                #self.driver.find_element_by_xpath("//UIAApplication[1]/UIAWindow[1]/UIAButton[1]").click()
            except:
                logging.info("*****wait for login window time out*****") 
    
    def common_enter_navigation(self, launch_app=True):
        if launch_app == True:
            self.__common_launch_app()

        self.__common_login()

        if self.platformName == 'Android':
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

        elif self.platformName == 'iOS': 
            self.testStep.wait_widget("//UIACollectionCell[@name='导航']")
            #click into Navigation
            self.testStep.tap_widget("//UIACollectionCell[@name='导航']")
            
        self.testStep.tap_permision_widget("accept")

        if self.platformName == 'Android':
            self.testStep.wait_widget("com.gexne.car.assistant:id/compass_map_btn")
            self.testStep.wait_widget("com.gexne.car.assistant:id/road_map_btn")
            self.testStep.wait_widget("com.gexne.car.assistant:id/locate_map_btn")
            self.testStep.wait_widget("com.gexne.car.assistant:id/zoom_in_map_btn")
            self.testStep.wait_widget("com.gexne.car.assistant:id/zoom_out_map_btn")
        elif self.platformName == 'iOS': 
            self.testStep.wait_widget("//UIAStaticText[@label='导航']")
        
        
    def navigation_search_and_push_destination(self):
        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
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
            
       
        finally:
            self = self
            
    def navigation_add_to_favorate(self):

        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
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

            self.testStep.tap_widget("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[1]")
            self.testStep.driver.switch_to_alert().accept()
            #self.testStep.tap_widget_if_image_alike("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[1]", RESOURCE_PATH+"not_fav.png", RESOURCE_PATH+"fav.png")
            
            #click into collect
            self.testStep.tap_widget("//UIANavigationBar/UIAButton[@label='icn collection']")

            #wait for the element loading
            self.testStep.wait_widget("//UIATableView/UIATableCell/UIAStaticText[contains(@label, '广州')]")

            self.testStep.tap_widget("//UIATableView/UIATableCell/UIAStaticText[contains(@label, '广州')]")
            
            # back to main window
            #self.testStep.tap_button("//UIANavigationBar/UIAButton[@label='Back']")

        finally:
            self = self
        
    
    def navigation_delete_from_favorate_list(self):

        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
            # gaode version is //UIAApplication[1]/UIAWindow[1]/UIAMapView[1]
            # baidu version is //UIAApplication[1]/UIAWindow[1]
            
            #self.testStep.wait_window("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            self.testStep.wait_widget("//UIASearchBar[@label='输入地址进行搜索']")
            
            #click into collect
            self.testStep.tap_widget("//UIANavigationBar/UIAButton[@label='icn collection']")

            #wait for the element loading
            self.testStep.wait_widget("//UIATableView/UIATableCell/UIAStaticText[contains(@label, '广州')]")
            #delete item from favorate list
            #self.testStep.swipe_widget_by_direction("//UIATableView/UIATableCell[contains(@name, '广州')]", "left")
            self.testStep.flick_widget_by_direction("//UIATableView/UIATableCell[contains(@name, '广州')]", "left")
            
            sleep(10)
            #back to navigation window
            self.testStep.tap_button("//UIANavigationBar/UIAButton[@name='Back']")


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

            #self.testStep.tap_widget_if_image_alike("//UIAApplication[1]/UIAWindow[1]/UIACollectionView[1]/UIACollectionCell[1]/UIAButton[1]", RESOURCE_PATH+"fav.png")
            

            
            # back to main window
            #self.testStep.tap_button("//UIANavigationBar/UIAButton[@label='Back']")

        finally:
            self = self
        
    
    def navigation_choose_destination_on_map(self):
        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
            # gaode version is //UIAApplication[1]/UIAWindow[1]/UIAMapView[1]
            # baidu version is //UIAApplication[1]/UIAWindow[1]
            
            #self.testStep.wait_window("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            self.testStep.wait_widget("//UIASearchBar[@label='输入地址进行搜索']")

            # select a location on the map
            self.testStep.long_tap_widget("//UIAApplication[1]/UIAWindow[1]")

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
            

        finally:
            self = self
 
    def navigation_search_history(self):
        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
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

            self.testStep.tap_button("//UIANavigationBar/UIAButton[@label='Back']")

            self.common_enter_navigation(False) # enter navigation window without reset app
        
            self.testStep.tap_widget("//UIASearchBar[@label='输入地址进行搜索']")
            
            self.testStep.precise_tap_widget("//UIAApplication[1]/UIAWindow[1]", "middle", 90)
        
            #wait for the element loading
            self.testStep.wait_widget("//UIACollectionView/UIACollectionCell/UIAStaticText[contains(@label, '广州')]")
    
            #push into koodar
            self.testStep.tap_widget("//UIAButton[@label='推送到 Koodar']")
            self.testStep.driver.switch_to_alert().accept()
            
        finally:
            self = self
        
        
    def navigation_not_exist(self):
        try: 
            # When I see the map window with searchbar '输入地址进行搜索'
            
            # gaode version is //UIAApplication[1]/UIAWindow[1]/UIAMapView[1]
            # baidu version is //UIAApplication[1]/UIAWindow[1]
            
            #self.testStep.wait_window("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            self.testStep.wait_widget("//UIASearchBar[@label='输入地址进行搜索']")

            # search destination by input name in the search text box
            self.testStep.input_textbox_uft8("//UIAApplication[1]/UIAWindow[1]/UIASearchBar[1]/UIASearchBar[1]", u"请问", "qingwen")
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

            self.testStep.wait_widget("//UIAAlert/UIAScrollView/UIAStaticText[@name='抱歉，没有找到结果']")
            self.testStep.driver.switch_to_alert().accept()
            self.testStep.tap_button("//UIANavigationBar/UIAButton[@label='Back']")
            
        finally:
            self = self    
        
        
    '''''
    # WebDriverException: Message: Unknown command, all the mobile commands except scroll have been removed.
    def navigation_pinch(self):
        try:
            # When I see the map window with searchbar '输入地址进行搜索'
            
            # gaode version is //UIAApplication[1]/UIAWindow[1]/UIAMapView[1]
            # baidu version is //UIAApplication[1]/UIAWindow[1]
            
            #self.testStep.wait_window("//UIAApplication[1]/UIAWindow[1]/UIAMapView[1]")
            self.testStep.wait_widget("//UIASearchBar[@label='输入地址进行搜索']")

            #enlarge the map(wrong)
            self.testStep.pinch_widget("//UIAApplication[1]/UIAWindow[1]", 200, 50)
            
        finally:
            self = self
    '''            
    # atom test function list here for random combination test 
    # make sure all all atom test tunction listed below
    atom_test_list = {'navigation_search_and_push_destination':navigation_search_and_push_destination,
        'navigation_add_to_favorate':navigation_add_to_favorate,
        'navigation_delete_from_favorate_list':navigation_delete_from_favorate_list,
        'navigation_choose_destination_on_map':navigation_choose_destination_on_map,
#       'navigation_smart_hints':navigation_smart_hints,
        'navigation_search_history':navigation_search_history,
#        'navigation_pinch':navigation_pinch,
        'navigation_not_exist':navigation_not_exist}  
                     
class KoodarIOSAssistantNavigationTests(unittest.TestCase):
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
        #desired_caps['bundleId'] = 'com.gexne.car.assistant.ih'
        desired_caps['language'] = 'zh-Hans' # for iphone simulator, input method should be force decided
        desired_caps['locale'] = 'zh_CN' # for iphone simulator, locale should be force decided
        #desired_caps['udid'] = '9c3bfe9438fcb01fde3cff021b8cfdff0cf2bc09' # for real ios devices

        self.testStep.init_appium(desired_caps, True)
        self.atomTest = KoodarIOSAssistantNavigationAtomTests(self.testStep, desired_caps['platformName'])
        self.atomTest.common_enter_navigation()

    def tearDown(self):
        logging.info("tearDown") 
        # end the session
        case_function_name = self.id().split(".")[-1]
        self.testStep.deinit_appium(case_function_name)
    
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
    def test_navigation_choose_destination_on_map(self):
        # select a location on the map
        # AV-4200	Android X助手导航-在地图上选择地点
        self.atomTest.navigation_choose_destination_on_map()

    #@unittest.skip("demostrating skipping")    
    def test_navigation_not_exist(self):
        # search destination does not exist
        # AV-4202	Android X助手导航-在搜索框搜索目的地不存在
        self.atomTest.navigation_not_exist()
        
    #@unittest.skip("demostrating skipping")    
    def test_navigation_search_history(self):
        # history record
        # AV-4545	Android 手机助手-导航，搜索历史
        self.atomTest.navigation_search_history()
        
    '''''
    # WebDriverException: Message: Unknown command, all the mobile commands except scroll have been removed.
        
    #@unittest.skip("demostrating skipping")    
    def test_navigation_pinch(self):
        # history record
        # AV-4545	Android 手机助手-导航，搜索历史
        self.atomTest.navigation_pinch()

    '''




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KoodarAssistantIOSTests)
    unittest.TextTestRunner(verbosity=2).run(suite)


