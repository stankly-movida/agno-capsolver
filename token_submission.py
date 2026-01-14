from selenium import webdriver
from selenium.webdriver.common.by import By
import requests

def submit_recaptcha_token(driver, token: str):
    """Inject reCAPTCHA token and submit"""
    recaptcha_response = driver.find_element(By.ID, "g-recaptcha-response")
    driver.execute_script("arguments[0].style.display = 'block';", recaptcha_response)
    recaptcha_response.clear()
    recaptcha_response.send_keys(token)

    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()

def submit_turnstile_token(driver, token: str):
    """Inject Turnstile token and submit"""
    turnstile_input = driver.find_element(By.NAME, "cf-turnstile-response")
    driver.execute_script("arguments[0].value = arguments[1];", turnstile_input, token)

    form = driver.find_element(By.TAG_NAME, "form")
    form.submit()

def access_cloudflare_protected_page(url: str, cf_solution: dict):
    """Use Cloudflare Challenge solution to access protected page."""
    session = requests.Session()

    for cookie in cf_solution["cookies"]:
        session.cookies.set(cookie["name"], cookie["value"])

    headers = {"User-Agent": cf_solution["user_agent"]}

    response = session.get(url, headers=headers)
    return response.text
