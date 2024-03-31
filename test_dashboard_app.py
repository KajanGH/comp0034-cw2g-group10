import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
