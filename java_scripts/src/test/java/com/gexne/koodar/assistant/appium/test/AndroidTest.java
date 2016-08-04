package com.gexne.koodar.assistant.appium.test;

import io.appium.java_client.AppiumDriver;
import io.appium.java_client.android.AndroidDriver;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.assertNotNull;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.File;
import java.net.URL;
import java.util.List;
import java.lang.Thread;

public class AndroidTest {
	private long thinkTimeMillis;
	private AndroidDriver<WebElement> driver;

	@Before
	public void setUp() throws Exception {
		File classpathRoot = new File(System.getProperty("user.dir"));
		File appDir = new File(classpathRoot, "apps/ApiDemos/bin");
		File app = new File(appDir, "ApiDemos-debug.apk");
		DesiredCapabilities capabilities = new DesiredCapabilities();
		capabilities.setCapability("deviceName", "Android Emulator");
		capabilities.setCapability("platformVersion", "5.1");
		capabilities.setCapability("app", app.getAbsolutePath());
		capabilities.setCapability("appPackage", "io.appium.android.apis");
		capabilities.setCapability("appActivity", ".ApiDemos");
		capabilities.setCapability("autoLaunch", "false");
		driver = new AndroidDriver<>(new URL("http://127.0.0.1:4723/wd/hub"), capabilities);
	}

	@After
	public void tearDown() throws Exception {
		driver.quit();
	}

	@Test
	public void testLogin() {
		// launch assistant app if it installed
		if (driver.isAppInstalled("com.gexne.car.assistant")) {
			driver.startActivity("com.gexne.car.assistant",
					"systems.xos.car.android.product.companion.startup.SplashActivity");
		} else {
			System.out.println("HUD Assistant not installed");
		}

		// wait for login activity
		try {
			(new WebDriverWait(driver, 3)).until(new ExpectedCondition<Boolean>() {
				public Boolean apply(WebDriver d) {
					return d.findElement(By.id("com.gexne.car.assistant:id/login_phone_number")).isDisplayed();
				}
			});

			// input account and password
			WebElement phone_number = driver.findElementById("com.gexne.car.assistant:id/login_phone_number");
			assertNotNull(phone_number);
			phone_number.sendKeys("13824470628");
			WebElement password = driver.findElementById("com.gexne.car.assistant:id/login_password");
			password.click();// because send_keys miss first character, so
									// here come one blank as to avoid this
									// problem
			password.sendKeys("ygvuhbijn");
			assertNotNull(password);
			try {
				Thread.sleep(thinkTimeMillis);
			} catch (Exception e) {
				System.out.println(e);
			}
			WebElement login = driver.findElementById("com.gexne.car.assistant:id/login_next");
			assertNotNull(login);
			login.click();
			try {
				Thread.sleep(thinkTimeMillis);
			} catch (Exception e) {
				System.out.println(e);
			}
			
			
		} catch (org.openqa.selenium.TimeoutException e) {
			System.out.println("*****wait for login activity time out*****");
		} catch (Exception e) {
			System.out.println(e);
		}

		// wait for main activity
		try {
			(new WebDriverWait(driver, 3)).until(new ExpectedCondition<Boolean>() {
				public Boolean apply(WebDriver d) {
					return d.findElements(By.className("android.widget.LinearLayout")).get(1).isDisplayed();
				}
			});
			driver.findElementsByClassName("android.widget.LinearLayout").get(1).click();

			try {
				Thread.sleep(thinkTimeMillis);
			} catch (Exception e) {
				System.out.println(e);
			}
		} catch (org.openqa.selenium.TimeoutException e) {
			System.out.println("*****wait for main activity time out*****");
		} catch (Exception e) {
			System.out.println(e);
		}
	}

}
