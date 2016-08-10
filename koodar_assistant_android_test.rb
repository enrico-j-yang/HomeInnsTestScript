# this test show you how to test koodar assistant
# it log in assistant by inputing user name and its password
# author: enrico yang
#
# run using:
# ruby koodar assistant.rb

require 'appium_lib'
require 'test/unit'
require 'rubygems'

class KoodarAssistantTest < Test::Unit::TestCase
  
  def setup
    caps   = { caps:       { platformName: 'Android', deviceName: 'Android Machine', appActivity: 'systems.xos.car.android.product.companion.startup.SplashActivity', appPackage: 'com.gexne.car.assistant', autoLaunch: 'false' },
               appium_lib: { sauce_username: nil, sauce_access_key: nil } }
    @dr = Appium::Driver.new(caps).start_driver
    Appium.promote_appium_methods self.class
    @wait = Selenium::WebDriver::Wait.new({:timeout => 5})
    @think_time = 2
  end
  
  def teardown
    #sleep @think_time
    driver_quit
  end
  
  def test_koodar_assistant_login

    if @dr.app_installed? "com.gexne.car.assistant"
      @dr.start_activity app_package: 'com.gexne.car.assistant',  app_activity: 'systems.xos.car.android.product.companion.startup.SplashActivity' 
    else
      puts "HUD Assistant not installed"
    end

    sleep @think_time
    puts @dr.current_activity
    #sleep 3
    
    #puts  @dr.find_element(:id, 'com.gexne.car.assistant:id/root').displayed?
    
    #exists { text('导航') }? puts('true'): puts('false')
    
    # check whethere log in activity exist or not
    # 
    begin
      #@wait.until { @dr.find_element(:id, 'com.gexne.car.assistant:id/root').displayed? }
      @wait.until { @dr.current_activity == 'systems.xos.car.android.product.companion.startup.login.LoginActivity'}
    rescue Selenium::WebDriver::Error::TimeOutError
      puts 'no login widget'
    else
      begin
        phone_number = @dr.find_element(id: 'com.gexne.car.assistant:id/login_phone_number')
      rescue Selenium::WebDriver::Error::NoSuchElementError
        puts 'no login edit box widget'
      else
        # Log in    
        phone_number.clear()
        phone_number.send_keys('13824470628')
        @dr.find_element(id: 'com.gexne.car.assistant:id/login_password').click
        @dr.find_element(id: 'com.gexne.car.assistant:id/login_password').send_keys('ygvuhbijn')

        sleep @think_time

        @dr.find_element(id: 'com.gexne.car.assistant:id/login_next').click
      end
    end 
    
    
    begin 
      @wait.until  { @dr.find_element(:id, 'com.gexne.car.assistant:id/recyclerView').displayed? }      
    rescue
      Selenium::WebDriver::Error::TimeOutError
      puts "no navigation widget"

    else
      @dr.find_elements(:class, 'android.widget.LinearLayout')[1].click
    end
  
  end
end

