# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
from types import *
import logging
import unittest
import datetime
from datetime import timedelta

#from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


from PIL import Image

from mywebdriver import WebDriver
from myelement import PositionProperty
from myelement import WebElement as MyElement

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
console.setLevel(logging.ERROR)
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

        if  objPtr.case_function_name != None:
            # take screen shot after every step function
            # it will slow down the test and use much more storage space
            step_function_name = func.__name__
            screenshotname = objPtr.case_function_name + "/step " + str(objPtr.step) + " "+ step_function_name + ".png"
            objPtr.driver.get_screenshot_as_file(screenshotname)
                
        return result
    return _func

class UnknownStringException(Exception):
    def __init__(self, value=None):
        self.value = value

class OutOfBoundException(Exception):
    def __init__(self, value=None):
        self.value = value

class WrongDirectionException(Exception):
    def __init__(self, value=None):
        self.value = value

class UnknownChoiceException(Exception):
    def __init__(self, value=None):
        self,value = value
        
class UnknownReferenceOptionError(Exception):
        def __init__(self, value=None):
            self.value = value
        
_YESTERDAY = 0b0001
_TOMORROW = 0b0010
_LASTWEEK = 0b0100
_NEXTWEEK = 0b1000
        

class CommonTestStep(unittest.TestCase):
    wait_duration = 30
    
    def __init__(self):
        self.step = 0
        self.tap_duration = 200
        self.long_tap_duration = 1000
        self.swipe_duration = 500
    
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
        os.path.splitext(filename)
        ref_image_true_name = os.path.splitext(filename)[0]
        logging.debug("ref_image_true_name:%s", ref_image_true_name) 
        ref_image_ext_name = os.path.splitext(filename)[1]
        logging.debug("ref_image_ext_name:%s", ref_image_ext_name) 
        
        ref_image_height = resolution['height']
        logging.debug("ref_image_height:%s", ref_image_height) 
        
        ref_image_width = resolution['width']
        logging.debug("ref_image_width:%s", ref_image_width) 
        
        added_file_name = ref_image_true_name+'_'+str(ref_image_width)+'_'+str(ref_image_height)+ref_image_ext_name
        logging.debug("added_file_name:%s", added_file_name)
         
        return added_file_name    
        
        
    def _find_day_widget_by_nearby_date(self, listView, target_date, ref_option):
        if self.platformName == 'Android':
            primary_date_string = "//android.widget.CheckedTextView"
            secondary_date_string = "//android.widget.TextView"

        if ref_option & _YESTERDAY == _YESTERDAY:
            yesterday_widget = listView.has_widget("//*[@text='"+str((target_date-datetime.timedelta(days=1)).day)+"']")
        elif ref_option & _TOMORROW == _TOMORROW:
            tomorrow_widget = listView.has_widget("//*[@text='"+str((target_date+datetime.timedelta(days=1)).day)+"']")
        elif ref_option & _LASTWEEK == _LASTWEEK:
            lastweek_widget = listView.has_widget("//*[@text='"+str((target_date-datetime.timedelta(days=7)).day)+"']")
        elif ref_option & _NEXTWEEK == _NEXTWEEK:    
            nextweek_widget = listView.has_widget("//*[@text='"+str((target_date+datetime.timedelta(days=7)).day)+"']")
        else:
            logging.error("Unknown reference option %s", str(ref_option))
            raise UnknownReferenceOptionError

        if ref_option == _YESTERDAY | _TOMORROW | _LASTWEEK | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif  ref_option == _YESTERDAY | _TOMORROW | _LASTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif ref_option == _YESTERDAY | _TOMORROW | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif ref_option == _TOMORROW | _LASTWEEK | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
        
        elif ref_option == _YESTERDAY | _LASTWEEK | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))

        elif ref_option == _YESTERDAY | _LASTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif ref_option == _YESTERDAY | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._right(str((target_date-datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
        
        elif ref_option == _TOMORROW | _LASTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif ref_option == _TOMORROW | _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._left(str((target_date+datetime.timedelta(days=1)).day))+
                                                 self._under("六"))

        elif ref_option == _LASTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._under(str((target_date-datetime.timedelta(days=7)).day))+
                                                 self._under("六"))

        elif ref_option == _NEXTWEEK:
            try:
                day_widget = listView.has_widget(primary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
            except NoSuchElementException:
                day_widget = listView.has_widget(secondary_date_string,
                                                 self._above(str((target_date+datetime.timedelta(days=7)).day))+
                                                 self._under("六"))
        return day_widget
    
    def _swipe_to_distination_half_by_half(self, start_element, end_element, distination_side="top2bottom", one_step=False):
        if distination_side == "top2top":
            start_x = start_element.location.get('x')+start_element.size['width']/2
            start_y = start_element.location.get('y')
            end_x = start_element.location.get('x')+start_element.size['width']/2
            end_y = end_element.location.get('y')
        elif distination_side == "top2bottom":
            start_x = start_element.location.get('x')+start_element.size['width']/2
            start_y = start_element.location.get('y')
            end_x = start_element.location.get('x')+start_element.size['width']/2
            end_y = end_element.location.get('y')+end_element.size['height']
        elif distination_side == "bottom2top":
            start_x = start_element.location.get('x')+start_element.size['width']/2
            start_y = start_element.location.get('y')+start_element.size['height']
            end_x = start_element.location.get('x')+start_element.size['width']/2
            end_y = end_element.location.get('y')
        elif distination_side == "bottom2bottom":
            start_x = start_element.location.get('x')+start_element.size['width']/2
            start_y = start_element.location.get('y')+start_element.size['height']
            end_x = start_element.location.get('x')+start_element.size['width']/2
            end_y = end_element.location.get('y')+end_element.size['height']
    
        window_size = self.driver.get_window_size()
        window_max_x = window_size['width']
        window_max_y = window_size['height']
        window_min_x = 0
        window_min_y = 0
    
        if start_x == window_min_x:
            start_x = 1
        elif start_x == window_max_x:
            start_x = window_max_x - 1
        
        if end_x == window_min_x:
            end_x = 1
        elif end_x == window_max_x:
            end_x = window_max_x - 1
    
        if start_y == window_min_y:
            start_y = 1
        elif start_y == window_max_y:
            start_y = window_max_y - 1
        
        if end_y == window_min_y:
            end_y = 1
        elif end_y == window_max_y:
            end_y = window_max_y - 1
        
        if not start_y==end_y:
            if one_step == False:
                while (abs(start_y-end_y)>100):
                    logging.debug("swipe:%d, %d", start_y, end_y)
                    self.driver.swipe(start_x, start_y, start_x, (start_y+end_y)/2)
                    start_y = (start_y+end_y)/2
                
            
            logging.debug("final swipe:%d, %d", start_y, end_y)
            self.driver.swipe(start_x, start_y, start_x, end_y)
            
            return True
        else:        
            return False
                
    @test_step_info
    def tap_date_in_calendar(self, des_date):
        logging.debug("des_date:%s", des_date)
        logging.debug("des_date.isoweekday():%d", des_date.isoweekday())
    
        current_date_bar = self.driver.find_element_by_string('年')
        current_date_bar_text = current_date_bar.text
        year = current_date_bar_text[0:current_date_bar_text.index(u"年")]
        month = current_date_bar_text[current_date_bar_text.index(u"年")+1:current_date_bar_text.index(u"月")]
        current_date = des_date.replace(day=1).replace(year=int(year)).replace(month=int(month))
        logging.debug("current_date:%s", current_date)
    
        
        listView = self.driver.find_element_by_string("com.ziipin.homeinn:id/date_list")
        
        try:
            destination_month = self.driver.find_element_by_string(str(des_date.year)+"年"+str(des_date.month)+"月")
            
        except NoSuchElementException:
            if des_date.month != current_date.month:
                # swipe up calendar certain times according to month count from today
                if (des_date.year - current_date.year) * 12 + des_date.month - current_date.month > 0:
                    next_month_date = current_date
                    for i in range((des_date.year - current_date.year) * 12 + des_date.month - current_date.month):
                        # find next month bar and swipe it to the top, otherwise swipe calendar from bottom to top
                        next_month_date = (next_month_date.replace(day=1) + timedelta(days=32)).replace(day=1)
                        logging.debug("next_month_date:%s", next_month_date)
                        try:
                            next_month = self.driver.find_element_by_string(\
                            str(next_month_date.year)+"年"+str(next_month_date.month)+"月")
                        except NoSuchElementException:
                            logging.debug(\
                            "self._swipe_to_distination_half_by_half(listView, listView, 'bottom2top')")
                            self._swipe_to_distination_half_by_half(listView, listView, "bottom2top")
                        else:
                            self.driver.drag_and_drop(next_month, current_date_bar)
                            next_month = self.driver.find_element_by_string(\
                            str(next_month_date.year)+"年"+str(next_month_date.month)+"月")
                            logging.debug(\
                            "self._swipe_to_distination_half_by_half(next_month, listView, 'top2top')")
                            self._swipe_to_distination_half_by_half(next_month, listView, "top2top")
                    
                    destination_month = self.driver.find_element_by_string(\
                    str(des_date.year)+"年"+str(des_date.month)+"月")
                    logging.debug("self._swipe_to_distination_half_by_half(destination_month, listView, 'top2top')")
                    self._swipe_to_distination_half_by_half(destination_month, listView, "top2top")
                        
                else:
                    previous_month_date = current_date
                    logging.debug("self._swipe_to_distination_half_by_half(current_date_bar, listView, 'top2bottom')")
                    self._swipe_to_distination_half_by_half(current_date_bar, listView, "bottom2bottom")
                    for i in range((current_date.year - des_date.year) * 12 + current_date.month - des_date.month):
                        # find previous month bar after swiping current month bar to the bottom
                        # swipe calendar from top to bottom 
                        previous_month_date = (previous_month_date.replace(day=1) - timedelta(days=1)).replace(day=1)
                        logging.debug("previous_month_date:%s", previous_month_date)
                        try:
                            previous_month = self.driver.find_element_by_string(\
                            str(previous_month_date.year)+"年"+str(previous_month_date.month)+"月")
                        except NoSuchElementException:
                            self._swipe_to_distination_half_by_half(listView, listView, "top2bottom")
                            logging.debug("self._swipe_to_distination_half_by_half(listView, listView, 'top2bottom')")
                        else:
                            self.driver.drag_and_drop(previous_month, current_date_bar)
                            previous_month = self.driver.find_element_by_string(\
                            str(previous_month_date.year)+"年"+str(previous_month_date.month)+"月")
                            logging.debug(\
                            "self._swipe_to_distination_half_by_half(previous_month, listView, 'top2top')")
                            self._swipe_to_distination_half_by_half(previous_month, listView, "top2top")
        else:
            # swipe up the calendar until destination month text bar reach the top of canlendar
            logging.debug("self.driver.drag_and_drop(destination_month, current_date_bar)")
            self.driver.drag_and_drop(destination_month, current_date_bar)
            logging.debug("self._swipe_to_distination_half_by_half(destination_month, listView, 'top2top')")
            destination_month = self.driver.find_element_by_string(str(des_date.year)+"年"+str(des_date.month)+"月")
            self._swipe_to_distination_half_by_half(destination_month, listView, "top2top")
            
        try:
            destination_day = self.driver.find_element_by_string(\
            "//*[@text='"+str(des_date.year)+"年"+str(des_date.month)+"月']\
            /parent::*//*[@text='"+str(des_date.day)+"']")
        except NoSuchElementException:
            if des_date.isoweekday() != 6 and des_date.isoweekday() != 7:
                if des_date.day>7\
                and des_date.day<(((des_date.replace(day=1) + timedelta(days=32)).replace(day=1)\
                 - datetime.timedelta(days=1)).day-7):
                    logging.info("It's work day")
                    destination_day = self._find_day_widget_by_nearby_date(\
                    listView, des_date, _YESTERDAY | _TOMORROW | _LASTWEEK | _NEXTWEEK)
                elif des_date.day<=7:
                    if des_date.day==1:
                        logging.info("It's work day at 1st")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _TOMORROW | _NEXTWEEK)
                    else:
                        logging.info("It's work day in first week")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _YESTERDAY | _TOMORROW | _NEXTWEEK)
                else:
                    if des_date.day==((des_date.replace(day=1) + timedelta(days=32)).replace(day=1)\
                    - datetime.timedelta(days=1)).day:
                        logging.info("It's work day at last day")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _YESTERDAY | _LASTWEEK)
                    else:
                        logging.info("It's work day in last week")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _YESTERDAY | _TOMORROW | _LASTWEEK)
            elif des_date.isoweekday() == 6:
                if des_date.day>7 and des_date.day<((des_date.replace(day=1) + timedelta(days=32)).replace(day=1)\
                 - datetime.timedelta(days=1)).day-7:
                    logging.info("It's saturday")
                    destination_day = self._find_day_widget_by_nearby_date(\
                    listView, des_date, _YESTERDAY | _LASTWEEK | _NEXTWEEK)
                elif des_date.day<=7:
                    if des_date.day==1:
                        logging.info("It's saturday on 1st")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _NEXTWEEK)
                    else:
                        logging.info("It's saturday in first week")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _YESTERDAY | _NEXTWEEK)
                else:
                    logging.info("It's saturday in last week")
                    destination_day = self._find_day_widget_by_nearby_date(\
                    listView, des_date, _YESTERDAY | _LASTWEEK)
            elif des_date.isoweekday() == 7:
                if des_date.day>7 and des_date.day<((des_date.replace(day=1) + timedelta(days=32)).replace(day=1)\
                 - datetime.timedelta(days=1)).day-7:
                    logging.info("It's sunday")
                    destination_day = self._find_day_widget_by_nearby_date(\
                    listView, des_date, _TOMORROW | _LASTWEEK | _NEXTWEEK)
                elif des_date.day<=7:
                    logging.info("It's sunday in first week")
                    destination_day = self._find_day_widget_by_nearby_date(\
                    listView, des_date, _TOMORROW | _NEXTWEEK)
                else:
                    if des_date.day==((des_date.replace(day=1) + timedelta(days=32)).replace(day=1)\
                     - datetime.timedelta(days=1)).day:
                        logging.info("It's sunday at last day")
                        destination_day = self._find_day_widget_by_nearby_date(listView, des_date, _LASTWEEK)
                    else:
                        logging.info("It's sunday in last week")
                        destination_day = self._find_day_widget_by_nearby_date(\
                        listView, des_date, _TOMORROW | _LASTWEEK)
            
        self.touchAction.press(destination_day).release().perform()
    
    def take_screen_shot_at_every_step(self, case_function_name):
        self.case_function_name = case_function_name
        if case_function_name != None:
            os.popen("rm -rf "+self.case_function_name)
            os.popen("mkdir "+self.case_function_name)
        
    def init_appium(self, desired_caps, server_port=4723, case_function_name=None):
        self.take_screen_shot_at_every_step(case_function_name)
            
        self.platformName = desired_caps['platformName']
        self.driver = WebDriver('http://localhost:'+str(server_port)+'/wd/hub', desired_caps)

        try:
            self.touchAction = TouchAction(self.driver)

            self.wait = WebDriverWait(self.driver, CommonTestStep.wait_duration, 1)
        
            if self.platformName == 'Android':
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
        except:
            self.driver.quit()
                       
    def deinit_appium(self, screen_shot_file=None):
        if screen_shot_file != None:
            screenshotname = "./" + screen_shot_file + ".png"
            sleep(1)
            self.driver.get_screenshot_as_file(screenshotname)
        self.driver.quit()
    
    def tap_button_if_exist(self, string, wait_duration=3):
        try:
            button = self.driver.find_element_by_string(string, wait_duration)        
            self.touchAction.tap(button).perform()
            self.last_tapped_widget = button
            logging.debug("%s button exists", string)
        except:
            logging.debug("%s button not exist", string)
    
    def _near(self, string):
        return self.driver._near(string)
            
    def _above(self, string):
        return self.driver._above(string)
        
    def _under(self, string):
        return self.driver._under(string)
    
    def _left(self, string):
        return self.driver._left(string)
    
    def _right(self, string):
        return self.driver._right(string)
    
    def _in(self, string):
        return self.driver._in(string)
            
    @test_step_info
    def wait_window(self, window, timeout=wait_duration, interval=1):
        if self.platformName == 'Android':
            return self.driver.wait_activity(window, timeout, interval)
        elif self.platformName == 'iOS':
            wait = WebDriverWait(self, timeout, interval)
            wait.until(lambda dr: dr.driver.find_element_by_string(window).is_displayed())
            return self.driver.find_element_by_string(window)
        else:
            raise UnsupportedPlatformException

    # function wait for act activity and check it show up or not within duration specified by parameter timeout
    # checking interval is specified by parameter interval 
    @test_step_info
    def wait_and_check_window_show_up(self, window, timeout=wait_duration, interval=1):
        if self.platformName == 'Android':
            if self.driver.wait_activity(window, timeout, interval):
               logging.debug("*****"+window+" OK*****") 
            else:
               logging.error("*****wait for "+window+" time out*****") 
   
            self.assertTrue(window == self.driver.current_activity)
        elif self.platformName == 'iOS':
            wait = WebDriverWait(self, timeout, interval)
            wait.until(lambda dr: dr.driver.find_element_by_string(window).is_displayed())
            return self.driver.find_element_by_string(window)
        else:
            raise UnsupportedPlatformException
        
    @test_step_info
    def has_widget(self, string, posprolist=None):
        return self.driver.has_widget(string, posprolist)
        
    @test_step_info
    def has_widgets(self, string, posprolist=None):
        return self.driver.has_widgets(string, posprolist)
        
    @test_step_info
    def wait_widget(self, string, timeout=wait_duration, interval=1, retry=False): 
        if retry:
            try:
                wait = WebDriverWait(self.driver, timeout, interval)
                wait.until(lambda dr: dr.find_element_by_string(string).is_displayed())
            except TimeoutException:
                try:
                    self.driver.has_widget('抱歉，暂无相关结果')
                except NoSuchElementException:
                    try:
                        self.driver.has_widget('您的网络好像不太给力，请稍后再试')
                    except:
                        raise TimeoutException
                    else:
                        try:
                            retry_widget = self.driver.has_widget('点击重试')
                        except NoSuchElementException:
                            self.tap_widget(self.last_tapped_widget)
                        else:
                            self.tap_widget(retry_widget)
                    
                        wait.until(lambda dr: dr.find_element_by_string(string).is_displayed())
                else:
                    logging.error("No result, may be network error.")
                    raise TimeoutException
            
        else:
            wait = WebDriverWait(self.driver, timeout, interval)
            wait.until(lambda dr: dr.find_element_by_string(string).is_displayed())
            
    @test_step_info
    def current_window(self):
        if self.platformName == 'Android':
            return self.driver.current_activity

    @test_step_info
    def current_app(self, app):
        if self.platformName == 'Android':
            current_activity = os.popen("adb shell dumpsys window w | grep mFocusedApp | awk '{printf $5}'").read()
            logging.debug("current_activity:%s", current_activity)
            return not (current_activity.find(app)==-1)
        
    @test_step_info
    def launch_app_if_installed(self, package, activity):
        el = self.driver.is_app_installed(package)
        self.assertTrue(el)
        el = self.driver.start_activity(package, activity)
        self.assertTrue(el)
    
    @test_step_info    
    def input_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
    
        if self.platformName == 'Android':
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            logging.debug("ime is %s", self.driver.active_ime_engine)
            self.driver.activate_ime_engine(self.ime)
            logging.debug("ime is %s", self.driver.active_ime_engine)
            
        textbox.clear()

        #self.touchAction.press(textbox, self.tap_duration).release().perform()    
        textbox.send_keys(text)
    
    @test_step_info    
    def input_secure_textbox(self, string, text):
        textbox = self.driver.find_element_by_string(string)
    
        if self.platformName == 'Android':
            # switch to non-appium ime in order to avoid send_keys ramdom error for numbers and english charactors
            # please be noticed that ime must be switch appium unicdoe ime for inputing Chinese charactor
            logging.debug("ime is %s", self.driver.active_ime_engine)
            self.driver.activate_ime_engine(self.ime)
            logging.debug("ime is %s", self.driver.active_ime_engine)
        
        self.touchAction.press(textbox, self.tap_duration).release().perform() # because send_keys miss first character, so here come one blank as to avoid this problem
        textbox.send_keys(text)
    
    @test_step_info
    def input_textbox_uft8(self, string, text, pinyin=None):
        textbox = self.driver.find_element_by_string(string)
    
        if self.platformName == 'Android':
            logging.debug("ime is %s", self.driver.active_ime_engine)
            self.driver.activate_ime_engine(u"io.appium.android.ime/.UnicodeIME")
            logging.debug("ime is %s", self.driver.active_ime_engine)
            
        self.touchAction.press(textbox, self.tap_duration).release().perform()
        
        if self.platformName == 'iOS':
            try:
                self.driver.find_element_by_string("//UIAKey[@label='Pinyin-Plane']")
            except NoSuchElementException:
                nextKeyBoard = self.driver.find_element_by_string("//UIAButton[@label='Next keyboard']")
                self.touchAction.press(nextKeyBoard, self.tap_duration).release().perform()
                self.driver.find_element_by_string("//UIATableCell[contains(@label, '简体拼音')]").click()
            except:
                logging.error("Unknown exception captured")
                
            if pinyin!=None:
                textbox.send_keys(pinyin)
                destination = self.driver.find_element_by_string("//UIACollectionCell[contains(@label, '"+text+"')]")
                self.touchAction.press(destination, self.tap_duration).release().perform()
                
        elif self.platformName == 'Android':
            textbox.send_keys(text)
    
        if self.platformName == 'Android':
            self.driver.activate_ime_engine(self.ime)
            logging.debug("ime is %s", self.driver.active_ime_engine)
        
    
    @test_step_info    
    def tap_button(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            widget = self.driver.find_element_by_string(string)
            self.touchAction.tap(widget).perform()
            self.last_tapped_widget = widget
        elif isinstance(string, MyElement):
            self.touchAction.tap(string).perform()
            self.last_tapped_widget = string
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
    
    @test_step_info    
    def tap_widget(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            widget = self.driver.find_element_by_string(string)
            self.touchAction.tap(widget).perform()
            self.last_tapped_widget = widget
        elif isinstance(string, MyElement):
            self.touchAction.tap(string).perform()
            self.last_tapped_widget = string
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        
        
    @test_step_info
    def click_widget(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            widget = self.driver.find_element_by_string(string)
            widget.click()
            self.last_tapped_widget = widget
        elif isinstance(string, MyElement):
            string.click()
            self.last_tapped_widget = string
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        
    @test_step_info
    def tap_permision_widget(self, choice="accept"):
        if choice == "accept":
            if self.platformName == 'Android':
                # in order to close permision widget, here is script to ensure script can deal with MIUI and Huawei system permision widget
                self.tap_button_if_exist("//android.widget.Button[@text='允许']")
                self.tap_button_if_exist("com.huawei.systemmanager:id/btn_allow")
            elif self.platformName == 'iOS':
                try:
                    self.driver.switch_to_alert().accept()
                except:
                    logging.info("no alert exist")
            else:
                raise UnsupportedPlatformException
                
        elif choice == "deny":
            if self.platformName == 'Android':
                # in order to close permision widget, here is script to ensure script can deal with MIUI and Huawei system permision widget
                self.tap_button_if_exist("//android.widget.Button[@text='拒绝']")
                self.tap_button_if_exist("com.huawei.systemmanager:id/btn_forbbid")
            elif self.platformName == 'iOS':
                self.driver.switch_to_alert().deny()
            else:
                raise UnsupportedPlatformException
        else:
            logging.error("Unknown choise %s", str(choice))
            raise UnknownChoiceException 
            
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
        self.touchAction.tap(button).perform()
        self.last_tapped_widget = button

    @test_step_info
    def long_tap_widget(self, string, x=0, y=0, duration=1000):
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

        if duration == 1000:
            duration = self.long_tap_duration
            
        self.touchAction.long_press(widget, x, y, duration).release().perform()
        self.last_tapped_widget = widget
        
    @test_step_info
    def tap_widget_if_image_alike(self, string, ref_image_name, after_image_name=None):
        star_btn = self.driver.find_element_by_string(string)
        elementImageName, elementImageSize = self.__capture_element(star_btn)
        logging.debug("elementImageSize:%s", elementImageSize) 
        added_file_name = self.__add_resolution_to_file_name(ref_image_name, elementImageSize)
        
        if self.__pil_image_similarity(added_file_name, elementImageName) == 0:
            self.touchAction.tap(star_btn).perform()
            self.last_tapped_widget = star_btn
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
        size = widget.size
        logging.debug("size %d %d", size["width"], size["height"])
        if startx=="middle":
            startx = size["width"] / 2
        
        if starty=="middle":
            starty = size["height"]/ 2
        
        if endx=="middle":
            endx = size["width"] / 2
        
        if endy=="middle":
            endy = size["height"]/ 2
        logging.debug("startx:%d starty:%d endx:%d endy:%d", startx, starty, endx, endy)

        lx = widget.location.get('x')
        ly = widget.location.get('y')
        logging.debug("location x:%d location y:%d", ly, ly)
        window_size = self.driver.get_window_size()
        logging.debug("window size %d %d", window_size["width"], window_size["height"])
        if (startx>size['width'] or startx<0
        or starty>size['height'] or starty<0
        or endx>size['width'] or endx<0
        or endy>size['height'] or endy<0
        or startx+lx>window_size['width'] 
        or starty+ly>window_size['height'] 
        or endx+lx>window_size['width']
        or endy+ly>window_size['height']):
            logging.error("Out of bound exception")
            raise OutOfBoundException

        if duration == 500:
            duration = self.swipe_duration
        self.driver.swipe(startx + lx, starty + ly, endx + lx, endy + ly, duration)
        
    @test_step_info        
    def swipe_widget_by_direction(self, string, direction, duration=500):
        widget = self.driver.find_element_by_string(string)
        #if self.platformName == 'Android':
        size = widget.size    
        logging.debug("size %s %s", size["width"], size["height"])
        lx = widget.location.get('x')
        ly = widget.location.get('y')
        logging.debug("location x:%s location y:%s", lx, ly)
        window_size = self.driver.get_window_size()
        logging.debug("window size %s %s", window_size["width"], window_size["height"])

        if (size['width']/2+lx>window_size['width'] 
        or size['height']/2+ly>window_size['height']):
            logging.error("Out of bound exception")
            raise OutOfBoundException

        if duration == 500:
            duration = self.swipe_duration
            
        if direction == "up":
            self.driver.swipe(size['width']/2+lx, size['height']-1+ly\
            , size['width']/2+lx, 1+ly,                duration)
        elif direction == "down":
            self.driver.swipe(size['width']/2+lx, 1+ly\
            , size['width']/2+lx, size['height']-1+ly, duration)
        elif direction == "left":
            self.driver.swipe(size['width']-1+lx, size['height']/2+ly\
            , 1+lx,               size['height']/2+ly, duration)
        elif direction == "right":
            self.driver.swipe(1+lx,               size['height']/2+ly\
            , size['width']-1+lx, size['height']/2+ly, duration)
        else:
            logging.error("Wrong direction %s", str(direction))
            raise WrongDirectionException
        
    @test_step_info        
    def swipe_by_direction(self, direction, duration=500):
        #if self.platformName == 'Android':
        window_size = self.driver.get_window_size()
        logging.debug("window size %s %s", window_size["width"], window_size["height"])
        lx = window_size["width"]
        ly = window_size["height"]

        if duration == 500:
            duration = self.swipe_duration
            
        if direction == "up":
            self.driver.swipe(lx/2, ly-1, lx/2, 1, duration)
        elif direction == "down":
            self.driver.swipe(lx/2, 1, lx/2, ly-1, duration)
        elif direction == "left":
            self.driver.swipe(lx-1, ly/2, 1, ly/2, duration)
        elif direction == "right":
            self.driver.swipe(1, ly/2, lx-1, ly/2, duration)
        else:
            logging.error("Wrong direction %s", str(direction))
            raise WrongDirectionException
    
    @test_step_info
    def swipe_up_and_retry(self, tips, button_string):
        self.swipe_by_direction("up")
        self.driver.has_widget(tips)
        retry_widget = self.driver.has_widget(button_string)
        self.tap_widget(retry_widget)
        
    @test_step_info
    def pinch_widget(self, string, percentage=200, steps=50):
        widget = self.driver.find_element_by_string(string)
        
        self.driver.pinch(widget, percentage, steps)