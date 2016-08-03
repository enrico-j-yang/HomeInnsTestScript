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
  @@think_time = 2
  def setup
    caps   = { caps:       { platformName: 'Android', deviceName: 'Android Machine', appActivity: '.Calculator', appPackage: 'com.android.calculator2', autoLaunch: 'false' },
               appium_lib: { sauce_username: nil, sauce_access_key: nil } }
    @wd = Appium::Driver.new(caps).start_driver
    Appium.promote_appium_methods self.class
    @wait = Selenium::WebDriver::Wait.new({:timeout => 3})
  end
  
  def teardown
    sleep @@think_time
    driver_quit
  end
  
  def test_koodar_assistant_login

    if @wd.app_installed? "com.gexne.car.assistant"
      @wd.start_activity app_package: 'com.gexne.car.assistant',  app_activity: 'systems.xos.car.android.product.companion.startup.SplashActivity' 
    else
      puts "HUD Assistant not installed"
    end

    #puts @wd.current_activity
    #sleep 3
    
    #puts  @wd.find_element(:id, 'com.gexne.car.assistant:id/root').displayed?
    
    #exists { text('导航') }? puts('true'): puts('false')
    
    # check whethere log in activity exist or not
    # 
    begin
      @wait.until { @wd.current_activity == 'systems.xos.car.android.product.companion.startup.login.LoginActivity' }
    rescue Selenium::WebDriver::Error::TimeOutError
      puts 'no login widget'
    else
      begin
        phone_number = @wd.find_element(id: 'com.gexne.car.assistant:id/login_phone_number')
      rescue Selenium::WebDriver::Error::NoSuchElementError
        puts 'no login edit box widget'
      else
        # Log in    
        phone_number.clear()
        phone_number.send_keys('13824470628')
        @wd.find_element(id: 'com.gexne.car.assistant:id/login_password').clear
        @wd.find_element(id: 'com.gexne.car.assistant:id/login_password').send_keys(' ')
        @wd.find_element(id: 'com.gexne.car.assistant:id/login_password').send_keys('ygvuhbijn')

        sleep @@think_time

        @wd.find_element(id: 'com.gexne.car.assistant:id/login_next').click
      end
    end 
    
    
    begin 
      #@wait.until  { @wd.find_element(:id, 'com.gexne.car.assistant:id/recyclerView').displayed? }      
      @wait.until { @wd.current_activity == 'systems.xos.car.android.product.companion.MainActivity' }
    rescue
      Selenium::WebDriver::Error::TimeOutError
      puts "no navigation widget"

    else
      @wd.find_elements(:class, 'android.widget.LinearLayout')[1].click
      sleep @@think_time
      @wd.navigate.back
      #@wd.find_elements(:class, 'android.widget.LinearLayout').each do |input|
        #input.click
        #@wd.navigate.back
        #end
    end
  
  end
end

