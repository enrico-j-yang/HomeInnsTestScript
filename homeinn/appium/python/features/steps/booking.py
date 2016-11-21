
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep
import time
import datetime
import logging
from simplecrypt import encrypt, decrypt

from behave import *
from behave.log_capture import capture

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction 
from selenium.common.exceptions import NoSuchElementException


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


class UnknownDateError(Exception):
    def __init__(self, value=None):
        self.value = value
    
def _parse_date(checkin):
    today = datetime.date.today()
    logging.debug("today:%s", today)
    logging.debug("%s", today.year)
    logging.debug("%s", today.month)
    logging.debug("%s", today.day)
    if checkin == u"今天":
        ret_date = today
    elif checkin == u"明天":
        ret_date = today + datetime.timedelta(days=1)
    elif checkin == u"后天":
        ret_date = today + datetime.timedelta(days=2)
    elif u"天后" in checkin:
        count = checkin[0:checkin.index(u"天后")]
        # if count is digit then convert to integer
        def is_num_by_except(num):
            try:
                int(num)
                return True
            except ValueError:
                # print "%s ValueError" % num
                return False
                
        if is_num_by_except(count):
            ret_date = today + datetime.timedelta(days=int(count))
        # if count is chinese then process
        else:
            # TODO
            raise NotImplementedError(u'中文天数未实现处理')
    elif (u"月" in checkin) and (u"号" in checkin):
        month = checkin[0:checkin.index(u"月")]
        logging.debug("month:%s", month)
        day = checkin[checkin.index(u"月")+1:checkin.index(u"号")]
        logging.debug("day:%s", day)
        ret_date = today.replace(month=int(month)).replace(day=int(day))
    elif (u"月" in checkin) and (u"日" in checkin):
        month = checkin[0:checkin.index(u"月")]
        logging.debug("month:%s", month)
        day = checkin[checkin.index(u"月")+1:checkin.index(u"日")]
        logging.debug("day:%s", day)
        ret_date = today.replace(month=int(month)).replace(day=int(day))
    else:
        raise UnknownDateError
        
    return ret_date
        
@given(u'手机已安装掌上如家')
def step_impl(context):
    el = context.testStep.driver.is_app_installed('com.ziipin.homeinn')
    assert el

@given(u'手机当前运行应用不为掌上如家')
def step_impl(context):
    if context.testStep.current_app('com.ziipin.homeinn'):
        context.current_app_right = True
    else:
        context.current_app_right = False
    
@when(u'用户启动掌上如家')
def step_impl(context):
    if context.current_app_right==False:
        el = context.testStep.driver.start_activity('com.ziipin.homeinn', '.activity.SplashActivity')
        assert el

@then(u'掌上如家会出现')
def step_impl(context):
    if context.current_app_right==False:
        context.testStep.wait_window('.activity.SplashActivity', 5)
        

@given(u'掌上如家是新版本安装后第一次启动')
def step_impl(context):
    if context.current_app_right==False:
        # wait for startshow activity
        if context.testStep.wait_window('.activity.StartShowActivity', 5):
            context.first_launch = True
        else:
            context.first_launch = False

@when(u'用户左划屏幕直到出现“{widget_text}”并点击“{widget_text}”')
def step_impl(context, widget_text):
    if context.current_app_right==False:
        if context.first_launch==True:
            finish = False
            while not (finish):
                try:
                    context.testStep.has_widget(widget_text)
                except Exception:
                    context.testStep.driver.swipe(600,486, 98,489, 500)
                else:
                    finish = True
        
            start = context.testStep.has_widget(widget_text)
            assert start
            context.testStep.tap_widget(start)
            
        # wait for main window
        context.testStep.wait_widget('过夜房')
        context.testStep.wait_widget('立即预订')
        context.testStep.wait_widget('预订')
        context.testStep.wait_widget('活动')
        context.testStep.wait_widget('服务')
        context.testStep.wait_widget('我的')  
        context.testStep.tap_permision_widget("accept")
        
@given(u'用户尚未登录掌上如家')
def step_impl(context):
    context.testStep.tap_widget('我的')

    try:
        context.testStep.wait_widget('请登录如家会员', 3)
        context.log_on = False
    except:
        context.log_on = True
    

@when(u'用户输入账号密码')
def step_impl(context):
    if context.log_on==False:
        context.testStep.input_textbox('com.ziipin.homeinn:id/login_id_input', decrypt("beHome", context.usr))
        context.testStep.input_textbox('com.ziipin.homeinn:id/login_pwd_input', decrypt("beHome", context.auth))
        context.testStep.tap_widget('登录')

@then(u'用户已经登录掌上如家')
def step_impl(context):
    context.testStep.has_widget('我的订单')

@then(u'掌上如家跳转到民宿选择酒店界面')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then 掌上如家跳转到民宿选择酒店界面')
    
@given(u'掌上如家当前界面不为首页')
def step_impl(context):
    if context.testStep.wait_window('.activity.MainActivity', 5):
        context.current_window_right = True
    else:
        context.current_window_right = False

@when(u'用户按返回直到有“预订”页面可点击')
def step_impl(context):
    try:
        booking_page_widget = context.testStep.has_widget("预订")
    except NoSuchElementException:
        found = False
    else:
        found = True
    
    while(found==False):
        context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")
        try:
            booking_page_widget = context.testStep.has_widget("预订")
        except NoSuchElementException:
            found = False
        else:
            found = True
        
        
#############################################################################
@given(u'掌上如家“当前位置”为“{widget_text}”')
def step_impl(context, widget_text):
    element = context.testStep.has_widget(widget_text, context.testStep._under('当前位置'))
    #element = context.testStep.has_widget("//*[@text='"+widget_text+"']", context.testStep._near(current_pos))
    context.element = element
    
@then(u'掌上如家“当前位置”为“{widget_text}”')
def step_impl(context, widget_text):
    element = context.testStep.has_widget(widget_text, context.testStep._under('当前位置'))
    #element = context.testStep.has_widget("//*[@text='"+widget_text+"']", context.testStep._near(current_pos))
    context.element = element
    
@then(u'掌上如家“{current_pos}”不为“{widget_text}”')
def step_impl(context, current_pos, widget_text):
    element = context.testStep.has_widget("com.ziipin.homeinn:id/city_text")
    logging.debug("current_pos:%s", element.text)
    if not element.text==widget_text:
        pass
    else:
        raise Exception

@when(u'用户点击以上的“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget(context.element)
    
@then(u'掌上如家城市显示为“{widget_text}”')
def step_impl(context, widget_text):
    current_city = context.testStep.has_widget("com.ziipin.homeinn:id/city_layout")
    current_city.find_element_by_string(widget_text)
    
@given(u'当前时间在{start_time}点到{end_time}点之间')
def step_impl(context, start_time, end_time):
    today = datetime.datetime.now()
    logging.debug("%s", today)
    if int(today.hour)>=int(start_time) and int(today.hour)<int(end_time):
        pass
    else:
        assert False

@then(u'掌上如家“{roomtype}”页面有“{keyword}”条件')
def step_impl(context, roomtype, keyword):
    context.testStep.wait_widget("//*[@text='"+roomtype+"']")
    context.testStep.wait_widget("//*[@text='"+keyword+"']")
    context.testStep.wait_widget(roomtype)
    context.testStep.wait_widget(keyword)

@then(u'掌上如家{verb}选择入住时间界面')
def step_impl(context, verb):
    today = datetime.date.today()
    context.testStep.wait_widget('选择入住时间')
    context.testStep.wait_widget('离店')
    logging.debug(str(today.year)+"年"+str(today.month)+"月")
    
    context.testStep.wait_widget(str(today.year)+"年"+str(today.month)+"月")
    
@when(u'用户点击入住日期为“{checkin}”')
def step_impl(context, checkin):
    context.check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(context.check_in_date))
    context.testStep.tap_date_in_calendar(context.check_in_date)
        
@then(u'掌上如家入住日期显示为“{checkin}”')
def step_impl(context, checkin):
    context.testStep.wait_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview = context.testStep.has_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview.text.find(str(context.check_in_date.month)+u"月")
    checkinview.text.find(str(context.check_in_date.day)+u"日")

@when(u'用户点击离店日期为“{checkout}”')
def step_impl(context, checkout):
    context.check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(context.check_out_date))
    context.testStep.tap_date_in_calendar(context.check_out_date)

@then(u'掌上如家“过夜房”页面显示为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    context.check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(context.check_out_date))

    context.testStep.has_widget(str(context.check_in_date.month)+"月")
    context.testStep.has_widget(str(context.check_out_date.month)+"月")
    context.testStep.has_widget(str(context.check_in_date.day))
    context.testStep.has_widget(str(context.check_out_date.day))

@then(u'掌上如家酒店页面显示为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    context.check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(context.check_out_date))

    if len(str(context.check_in_date.day)) == 1:
        context.testStep.has_widget(str(context.check_in_date.month)+"月0"+str(context.check_in_date.day)+"日")
    else:
        context.testStep.has_widget(str(context.check_in_date.month)+"月"+str(context.check_in_date.day)+"日")
        
    if len(str(context.check_out_date.day)) == 1:
        context.testStep.has_widget(str(context.check_out_date.month)+"月0"+str(context.check_out_date.day)+"日")
    else:
        context.testStep.has_widget(str(context.check_out_date.month)+"月"+str(context.check_out_date.day)+"日")
    
@when(u'用户选择第一个酒店')
def step_impl(context):
    context.hotel = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name").text
    context.testStep.tap_widget("com.ziipin.homeinn:id/text_hotel_name")
    
@when(u'用户选择第一个不是已满的酒店')
def step_impl(context):
    hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name")
    hotel_widget_text = hotel_widget.text
    if len(hotel_widget_text)>8:
        hotel_widget_text=hotel_widget_text[0:8]
    logging.debug("hotel_widget_text:%s", hotel_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'已满':
        found = False
    else:
        found = True

    
    while (found==False):
        next_hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name", 
        context.testStep._under(hotel_widget_text))
        next_hotel_widget_text = next_hotel_widget.text
        if len(next_hotel_widget_text)>8:
            next_hotel_widget_text=next_hotel_widget_text[0:8]
        logging.debug("next_hotel_widget_text:%s", next_hotel_widget_text)
        price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price", 
        context.testStep._under(next_hotel_widget_text)).text
        logging.debug("price_widget_text:%s", price_widget_text)
        
        if price_widget_text==u'已满':
            found = False
            context.testStep._swipe_to_distination_half_by_half(hotel_widget, next_hotel_widget, "top2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        hotel_widget_text = next_hotel_widget_text
        hotel_widget = next_hotel_widget
                                
    context.hotel = hotel_widget_text
    context.testStep.tap_widget(hotel_widget)
    
@when(u'用户选择第二个不是已满的酒店')
def step_impl(context):
    index = 0
    hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name")
    hotel_widget_text = hotel_widget.text
    logging.debug("hotel_widget_text:%s", hotel_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'已满':
        found = False
    else:
        found = True
        index = index + 1
    
    while (found==False) and (index<2):
        next_hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name", 
                            context.testStep._under(hotel_widget_text))
        logging.debug("hotel_widget_text:%s", hotel_widget_text)
        next_hotel_widget_text = next_hotel_widget.text
        price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price", 
                            context.testStep._under(hotel_widget_text)).text
        logging.debug("price_widget_text:%s", price_widget_text)
        
        if price_widget_text==u'已满':
            found = False
            context.testStep._swipe_to_distination_half_by_half(hotel_widget, hotel_widget, "bottom2top")
        else:
            found = True
            index = index + 1
        
        hotel_widget_text = next_hotel_widget_text
        hotel_widget = next_hotel_widget
                                
    context.hotel = hotel_widget_text
    context.testStep.tap_widget(hotel_widget)
    
    
    
@when(u'用户选择第一个不是已满的房型')
def step_impl(context):
    room_widget = context.testStep.has_widget("com.ziipin.homeinn:id/room_info_layout")
    room_widget_text = room_widget.text
    logging.debug("room_widget_text:%s", room_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/room_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'已满':
        found = False
    else:
        found = True

    
    while (found==False):
        next_room_widget = context.testStep.has_widget("com.ziipin.homeinn:id/room_info_layout", 
        context.testStep._under(room_widget_text))
        logging.debug("room_widget_text:%s", hotel_widget_text)
        next_room_widget_text = next_room_widget.text
        price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/room_price", 
        context.testStep._under(room_widget_text)).text
        logging.debug("price_widget_text:%s", price_widget_text)
        
        if price_widget_text==u'已满':
            found = False
            context.testStep._swipe_to_distination_half_by_half(room_widget, room_widget, "bottom2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        room_widget_text = next_room_widget_text
        room_widget = next_room_widget
                                
    context.hotel = room_widget_text
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(room_widget, end_p)
    context.testStep.tap_widget(room_widget)
    
@then(u'掌上如家跳转到选房预订界面')
def step_impl(context):
    try:
        context.testStep.wait_widget(context.hotel)
    except NoSuchElementException:
        context.testStep.wait_widget((context.hotel)[0:9])


@when(u'用户上划屏幕查看房型直到酒店房型有“{room_type}”')
def step_impl(context, room_type):
    try:
        room_type_widget = context.testStep.has_widget(room_type)
    except NoSuchElementException:
        found = False
    else:
        found = True
        context.room_type_widget = room_type_widget

    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    start_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_name")
    start_p_text = start_p.text
    logging.debug("start_p_text is %s", start_p_text)
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)
    end_location = end_p.location.get('y')
    logging.debug("end_location is %s", end_location)
    last_location = None
    
    while (not found):
        end_p = context.testStep.has_widget(start_p_text)
        start_p = context.testStep.has_widgets('房', context.testStep._under(end_p))
        start_p_text = start_p[0].text
        logging.debug("start_p_text is %s", start_p_text)
        location = start_p[0].location.get('y')
        logging.debug("location is %s", location)
        if not location == last_location:
            last_location = location
            logging.debug("last_location is %s", last_location)
        else:
            break
        #logging.info(str(start_p.location))
        #logging.info(str(start_p.size))
        #context.testStep.swipe_widget_by_direction("com.ziipin.homeinn:id/room_info_layout", "up")
        context.testStep._swipe_to_distination_half_by_half(start_p[0], end_p, "bottom2bottom")
        try:
            room_type_widget = context.testStep.has_widget(room_type)
        except NoSuchElementException:
            found = False
        else:
            found = True
            context.room_type_widget = room_type_widget
    
@when(u'用户在关键字中输入“{destination}”')
def step_impl(context, destination):
    context.expectation = destination
    context.testStep.input_textbox_uft8("com.ziipin.homeinn:id/search_filter_input", destination)

@when(u'用户在城市中输入“{city}”')
def step_impl(context, city):
    context.expectation = city
    context.testStep.input_textbox_uft8("com.ziipin.homeinn:id/city_input", city)

@then(u'掌上如家关键词搜索列表显示“{hotel}”')
def step_impl(context, hotel):
    try:
        hotel_widget = context.testStep.has_widget(hotel)
    except NoSuchElementException:
        hotel_widget = context.testStep.has_widget(hotel[0:9])
    context.hotel = hotel


@when(u'用户上划“{room_type}”到屏幕最顶')
def step_impl(context, room_type):
    room_type_widget = context.testStep.has_widget(room_type)
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(room_type_widget, end_p)

#@given(u'“{room_type}”有“{member_price}”房间')
#def step_impl(context, room_type, member_price):
    #room_type_widget = context.testStep.has_widget(room_type)
    #context.room_type_widget
    #member_price_widget = context.testStep.has_widget(member_price)

    #booking_widget = context.testStep.has_widget("//android.widget.Button",
                                             #context.testStep._under(room_type_widget)+
                                             #context.testStep._right(member_price_widget))
    
    #logging.debug(booking_widget.text)
    #logging.debug(str(booking_widget.location))
    #room_of_booking_widget = context.testStep.has_widget('房',
                                                    #context.testStep._above(booking_widget)+
                                                    #context.testStep._near(booking_widget))
                                                    
    
    #logging.debug(room_of_booking_widget.text)
    #logging.debug(room_type_widget.text)
    #assert room_of_booking_widget.text == room_type_widget.text
    #context.booking_widget = booking_widget

@given(u'掌上如家“{room_type}”有“{member_price}”房间')
def step_impl(context, room_type, member_price):
    room_type_widget = context.testStep.has_widget(room_type)
    #context.room_type_widget
    member_price_widget = context.testStep.has_widget(member_price, context.testStep._under(room_type_widget))

    booking_widgets = context.testStep.has_widgets("//android.widget.Button[@text='预订']",
                                             context.testStep._under(room_type_widget)+
                                             context.testStep._right(member_price_widget))
    # find widget that is exactly right of member price widget
    i = 0
    logging.debug("i:%d", i)
    found = False
    while (i < len(booking_widgets)):
        # if top of member price widget is higher than bottom of booking widget
        # and bottom of member price widget is lower than top of booking widget
        # we consider them are on the same horizontal lines
        logging.debug("member_price_widget top: %d booking_widgets[%d] bottom: %d",
        member_price_widget.location.get('y') ,i ,booking_widgets[i].location.get('y')+booking_widgets[i].size["height"])
        logging.debug("member_price_widget bottom: %d booking_widgets[%d] top: %d",
        member_price_widget.location.get('y')+member_price_widget.size["height"] ,i ,booking_widgets[i].location.get('y'))
        if member_price_widget.location.get('y') < booking_widgets[i].location.get('y')+booking_widgets[i].size["height"] \
        and member_price_widget.location.get('y')+member_price_widget.size["height"] > booking_widgets[i].location.get('y'):
            found = True
            logging.debug("found")
            break
        
        i = i + 1
        logging.debug("i:%d", i)
        
    if found == False:
        context.failed
        
    context.booking_widget = booking_widgets[i]
    
    
@when(u'用户点击“{member_price}”右边的“{booking}”按钮')
def step_impl(context, member_price, booking):
    context.testStep.tap_widget(context.booking_widget)

@when(u'用户选择“{hotel}”')
def step_impl(context, hotel):
    try:
        hotel_widget = context.testStep.tap_widget(hotel)
    except NoSuchElementException:
        hotel_widget = context.testStep.tap_widget(hotel[0:8])
    context.hotel = hotel

#@then(u'检查酒店显示是否正确')
#def step_impl(context):
    #hotel_element = context.testStep.find_element_by_id("com.ziipin.homeinn:id/order_hotel_name")
    #hotel_name = hotel_element.getText()
    #if :
        

@when(u'用户向下滑动填写订单页面')
def step_imp(context):
    start_p = context.testStep.has_widget('信用住，先住后付')
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/order_hotel_name")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)

@when(u'用户向下滑动首页')
def step_imp(context):
    start_p = context.testStep.has_widget('立即预订')
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/main_brand_text")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)

#@then(u'检查酒店')
#def step_imp(context):
    #org_text = '如家-广州琶洲会展中心琶洲地铁站店'
    #element_text = context.testStep.has_widget("com.ziipin.homeinn:id/order_hotel_name").text
    #count = 2
    #if count > 1 :
        #print element_text
    #else :
        #logging.error("string is wrong")
    


@when(u'用户上划屏幕查看订单详情直到有“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.wait_widget("com.ziipin.homeinn:id/main_content")
    start_p = context.testStep.has_widget("com.ziipin.homeinn:id/main_content")
    
    end_p = start_p
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p, "bottom2top")
    
    try:
        cancel_booking_widget = context.testStep.has_widget(widget_text)
    except NoSuchElementException:
        found = False
    else:
        found = True
    
    while (not found):
        start_p = context.testStep.has_widget("com.ziipin.homeinn:id/main_content")
    
        end_p = start_p
        context.testStep._swipe_to_distination_half_by_half(start_p, end_p, "bottom2top")
        try:
            cancel_booking_widget = context.testStep.has_widget(widget_text)
        except NoSuchElementException:
            found = False
        else:
            found = True

@when(u'用户上划屏幕查看我的页面直到有“{widget_text}”')
def step_impl(context, widget_text):
    start_p = context.testStep.has_widget("我的", context.testStep._right("服务")+context.testStep._under("我的发票"))
    
    end_p = context.testStep.has_widget("我的订单")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p, "top2bottom")
    
    try:
        my_option_widget = context.testStep.has_widget(widget_text)
    except NoSuchElementException:
        found = False
    else:
        found = True
    
    while (not found):
        start_p = context.testStep.has_widget("我的", context.testStep._right("服务")+context.testStep._under("我的发票"))
    
        end_p = context.testStep.has_widget("我的订单")
        context.testStep._swipe_to_distination_half_by_half(start_p, end_p, "top2bottom")
        try:
            my_option_widget = context.testStep.has_widget(widget_text)
        except NoSuchElementException:
            found = False
        else:
            found = True



@when(u'用户上划屏幕查看房型直到有“{widget_text}”按钮')
def step_impl(context, widget_text):

    try:
        button_widget = context.testStep.has_widget(widget_text)
    except NoSuchElementException:
        found = False
    else:
        found = True

    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    start_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_name")
    start_p_text = start_p.text
    logging.debug("start_p_text is %s", start_p_text)
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)
    end_location = end_p.location.get('y')
    logging.debug("end_location is %s", end_location)
    last_location = None
    
    while (not found):
        end_p = context.testStep.has_widget(start_p_text)
        start_p = context.testStep.has_widgets('房', context.testStep._under(end_p))
        start_p_text = start_p[0].text
        logging.debug("start_p_text is %s", start_p_text)
        location = start_p[0].location.get('y')
        logging.debug("location is %s", location)
        if not location == last_location:
            last_location = location
            logging.debug("last_location is %s", last_location)
        else:
            break
        #logging.info(str(start_p.location))
        #logging.info(str(start_p.size))
        #context.testStep.swipe_widget_by_direction("com.ziipin.homeinn:id/room_info_layout", "up")
        context.testStep._swipe_to_distination_half_by_half(start_p[0], end_p, "bottom2bottom")
        try:
            button_widget = context.testStep.has_widget(widget_text)
        except NoSuchElementException:
            found = False
        else:
            found = True

@given(u'掌上如家有“{widget_text}”的订单')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)
    order_widget = context.testStep.has_widget(widget_text)
    context.order_widget = order_widget

@when(u'用户点击以上订单')
def step_impl(context):
    context.testStep.tap_widget(context.order_widget)
    
@when(u'用户上划自助服务页面')
def step_impl(context):
    context.testStep.swipe_widget_by_direction("com.ziipin.homeinn:id/main_content", "up")

@when(u'用户取消订单')
def step_impl(context):
    context.execute_steps(u'''
##########################################################
        假如    掌上如家显示“过夜房”页面
        当      用户点击“我的”

        那么    掌上如家跳转到我的界面
        当      用户点击“我的订单”

        那么    掌上如家跳转到“我的订单”界面
        假如    掌上如家有“预订成功”的订单
        当      用户点击以上订单

###############订单详情界面################################
        那么    掌上如家跳转到“订单详情”界面
        而且    掌上如家有“立即支付”按钮
        当      用户上划屏幕查看订单详情直到有“取消订单”
        当      用户点击“取消订单”
        那么    掌上如家提示“是否取消当前订单”
        当      用户点击“是”
        那么    掌上如家提示“订单取消成功”
        那么    掌上如家跳转到“我的订单”界面
        当      用户点击左上角返回按钮
        那么    掌上如家跳转到我的界面
        当      用户点击“预订”
    ''')
    
@given(u'掌上如家“过夜房”页面显示不为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    context.check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(context.check_out_date))

    try:
        context.testStep.has_widget(str(context.check_in_date.month)+"月")
        context.testStep.has_widget(str(context.check_out_date.month)+"月")
        context.testStep.has_widget(str(context.check_in_date.day), context.testStep._left("入住"))
        context.testStep.has_widget(str(context.check_out_date.day), context.testStep._left("离店"))
    except:
        context.check_in_out_right = False
    else:
        context.check_in_out_right = True
    

@when(u'用户修改入住日期为“{checkin}”，离店日期为“{checkout}”')
def step_impl(context, checkin, checkout):
    if context.check_in_out_right == False:
        context.execute_steps(u'''
            当      用户点击“入住”日期
    ###############选择入住时间界面################################
            那么    掌上如家跳转到选择入住时间界面
            而且    掌上如家有“可选择90天内日期”提示
            而且    掌上如家有“完成”按键
            当      用户点击入住日期为“'''+checkin+u'''”
            那么    掌上如家入住日期显示为“'''+checkin+u'''”
            当      用户点击离店日期为“'''+checkout+u'''”
    ##########################################################
        ''')

@given(u'掌上如家的“{widget_text}”按钮为灰色不可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="false":
        pass
    else:
        raise Exception
    
    
@given(u'掌上如家的“{widget_text}”按钮为可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="true":
        pass
    else:
        raise Exception    
        
@when(u'用户选择第一个房间')
def step_impl(context):
    room_widget = context.testStep.has_widget('com.ziipin.homeinn:id/room_sel_checker', context.testStep._under('自助选房'))
    context.testStep.tap_widget(room_widget)

@when(u'用户选择最后一个房间')
def step_impl(context):
    room_widget = context.testStep.has_widget('com.ziipin.homeinn:id/room_sel_checker', context.testStep._above('确定选房'))
    context.testStep.tap_widget(room_widget)
    
######################wait_widget############################################
@then(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)
    
@given(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)
    
@when(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家{verb}“{widget_text}”界面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)

@then(u'掌上如家{verb}“{widget_text}”提示')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)

@then(u'掌上如家{verb}“{widget_text}”按键')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家{verb}“{widget_text}”按钮')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家跳转到地图选择酒店界面')
def step_impl(context):
    context.testStep.wait_widget('全部')
    
@then(u'掌上如家提示“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家有“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家房型会有“{widget_text}”控件')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)

@given(u'掌上如家用户有可用电子券')
def step_impl(context):
    try:
        context.coupon = context.testStep.has_widget('您有可用电子券')
    except NoSuchElementException:
        context.coupon = None
        logging.info("no coupon available")
        
@then(u'掌上如家页面有酒店列表')
def step_impl(context):
    context.testStep.wait_widget("com.ziipin.homeinn:id/text_hotel_name")

@then(u'掌上如家有房型列表')
def step_impl(context):
    context.testStep.wait_widget("com.ziipin.homeinn:id/room_info_layout")
    
@then(u'掌上如家有收藏酒店列表')
def step_impl(context):
    context.testStep.wait_widget("com.ziipin.homeinn:id/favorite_list")
        
@then(u'掌上如家出现选择优惠券界面')
def step_impl(context):
    if not (context.coupon == None):
        context.testStep.wait_widget('选择优惠券')

@then(u'掌上如家出现自助服务界面')
def step_impl(context):
    if not (context.select_room == None):
        context.testStep.wait_widget('自助服务')
            
@then(u'掌上如家有“{district}”、“{circle}”和“{subway}”三个页面')
def step_impl(context, district, circle, subway):
    context.testStep.wait_widget(district)
    context.testStep.wait_widget(circle)
    context.testStep.wait_widget(subway)

@then(u'掌上如家跳转到过夜房选择酒店界面')
def step_impl(context):
    context.testStep.wait_widget('排序')
    context.testStep.wait_widget('品牌')
    context.testStep.wait_widget('筛选')
    context.testStep.wait_widget('查看地图')

@then(u'掌上如家跳转到选择时租房酒店界面')
def step_impl(context):
    context.testStep.wait_widget('排序')
    context.testStep.wait_widget('品牌')
    context.testStep.wait_widget('查看地图')

@then(u'掌上如家{verb}我的界面')
def step_impl(context, verb):
    my_account_widget = context.testStep.has_widget('我的', context.testStep._right("服务")+context.testStep._under("我的订单"))
    
    if my_account_widget.get_attribute('checked')=="true":
        pass
    else:
        assert False
    
@then(u'掌上如家“品牌”界面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['brand'])
        context.testStep.wait_widget(row['brand'])


@then(u'掌上如家“品牌”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['brand'])
        context.testStep.wait_widget(row['brand'])


@then(u'掌上如家“筛选”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['filter'])
        context.testStep.wait_widget(row['filter'])

@then(u'掌上如家“排序”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['sort'])
        context.testStep.wait_widget(row['sort'])

@then(u'掌上如家“行政区”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['district'])
        context.testStep.wait_widget(row['district'])
    
@then(u'掌上如家“商圈”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['area'])
        context.testStep.wait_widget(row['area'])

@then(u'掌上如家“地铁”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['subway'])
        context.testStep.wait_widget(row['subway'])

@then(u'掌上如家“选择出行目的”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['target'])
        context.testStep.wait_widget(row['target'])
        
@then(u'掌上如家“分享酒店”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['share'])
        context.testStep.wait_widget(row['share'])
        
########################tap_widget#####################################
@when(u'用户点击城市')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/n_main_city_text")
    
@when(u'用户点击“{widget_text}”日期')
def step_impl(context, widget_text):
    context.testStep.tap_widget(widget_text)

@when(u'用户点击“{widget_text}”')
def step_impl(context, widget_text):
    #context.testStep.click_widget(widget_text)
    context.testStep.tap_widget(widget_text)

@when(u'用户点击“{widget_text}”页面')
def step_impl(context, widget_text):
    context.testStep.tap_widget(widget_text)

@when(u'用户点击“{widget_text}”按键')
def step_impl(context, widget_text):
    widget = context.testStep.has_widget("//android.widget.Button[contains(@text, "+widget_text+")]")
    context.testStep.tap_widget(widget)

@when(u'用户点击“{widget_text}”按钮')
def step_impl(context, widget_text):
    widget = context.testStep.has_widget("//android.widget.Button[contains(@text, "+widget_text+")]")
    context.testStep.tap_widget(widget)
    
@when(u'用户点击城市列表中的“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget(widget_text)

@when(u'用户点击民宿')
def step_impl(context):
    context.testStep.tap_widget("//android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ScrollView[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[3]/android.widget.HorizontalScrollView[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]")

@when(u'用户点击定位城市')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/top_title")

@when(u'用户点击左上角返回按钮')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")  

@when(u'用户点击当前位置')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_layout")

@when(u'用户点击收藏')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/favorite_btn")

@when(u'用户点击酒店详情')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_info_layout")

@when(u'用户点击分享酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/share_btn")

@when(u'用户点击酒店地址')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/hotel_address_text")

@when(u'用户点击电话按钮')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/tell_btn")

@when(u'用户点击入店和离店时间')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_date")

@when(u'用户点击搜索列表中“{hotel}”')
def step_impl(context, hotel):
    context.testStep.tap_widget(hotel)
    
@when(u'用户点击电子券')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/coupon_price")

@when(u'用户点击积分加速计划说明')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/speed_desp_btn")

@when(u'用户点击积分加速计划')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/speed_checker")

@when(u'用户点击出行目的')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/commit_aim_layout")

@when(u'用户点击发票')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/invoice_input")

@when(u'用户点击订单详情')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/right_btn")

@when(u'用户点击电话')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/tell_btn")
    #com.ziipin.homeinn:id/order_taxi_btn
    #com.ziipin.homeinn:id/order_service_btn
    #com.ziipin.homeinn:id/cancel_btn

@when(u'用户点击支付宝支付')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_tab_ali")

@when(u'用户点击微信支付')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_tab_wechat")

@when(u'用户点击如家钱包支付')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_tab_wallet")

@when(u'用户点击银行卡支付')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_tab_union")

@when(u'用户点击立即支付')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/order_pay_btn")

@when(u'用户点击拨打电话')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/tell_btn")

@when(u'用户点击第一个酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/text_hotel_name")

@when(u'用户点击添加酒店天数')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/num_add_btn")

@when(u'用户点击减少酒店天数')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/num_dec_btn")

@when(u'用户点击联系人')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/contact_name")

@when(u'用户点击商城券说明')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/product_desp_btn")    

@when(u'用户点击添加商城券')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/add_btn")  

@when(u'用户点击减少商城券')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/dec_btn")  

@when(u'用户点击信用住说明')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/credit_desp_btn")

@when(u'用户点击信用住')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/credit_checker")

@when(u'用户点击图片')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_photo")

@when(u'用户点击关闭')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/close_btn")

@when(u'用户点击增值服务')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_service_layout")

@when(u'用户点击地址')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_address_layout")

@when(u'用户点击分享')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/share_btn") 
    
@when(u'用户点击确认选择')
def step_impl(context):
    if not (context.coupon == None):
        context.testStep.tap_widget('确认选择')
    
@when(u'用户取消选择已选房号')
def step_impl(context):
    context.testStep.tap_widget('com.ziipin.homeinn:id/sel_room_1')
    
@when(u'用户点击品牌筛选')
def step_impl(context):
    context.testStep.tap_widget('com.ziipin.homeinn:id/n_main_brand_text')
        