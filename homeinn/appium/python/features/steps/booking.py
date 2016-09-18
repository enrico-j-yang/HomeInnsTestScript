
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
    

@then(u'“品牌”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['brand'])
        #context.testStep.wait_widget("//*[@text='"+row['brand']+"']")
        context.testStep.wait_widget("//*[contains(@text, '"+row['brand']+"')]")

@then(u'掌上如家出现选择酒店页面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '查看地图')]")
    context.testStep.wait_widget("//*[contains(@text, '排序')]")
    context.testStep.wait_widget("//*[contains(@text, '品牌')]")
    context.testStep.wait_widget("com.ziipin.homeinn:id/text_hotel_name")



@when(u'用户点击定位城市')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/top_title")

@when(u'用户点击返回')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/back_btn")

@when(u'用户点击查看地图')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/right_btn")

@when(u'用户点击立即预定')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/search_start_btn")

@when(u'用户点击当前位置')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/type_layout")

@when(u'用户点击排序')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/sort_layout")

@when(u'用户点击品牌')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/brand_layout")

@when(u'用户点击筛选')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/filter_layout")

@then(u'“排序”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['rank'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['rank']+"')]")

@then(u'“筛选”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['select'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['select']+"')]")

@when(u'用户点击分享')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/share_btn")

@then(u'“分享酒店”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['share'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['share']+"')]")

@when(u'用户点击收藏')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/favorite_btn")


@when(u'用户点击图片')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_photo")


@when(u'用户点击关闭')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/close_btn")

@when(u'用户点击酒店详情')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_info_layout")

@when(u'用户点击增值服务')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_service_layout")

@when(u'用户点击地址')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/detail_address_layout")

@then(u'掌上如家出现选择地图导航页面')
def step_impl(context):
    context.testStep.wait_widget("//*[contains(@text, '导航')]")

@when(u'用户点击拨打电话')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/tell_btn")

@when(u'用户点击预定')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/normal_book_btn")

@when(u'用户点击常住联系人')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/order_contact_btn")

@when(u'用户点击明细')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/price_detail_tag")

@when(u'用户点击提交订单')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/commit_order_btn")

@when(u'用户点击第一个酒店')
def step_impl(context):
    context.testStep.tap_widget("com.ziipin.homeinn:id/text_hotel_name")

#@then(u'检查酒店显示是否正确')
#def step_impl(context):
    #hotel_element = context.testStep.find_element_by_id("com.ziipin.homeinn:id/order_hotel_name")
    #hotel_name = hotel_element.getText()
    #if :
        
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


@then(u'填写订单页面向下滑动')
def step_imp(context):
    start_p = context.testStep.has_widget("//android.widget.TextView[@text='信用住，先住后付']")
    end_p = context.testStep.has_widget("com.ziipin.homeinn:id/order_hotel_name")
    context.testStep._swipe_to_distination_half_by_half(start_p, end_p)

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

@then(u'“选择出行目的”页面内有')
def step_impl(context):
    for row in context.table:
        logging.debug(row['target'])
        context.testStep.wait_widget("//*[contains(@text, '"+row['target']+"')]")

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

#@then(u'检查酒店')
#def step_imp(context):
    #org_text = '如家-广州琶洲会展中心琶洲地铁站店'
    #element_text = context.testStep.has_widget("com.ziipin.homeinn:id/order_hotel_name").text
    #count = 2
    #if count > 1 :
        #print element_text
    #else :
        #logging.error("string is wrong")

    