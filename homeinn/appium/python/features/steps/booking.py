
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
from selenium.common.exceptions import TimeoutException


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
    elif checkin == u"昨天":
        ret_date = today - datetime.timedelta(days=1)
    elif checkin == u"前天":
        ret_date = today - datetime.timedelta(days=2)
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
        context.testStep.wait_widget('com.ziipin.homeinn:id/n_search_start_btn')
        context.testStep.wait_widget('预订')
        context.testStep.wait_widget('活动')
        context.testStep.wait_widget('服务')
        context.testStep.wait_widget('我的')  
        context.testStep.tap_permision_widget("accept")
        
@given(u'用户尚未登录掌上如家')
def step_impl(context):
    context.testStep.tap_widget('我的')

    try:
        context.testStep.wait_widget('密码登录', 1)
        context.log_on = False
    except:
        context.log_on = True
    
    
@given(u'掌上如家的“{widget_text}”为灰色不可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="false":
        pass
    else:
        raise Exception
    
    
@given(u'掌上如家的“{widget_text}”为可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="true":
        pass
    else:
        raise Exception  
    

@when(u'用户输入账号密码')
def step_impl(context):
    if context.log_on==False:
        context.testStep.input_textbox('com.ziipin.homeinn:id/login_id_input', decrypt("beHome", context.usr))
        context.testStep.input_textbox('com.ziipin.homeinn:id/login_pwd_input', decrypt("beHome", context.auth))
        context.testStep.tap_widget('登录')

@then(u'用户已经登录掌上如家')
def step_impl(context):
    context.testStep.wait_widget('我的订单')

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
    context.element = element
    
@given(u'当前时间在{start_time}点到{end_time}点之间')
def step_impl(context, start_time, end_time):
    today = datetime.datetime.now()
    logging.debug("%s", today)
    if int(today.hour)>=int(start_time) and int(today.hour)<int(end_time):
        pass
    else:
        assert False
    
@given(u'掌上如家有“再次预订”')
def step_impl(context):
    context.testStep.wait_widget("再次预订", 1, 1, True)
    hotel_widget = context.testStep.has_widget('com.ziipin.homeinn:id/item_hotel_name')
    context.hotel = hotel_widget.text
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    logging.info("hotel:%s", context.hotel)

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
        member_price_widget.location.get('y') ,i\
        , booking_widgets[i].location.get('y')+booking_widgets[i].size["height"])
        logging.debug("member_price_widget bottom: %d booking_widgets[%d] top: %d",
        member_price_widget.location.get('y')+member_price_widget.size["height"] ,i\
        , booking_widgets[i].location.get('y'))
        if member_price_widget.location.get('y')\
        < booking_widgets[i].location.get('y')+booking_widgets[i].size["height"] \
        and member_price_widget.location.get('y')+member_price_widget.size["height"]\
        > booking_widgets[i].location.get('y'):
            found = True
            logging.debug("found")
            break
        
        i = i + 1
        logging.debug("i:%d", i)
        
    if found == False:
        context.failed
        
    context.booking_widget = booking_widgets[i]

@given(u'掌上如家有“{widget_text}”的订单')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)
    order_widget = context.testStep.has_widget(widget_text)
    context.order_widget = order_widget
    
@given(u'掌上如家“过夜房”页面显示不为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(check_in_date))
    check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(check_out_date))
    
    check_in_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_1').text
    logging.debug("check_in_date_month: " + check_in_date_month)
    
    check_in_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_1').text
    logging.debug("check_in_date_day: " + check_in_date_day)
    
    check_out_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_2').text
    logging.debug("check_out_date_month: " + check_out_date_month)
    
    check_out_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_2').text
    logging.debug("check_out_date_day: " + check_out_date_day)

    context.check_in_date = _parse_date(check_in_date_month+check_in_date_day+u'日')
    logging.debug("context.check_in_date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(check_out_date_month+check_out_date_day+u'日')
    logging.debug("context.check_out_date: " + str(context.check_out_date))
    
    if (check_in_date)==context.check_in_date and (check_out_date)==context.check_out_date:
        #context.testStep.has_widget(str(check_in_date.month)+"月")
        #context.testStep.has_widget(str(check_out_date.month)+"月")
        #context.testStep.has_widget(str(check_in_date.day), context.testStep._left("入住"))
        #context.testStep.has_widget(str(check_out_date.day), context.testStep._left("离店"))
        context.check_in_out_right = True
    else:
        context.check_in_out_right = False
    
@given(u'掌上如家显示“{widget_text}”或者有“{tips}”的订单')
def step_impl(context, widget_text, tips):
    try:
        context.testStep.wait_widget(widget_text)
    except:
        context.testStep.wait_widget(tips, 3)

@given(u'用户有可用电子券')
def step_impl(context):
    try:
        context.coupon = context.testStep.has_widget('您有可用电子券')
    except NoSuchElementException:
        context.coupon = None
        logging.info("no coupon available")

@when(u'用户点击以上的“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget(context.element)
    
@when(u'用户点击入住日期为“{checkin}”')
def step_impl(context, checkin):
    check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(check_in_date))
    context.testStep.tap_date_in_calendar(check_in_date)

@when(u'用户点击离店日期为“{checkout}”')
def step_impl(context, checkout):
    check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(check_out_date))
    context.testStep.tap_date_in_calendar(check_out_date)
    
@when(u'用户选择第一个酒店')
def step_impl(context):
    context.hotel = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name").text

    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    
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
    if price_widget_text==u'满房':
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
        
        if price_widget_text==u'满房':
            found = False
            context.testStep._swipe_to_distination_half_by_half(next_hotel_widget, hotel_widget, "top2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        hotel_widget_text = next_hotel_widget_text
        hotel_widget = next_hotel_widget
                                
    context.hotel = hotel_widget_text
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    logging.info("hotel:%s", context.hotel)
    context.testStep.tap_widget(hotel_widget)
    
@when(u'用户选择第二个不是已满的酒店')
def step_impl(context):
    index = 0
    hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name")
    hotel_widget_text = hotel_widget.text
    logging.debug("hotel_widget_text:%s", hotel_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'满房':
        found = False
    else:
        found = True
        index = index + 1
    
    while (found==False) or (index<2):
        next_hotel_widget = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_name", 
                            context.testStep._under(hotel_widget_text))
        logging.debug("hotel_widget_text:%s", hotel_widget_text)
        next_hotel_widget_text = next_hotel_widget.text
        price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/text_hotel_price", 
                            context.testStep._under(hotel_widget_text)).text
        logging.debug("price_widget_text:%s", price_widget_text)
        
        if price_widget_text==u'满房':
            found = False
            context.testStep._swipe_to_distination_half_by_half(next_hotel_widget, hotel_widget, "top2top")
        else:
            found = True
            index = index + 1
        
        hotel_widget_text = next_hotel_widget_text
        hotel_widget = next_hotel_widget
                                
    context.hotel = hotel_widget_text
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    logging.info("hotel:%s", context.hotel)
    context.testStep.tap_widget(hotel_widget)
    
    
    
@when(u'用户展开第一个不是已满的房型')
def step_impl(context):
    room_widget = context.testStep.has_widget("com.ziipin.homeinn:id/room_name")
    room_widget_text = room_widget.text
    logging.debug("room_widget_text:%s", room_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/room_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'满房':
        found = False
    else:
        found = True

    
    while (found==False):
        next_room_widget = context.testStep.has_widget("com.ziipin.homeinn:id/room_name", 
        context.testStep._under(room_widget_text))
        next_room_widget_text = next_room_widget.text
        logging.debug("next_room_widget_text:%s", next_room_widget_text)
        price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/room_price", 
        context.testStep._under(next_room_widget_text)).text
        logging.debug("price_widget_text:%s", price_widget_text)
        
        if price_widget_text==u'满房':
            found = False
            context.testStep._swipe_to_distination_half_by_half(next_room_widget, room_widget, "bottom2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        room_widget_text = next_room_widget_text
        room_widget = next_room_widget

    context.room_type = room_widget_text
    logging.debug("room_type:%s", context.room_type)
    
    if price_widget_text.find(u'门市价')==-1:
        end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
        context.testStep._swipe_to_distination_half_by_half(room_widget, end_p)
        context.testStep.tap_widget(room_widget)
    
@when(u'用户划动第一个不是已满的房型到最顶')
def step_impl(context):
    room_widget = context.testStep.has_widget("com.ziipin.homeinn:id/room_name")
    room_widget_text = room_widget.text
    logging.debug("room_widget_text:%s", room_widget_text)
    price_widget_text = context.testStep.has_widget("com.ziipin.homeinn:id/room_price").text
    logging.debug("price_widget_text:%s", price_widget_text)
    if price_widget_text==u'满房':
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
        
        if price_widget_text==u'满房':
            found = False
            context.testStep._swipe_to_distination_half_by_half(room_widget, room_widget, "bottom2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        room_widget_text = next_room_widget_text
        room_widget = next_room_widget
                                
    context.room_type = room_widget_text
    logging.info("room_type:%s", context.room_type)
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(room_widget, end_p)


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
    
@when(u'用户在关键字搜索栏中输入“{destination}”')
def step_impl(context, destination):
    context.testStep.input_textbox_uft8("com.ziipin.homeinn:id/search_filter_input", destination)

@when(u'用户在城市中输入“{city}”')
def step_impl(context, city):
    context.testStep.input_textbox_uft8("com.ziipin.homeinn:id/city_input", city)

@when(u'用户上划“{room_type}”到屏幕最顶')
def step_impl(context, room_type):
    room_type_widget = context.testStep.has_widget(room_type)
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(room_type_widget, end_p)
    
    
@when(u'用户点击“{member_price}”右边的“{booking}”按钮')
def step_impl(context, member_price, booking):
    context.testStep.tap_widget(context.booking_widget)

@when(u'用户选择“{hotel}”酒店')
def step_impl(context, hotel):
    try:
        hotel_widget = context.testStep.tap_widget(hotel)
    except NoSuchElementException:
        hotel_widget = context.testStep.tap_widget(hotel[0:8])
    context.hotel = hotel
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
        
@when(u'用户向下滑动提交订单页面')
def step_imp(context):
    start_p = context.testStep.has_widget('信用住，先住后付')
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/order_hotel_name")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)

@when(u'用户向下滑动首页')
def step_imp(context):
    start_p = context.testStep.has_widget('立即预订')
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/main_brand_text")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)

@when(u'用户上划屏幕查看订单详情直到有“{widget_text}”')
def step_impl(context, widget_text):
    #context.testStep.wait_widget("com.ziipin.homeinn:id/main_content")
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
    start_p = context.testStep.has_widget("我的", context.testStep._right("服务"))
    
    end_p = context.testStep.has_widget("我的订单")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p, "top2bottom")
    
    try:
        my_option_widget = context.testStep.has_widget(widget_text)
    except NoSuchElementException:
        found = False
    else:
        found = True
    
    while (not found):
        start_p = context.testStep.has_widget("我的", context.testStep._right("服务"))
    
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

@when(u'用户点击以上订单')
def step_impl(context):
    context.testStep.tap_widget(context.order_widget)
    
@when(u'用户上划自助服务页面')
def step_impl(context):
    context.testStep.swipe_widget_by_direction("com.ziipin.homeinn:id/main_content", "up")
        
@when(u'用户选择第一个房间')
def step_impl(context):
    room_widget = context.testStep.has_widget('com.ziipin.homeinn:id/room_sel_checker', context.testStep._under('自助选房'))
    context.testStep.tap_widget(room_widget)

@when(u'用户选择最后一个房间')
def step_impl(context):
    room_widget = context.testStep.has_widget('com.ziipin.homeinn:id/room_sel_checker', context.testStep._above('确定选房'))
    context.testStep.tap_widget(room_widget)
    
@when(u'用户点击过夜房入住离店日期')
def step_impl(context):
    check_in_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_1').text
    logging.debug("check_in_date_month: " + check_in_date_month)
    
    check_in_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_1').text
    logging.debug("check_in_date_day: " + check_in_date_day)
    
    check_out_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_2').text
    logging.debug("check_out_date_month: " + check_out_date_month)
    
    check_out_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_2').text
    logging.debug("check_out_date_day: " + check_out_date_day)

    context.check_in_date = _parse_date(check_in_date_month+check_in_date_day+u'日')
    logging.info("context.check_in_date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(check_out_date_month+check_out_date_day+u'日')
    logging.info("context.check_out_date: " + str(context.check_out_date))
    
    context.testStep.tap_widget('com.ziipin.homeinn:id/n_date_layout')
    
@when(u'用户点击酒店详情页入店离店时间')
def step_impl(context):
    check_in_date = context.testStep.has_widget('com.ziipin.homeinn:id/start_date').text
    logging.debug("check_in_date: " + check_in_date)
    
    check_out_date = context.testStep.has_widget('com.ziipin.homeinn:id/end_date').text
    logging.debug("check_out_date: " + check_out_date)

    context.check_in_date = _parse_date(check_in_date)
    logging.info("context.check_in_date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(check_out_date)
    logging.info("context.check_out_date: " + str(context.check_out_date))
    
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_date")
        
@when(u'用户选择搜索结果中第一个地点')
def step_impl(context):
    result_type_widget = context.testStep.has_widget("com.ziipin.homeinn:id/type_text")
    result_type_widget_text = result_type_widget.text
    logging.debug("result_type_widget_text:%s", result_type_widget_text)
    result_widget = context.testStep.has_widget("com.ziipin.homeinn:id/area_text")
    result_widget_text = result_widget.text
    logging.debug("result_widget_text:%s", result_widget_text)
    
    if not result_type_widget_text==u'地点':
        found = False
    else:
        found = True

    
    while (found==False):
        next_result_type_widget = context.testStep.has_widget("com.ziipin.homeinn:id/type_text", 
        context.testStep._under(result_widget_text))
        next_result_type_widget_text = next_result_type_widget.text
        logging.debug("next_result_type_widget_text:%s", next_result_type_widget_text)
        result_widget = context.testStep.has_widget("com.ziipin.homeinn:id/area_text", 
        context.testStep._under(result_widget_text))
        result_widget_text = result_widget.text
        logging.debug("result_widget_text:%s", result_widget_text)
        
        if not next_result_type_widget_text==u'地点':
            found = False
            context.testStep._swipe_to_distination_half_by_half(next_result_type_widget,\
            result_type_widget, "bottom2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        result_widget_text = result_widget_text
        result_type_widget = next_result_type_widget

    context.destination_key_word = result_widget_text
    logging.info("destination_key_word:%s", context.destination_key_word)
    context.testStep.tap_widget(result_type_widget)
        
@when(u'用户选择搜索结果中第一个酒店')
def step_impl(context):
    result_type_widget = context.testStep.has_widget("com.ziipin.homeinn:id/type_text")
    result_type_widget_text = result_type_widget.text
    logging.debug("result_type_widget_text:%s", result_type_widget_text)
    result_widget = context.testStep.has_widget("com.ziipin.homeinn:id/area_text")
    result_widget_text = result_widget.text
    logging.debug("result_widget_text:%s", result_widget_text)
    
    if not result_type_widget_text==u'酒店':
        found = False
    else:
        found = True

    
    while (found==False):
        next_result_type_widget = context.testStep.has_widget("com.ziipin.homeinn:id/type_text", 
        context.testStep._under(result_widget_text))
        next_result_type_widget_text = next_result_type_widget.text
        logging.debug("next_result_type_widget_text:%s", next_result_type_widget_text)
        result_widget = context.testStep.has_widget("com.ziipin.homeinn:id/area_text", 
        context.testStep._under(result_widget_text))
        result_widget_text = result_widget.text
        logging.debug("result_widget_text:%s", result_widget_text)
        
        if not next_result_type_widget_text==u'酒店':
            found = False
            context.testStep._swipe_to_distination_half_by_half(next_result_type_widget,\
            result_type_widget, "bottom2top")
            logging.debug("not found")
        else:
            found = True
            logging.debug("found")
        
        result_widget_text = result_widget_text
        result_type_widget = next_result_type_widget

    context.hotel = result_widget_text
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    logging.info("context.hotel:%s", context.hotel)
    context.testStep.tap_widget(result_type_widget)
    
@when(u'用户点击关键词搜索')
def step_impl(context):
    key_word_widget = context.testStep.has_widget("com.ziipin.homeinn:id/n_main_key_text")
    context.destination_key_word = key_word_widget.text
    logging.debug("context.destination_key_word:%s", context.destination_key_word)
    context.testStep.tap_widget(key_word_widget)
    
@when(u'用户选择列表中第一个{area}')
def step_impl(context, area):
    district_widget = context.testStep.has_widget("com.ziipin.homeinn:id/area_text")
    context.destination_key_word = district_widget.text
    logging.debug("context.destination_key_word:%s", context.destination_key_word)
    context.testStep.tap_widget(district_widget)
    
@when(u'用户选择列表中中间一个{area}')
def step_impl(context, area):
    district_widgets = context.testStep.has_widgets("com.ziipin.homeinn:id/area_text")
    context.destination_key_word = district_widgets[int(len(district_widgets)/2)-1].text
    logging.debug("context.destination_key_word:%s", context.destination_key_word)
    context.testStep.tap_widget(district_widgets[int(len(district_widgets)/2)-1])
    
@when(u'用户选择列表中最后一个{area}')
def step_impl(context, area):
    district_widgets = context.testStep.has_widgets("com.ziipin.homeinn:id/area_text")
    district_widget_text = district_widgets[0].text
    
    result_list_widget = context.testStep.has_widget("com.ziipin.homeinn:id/result_list")
    bottom = False
    
    while (bottom==False):
        context.testStep._swipe_to_distination_half_by_half(result_list_widget, result_list_widget, "bottom2top")
        district_widgets = context.testStep.has_widgets("com.ziipin.homeinn:id/area_text")
        logging.debug("district_widget_text:%s", district_widget_text)
        logging.debug("district_widgets[0].text:%s", district_widgets[0].text)
        
        if district_widget_text==district_widgets[0].text:
            bottom = True
        else:
            district_widget_text = district_widgets[0].text
            
    context.destination_key_word = district_widgets[len(district_widgets)-1].text
    logging.debug("context.destination_key_word:%s", context.destination_key_word)
    context.testStep.tap_widget(district_widgets[len(district_widgets)-1])
    

@when(u'用户滑动列表直到有“{brand}”品牌并选择')
def step_impl(context, brand):
    try:
        widget = context.testStep.has_widget(brand)
    except NoSuchElementException:
        found = False
    else:
        found = True
        
    bottom = False
    brand_widget_text = None

    checker_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
    brand_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/brand_name_text')
    
    while (found==False) and (bottom==False):

        logging.debug("brand_widget_text:%s", brand_widget_text)
        logging.debug("len(brand_widgets):%d", len(brand_widgets))
        logging.debug("brand_widgets[0].text:%s", brand_widgets[0].text)
        
        if brand_widget_text==brand_widgets[0].text:
            bottom = True
        else:
            brand_widget_text = brand_widgets[0].text
        
        context.testStep._swipe_to_distination_half_by_half(checker_widgets[len(checker_widgets)-1], checker_widgets[0], "bottom2top")
        try:
            widget = context.testStep.has_widget(brand)
        except NoSuchElementException:
            found = False
            checker_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
            brand_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/brand_name_text')
        else:
            found = True
        
    if found==True:
        found = False
        i = 0
    
        while (found==False):
            logging.debug("checker_widgets[i].location.get('y'): " + str(checker_widgets[i].location.get('y')))
        
            if widget.location.get('y')<checker_widgets[i].location.get('y')+checker_widgets[i].size['height']\
            and widget.location.get('y')+widget.size['height']>checker_widgets[i].location.get('y'):
                found = True
                if checker_widgets[i].get_attribute('checked')=='false':
                    context.testStep.tap_widget(widget)
            else:
                i = i + 1
                logging.debug("i: %d", i)
            
    else:
        assert False



@when(u'用户滑动列表并点击所有品牌')
def step_impl(context):
    found = False
    bottom = False
    brand_widget_text = None
    
    while (found==False) and (bottom==False):
        checker_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
        brand_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/brand_name_text')

        logging.debug("len(checker_widgets):%d", len(checker_widgets))
        logging.debug("len(brand_widgets):%d", len(brand_widgets))
        logging.debug("brand_widget_text:%s", brand_widget_text)
        logging.debug("brand_widgets[0].text:%s", brand_widgets[0].text)
        
        if brand_widget_text==brand_widgets[0].text:
            bottom = True
        else:
            brand_widget_text = brand_widgets[0].text
        
            for i in range(len(checker_widgets)):
                logging.debug("i: %d", i)
                logging.debug("brand_widgets[%s].text:%s", i, brand_widgets[i].text)
                if checker_widgets[i].get_attribute('checked')=='false':
                    logging.debug("tap checker_widgets[%s]", i)
                    context.testStep.tap_widget(checker_widgets[i])
        
            context.testStep._swipe_to_distination_half_by_half(checker_widgets[len(checker_widgets)-1], checker_widgets[0], "bottom2top")
    

@when(u'用户划动右则字母控件，从顶划到n字')
def step_impl(context):
    list_sider_widget = context.testStep.has_widget('com.ziipin.homeinn:id/list_sider')
    context.testStep.swipe_widget('com.ziipin.homeinn:id/list_sider', "middle", 1, "middle", "middle")
    
    
@when(u'用户执行取消订单等一系列动作')
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
    ''')
    

@when(u'用户执行修改入住日期为“{checkin}”，离店日期为“{checkout}”等一系列动作')
def step_impl(context, checkin, checkout):
    if context.check_in_out_right == False:
        context.execute_steps(u'''
            当      用户点击过夜房入住离店日期
    ###############选择入住时间界面################################
            那么    掌上如家跳转到选择入住时间界面
            而且    掌上如家有“可选择90天内日期”提示
            而且    掌上如家有“完成”按键
            当      用户点击入住日期为“'''+checkin+u'''”
            那么    掌上如家入住日期显示为“'''+checkin+u'''”
            当      用户点击离店日期为“'''+checkout+u'''”
    ##########################################################
        ''')
        
@when(u'用户执行选择第一个不是已满的酒店，选择第一个不是已满的房型，提交订单等一系列动作')
def step_impl(context):
    context.execute_steps(u'''
		当      用户选择第一个不是已满的酒店
#--------------酒店详情界面------------------------------------#
        那么    掌上如家跳转到选房预订界面
        而且    掌上如家有房型列表
		当      用户展开第一个不是已满的房型
        那么    掌上如家房型会有“门市价”控件
        当      用户划动第一个不是已满的房型到最顶
        那么    掌上如家房型会有“会员价”控件
        而且    掌上如家房型会有“预订”按钮
        当      用户点击“预订”按钮
#--------------提交订单界面-----------------------------------#
        那么    掌上如家跳转到“提交订单”界面
		当      用户点击“提交订单”按钮
    ''')
    

@when(u'用户执行选择第一个不是已满的房型，提交订单等一系列动作')
def step_impl(context):
    context.execute_steps(u'''
#--------------酒店详情界面------------------------------------#
        那么    掌上如家跳转到选房预订界面
        而且    掌上如家有房型列表
		当      用户展开第一个不是已满的房型
        那么    掌上如家房型会有“门市价”控件
        当      用户划动第一个不是已满的房型到最顶
        那么    掌上如家房型会有“会员价”控件
        而且    掌上如家房型会有“预订”按钮
        当      用户点击“预订”按钮
#--------------提交订单界面-----------------------------------#
        那么    掌上如家跳转到“提交订单”界面
		当      用户点击“提交订单”按钮
    ''')
    
@then(u'掌上如家“当前位置”为“{widget_text}”')
def step_impl(context, widget_text):
    element = context.testStep.has_widget(widget_text, context.testStep._under('当前位置'))
    context.element = element
    
@then(u'掌上如家“最近选择”不为空')
def step_impl(context):
    context.testStep.has_widget('最近选择')
    context.testStep.has_widget('com.ziipin.homeinn:id/city_text',\
    context.testStep._under('最近选择')+context.testStep._above('热门城市'))
    
@then(u'掌上如家“最近选择”为空')
def step_impl(context):
    try:
        context.testStep.has_widget('最近选择')
    except NoSuchElementException:
        pass
    else:
        assert False
    
@then(u'掌上如家“当前位置”不为“{widget_text}”')
def step_impl(context, widget_text):
    element = context.testStep.has_widget("com.ziipin.homeinn:id/city_text")
    logging.debug("current_pos:%s", element.text)
    if not element.text==widget_text:
        pass
    else:
        raise Exception
    
@then(u'掌上如家城市显示为“{widget_text}”')
def step_impl(context, widget_text):
    current_city = context.testStep.has_widget("com.ziipin.homeinn:id/city_layout")
    current_city.find_element_by_string(widget_text)

@then(u'掌上如家“{roomtype}”页面有“{keyword}”条件')
def step_impl(context, roomtype, keyword):
    context.testStep.wait_widget(roomtype)
    context.testStep.wait_widget(keyword)

@then(u'掌上如家{verb}选择入住时间界面')
def step_impl(context, verb):
    today = datetime.date.today()
    context.testStep.wait_widget('选择入住时间')
    context.testStep.wait_widget('离店')
        
@then(u'掌上如家入住日期显示为“{checkin}”')
def step_impl(context, checkin):
    context.testStep.wait_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview = context.testStep.has_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview.text.find(str(context.check_in_date.month)+u"月")
    checkinview.text.find(str(context.check_in_date.day)+u"日")
    
@then(u'掌上如家离店日期显示为“请选择离店时间”')
def step_impl(context):
    checkoutview = context.testStep.has_widget("com.ziipin.homeinn:id/end_date_tab")
    if checkoutview.text.find(u'请选择离店时间')==-1:
        assert False
    else:
        pass

@then(u'掌上如家“过夜房”页面显示为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    context.check_in_date = _parse_date(checkin)
    logging.info("check in date: " + str(context.check_in_date))
    context.check_out_date = _parse_date(checkout)
    logging.info("check out date: " + str(context.check_out_date))

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
    
@then(u'掌上如家跳转到选房预订界面')
def step_impl(context):
    try:
        context.testStep.wait_widget(context.hotel)
    except NoSuchElementException:
        context.testStep.wait_widget((context.hotel)[0:9])

@then(u'掌上如家关键词搜索列表显示“{hotel}”')
def step_impl(context, hotel):
    try:
        hotel_widget = context.testStep.has_widget(hotel)
    except NoSuchElementException:
        hotel_widget = context.testStep.has_widget(hotel[0:9])
    context.hotel = hotel  
    # remove brand of full hotel name
    context.hotel = context.hotel[context.hotel.find('-')+1:len(context.hotel)]
    
@then(u'掌上如家的“{widget_text}”为灰色不可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="false":
        pass
    else:
        raise Exception
    
    
@then(u'掌上如家的“{widget_text}”为可用')
def step_impl(context, widget_text):
    button_widget = context.testStep.has_widget(widget_text)
    
    if button_widget.get_attribute('clickable')=="true":
        pass
    else:
        raise Exception  
        
@then(u'掌上如家品牌列表的“{widget_text}”右方圆圈为已勾选')
def step_impl(context, widget_text):
    found = False
    i = 0
    brand_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
    button_widget = context.testStep.has_widget(widget_text)
    
    while (found==False):
        logging.debug("button_widget.location.get('y'): " + str(button_widget.location.get('y')))
        logging.debug("brand_widgets[i].location.get('y')+brand_widgets[i].size['height']: " \
        + str(brand_widgets[i].location.get('y')+brand_widgets[i].size['height']))
        logging.debug("button_widget.location.get('y')+button_widget.size['height']: " \
        + str(button_widget.location.get('y')+button_widget.size['height']))
        logging.debug("brand_widgets[i].location.get('y'): " + str(brand_widgets[i].location.get('y')))
        
        if button_widget.location.get('y')<brand_widgets[i].location.get('y')+brand_widgets[i].size['height']\
        and button_widget.location.get('y')+button_widget.size['height']>brand_widgets[i].location.get('y'):
            found = True
        else:
            i = i + 1
            logging.debug("i: %d", i)
    
    if brand_widgets[i].get_attribute('checked')=="true":
        pass
    else:
        raise Exception 

@then(u'掌上如家品牌列表所有品牌为不可用，全部为可用')
def step_impl(context):
    top = False
    checker_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
    brand_widget = context.testStep.has_widget('com.ziipin.homeinn:id/brand_name_text')
    brand_widget_text = brand_widget.text
    logging.debug("brand_widget_text: %s", brand_widget_text)
    
    while (top==False):
        if brand_widget_text==u'全部品牌':
            if checker_widgets[0].get_attribute('checked')=="false":
                raise Exception
                
            i = 1                
            logging.debug("i: %d", i)
            while i<len(checker_widgets):
                if checker_widgets[i].get_attribute('checked')=="true":
                    raise Exception
                i += 1
        else:
            for i in range(len(checker_widgets)):
                logging.debug("i: %d", i)
                if checker_widgets[i].get_attribute('checked')=="true":
                    raise Exception
                    

        logging.debug("_swipe_to_distination_half_by_half")
        context.testStep._swipe_to_distination_half_by_half(checker_widgets[0]\
        , checker_widgets[len(checker_widgets)-1], "top2bottom")
        
        checker_widgets = context.testStep.has_widgets('com.ziipin.homeinn:id/checker')
        if brand_widget_text==brand_widget.text:
            top = True
        else:
            brand_widget_text = brand_widget.text
            logging.debug("brand_widget_text: %s", brand_widget_text)
    
    
        

@then(u'掌上如家订单的入住日期为“{checkin}”，离店日期为“{checkout}”')
def step_impl(context, checkin, checkout):
    check_in_date = _parse_date(checkin)
    logging.debug("check in date: " + str(check_in_date))
    check_out_date = _parse_date(checkout)
    logging.debug("check out date: " + str(check_out_date))
    context.testStep.has_widget('入住 '+str(check_in_date)+' / 离店 '+str(check_out_date))
    

@then(u'掌上如家“过夜房”页面入住和离店日期显示为原来的日期')
def step_impl(context):
    check_in_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_1').text
    logging.debug("check_in_date_month: " + check_in_date_month)
    
    check_in_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_1').text
    logging.debug("check_in_date_day: " + check_in_date_day)
    
    check_out_date_month = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_month_2').text
    logging.debug("check_out_date_month: " + check_out_date_month)
    
    check_out_date_day = context.testStep.has_widget('com.ziipin.homeinn:id/n_date_day_2').text
    logging.debug("check_out_date_day: " + check_out_date_day)

    check_in_date = _parse_date(check_in_date_month+check_in_date_day+u'日')
    logging.info("check_in_date: " + str(check_in_date))
    check_out_date = _parse_date(check_out_date_month+check_out_date_day+u'日')
    logging.info("check_out_date: " + str(check_out_date))
    logging.info("context.check_in_date: " + str(context.check_in_date))
    logging.info("context.check_out_date: " + str(context.check_out_date))
    
    if context.check_in_date==check_in_date and context.check_out_date==check_out_date:
        pass
    else:
        assert False
    
@then(u'掌上如家离店日期显示“{widget_text}”')
def step_impl(context, widget_text):
    widget = context.testStep.has_widget('com.ziipin.homeinn:id/end_date_tab')
    if widget.text.find(widget_text)==-1:
        assert False
        
@when(u'用户选择第一个周边商户的“去这里”按钮')
def step_impl(context):
    context.testStep.tap_widget('com.ziipin.homeinn:id/near_layout')
    context.testStep.tap_widget('去这里')
    
######################wait_widget############################################
@then(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@given(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@when(u'掌上如家{verb}“{widget_text}”页面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@then(u'掌上如家{verb}“{widget_text}”界面')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)

@then(u'掌上如家{verb}“{widget_text}”提示')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text)

@then(u'掌上如家{verb}“{widget_text}”按键')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@then(u'掌上如家{verb}“{widget_text}”按钮')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@then(u'掌上如家{verb}“{widget_text}”控件')
def step_impl(context, verb, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
    
@given(u'掌上如家有去选房控件')
def step_impl(context):
    try:
        context.testStep.wait_widget('去选房', 5, 1, True)
        context.select_room = None
    except:
        pass
    
@then(u'掌上如家跳转到地图选择酒店界面')
def step_impl(context):
    context.testStep.wait_widget(context.city)
    
@then(u'掌上如家提示“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text)
    
@then(u'掌上如家有“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.wait_widget(widget_text, 30, 1, True)
        
@then(u'掌上如家页面有酒店列表')
def step_impl(context):
    context.testStep.wait_widget("com.ziipin.homeinn:id/text_hotel_name", 30, 1, True)

@then(u'掌上如家有房型列表')
def step_impl(context):
    try:
        context.testStep.wait_widget("com.ziipin.homeinn:id/room_info_layout", 30, 1, True)
    except TimeoutException:
        context.testStep.swipe_up_and_retry('您的网络好像不太给力，请稍后再试', '点击重试')
        context.testStep.wait_widget("com.ziipin.homeinn:id/room_info_layout")
    
@then(u'掌上如家有收藏酒店列表')
def step_impl(context):
    context.testStep.wait_widget("com.ziipin.homeinn:id/favorite_list", 30, 1, True)
        
@then(u'掌上如家出现选择优惠券界面')
def step_impl(context):
    if not (context.coupon == None):
        context.testStep.wait_widget('选择优惠券')
    
@then(u'掌上如家有预订酒店名')
def step_impl(context):
    logging.debug("context.hotel: " + context.hotel)
    context.testStep.wait_widget(context.hotel, 5)

@then(u'掌上如家有预订房型')
def step_impl(context):
    logging.debug("context.room_type: " + context.room_type)
    context.testStep.wait_widget(context.room_type, 5)

@then(u'掌上如家有搜索结果')
def step_impl(context):
    context.testStep.wait_widget('com.ziipin.homeinn:id/area_text', 5)

@then(u'掌上如家“过夜房”页面有{area}的条件')
def step_impl(context, area):
    context.testStep.wait_widget(context.destination_key_word, 5)
        
@then(u'掌上如家“过夜房”页面的品牌不变')
def step_impl(context):
    context.testStep.wait_widget(context.brand, 5)
            
@then(u'掌上如家出现通讯录界面')
def step_impl(context):
    context.testStep.wait_widget('选择联系人', 5)
    context.testStep.tap_permision_widget("accept")          
            
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
    my_account_widget = context.testStep.has_widget('我的')
    
    if my_account_widget.get_attribute('checked')=="true":
        pass
    else:
        assert False
        
@then(u'掌上如家“最近选择”有四个城市')
def step_impl(context):
    elements = context.testStep.has_widgets('//android.widget.TextView[@text]',\
    context.testStep._under('最近选择')+context.testStep._above('热门城市'))
    logging.debug('len(elements):%d', len(elements))
    for i in range(len(elements)):
        logging.debug('city:%s', elements[i].text)
        
    if len(elements)==4:
        pass
    else:
        assert False
        
@then(u'掌上如家“最近选择”少于四个城市')
def step_impl(context):
    elements = context.testStep.has_widgets('//android.widget.TextView[@text]',\
    context.testStep._under('最近选择')+context.testStep._above('热门城市'))
        
    if len(elements)<4:
        pass
    else:
        assert False
        
@then(u'掌上如家过夜房页面城市条件为“{city}”')
def step_impl(context, city):
    city_widget = context.testStep.has_widget('com.ziipin.homeinn:id/n_main_city_text')
    context.city = city_widget.text
    assert (context.city==city)
    
@then(u'掌上如家出现周边地图')
def step_impl(context):
    context.testStep.wait_widget('com.ziipin.homeinn:id/map_view')

@then(u'掌上如家有周边列表')
def step_impl(context):
    context.testStep.wait_widget('com.ziipin.homeinn:id/near_list')
    
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

@then(u'掌上如家“过夜房”页面的品牌为')
def step_impl(context):
    context.brand = None
    for row in context.table:
        logging.debug(row['brand'])
        context.testStep.wait_widget(row['brand'])
        if context.brand==None:
            context.brand = row['brand']
        else:
            context.brand = context.brand + ',' + row['brand']
            
@then(u'掌上如家城市列表有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['city'])
        context.testStep.wait_widget(row['city'])
        
@then(u'掌上如家“导航”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['navigation'])
        context.testStep.wait_widget(row['navigation'])
        
@then(u'掌上如家“到店时间”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['arrival'])
        context.testStep.wait_widget(row['arrival'])
        
@then(u'掌上如家“偏好选择”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['peference'])
        context.testStep.wait_widget(row['peference'])
    
########################tap_widget#####################################
@when(u'用户点击城市')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/n_main_city_text")

@when(u'用户点击“{widget_text}”')
def step_impl(context, widget_text):
    #context.testStep.click_widget(widget_text)
    context.testStep.tap_widget(widget_text)

@when(u'用户点击“{widget_text}”页面')
def step_impl(context, widget_text):
    context.testStep.tap_widget(widget_text)

@when(u'用户点击“{widget_text}”按键')
def step_impl(context, widget_text):
    widget = context.testStep.has_widget("//android.widget.Button[@text='"+widget_text+"']")
    context.testStep.tap_widget(widget)

@when(u'用户点击“{widget_text}”按钮')
def step_impl(context, widget_text):
    widget = context.testStep.has_widget("//android.widget.Button[@text='"+widget_text+"']")
    context.testStep.tap_widget(widget)

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
    
@when(u'用户点击城市列表中的“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget("//android.widget.TextView[@text='"+widget_text+"']")
    
@when(u'用户点击城市列表中“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget("//android.widget.TextView[@text='"+widget_text+"']")

@when(u'用户点击搜索列表中“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget("//android.widget.TextView[@text='"+widget_text+"']")
    
@when(u'用户点击热门城市里的“{widget_text}”')
def step_impl(context, widget_text):
    element = context.testStep.has_widget(widget_text, context.testStep._under('热门城市'))
    context.testStep.tap_widget(element)
    
@when(u'用户点击当前位置里的城市')
def step_impl(context):
    element = context.testStep.has_widget('//android.widget.TextView[@text]',\
    context.testStep._under('当前位置')+context.testStep._above('热门城市'))
    context.testStep.tap_widget(element)
    
@when(u'用户点击最近选择里的城市')
def step_impl(context):
    element = context.testStep.has_widget('//android.widget.TextView[@text]',\
    context.testStep._under('最近选择')+context.testStep._above('热门城市'))
    context.testStep.tap_widget(element)
    
@when(u'用户点击电子券')
def step_impl(context):
    if not (context.coupon==None):
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
    
@when(u'用户点击去选房')
def step_impl(context):
    try:
        if (context.select_room == None):
            context.testStep.tap_widget('去选房')
    except:
        pass

@when(u'用户选择搜索结果中第一个结果')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/area_text")
    
@when(u'用户点击过夜房页面品牌筛选')
def step_impl(context):
    brand_widget = context.testStep.has_widget("com.ziipin.homeinn:id/n_main_brand_text")
    context.brand = brand_widget.text
    context.testStep.tap_widget(brand_widget)
    

@when(u'用户点击立即预订')
def step_impl(context):
    context.city = context.testStep.has_widget('com.ziipin.homeinn:id/n_main_city_text').text
    context.testStep.tap_widget("com.ziipin.homeinn:id/n_search_start_btn")
    
    