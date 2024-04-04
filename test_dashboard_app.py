import pytest
import pandas as pd
import os
import jwt
from datetime import datetime,timedelta, timezone
from flask import Flask
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select  # Import Select class
from helpers import encode_auth_token, decode_auth_token, trends_box, get_user

@pytest.fixture
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "eyJ1IjoiZ3JlZW55NzMiLCJhIjoiY2szNXFhY3B4MWVoeTNobzJ0cjBrenl1biJ9"  # Set your secret key here
    return app

@pytest.fixture
def sample_users_data():
    data = {
        'id': [1, 2, 3],
        'fullname': ['Alice Smith', 'Bob Johnson', 'Charlie Brown'],
        'username': ['alice', 'bob', 'charlie'],
        'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
        'password': ['password1', 'password2', 'password3'],
        'repeatpassword': ['password1', 'password2', 'password3'],
    }
    return pd.DataFrame(data)

###HELPER FUNCTIONS###
def sign_up_user(browser):
    df = pd.DataFrame(columns=['id','fullname','username','email','password','repeatpassword'])
    df.to_csv('dataset\\users.csv', index=False)

    browser.get("http://127.0.0.1:5000/sign-up")

    # Fill in sign up form
    fullname_input = browser.find_element(By.ID, "fullname")
    fullname_input.send_keys("John Doe")

    username_input = browser.find_element(By.ID, "username")
    username_input.send_keys("johndoe")

    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys("johndoe@example.com")

    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("password123")

    repeat_password_input = browser.find_element(By.ID, "repeatpassword")
    repeat_password_input.send_keys("password123")

    # Check the checkbox
    checkbox = browser.find_element(By.CLASS_NAME, "rectangle-input")
    checkbox.click()

    # Submit the form
    submit_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    #Wait for and accept alert
    alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    assert "User registered successfully" in alert.text
    alert.accept()
def log_in_user(browser):
    browser.get("http://127.0.0.1:5000/log-in")

    email_input = browser.find_element(By.ID, "email")
    email_input.send_keys("johndoe@example.com")

    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys("password123")

    # Submit the login form
    login_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()

    # Wait for the success alert
    alert = WebDriverWait(browser, 10).until(EC.alert_is_present())
    
    # Verify the alert text
    assert "Logged in successfully" in alert.text

    # Accept the alert
    alert.accept()
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

###LOG-IN/SIGN-UP PAGE TESTS###
 
def test_sign_up(browser):
    sign_up_user(browser)

def test_log_in_after_sign_up(browser):
    # Sign up a new user
    sign_up_user(browser)
    # Log in with the same credentials
    log_in_user(browser)


####MAP PAGE TESTS#########
def test_png_image(browser):
    # Open the website
    browser.get("http://127.0.0.1:5000/") 
    browser.maximize_window()

    # Wait up to 10 seconds for the PNG image to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[src='/static/public/frame-12@2x.png']")))

    # Check if the PNG image is present on the page
    png_image = browser.find_element(By.CSS_SELECTOR, "img[src='/static/public/frame-12@2x.png']")
    assert png_image.is_displayed(), "PNG image not found on the page"

def test_map_functionality(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/map") 
    browser.maximize_window()

    # Wait up to 10 seconds for the map content to be present
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "map")))

    # Check if the map content is present on the page
    map_content = browser.find_element(By.ID, "map")
    assert map_content.is_displayed(), "Map content not found on the page"

def test_submit_data(browser):
    log_in_user(browser) #Provide token for page access
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
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/map")
    browser.maximize_window()
    
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
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/map")
    browser.maximize_window()
    
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
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/map")
    browser.maximize_window()
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
def test_logo_navigation_analytics(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Click on the logo
    logo = browser.find_element(By.ID, "logoImage")
    logo.click()

    # Check if the URL redirects to the home page
    assert browser.current_url == "http://127.0.0.1:5000/"

def test_table_icon_navigation_analytics(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Click on the table icon
    table_icon = browser.find_element(By.ID, "tableIcon")
    table_icon.click()

    # Check if the URL redirects to the analytics page
    assert browser.current_url == "http://127.0.0.1:5000/analytics"

def test_camera_icon_navigation_analytics(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Click on the camera icon
    camera_icon = browser.find_element(By.ID, "cameraICon")
    camera_icon.click()

    # Check if the URL redirects to the snapshot page
    assert browser.current_url == "http://127.0.0.1:5000/snapshot"

def test_user_icon_navigation_analytics(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get(f"http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Click on the user icon
    user_icon = browser.find_element(By.ID, "userIcon")
    user_icon.click()

    # Check if the URL redirects to the account page
    assert browser.current_url == f"http://127.0.0.1:5000/account"

def test_settings_icon_navigation_analytics(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get(f"http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Click on the settings icon
    settings_icon = browser.find_element(By.ID, "settingsIcon")
    settings_icon.click()

    # Check if the URL redirects to the settings page
    assert browser.current_url == f"http://127.0.0.1:5000/settings"

def test_search_form_submission(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    populate_search_form(browser)
    
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
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()
    populate_search_form(browser)

    # Wait for the page to reload and fetch the element with class "camden-female-30-41"
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".camden-female-30-41")))
    data_to_render_element = browser.find_element(By.CSS_SELECTOR, ".camden-female-30-41")
    new_data_to_render = data_to_render_element.text

    # Check if the new top search matches the expected value
    expected_value = "> London Male 20-40 in January 2022"
    assert new_data_to_render == expected_value


def test_heart_button_visibility(browser):
    log_in_user(browser) #Provide token for page access
    # Delete image sources to simulate no images being displayed
    for i in range(1, 7):
        if os.path.exists(f'static\\public\\graph{i}.png'): os.remove(f'static\\public\\graph{i}.png')

    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()

    # Check if heart buttons are visible when images are not displayed
    heart_buttons = browser.find_elements(By.CLASS_NAME, "heart-button")
    for button in heart_buttons:
        assert not button.is_displayed()

    populate_search_form(browser)

    WebDriverWait(browser, 10).until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "heart-button")))
    # Check if heart buttons become visible after form submission
    heart_buttons = browser.find_elements(By.CLASS_NAME, "heart-button") #List remade to avoid stale element reference
    for button in heart_buttons:
        assert button.is_displayed()

def test_enlarge_graph_and_close(browser):
    log_in_user(browser) #Provide token for page access
    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()
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

####SNAPSHOT PAGE TESTS####
def test_heart_button_click(browser):
    log_in_user(browser) #Provide token for page access
    # Empty existing snapshot data
    for i in range(0, 10):
        if os.path.exists(f'static\\snapshot\\graph{i}.png'):
            os.remove(f'static\\snapshot\\graph{i}.png')

    # Empty existing snapshot data CSV
    df = pd.DataFrame(columns=['date','form','img'])
    df.to_csv('static\\snapshot\\snapshotdata.csv', index=False)

    # Open the website
    browser.get("http://127.0.0.1:5000/analytics")
    browser.maximize_window()
    
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
    today_date = datetime.today().strftime("%Y-%m-%d")
    expected_data = f"{today_date},London Male 20-40 in January 2022"
    with open('static\\snapshot\\snapshotdata.csv', 'r') as file:
        csv_data = file.read()
        assert expected_data in csv_data, f"Expected data '{expected_data}' not found in the CSV file"

def test_logo_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()
    logo_icon = browser.find_element(By.CLASS_NAME, "logo-icon9")
    logo_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/"

def test_world_icon_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot") 
    browser.maximize_window()
    world_icon = browser.find_element(By.ID, "worldIcon")
    world_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/map"

def test_table_icon_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()

    table_icon = browser.find_element(By.ID, "tableIcon")
    table_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/analytics"

def test_camera_icon_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot") 
    browser.maximize_window()

    camera_icon = browser.find_element(By.CLASS_NAME, "camera-icon9")
    camera_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/snapshot"

def test_user_icon_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot") 
    browser.maximize_window()

    user_icon = browser.find_element(By.ID, "userIcon")
    user_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/account"

def test_settings_icon_click_navigation_snapshot(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot") 
    browser.maximize_window()

    settings_icon = browser.find_element(By.ID, "settingsIcon")
    settings_icon.click()
    assert browser.current_url == "http://127.0.0.1:5000/settings"

def test_image_click_overlay(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()

    images = browser.find_elements(By.CLASS_NAME, "saved-image")
    overlay = browser.find_element(By.ID, "overlay")
    overlay_img = browser.find_element(By.ID, "overlayImg")
    for image in images: # Check all images
        image.click()
        assert overlay.is_displayed()
        assert overlay_img.get_attribute("src") == image.get_attribute("src")
        close_btn = browser.find_element(By.CLASS_NAME, "close")
        close_btn.click()
        assert not overlay.is_displayed()

def test_check_image_links(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()

    images = browser.find_elements(By.CLASS_NAME, "saved-image")
    for image in images:
        assert image.get_attribute("src") != ""

def test_check_additional_info_display(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()

    additional_infos = browser.find_elements(By.CLASS_NAME, "additional-info")
    for info in additional_infos:
        assert info.text != ""

def test_verify_date_display(browser):
    log_in_user(browser) #Provide token for page access
    browser.get("http://127.0.0.1:5000/snapshot")
    browser.maximize_window()

    date_saved = browser.find_elements(By.CLASS_NAME, "date-saved")
    for date in date_saved:
        assert date.text != ""

###HELPER FUNCTION TESTS###
def test_encode_auth_token(app):
    """Test case for encode_auth_token function."""
    with app.app_context():
        user_id = 1
        token = encode_auth_token(user_id)

        # Decode the token to verify its correctness
        decoded_token = jwt.decode(token.encode(), app.config['SECRET_KEY'], algorithms=['HS256'])

        # Check if decoded token contains expected fields
        assert 'exp' in decoded_token
        assert 'iat' in decoded_token
        assert 'sub' in decoded_token

        # Check if the sub field matches the user_id provided
        assert decoded_token['sub'] == user_id

        # Check if the expiration time is within the expected range
        expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
        assert expiration_time > datetime.utcnow()
        assert expiration_time <= datetime.utcnow() + timedelta(minutes=5)

def test_decode_auth_token(app):
    """Test case for decode_auth_token function."""
    with app.app_context():
        user_id = 1
        auth_token = encode_auth_token(user_id)

        decoded_payload = decode_auth_token(auth_token)

        # Check if the decoded payload contains the expected user_id
        assert 'sub' in decoded_payload
        assert decoded_payload['sub'] == user_id

def test_trends_box():
    sexChoice = 'male'
    formatted_date = '2020-10-01'
    selected_layer = 'rgn'

    result = trends_box(sexChoice, formatted_date, selected_layer)

    # Check if the result is a list
    assert isinstance(result, list)

    # Check if the result has 8 elements
    assert len(result) == 8

    # Check if each element of the result is a list with 2 elements
    assert all(isinstance(item, list) and len(item) == 2 for item in result)

    # Check if each element's first item is a string (Region)
    assert all(isinstance(item[0], str) for item in result)

    # Check if each element's second item is a float (percentage change)
    assert all(isinstance(item[1], float) for item in result)

def test_get_user_existing_id(sample_users_data):
    users_file = 'test_users.csv'
    sample_users_data.to_csv(users_file, index=False)
    id = 1
    user = get_user(id, users_file)

    assert user is not None
    assert isinstance(user, dict)
    assert user['id'] == 1
    assert user['fullname'] == 'Alice Smith'
    assert user['username'] == 'alice'
    assert user['email'] == 'alice@example.com'
    assert user['password'] == 'password1'
    assert user['repeatpassword'] == 'password1'

def test_get_user_non_existing_id(sample_users_data):
    users_file = 'test_users.csv'
    sample_users_data.to_csv(users_file, index=False)
    id = 4
    user = get_user(id, users_file)

    assert user is None