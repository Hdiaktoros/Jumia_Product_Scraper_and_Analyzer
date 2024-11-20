import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import logging
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Set up logging
logging.basicConfig(level=logging.INFO)

# Base URL for Jumia
BASE_URL = "https://www.jumia.com.gh"

# Function to select the available WebDriver
def get_webdriver():
    try:
        # Try initializing Edge WebDriver
        try:
            options = webdriver.EdgeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            logging.info("Using Microsoft Edge WebDriver.")
            return webdriver.Edge(options=options)
        except WebDriverException:
            logging.warning("Microsoft Edge WebDriver not found in system PATH.")

        # Try initializing Chrome WebDriver
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            logging.info("Using Google Chrome WebDriver.")
            return webdriver.Chrome(options=options)
        except WebDriverException:
            logging.warning("Google Chrome WebDriver not found in system PATH.")

        # Try initializing Firefox WebDriver
        try:
            options = webdriver.FirefoxOptions()
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            logging.info("Using Mozilla Firefox WebDriver.")
            return webdriver.Firefox(options=options)
        except WebDriverException:
            logging.warning("Mozilla Firefox WebDriver not found in system PATH.")

        # Raise an error if no WebDriver is available
        raise WebDriverException("No compatible WebDriver found in system PATH. Ensure Edge, Chrome, or Firefox WebDriver is installed and added to PATH.")

    except Exception as e:
        logging.error(f"Error initializing WebDriver: {e}")
        raise

# Function to extract product details
def extract_product_details(product):
    details = {}
    try:
        details["Name"] = product.find_element(By.CLASS_NAME, "name").text
    except NoSuchElementException:
        details["Name"] = ""

    try:
        current_price = product.find_element(By.CLASS_NAME, "prc").text
        details["Current_price"] = float(current_price.replace("GH₵", "").replace(",", ""))
    except (NoSuchElementException, ValueError):
        details["Current_price"] = np.nan

    try:
        initial_price = product.find_element(By.CLASS_NAME, "old").text
        details["Initial_price"] = float(initial_price.replace("GH₵", "").replace(",", ""))
    except (NoSuchElementException, ValueError):
        details["Initial_price"] = np.nan

    details["Discount"] = ""
    try:
        details["Discount"] = product.find_element(By.CLASS_NAME, "bdg._dsct._sm").text
    except NoSuchElementException:
        pass

    details["Reviews"] = ""
    try:
        details["Reviews"] = product.find_element(By.CLASS_NAME, "rev ").text
    except NoSuchElementException:
        pass

    details["Stars"] = ""
    try:
        details["Stars"] = product.find_element(By.CLASS_NAME, "stars._s").text
    except NoSuchElementException:
        pass

    details["URL"] = ""
    try:
        details["URL"] = product.find_element(By.TAG_NAME, "a").get_attribute("href")
    except NoSuchElementException:
        pass

    return details

# Function to create the URL with options
def create_url(base_path, express, shipped_from_local, page):
    url = f"{BASE_URL}{base_path}?page={page}"
    if express:
        url += "&shop_premium_services=shop_express"
    if shipped_from_local:
        url += "&shipped_from=country_local"
    return url

# Function to scrape Black Friday products
def scrape_black_friday_products(express=False, shipped_from_local=False):
    all_products = []
    page = 1  # Start with the first page

    try:
        while True:
            url = create_url("/mlp-black-friday/", express, shipped_from_local, page)
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, "prd"))
                )
            except TimeoutException:
                logging.warning(f"No products found on page {page}. Stopping.")
                break

            logging.info(f"Scraping Black Friday products on page {page}...")

            product_elements = driver.find_elements(By.CLASS_NAME, "prd")
            for product in product_elements:
                product_dict = extract_product_details(product)
                all_products.append(product_dict)

            page += 1
            time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior

        product_df = pd.DataFrame(all_products)
        product_df = product_df.sort_values(by="Current_price", ascending=True)

        logging.info(f"Scraped {len(all_products)} Black Friday products.")
        print(product_df.to_string())
        product_df.to_csv("black_friday_sorted_products.csv", index=False)
        logging.info("Data saved to 'black_friday_sorted_products.csv'.")
        visualize_data(product_df)

    finally:
        driver.quit()

# Function to search for products
def search_products(search_query, express=False, shipped_from_local=False):
    all_products = []
    page = 1

    try:
        while True:
            search_url = create_url(f"/catalog/?q={search_query.replace(' ', '+')}", express, shipped_from_local, page)
            driver.get(search_url)
            try:
                WebDriverWait(driver, 10).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, "prd"))
                )
            except TimeoutException:
                logging.warning(f"No more products found for '{search_query}' on page {page}. Stopping.")
                break

            logging.info(f"Scraping results for '{search_query}' on page {page}...")

            product_elements = driver.find_elements(By.CLASS_NAME, "prd")
            for product in product_elements:
                product_dict = extract_product_details(product)
                all_products.append(product_dict)

            try:
                next_page = driver.find_element(By.XPATH, "//a[@aria-label='Next Page']")
                if not next_page:
                    break
            except NoSuchElementException:
                break

            page += 1
            time.sleep(random.uniform(2, 5))  # Random delay to mimic human behavior

        product_df = pd.DataFrame(all_products)
        product_df = product_df.sort_values(by="Current_price", ascending=True)

        logging.info(f"Found {len(all_products)} products for '{search_query}'.")
        print(product_df.to_string())
        product_df.to_csv(f"{search_query.replace(' ', '_')}_sorted_products.csv", index=False)
        logging.info(f"Data saved to '{search_query.replace(' ', '_')}_sorted_products.csv'.")
        visualize_data(product_df)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Function to scrape flash sales
def scrape_flash_sales(express=False, shipped_from_local=False):
    all_products = []

    try:
        url = create_url("/flash-sales/", express, shipped_from_local, 1)
        driver.get(url)
        time.sleep(3)  # Allow time for the page to load

        # Wait for product elements to be present
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME, "prd"))
        )

        logging.info("Scraping flash sales...")

        product_elements = driver.find_elements(By.CLASS_NAME, "prd")
        for product in product_elements:
            product_dict = extract_product_details(product)
            all_products.append(product_dict)

        product_df = pd.DataFrame(all_products)
        product_df = product_df.sort_values(by="Current_price", ascending=True)

        logging.info(f"Scraped {len(all_products)} flash sale products.")
        print(product_df.to_string())
        product_df.to_csv("flash_sales_sorted_products.csv", index=False)
        logging.info("Data saved to 'flash_sales_sorted_products.csv'.")
        visualize_data(product_df)

    except Exception as e:
        logging.error(f"An error occurred while scraping flash sales: {e}")
    finally:
        driver.quit()

def visualize_data(product_df):
    product_df["Current_price"] = pd.to_numeric(product_df["Current_price"], errors="coerce")
    product_df["Initial_price"] = pd.to_numeric(product_df["Initial_price"], errors="coerce")

    top_10 = product_df.nsmallest(10, "Current_price")

    plt.figure(figsize=(10, 6))
    plt.barh(top_10["Name"], top_10["Current_price"], color="skyblue")
    plt.xlabel("Price (GH₵)")
    plt.ylabel("Product")
    plt.title("Top 10 Cheapest Products")
    plt.gca().invert_yaxis()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.hist(product_df["Current_price"].dropna(), bins=20, color="lightgreen", edgecolor="black")
    plt.xlabel("Price (GH₵)")
    plt.ylabel("Frequency")
    plt.title("Price Distribution")
    plt.show()

# Interactive Panel
def main_panel():
    print("Welcome to the Product Scraper!")
    print("1. Scrape Black Friday Products")
    print("2. Search for a Specific Product")
    print("3. Scrape Flash Sales")
    express = input("Do you want express shipping? (yes/no): ").strip().lower() == "yes"
    shipped_from_local = input("Do you want to ship from local? (yes/no): ").strip().lower() == "yes"
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == "1":
        scrape_black_friday_products(express, shipped_from_local)
    elif choice == "2":
        search_query = input("Enter the product name to search for: ")
        search_products(search_query, express, shipped_from_local)
    elif choice == "3":
        scrape_flash_sales(express, shipped_from_local)
    else:
        print("Invalid choice. Please restart and choose 1, 2, or 3.")

# Initialize the WebDriver
driver = get_webdriver()

if __name__ == "__main__":
    main_panel()