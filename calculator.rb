require 'appium_lib'

caps   = { caps:       { platformName: 'Android', deviceName: 'Android HUD', appActivity: '.Calculator', appPackage: 'com.android.calculator2' },
           appium_lib: { sauce_username: nil, sauce_access_key: nil } }
driver = Appium::Driver.new(caps).start_driver

wait = Selenium::WebDriver::Wait.new({:timeout => 30})
wait.until { driver.find_element(:id, 'com.android.calculator2:id/clear').displayed? }

driver.find_element(id: 'com.android.calculator2:id/clear').click
driver.find_element(id: 'com.android.calculator2:id/digit9').click

#driver.exists{button('9')}?puts('true'):puts('false')

driver.quit
