
# -*- coding: utf-8 -*-


import os
import sys
from time import sleep
import time
import datetime
import logging

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

@when(u'用户启动掌上如家')
def step_impl(context):
    el = context.testStep.driver.start_activity('com.ziipin.homeinn', '.activity.SplashActivity')
    assert el

@then(u'掌上如家会出现')
def step_impl(context):
    # wait for startshow activity
    if context.testStep.wait_window('.activity.StartShowActivity'):
        finish = False
        while not (finish):
            try:
                context.testStep.has_widget("com.ziipin.homeinn:id/start_use_btn")
            except Exception:
                context.testStep.driver.swipe(600,486, 98,489, 500)
            else:
                finish = True
        
        start = context.testStep.has_widget("com.ziipin.homeinn:id/start_use_btn")
        assert start
        context.touchAction.press(start).release().perform()
    else:
        logging.debug("*****wait for startshow activity time out*****")   
    
    # wait for main activity
    if context.testStep.wait_window('.activity.MainActivity'):
        logging.debug("*****main activity OK*****")
    else:
        logging.debug("*****wait for main activity time out*****")

    assert ('.activity.MainActivity' == context.testStep.current_window())
    context.testStep.tap_permision_widget("accept")
    
@then(u'掌上如家出现“{widget_text}”页面')
def step_impl(context, widget_text):
    context.testStep.wait_widget("//*[@text='"+widget_text+"']")
    
@then(u'掌上如家出现“{widget_text}”界面')
def step_impl(context, widget_text):
    context.testStep.wait_widget("//*[@text='"+widget_text+"']")

@then(u'页面有“{widget_text}”提示')
def step_impl(context, widget_text):
    context.testStep.wait_widget("//*[@text='"+widget_text+"']")

@then(u'页面有“{widget_text}”按键')
def step_impl(context, widget_text):
    context.testStep.wait_widget("//*[@text='"+widget_text+"']")

@then(u'掌上如家跳转到“{widget_text}”页面')
def step_impl(context, widget_text):
    context.testStep.wait_widget("//*[@text='"+widget_text+"']")
    
@when(u'用户点击城市')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/city_layout")
    
@when(u'用户点击“入住”日期')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/date_layout")

@when(u'用户点击“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.tap_widget("//*[@text='"+widget_text+"']")

@when(u'用户点击“{widget_text}”页面')
def step_impl(context, widget_text):
    context.testStep.tap_widget("//*[@text='"+widget_text+"']")

@given(u'“{current_pos}”为“{widget_text}”')
def step_impl(context, current_pos, widget_text):
    
    element = context.testStep.has_widget("//*[@text='"+widget_text+"']", context.testStep._under(current_pos)+context.testStep._above("最近选择"))
    #element = context.testStep.has_widget("//*[@text='"+widget_text+"']", context.testStep._near(current_pos))
    context.element = element

@when(u'用户点击以上的“{widget_text}”')
def step_impl(context, widget_text):
    context.testStep.touchAction.press(context.element).release().perform()
    #assert False
    
@then(u'城市显示为“{widget_text}”')
def step_impl(context, widget_text):
    current_city = context.testStep.has_widget("com.ziipin.homeinn:id/city_layout")
    current_city.find_element_by_string("//*[@text='"+widget_text+"']")
    
@given(u'当前时间超过{hour}点')
def step_impl(context, hour):
    logging.debug("%s", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    if (time.struct_time.tm_hour>12 or (time.struct_time.tm_hour==12 and time.struct_time.tmmin>0)):
        pass
    else:
        assert False


@then(u'掌上如家有“{district}”、“{circle}”和“{subway}”三个页面')
def step_impl(context, district, circle, subway):
    context.testStep.wait_widget("//*[@text='"+district+"']")
    context.testStep.wait_widget("//*[@text='"+circle+"']")
    context.testStep.wait_widget("//*[@text='"+subway+"']")

@then(u'“行政区”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['district'])
        context.testStep.wait_widget("//*[@text='"+row['district']+"']")
    
@then(u'“商圈”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['area'])
        context.testStep.wait_widget("//*[@text='"+row['area']+"']")

@then(u'“地铁”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['subway'])
        context.testStep.wait_widget("//*[@text='"+row['subway']+"']")
        
@then(u'“{roomtype}”页面有“{keyword}”条件')
def step_impl(context, roomtype, keyword):
    context.testStep.wait_widget("//*[@text='"+roomtype+"']")
    context.testStep.wait_widget("//*[@text='"+keyword+"']")

@then(u'掌上如家跳转到“{widget_text}”界面')
def step_impl(context, widget_text):
    today = datetime.date.today()
    context.testStep.wait_widget("//*[contains(@text, '"+widget_text+"')]")
    context.testStep.wait_widget("//*[contains(@text, '离店')]")
    logging.debug("//*[contains(@text, '"+str(today.year)+"年"+str(today.month)+"月')]")
    
    context.testStep.wait_widget("//*[contains(@text, '"+str(today.year)+"年"+str(today.month)+"月')]")

    
@when(u'用户点击入住日期为“{checkin}”')
def step_impl(context, checkin):
    context.check_in_date = _parse_date(checkin)
    context.testStep.tap_date_in_calendar(context.check_in_date)
        
@then(u'入住日期显示为“{checkin}”')
def step_impl(context, checkin):
    context.testStep.wait_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview = context.testStep.has_widget("com.ziipin.homeinn:id/start_date_tab")
    checkinview.text.find(str(context.check_in_date.month)+u"月")
    checkinview.text.find(str(context.check_in_date.day)+u"日")

@when(u'用户点击离店日期为“{checkout}”')
def step_impl(context, checkout):
    context.check_out_date = _parse_date(checkout)
    context.testStep.tap_date_in_calendar(context.check_out_date)

@then(u'“过夜房”页面显示为“{checkin}”入住，“{checkout}”离店')
def step_impl(context, checkin, checkout):
    context.check_in_date = _parse_date(checkin)
    context.check_out_date = _parse_date(checkout)

    date_layout = context.testStep.has_widget("com.ziipin.homeinn:id/date_layout")
    date_layout.find_element_by_string("//*[@text='"+str(context.check_in_date.month)+"月']")
    date_layout.find_element_by_string("//*[@text='"+str(context.check_out_date.month)+"月']")
    date_layout.find_element_by_string("//*[@text='"+str(context.check_in_date.day)+"']")
    date_layout.find_element_by_string("//*[@text='"+str(context.check_out_date.day)+"']")
    
@then(u'“品牌”界面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['brandselection'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['brandselection']+"')]")

@then(u'掌上如家跳转到选择酒店界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '排序')]")
    context.testStep.wait_widget("//*[contains(@text, '品牌')]")
    context.testStep.wait_widget("//*[contains(@text, '筛选')]")
    context.testStep.wait_widget("//*[contains(@text, '查看地图')]")

@then(u'“品牌”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['brand'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['brand']+"')]")

@then(u'“筛选”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['filter'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['filter']+"')]")

@then(u'“排序”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['sort'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['sort']+"')]")

@when(u'用户点击”查看地图“')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/right_btn")

@then(u'选择酒店界面跳转到地图选房界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '全部')]")

@when(u'用户返回选择酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户选择第一个酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/text_hotel_name")

@then(u'选择酒店界面跳转到选房预订界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '详情')]")
    context.testStep.wait_widget("//*[contains(@text, '预订')]")

@when(u'用户点击”详情“')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/room_detail_tag")

@when(u'用户点击”返回“')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户点击收藏')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/favorite_btn")

@when(u'用户点击酒店详情')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_info_layout")

@then(u'选房预订界面跳转到”酒店详情“界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '酒店详情')]")

@when(u'用户点击分享酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/share_btn")

@then(u'”酒店详情“界面出现”分享酒店“界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '分享酒店')]")

@when(u'用户点击”完成“')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/btn_done")

@when(u'用户返回选择酒店界面')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户点击酒店地址')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/hotel_address_text")

@then(u'选房预订界面跳转到导航界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '导航')]")

@when(u'用户返回到选房预订界面')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户点击电话按钮')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/tell_btn")

@when(u'用户返回选房预订界面')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户点击入店和离店时间')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_date")

@then(u'选房预订界面出现“选择入住时间”界面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '完成')]")
    context.testStep.wait_widget("//*[contains(@text, '入住')]")
    context.testStep.wait_widget("//*[contains(@text, '离店')]")

@when(u'用户点击“完成”按钮')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/btn_done")

@when(u'用户选择房型')
def step_impl(context):
    start_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_info_layout")
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)
    if 

@when(u'用户点击“预订”按钮')
def step_impl(context):
    start_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_info_layout")
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/room_title_layout")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)
    
    day_widget = context.testStep.has_widget("//android.widget.Button",
                                             context.testStep._under("特惠商务房")+
                                             context.testStep._above("特惠双床房")+
                                             context.testStep._right("会员价"))






