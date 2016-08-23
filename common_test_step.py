# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging
import unittest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support.ui import WebDriverWait  

from PIL import Image

from mywebdriver import MyWebDriver

import logging

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='appium_python_client.log',
                filemode='w')
#################################################################################################
#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
#################################################################################################


def test_step_info(func):
    def _func(*args, **kw):
        objPtr = args[0]
        objPtr.step = objPtr.step + 1
        logging.info("test step %d %s", objPtr.step, func.__name__)
        result=func(*args, **kw)

        if  objPtr.step_screen_shot == True:
            # take screen shot after every step function
            # it will slow down the test and use much more storage space
            case_function_name = func.__name__
            screenshotname = "./step " + str(objPtr.step) + " "+ case_function_name + ".png"
            objPtr.driver.get_screenshot_as_file(screenshotname)
                
        return result
    return _func


class CommonTestStep(unittest.TestCase):
    def __init__(self):
        self.step = 0
        
    def __pil_image_similarity(self, filepath1, filepath2):
        import math
        import operator

        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

    #    image1 = get_thumbnail(img1)
    #    image2 = get_thumbnail(img2)

        h1 = image1.histogram()
        h2 = image2.histogram()

        rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
        return rms
        
    def __add_resolution_to_file_name(self, filename, resolution):
        ref_image_true_name = filename[0:filename.rfind(".")]
        ref_image_ext_name = filename[filename.rfind(".")+1:len(filename)]
        logging.debug("ref_image_true_name:%s", ref_image_true_name) 
        
        ref_image_height = resolution['height']
        logging.debug("ref_image_height:%s", ref_image_height) 
        
        ref_image_width = resolution['width']
        logging.debug("ref_image_width:%s", ref_image_width) 
        
        added_file_name = ref_image_true_name+'_'+str(ref_image_width)+'_'+str(ref_image_height)+'.'+ref_image_ext_name
        logging.debug("added_file_name:%s", added_file_name)
         
        return added_file_name    
        
    def init_appium(self, desired_caps, step_screen_shot=False):
        self.step_screen_shot = step_screen_shot
        self.driver = MyWebDriver('http://localhost:4723/wd/hub', desired_caps)
        self.touchAction = TouchAction(self.driver)

        self.wait = WebDriverWait(self.driver, 10, 1)
        
        self.ime = self.driver.active_ime_engine
        logging.debug("self.ime is %s", self.ime)
        if self.ime == u"io.appium.android.ime/.UnicodeIME":
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            imes = self.driver.available_ime_engines
            for i in [1, len(imes)]:
                if imes[i - 1] != u"io.appium.android.ime/.UnicodeIME":
                    self.driver.activate_ime_engine(imes[i - 1])
                    self.ime = imes[i - 1]
                    logging.debug("self.ime is %s", self.ime)
                       
    def deinit_appium(self, screen_shot_file):
        screenshotname = "./" + screen_shot_file + ".png"
        sleep(1)
        self.driver.get_screenshot_as_file(screenshotname)
        self.driver.quit()
        
    @test_step_info
    def wait_window(self, window, timeout=10, interval=1):
        return self.driver.wait_activity(window, timeout, interval)

    # function wait for act activity and check it show up or not within duration specified by parameter timeout
    # checking interval is specified by parameter interval 
    @test_step_info
    def wait_and_check_window_show_up(self, activity, timeout=10, interval=1):
        if self.driver.wait_activity(activity, timeout, interval):
           logging.debug("*****"+activity+" OK*****") 
        else:
           logging.error("*****wait for "+activity+" time out*****") 
   
        self.assertTrue(activity == self.driver.current_activity)
        
    @test_step_info
    def wait_widget(self, string, timeout=10, interval=1): 
        wait = WebDriverWait(self.driver, timeout, interval)
        wait.until(lambda dr: dr.find_element_by_string(string).is_displayed())

    @test_step_info
    def current_window(self):
        return self.driver.current_activity
        
    @test_step_info
    def launch_app_if_installed(self, package, activity):
        el = self.driver.is_app_installed(package)
        self.assertTrue(el)
        el = self.driver.start_activity(package, activity)
        self.assertTrue(el)
    
    @test_step_info    
    def input_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
        # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)

        self.touchAction.press(textbox).release().perform()
        textbox.send_keys(text)
    
    @test_step_info    
    def input_secure_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        
        # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
        # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)
        
        self.touchAction.press(textbox).release().perform() # because send_keys miss first character, so here come one blank as to avoid this problem
        textbox.send_keys(text)
    
    @test_step_info
    def input_textbox_uft8(self, string, text):
        textbox = self.driver.find_element_by_string(string)
        logging.debug("ime is %s", self.driver.active_ime_engine)
        self.driver.activate_ime_engine(u"io.appium.android.ime/.UnicodeIME")
        logging.debug("ime is %s", self.driver.active_ime_engine)
        textbox.send_keys(text)
        self.driver.activate_ime_engine(self.ime)
        logging.debug("ime is %s", self.driver.active_ime_engine)
    
    @test_step_info    
    def tap_button(self, string):
        button = self.driver.find_element_by_string(string)
        self.touchAction.press(button).release().perform()
    
    @test_step_info    
    def tap_widget(self, string):
        widget = self.driver.find_element_by_string(string)
        self.touchAction.press(widget).release().perform()
        
    @test_step_info
    def tap_button_sibling_widget(self, button_string, widget_string):
        widget = self.driver.find_element_by_string(widget_string)
        
        if (self.driver.check_string_type(button_string) == "id"):
            logging.debug("string is id")
            button = widget.parent.find_element_by_id(button_string)
        elif (self.driver.check_string_type(button_string) == "xpath"):
            logging.debug("string is xpath")
            button = widget.parent.find_element_by_xpath(button_string)
        else:
            logging.error("string is unknown")
            raise UnknownStringException
            
        self.assertTrue(button)
        self.touchAction.press(button).release().perform()

    @test_step_info
    def long_tap_widget(self, string, x=0, y=0, duration=1000):
        self.touchAction = TouchAction(self.driver)
        widget = self.driver.find_element_by_string(string)
        size = widget.size
        if x=="middle":
            x = size["width"] / 2
        
        if y=="middle":
            y = size["height"]/ 2
        
        if x==0 and y==0:
            size = widget.size
            x = size["width"] / 2
            y = size["height"]/ 2
        
        self.touchAction.long_press(widget, x, y, duration).release().perform()
        
    @test_step_info
    def precise(self, string, x=0, y=0, duration=1000):
        widget = self.driver.find_element_by_string(string)
        lx = widget.location.get('x')
        ly = widget.location.get('y')

        logging.debug("location x:%s location y:%s", lx, ly)
        size = widget.size
        logging.debug("size %s %s", size["width"], size["height"])
        if x=="middle":
            x = size["width"] / 2
        
        if y=="middle":
            y = size["height"]/ 2
        
        if x==0 and y==0:
            x = size["width"] / 2
            y = size["height"]/ 2
        
        
        window_size = self.driver.get_window_size()
        logging.debug("window size %s %s", window_size["width"], window_size["height"])
        
        if (x>size['width'] or x<0
        or y>size['height'] or y<0
        or x+lx>window_size['width'] 
        or y+ly>window_size['height']):
            raise OutOfBoundException
            
        self.touchAction.press(widget, x+lx, y+ly).release().perform()
    
    @test_step_info
    def tap_button_if_exist(self, string):
        try:
            button = self.driver.find_element_by_string(string)        
            self.touchAction.press(button).release().perform()
            logging.debug("%s button exists", string)
        except:
            logging.debug("%s button not exist", string)
        
    @test_step_info
    def tap_widget_if_image_alike(self, string, ref_image_name, after_image_name=None):
        star_btn = self.driver.find_element_by_string(string)
        elementImageName, elementImageSize = self.__capture_element(star_btn)
        logging.debug("elementImageSize:%s", elementImageSize) 
        added_file_name = self.__add_resolution_to_file_name(ref_image_name, elementImageSize)
        
        if self.__pil_image_similarity(added_file_name, elementImageName) == 0:
            self.touchAction.press(star_btn).release().perform()
        else:
            logging.debug("image not alike")
            self.assertTrue(0)
        
        if after_image_name != None:
            elementImageName, elementImageSize = self.__capture_element(star_btn)
            added_file_name = self.__add_resolution_to_file_name(after_image_name, elementImageSize)
            similarity = self.__pil_image_similarity(added_file_name, elementImageName)
            self.assertEqual(0, similarity)
            
    @test_step_info
    def check_widget_if_image_alike(self, string, ref_image_name):
        star_btn = self.driver.find_element_by_string(string)
        elementImageName, elementImageSize = self.__capture_element(star_btn)
        logging.debug("elementImageSize:%s", elementImageSize) 
        added_file_name = self.__add_resolution_to_file_name(ref_image_name, elementImageSize)
        
        if self.__pil_image_similarity(added_file_name, elementImageName) == 0:
            self.touchAction.press(star_btn).release().perform()
        else:
            logging.debug("image not alike")
            self.assertTrue(0)
        
    @test_step_info
    def swipe_widget(self, string, startx=0, starty=0, endx=0, endy=0, duration=500):
        widget = self.driver.find_element_by_string(string)
        lx = widget.location.get('x')
        ly = widget.location.get('y')
        logging.debug("location x:%s location y:%s", lx, ly)
        size = widget.size
        logging.debug("size %s %s", size["width"], size["height"])
        if startx=="middle":
            startx = size["width"] / 2
        
        if starty=="middle":
            starty = size["height"]/ 2
        
        if endx=="middle":
            endx = size["width"] / 2
        
        if endy=="middle":
            endy = size["height"]/ 2
        
        window_size = self.driver.get_window_size()
        logging.debug("window size %s %s", window_size["width"], window_size["height"])
        if (startx>size['width'] or startx<0
        or starty>size['height'] or starty<0
        or endx>size['width'] or endx<0
        or endy>size['height'] or endy<0
        or startx+lx>window_size['width'] 
        or starty+ly>window_size['height'] 
        or endx+lx>window_size['width']
        or endy+ly>window_size['height']):
            raise OutOfBoundException
        
        self.driver.swipe(startx + lx, starty + ly, endx + lx, endy + ly, duration)
        
    @test_step_info        
    def swipe_widget_by_direction(self, string, direction, duration=500):
        widget = self.driver.find_element_by_string(string)
        size = widget.size
        if direction == "up":
            self.driver.swipe(size['width']/2, size['height'] - 50, size['width']/2, 50, duration)
        elif direction == "down":
            self.driver.swipe(size['width']/2, 50, size['width']/2, size['height'] - 50, duration)
        elif direction == "left":
            self.driver.swipe(size['width'] - 50, size['height']/2, 50, size['height']/2, duration)
        elif direction == "right":
            self.driver.swipe(50, size['height']/2, size['width'] - 50, size['height']/2, duration)
        else:
            raise WrongDirectionException
    
    def __capture_element(self, what):
        begin = what.location
        size = what.size
        start_x = begin['x']
        start_y = begin['y']
        end_x = start_x + size['width']
        end_y = start_y + size['height']
        name = str(start_x)+'_'+str(start_y)+'_'+'_'+str(end_x)+'_'+str(end_y)
        box = (start_x, start_y, end_x, end_y)
        self.driver.get_screenshot_as_file('./' + 'full_screen.png')
        image = Image.open('./' + 'full_screen.png')        #tmp是临时文件夹
        newimage = image.crop(box)
        name = './' + name + '.png'
        newimage.save(name)
        os.popen('rm ./full_screen.png')   
        return name, size
            