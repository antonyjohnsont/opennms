package org.opennms.smoketest;

import java.net.URL;

import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverBackedSelenium;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.thoughtworks.selenium.SeleneseTestBase;



public class NotificationsPageTest extends SeleneseTestBase {
    @Before
    public void setUp() throws Exception {
        DesiredCapabilities capability = DesiredCapabilities.firefox();
        WebDriver driver = new RemoteWebDriver(new URL("http://localhost:4444/wd/hub"), capability);
        String baseUrl = "http://localhost:8980/";
        selenium = new WebDriverBackedSelenium(driver, baseUrl);
        //selenium.start();
        selenium.open("/opennms/login.jsp");
        selenium.type("name=j_username", "admin");
        selenium.type("name=j_password", "admin");
        selenium.click("name=Login");
        selenium.waitForPageToLoad("30000");
        selenium.click("link=Notifications");
        selenium.waitForPageToLoad("30000");
    }

    @Test
    public void testAllTextIsPresent() throws Exception {
        assertTrue(selenium.isTextPresent("Notification queries"));
        assertTrue(selenium.isTextPresent("Outstanding and Acknowledged Notices"));
        assertTrue(selenium.isTextPresent("Notification Escalation"));
        assertTrue(selenium.isTextPresent("Check your outstanding notices"));
        assertTrue(selenium.isTextPresent("Once a notice is sent"));
        assertTrue(selenium.isTextPresent("User:"));
        assertTrue(selenium.isTextPresent("Notice:"));
    }

    @Test
    public void testAllLinksArePresent() {
        assertTrue(selenium.isElementPresent("link=Your outstanding notices"));
        assertTrue(selenium.isElementPresent("link=All outstanding notices"));
        assertTrue(selenium.isElementPresent("link=All acknowledged notices"));
    }

    @Test 
    public void testAllFormsArePresent() {
        assertTrue(selenium.isElementPresent("css=input[type=submit]"));
        assertTrue(selenium.isElementPresent("//input[@value='Get details']"));
    }

    @Test
    public void testAllLinks() {
        selenium.click("link=Your outstanding notices");
        selenium.waitForPageToLoad("30000");
        assertTrue(selenium.isTextPresent("admin was notified"));
        assertTrue(selenium.isElementPresent("link=[Remove all]"));
        assertTrue(selenium.isElementPresent("link=Sent Time"));
        assertTrue(selenium.isElementPresent("//input[@value='Acknowledge Notices']"));
        selenium.click("link=Notices");
        selenium.waitForPageToLoad("30000");
        selenium.click("link=All outstanding notices");
        selenium.waitForPageToLoad("30000");
        assertTrue(selenium.isTextPresent("only outstanding notices"));
        assertTrue(selenium.isElementPresent("link=Respond Time"));
        assertTrue(selenium.isElementPresent("css=input[type=button]"));
        selenium.click("link=Notices");
        selenium.waitForPageToLoad("30000");
        selenium.click("link=All acknowledged notices");
        selenium.waitForPageToLoad("30000");
        assertTrue(selenium.isTextPresent("only acknowledged notices"));
        assertTrue(selenium.isElementPresent("link=Node"));
        assertTrue(selenium.isElementPresent("css=input[type=submit]"));
        selenium.click("link=Notices");
        selenium.waitForPageToLoad("30000");
        selenium.click("link=Log out");
        selenium.waitForPageToLoad("30000");
    }

    @After
    public void tearDown() throws Exception {
        selenium.stop();
    }
}