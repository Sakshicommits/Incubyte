from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException


# Function to initialize the driver
def init_driver():
    try:
        # Setup Chrome options to ensure it works smoothly
        options = Options()
        options.add_argument("--start-maximized")  # Open the browser in maximized mode
        options.add_argument("--disable-notification")  # Disable any notoficaton popups
        options.add_experimental_option('excludeSwitches', ['enable-logging']) #ignoring Dev listening warnings
        Service_obj=Service("C:/Users/Downloads/edgedriver_win64/msedgedriver.exe")
        driver = webdriver.Edge(service=Service_obj, options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing the WebDriver: {e}")
        return None

# Function to fill out the registration form
def fill_signup_form(driver):
    try:
        # Open the sign-up page
        driver.get("https://magento.softwaretestingboard.com/")
        driver.find_element(By.XPATH, "//a[@href='https://magento.softwaretestingboard.com/customer/account/create/']").click()
        
        # Wait for the page to load and the form to be ready
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "firstname")))

        # Fill in the form fields with example data
        driver.find_element(By.ID, "firstname").send_keys("Incu")
        time.sleep(2)
        driver.find_element(By.ID, "lastname").send_keys("Byte")
        time.sleep(2)
        driver.find_element(By.ID, "email_address").send_keys("Incubyte45@example.com")
        time.sleep(2)
        driver.find_element(By.ID, "password").send_keys("Incubyte@123")
        time.sleep(2)
        driver.find_element(By.ID, "password-confirmation").send_keys("Incubyte@123")
        time.sleep(2)

        
        # Click the "Create an Account" button
        driver.find_element(By.XPATH,"//button[@class='action submit primary']").click()

        # Wait for the success or error message after form submission
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'Thank you for registering with Main Website Store.')]")))
        print("Sign Up Successful")

        log_out(driver) #call log_out function to sign in

        
         
    except Exception:
        WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'There is already an account with this email address')]")))
        print("Email already exists, you can try password reset")

    except TimeoutException:
        print("Timeout: The page took too long to load or the element was not found.")
    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")
    
def log_out(driver):
    try:
        
        driver.find_element(By.XPATH, "//button[@class='action switch']").click()
        time.sleep(2)
        action=ActionChains(driver)
        action.move_to_element(driver.find_element(By.LINK_TEXT, "Sign Out")).perform()
        driver.find_element(By.LINK_TEXT, "Sign Out").click()
        
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'You are signed out')]")))
        print("Sign Out Successful")

        sign_in(driver) #call sign_in to see if sign up was successful

        
    except Exception:
        print("Unknown Exception")


def sign_in(driver):
    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign In")))
        
        driver.find_element(By.LINK_TEXT, "Sign In").click()
        
        # Wait for the page to load 
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email")))

        # Fill in the fields with same credentials
        driver.find_element(By.ID, "email").send_keys("Incubyte45@example.com")
        time.sleep(2)
        driver.find_element(By.ID, "pass").send_keys("Incubyte@123")
        time.sleep(2)
                
        # Click the "SignIn" button
        driver.find_element(By.XPATH,"//button[@id='send2']").click()

        
        # Wait for the success or error message after form submission
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Welcome')]")))
        print("User SignIn Successful")
        
        
         
    except Exception:
        WebDriverWait(driver,2).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'The account sign-in was incorrect or your account is disabled temporarily. Please wait and try again later.')]")))
        print("The account sign-in was incorrect or your account is disabled temporarily..")

    except TimeoutException:
        print("Timeout: The page took too long to load or the element was not found.")
    except NoSuchElementException as e:
        print(f"Error: Element not found - {e}")        


# Main function to run the script
def main():
    driver = None
    try:
        # Initialize WebDriver
        driver = init_driver()
        if driver is None:
            return

        # Fill the sign-up form
        fill_signup_form(driver)

    except Exception as e:
        print(f"An unknown error occurred: {e}")
    finally:
        if driver:
            # Close the browser after completion
            driver.quit()

if __name__ == "__main__":
    main()
