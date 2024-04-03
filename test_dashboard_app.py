import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select  # Import Select class

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_png_image(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/") 

    # Wait up to 10 seconds for the PNG image to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/static/public/frame-12@2x.png']")))

    # Check if the PNG image is present on the page
    png_image = browser.find_element(By.CSS_SELECTOR, "img[src='/static/public/frame-12@2x.png']")
    assert png_image.is_displayed(), "PNG image not found on the page"

def test_map_functionality(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/map") 

    # Wait up to 10 seconds for the map content to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "map")))

    # Check if the map content is present on the page
    map_content = browser.find_element(By.ID, "map")
    assert map_content.is_displayed(), "Map content not found on the page"

def test_submit_data(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/map")
    browser.maximize_window()
    
    # Choose a region (e.g., Region)
    region_radio = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "rgn"))
    )
    region_radio.click()
    
    # Choose start and end age
    start_age_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "start_age"))
    )
    start_age_input.clear()
    start_age_input.send_keys("20")  # Example start age
    
    end_age_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "end_age"))
    )
    end_age_input.clear()
    end_age_input.send_keys("40")  # Example end age
    
    # Choose a sex
    sex_radio = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "male"))
    )
    sex_radio.click()

    # Choose a year - assuming the year is selected via a slider or input
    year_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "year"))
    )
    browser.execute_script("arguments[0].setAttribute('value', '24291')", year_input)

    # Submit the form
    submit_button = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "log-in-container"))
    )
    submit_button.click()
    # Assert that the submission was successful
    success_message = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'None Hidden')]"))
    )
    
    assert "None Hidden" in success_message.text, "Form submission failed"