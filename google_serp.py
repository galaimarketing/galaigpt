from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import json
import os

def search_google_web_automation(query):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--no-sandbox")  # Add this line for Linux compatibility
    options.add_argument("--disable-dev-shm-usage")  # Add this line for Linux compatibility
    driver = webdriver.Chrome(options=options, executable_path='/path/to/chromedriver')  # Specify the path to chromedriver

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Linux",  # Change platform to Linux
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    n_pages = 2
    results = []
    counter = 0
    for page in range(1, n_pages):
        url = (
            "http://www.google.com/search?q="
            + str(query)
            + "&start="
            + str((page - 1) * 10)
        )

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search = soup.find_all("div", class_="yuRUbf")
        for h in search:
            counter = counter + 1
            title = h.a.h3.text
            link = h.a.get("href")
            rank = counter
            results.append(
                {
                    "title": h.a.h3.text,
                    "url": link,
                    "domain": urlparse(link).netloc,
                    "rank": rank,
                }
            )
    return results[:3]
