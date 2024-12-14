from csrf import detect_csrf  # CSRF testing
from decryption import evaluate_ssl_tls  # SSL/TLS evaluation
from xss import test_xss_with_browser  # XSS testing

def main():
    print("Welcome to the Web Vulnerability Scanner!")
    print("Please choose the type of vulnerability test to perform:")
    print("1. Detect CSRF vulnerabilities")
    print("2. Evaluate SSL/TLS configuration")
    print("3. Test for XSS vulnerabilities")
    
    choice = input("Enter the number of your choice (1/2/3): ").strip()

    if choice == "1":
        print("\n[CSRF Vulnerability Test Selected]")
        target_url = input("Enter the URL to test (e.g., http://example.com): ").strip()
        username = input("Enter the username for login (if required, press Enter to skip): ").strip()
        password = input("Enter the password for login (if required, press Enter to skip): ").strip()

        session = None
        if username and password:
            from csrf import authenticate_and_get_session
            session = authenticate_and_get_session(target_url, username, password)

        results = detect_csrf(target_url, session=session)
        print(f"Forms Analyzed: {results['forms_analyzed']}")
        if results["csrf_vulnerabilities"]:
            print("CSRF vulnerabilities detected:")
            for vuln in results["csrf_vulnerabilities"]:
                print(f"- Form action: {vuln['action']}, method: {vuln['method']}, inputs: {vuln['inputs']}")
        else:
            print("No CSRF vulnerabilities detected.")

    elif choice == "2":
        print("\n[SSL/TLS Configuration Evaluation Selected]")
        hostname = input("Enter the hostname or IP address to evaluate (e.g., example.com): ").strip()
        evaluate_ssl_tls(hostname)

    elif choice == "3":
        print("\n[XSS Vulnerability Test Selected]")
        print("This test requires Selenium WebDriver and a file named 'S-payloads.txt' with XSS payloads.")
        test_xss_with_browser()

    else:
        print("Invalid choice. Please run the program again and select a valid option.")

if __name__ == "__main__":
    main()
