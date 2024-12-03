from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

# Fetch dynamic content using Selenium
def fetch_dynamic_content(url):
    driver = webdriver.Chrome()  # Ensure chromedriver is installed
    driver.get(url)
    page_source = driver.page_source
    driver.quit()
    return BeautifulSoup(page_source, 'html.parser')

# Detect XSS vulnerabilities in forms
def detect_xss(url):
    print(f"Scanning {url} for XSS vulnerabilities...")
    soup = fetch_dynamic_content(url)

    forms = soup.find_all('form')
    results = {
        "forms_analyzed": len(forms),
        "xss_vulnerabilities": []
    }

    if len(forms) == 0:
        print("No forms detected on the page.")
        return results

    xss_test_script = "<script>alert('XSS')</script>"

    for form in forms:
        action = form.get('action')
        method = form.get('method', 'get').lower()
        inputs = form.find_all('input')

        for input_field in inputs:
            if input_field.get('type') not in ['submit', 'hidden']:
                # Test for XSS by injecting the script into inputs
                form_data = {inp.get('name'): xss_test_script for inp in inputs if inp.get('name')}
                
                full_action_url = action if action.startswith('http') else url + action

                try:
                    if method == 'post':
                        response = requests.post(full_action_url, data=form_data)
                    else:
                        response = requests.get(full_action_url, params=form_data)

                    # Check if the script appears in the response (indicative of XSS vulnerability)
                    if xss_test_script in response.text:
                        vulnerability = {
                            "action": action,
                            "method": method,
                            "inputs": [inp.get('name') for inp in inputs]
                        }
                        results["xss_vulnerabilities"].append(vulnerability)
                        print(f"Potential XSS vulnerability detected in form with action: {action}")
                except Exception as e:
                    print(f"Error testing form with action {action}: {e}")

    return results

# Main function
if __name__ == "__main__":
    # Get URL from the user
    target_url = input("Enter the URL to test (e.g., http://example.com): ")

    # Scan the URL for XSS vulnerabilities
    results = detect_xss(target_url)
    print(f"Forms Analyzed: {results['forms_analyzed']}")
    if results["xss_vulnerabilities"]:
        print("XSS vulnerabilities detected:")
        for vuln in results["xss_vulnerabilities"]:
            print(f"- Form action: {vuln['action']}, method: {vuln['method']}, inputs: {vuln['inputs']}")
    else:
        print("No XSS vulnerabilities detected.")



# https://owasp.glueup.com/my/home/
# f219183@cfd.nu.edu.pk
# $4kw47i7WWb*6H*

# https://juice-shop.herokuapp.com/#/search