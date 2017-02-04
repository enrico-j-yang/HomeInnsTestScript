# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import logging

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import NoSuchElementException

from myelement import WebElement as MyElement
from myelement import PositionProperty

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
        
class WebDriver(webdriver.Remote):
    wait_duration = 60
    
    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None, keep_alive=False):

        super(WebDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive)
        self.platformName = desired_capabilities['platformName']
        


    def create_web_element(self, element_id):
        """
        Creates a web element with the specified element_id.
        Overrides method in Selenium WebDriver in order to always give them
        Appium WebElement
        """
        return MyElement(self, element_id)
    
    
    def calc_distance(self, ref_rect, rect, position):
        # 判断两个矩形的距离
        logging.debug(str(("ref_rect: ", ref_rect['leftside'], ref_rect['rightside'], ref_rect['topside'], ref_rect['bottomside'])))
        logging.debug(str(("rect: ", rect['leftside'], rect['rightside'], rect['topside'], rect['bottomside'])))

        # 假如矩形1的中心大于矩形2的左边，小于矩形2的右边，大于矩形2的上边，小于矩形2的下边
        # 那么定义矩形1在矩形2之内，否则为在之外
        if position == PositionProperty._NEAR:
            logging.debug("(rect['leftside']+rect['rightside'])/2: " + str((rect['leftside']+rect['rightside'])/2))
            logging.debug("(rect['topside']+rect['bottomside'])/2: " + str((rect['topside']+rect['bottomside'])/2))
            logging.debug("(ref_rect['leftside']+ref_rect['rightside'])/2: " + str((ref_rect['leftside']+ref_rect['rightside'])/2))
            logging.debug("(ref_rect['topside']+ref_rect['bottomside'])/2: " + str((ref_rect['topside']+ref_rect['bottomside'])/2))
            
            if (((rect['leftside']+rect['rightside'])/2<ref_rect['leftside'] and rect['rightside']<(ref_rect['leftside']+ref_rect['rightside'])/2) or
                ((rect['leftside']+rect['rightside'])/2>ref_rect['rightside'] and rect['leftside']>(ref_rect['leftside']+ref_rect['rightside'])/2) or
                ((rect['topside']+rect['bottomside'])/2<ref_rect['topside'] and rect['bottomside']<(ref_rect['topside']+ref_rect['bottomside'])/2) or
                ((rect['topside']+rect['bottomside'])/2>ref_rect['bottomside'] and rect['topside']>(ref_rect['topside']+ref_rect['bottomside'])/2)):
                x_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
                y_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
                dist = (x_dist**2+y_dist**2)**0.5
            else:
                dist = None
                
            logging.debug( "dist: " + str(dist))
        
            return dist
        elif position == PositionProperty._LEFT:
            logging.debug("(rect['leftside']+rect['rightside'])/2: " + str((rect['leftside']+rect['rightside'])/2))
            
            if ((rect['leftside']+rect['rightside'])/2<ref_rect['leftside'] and rect['rightside']<(ref_rect['leftside']+ref_rect['rightside'])/2):
                x_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
            else:
                x_dist = None
                
            logging.debug( "x_dist: " + str(x_dist))
            
            dist = x_dist
            
            return dist
        elif position == PositionProperty._RIGHT:
            logging.debug("(rect['leftside']+rect['rightside'])/2: " + str((rect['leftside']+rect['rightside'])/2))
            
            if ((rect['leftside']+rect['rightside'])/2>ref_rect['rightside'] and rect['leftside']>(ref_rect['leftside']+ref_rect['rightside'])/2):
                x_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
            else:
                x_dist = None
                
            logging.debug( "x_dist: " + str(x_dist))
            
            dist = x_dist
            return dist
        elif position == PositionProperty._ABOVE:
            logging.debug("(rect['topside']+rect['bottomside'])/2: " + str((rect['topside']+rect['bottomside'])/2))
            
            if ((rect['topside']+rect['bottomside'])/2<ref_rect['topside'] and rect['bottomside']<(ref_rect['topside']+ref_rect['bottomside'])/2):
                y_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
            else:
                y_dist = None
                
            logging.debug( "y_dist: " + str(y_dist))
            
            dist = y_dist
            return dist
        elif position == PositionProperty._UNDER:
            logging.debug("(rect['topside']+rect['bottomside'])/2: " + str((rect['topside']+rect['bottomside'])/2))
            
            if ((rect['topside']+rect['bottomside'])/2>ref_rect['bottomside'] and rect['topside']>(ref_rect['topside']+ref_rect['bottomside'])/2):
                y_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
            else:
                y_dist = None
                
            logging.debug( "y_dist: " + str(y_dist))
            
            dist = y_dist
            return dist
        # 假如矩形1的中心大于矩形2的左边，小于矩形2的右边，大于矩形2的上边，小于矩形2的下边
        # 那么定义矩形1在矩形2之内
        elif position == PositionProperty._IN:
            logging.debug("(rect['leftside']+rect['rightside'])/2: " + str((rect['leftside']+rect['rightside'])/2))
            logging.debug("(rect['topside']+rect['bottomside'])/2: " + str((rect['topside']+rect['bottomside'])/2))
            
            if ((rect['leftside']+rect['rightside'])/2>=ref_rect['leftside'] and
                (rect['leftside']+rect['rightside'])/2<=ref_rect['rightside'] and
                (rect['topside']+rect['bottomside'])/2>=ref_rect['topside'] and
                (rect['topside']+rect['bottomside'])/2<=ref_rect['bottomside']):
                x_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
                y_dist = abs((rect['topside']+rect['bottomside'])/2 - (ref_rect['topside']+ref_rect['bottomside'])/2)
                dist = (x_dist**2+y_dist**2)**0.5
            else:
                dist = None
                
            logging.debug( "dist: " + str(dist))
        
            return dist
            
            
    def check_string_type(self, string):
        logging.debug("string is "+string)
        
        try:
            # id string?
            pos = string.index(":id/")
            logging.debug("pos is "+str(pos))
        except:
            try:
                # xpath string?
                pos = string.index("//")
                logging.debug("pos is "+str(pos))
            except:
                return "unknown"
            else:
                if pos == 0:  
                    return "xpath"
        else:
            return "id"
            
    def has_widget(self, string, posprolist=None):
        logging.debug("has_widget searching string is "+string)
        if posprolist == None:
            return self.find_element_by_string(string)
        else:
            logging.debug("posprolist %d", len(posprolist))
            candidates = self.find_elements_by_string(string)
            logging.debug("candidates %s", str(candidates))
            qualified_candidates = candidates
            for ref_pos in posprolist:
                logging.debug("ref_pos.pos:%d", ref_pos.pos)
                logging.debug("ref_pos.pos:%s", str(ref_pos.rect))
                rect_distance_dic = {}
                candidates = qualified_candidates
                logging.debug("candidates count %s", len(candidates))
                qualified_candidates = []
                for element in candidates:
                    can_rect = {'leftside': element.location.get('x'), 
                                'topside': element.location.get('y'),
                                'rightside': element.location.get('x')+element.size['width'], 
                                'bottomside': element.location.get('y')+element.size['height']}
                    logging.debug("candidate %s rect: %s", element.text, str(can_rect))
                    distance = self.calc_distance(ref_pos.rect, can_rect, ref_pos.pos)
                    logging.debug("candidate %s distance:%s", element.text, str(distance))
                    if distance != None:
                        rect_distance_dic[distance] = element
                        qualified_candidates.append(element)
                        logging.debug("add element %s", element.text)
                        logging.debug("rect_distance_dic %s", str(rect_distance_dic))
                        logging.debug("qualified_candidates %s", str(qualified_candidates))

            #assert len(rect_distance_dic)==len(qualified_candidates)
            
            if len(qualified_candidates) == 0:
                raise NoSuchElementException
            else:
                qualified_candidates.sort()
                logging.debug("return %s %s", str(rect_distance_dic.values()[0]), str(qualified_candidates[0]))
                return qualified_candidates[0]
    

    def has_widgets(self, string, posprolist=None):
        logging.debug("has_widget searching string is "+string)
        if posprolist == None:
            return self.find_elements_by_string(string)
        else:
            logging.debug("posprolist %d", len(posprolist))
            candidates = self.find_elements_by_string(string)
            logging.debug("candidates %s", str(candidates))
            qualified_candidates = candidates
            for ref_pos in posprolist:
                logging.debug("ref_pos.pos:%d", ref_pos.pos)
                logging.debug("ref_pos.pos:%s", str(ref_pos.rect))
                rect_distance_dic = {}
                candidates = qualified_candidates
                logging.debug("candidates count %s", len(candidates))
                qualified_candidates = []
                for element in candidates:
                    can_rect = {'leftside': element.location.get('x'), 
                                'topside': element.location.get('y'),
                                'rightside': element.location.get('x')+element.size['width'], 
                                'bottomside': element.location.get('y')+element.size['height']}
                    logging.debug("candidate %s rect: %s", element.text, str(can_rect))
                    distance = self.calc_distance(ref_pos.rect, can_rect, ref_pos.pos)
                    logging.debug("candidate %s distance:%s", element.text, str(distance))
                    if distance != None:
                        rect_distance_dic[distance] = element
                        qualified_candidates.append(element)
                        logging.debug("add element %s", element.text)
                        logging.debug("rect_distance_dic %s", str(rect_distance_dic))
                        logging.debug("qualified_candidates %s", str(qualified_candidates))

            #assert len(rect_distance_dic)==len(qualified_candidates)
            
            if len(qualified_candidates) == 0:
                raise NoSuchElementException
            else:
                qualified_candidates.sort()
                logging.debug("return %s %s", str(rect_distance_dic.values()), str(qualified_candidates))
                return qualified_candidates
                
    def find_element_by_string(self, string):
        logging.debug("find_element_by_string: "+string)
        if (self.check_string_type(string) == "id"):
            logging.debug("string is id")
            element = self.find_element_by_id(string)
        elif (self.check_string_type(string) == "xpath"):
            logging.debug("string is xpath")
            element = self.find_element_by_xpath(string)
        else:
            try:
                element = self.find_element_by_visible_text(string)
            except NoSuchElementException:
                raise NoSuchElementException
        return element
            

    def find_elements_by_string(self, string, timeout=wait_duration, interval=1):
        logging.debug("find_elements_by_string: "+string)
        wait = WebDriverWait(self, timeout, interval)
        #logging.debug("element is %s", element)
        if (self.check_string_type(string) == "id"):
            logging.debug("string is id")
            #wait.until(lambda dr: dr.find_element_by_id(string).is_displayed())
            elements = self.find_elements_by_id(string)
        elif (self.check_string_type(string) == "xpath"):
            logging.debug("string is xpath")
            #wait.until(lambda dr: dr.find_element_by_xpath(string).is_displayed())
            elements = self.find_elements_by_xpath(string)
        else:
            try:
                elements = self.find_elements_by_visible_text(string)
            except NoSuchElementException:
                raise NoSuchElementException

            
        logging.debug("elements is "+str(elements))
        return elements
        
    def find_element_by_visible_text(self, text):
        try:
            logging.debug("using find_element_by_accessibility_id")
            element = self.find_element_by_accessibility_id(text)
            if element==None:
                raise NoSuchElementException
                
        except NoSuchElementException:
            if self.platformName == 'Android':
                try:
                    logging.debug("using find_element_by_xpath with identical text property")
                    element = self.find_element_by_xpath("//*[@text='"+text+"']")
                    if element==None:
                        raise NoSuchElementException
                except NoSuchElementException:
                    try:
                        logging.debug("using find_element_by_xpath with partial text property")
                        element = self.find_element_by_xpath("//*[contains(@text, '"+text+"')]")
                        if element==None:
                            raise NoSuchElementException
                    except NoSuchElementException:
                        raise NoSuchElementException
            elif self.platformName == 'iOS':
                try:
                    logging.debug("using find_element_by_xpath with identical label property")
                    element = self.find_element_by_xpath("//*[@label='"+text+"']")
                    if element==None:
                        raise NoSuchElementException
                except NoSuchElementException:
                    try:
                        logging.debug("using find_element_by_xpath with identical name property")
                        element = self.find_element_by_xpath("//*[@name='"+text+"']")
                        if element==None:
                            raise NoSuchElementException
                    except NoSuchElementException:
                        try:
                            logging.debug("using find_element_by_xpath with partial label property")
                            element = self.find_element_by_xpath("//*[contains(@label, '"+text+"')]")
                            if element==None:
                                raise NoSuchElementException
                        except NoSuchElementException:
                            try:
                                logging.debug("using find_element_by_xpath with partial name property")
                                element = self.find_element_by_xpath("//*[contains(@name, '"+text+"')]")
                                if element==None:
                                    raise NoSuchElementException
                            except NoSuchElementException:
                                raise NoSuchElementException
            else:
                raise UnsupportedPlatformException
        return element
        
    def find_elements_by_visible_text(self, text):
        try:
            logging.debug("using find_elements_by_accessibility_id")
            elements = self.find_elements_by_accessibility_id(text)
            if len(elements)==0:
                raise NoSuchElementException
        except NoSuchElementException:
            if self.platformName == 'Android':
                try:
                    logging.debug("using find_elements_by_xpath with partial text property")
                    elements = self.find_elements_by_xpath("//*[contains(@text, '"+text+"')]")
                    if len(elements)==0:
                        raise NoSuchElementException
                except NoSuchElementException:
                    raise NoSuchElementException
            elif self.platformName == 'iOS':
                try:
                    logging.debug("using find_elements_by_xpath with partial label property")
                    elements = self.find_elements_by_xpath("//*[contains(@label, '"+text+"')]")
                    if len(elements)==0:
                        raise NoSuchElementException
                except NoSuchElementException:
                    try:
                        logging.debug("using find_elements_by_xpath with partial name property")
                        elements = self.find_elements_by_xpath("//*[contains(@name, '"+text+"')]")
                        if len(elements)==0:
                            raise NoSuchElementException
                    except NoSuchElementException:
                        raise NoSuchElementException
            else:
                raise UnsupportedPlatformException
        return elements
        
    def get_position_property_of_element_by_visible_text(self, string, position):
        logging.debug("get_position_property_of_element_by_visible_text:%s", string)
        element = self.find_element_by_visible_text(string)
        
        rect = {'leftside': element.location.get('x'), 
                'topside': element.location.get('y'),
                'rightside': element.location.get('x')+element.size['width'], 
                'bottomside': element.location.get('y')+element.size['height']}
        logging.debug("rect:"+str(rect))
        posPro = PositionProperty(rect, position)
        #element.set_position_property(posPro)
        return posPro

    def _near(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._NEAR)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.info("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._NEAR)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        posprolist = (posPro,);
        return posprolist
            
    def _above(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._ABOVE)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.info("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._ABOVE)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        
        posprolist = (posPro,);
        return posprolist
        
    def _under(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._UNDER)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.debug("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._UNDER)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        posprolist = (posPro,);
        return posprolist
    
    def _left(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._LEFT)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.info("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._LEFT)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        posprolist = (posPro,);
        return posprolist
    
    def _right(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._RIGHT)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.debug("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._RIGHT)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        posprolist = (posPro,);
        return posprolist
    
    def _in(self, string):
        if isinstance(string, unicode) or isinstance(string, str):
            posPro = self.get_position_property_of_element_by_visible_text(string, PositionProperty._IN)
        elif isinstance(string, MyElement):
            rect = {'leftside': string.location.get('x'), 
                    'topside': string.location.get('y'),
                    'rightside': string.location.get('x')+string.size['width'], 
                    'bottomside': string.location.get('y')+string.size['height']}
            logging.info("rect:"+str(rect))
            posPro = PositionProperty(rect, PositionProperty._IN)
        else:
            logging.error("string class is: %s", string.__class__.__name__)
            raise Exception
        posprolist = (posPro,);
        return posprolist