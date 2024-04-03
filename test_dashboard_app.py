import pytest
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # Import Select class
import datetime

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
def populate_search_form(browser):
    region_input = browser.find_element(By.ID, "Region")
    region_input.send_keys("London")

    low_age_input = browser.find_element(By.ID, "low-age")
    low_age_input.send_keys("20")

    high_age_input = browser.find_element(By.ID, "high-age")
    high_age_input.send_keys("40")

    year_input = browser.find_element(By.ID, "year")
    year_input.send_keys("2022")

    month_input = browser.find_element(By.ID, "month")
    month_input.send_keys("January")

    sex_input = browser.find_element(By.ID, "sex")
    sex_input.send_keys("Male")

    # Submit the form
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

####MAP PAGE TESTS#########
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

def test_invalid_age_range(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/map")
    
    # Choose a start age greater than end age
    start_age_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "start_age"))
    )
    start_age_input.clear()
    start_age_input.send_keys("40")  # Example start age
    
    end_age_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "end_age"))
    )
    end_age_input.clear()
    end_age_input.send_keys("20")  # Example end age

    # Choose a region (e.g., Region)
    region_radio = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "rgn"))
    )
    region_radio.click()
    
    # Choose a sex
    sex_radio = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "male"))
    )
    sex_radio.click()
    
    # Submit the form
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "log-in-container"))
    )
    submit_button.click()
    
    # Assert that an alert message is displayed
    alert = WebDriverWait(browser, 10).until(
        EC.alert_is_present()
    )
    assert "Start age must be equal to or lower than end age." in alert.text, "Invalid age range not detected"

def test_show_stats(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/map")

    # Click on the "Show stats" button
    show_stats_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "toggleStatsBtn"))
    )
    show_stats_button.click()

    # Check if the stats box is displayed
    stats_box = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "stats-box"))
    )
    assert stats_box.is_displayed(), "Stats box not displayed"

def test_missing_required_fields(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/map")

    # Submit the form without filling in required fields (layer and sex)
    submit_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "log-in-container"))
    )
    submit_button.click()

    try:
        # Wait for an alert to be present indicating the missing required fields
        alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    except TimeoutException:
        # If no alert is present and timeout occurs, it's expected behavior
        assert True
        return
    
    # If an alert is present, it's an unexpected behavior
    assert False, "Unexpected behavior: Alert for missing required fields not found"

####ANALYTICS/SNAPSHOT PAGE TESTS####
def test_logo_navigation(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    # Click on the logo
    logo = browser.find_element(By.ID, "logoImage")
    logo.click()

    # Check if the URL redirects to the home page
    assert browser.current_url == "http://127.0.0.1:5000/"

def test_table_icon_navigation(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    # Click on the table icon
    table_icon = browser.find_element(By.ID, "tableIcon")
    table_icon.click()

    # Check if the URL redirects to the analytics page
    assert browser.current_url == "http://127.0.0.1:5000/analytics"

def test_camera_icon_navigation(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    # Click on the camera icon
    camera_icon = browser.find_element(By.ID, "cameraICon")
    camera_icon.click()

    # Check if the URL redirects to the snapshot page
    assert browser.current_url == "http://127.0.0.1:5000/snapshot"

def test_user_icon_navigation(browser):
    # Open the website
    browser.get(f"http://127.0.0.1:5000/analytics")

    # Click on the user icon
    user_icon = browser.find_element(By.ID, "userIcon")
    user_icon.click()

    # Check if the URL redirects to the account page
    assert browser.current_url == f"http://127.0.0.1:5000/account"

def test_settings_icon_navigation(browser):
    # Open the website
    browser.get(f"http://127.0.0.1:5000/analytics")

    # Click on the settings icon
    settings_icon = browser.find_element(By.ID, "settingsIcon")
    settings_icon.click()

    # Check if the URL redirects to the settings page
    assert browser.current_url == f"http://127.0.0.1:5000/settings"

def test_search_form_submission(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    # Capture the initial timestamps of the graph image files
    initial_timestamps = []
    initial_graph_elements = browser.find_elements(By.CLASS_NAME, "img")
    for graph_element in initial_graph_elements:
        graph_src = graph_element.get_attribute("src")
        # Extract the relative path of the image file
        graph_file_path = "/".join(graph_src.split("/")[-3:])
        # Get the timestamp of the image file
        initial_timestamps.append(os.path.getmtime(graph_file_path))

    populate_search_form(browser)


    # Capture the updated timestamps of the graph image files
    updated_timestamps = []
    updated_graph_elements = browser.find_elements(By.CLASS_NAME, "img")
    for graph_element in updated_graph_elements:
        graph_src = graph_element.get_attribute("src")
        # Extract the relative path of the image file
        graph_file_path = "/".join(graph_src.split("/")[-3:])
        # Get the timestamp of the image file
        updated_timestamps.append(os.path.getmtime(graph_file_path))

    # Check if the timestamps have changed after form submission
    assert initial_timestamps != updated_timestamps


def test_form_submission_changes_recent_search(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    populate_search_form(browser)

    # Wait for the page to reload and fetch the element with class "camden-female-30-41"
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".camden-female-30-41")))
    data_to_render_element = browser.find_element(By.CSS_SELECTOR, ".camden-female-30-41")
    new_data_to_render = data_to_render_element.text

    # Check if the new top search matches the expected value
    expected_value = "> London Male 20-40 in January 2022"
    assert new_data_to_render == expected_value


def test_heart_button_visibility(browser):
    # Delete image sources to simulate no images being displayed
    for i in range(1, 7):
        if os.path.exists(f'static\\public\\graph{i}.png'): os.remove(f'static\\public\\graph{i}.png')

    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")


    # Check if heart buttons are visible when images are not displayed
    heart_buttons = browser.find_elements(By.CLASS_NAME, "heart-button")
    for button in heart_buttons:
        assert not button.is_displayed()

    populate_search_form(browser)


    # Check if heart buttons become visible after form submission
    heart_buttons = browser.find_elements(By.CLASS_NAME, "heart-button") #List remade to avoid stale element reference
    for button in heart_buttons:
        assert button.is_displayed()

def test_enlarge_graph_and_close(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")

    populate_search_form(browser)

    # Click on one of the graphs to enlarge it
    graph_to_enlarge = browser.find_element(By.CLASS_NAME, "img")
    graph_to_enlarge.click()

    # Wait for the close button to become visible
    close_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "close")))
    # Click on the close button
    close_button.click()

    # Verify that the overlay is closed
    overlay = browser.find_element(By.ID, "overlay")
    assert not overlay.is_displayed()

def test_heart_button_click(browser):
    # Empty existing snapshot data
    for i in range(0, 10):
        if os.path.exists(f'static\\snapshot\\graph{i}.png'):
            os.remove(f'static\\snapshot\\graph{i}.png')

    # Empty existing snapshot data CSV
    df = pd.DataFrame(columns=['date','form','img'])
    df.to_csv('static\\snapshot\\snapshotdata.csv', index=False)

    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    
    populate_search_form(browser)

    # Wait for the heart buttons to become visible
    WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "heart-button")))

    # Click on the heart button of the first graph
    heart_button = browser.find_element(By.NAME, "heart_button_1")
    heart_button.click()

    # Check if the snapshot folder contains any PNG files
    snapshot_files = [file for file in os.listdir('static\\snapshot') if file.endswith(".png")]
    
    assert snapshot_files, "No snapshot image files found in the snapshot folder"
    
    # Check if today's date and form data have been written to the CSV file
    today_date = datetime.date.today().strftime("%Y-%m-%d")
    expected_data = f"{today_date},London Male 20-40 in January 2022"
    with open('static\\snapshot\\snapshotdata.csv', 'r') as file:
        csv_data = file.read()
        assert expected_data in csv_data, f"Expected data '{expected_data}' not found in the CSV file"
