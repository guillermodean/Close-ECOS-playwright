import re
from playwright.sync_api import sync_playwright
import time
import pandas as pd

# Load your dataframe
orders = pd.read_csv(filepath_or_buffer="data/closed _ECOS _WF.csv", sep=";")
orders.rename(columns={'ECO-12358': 'ECO', 'C': 'Rev'}, inplace=True)

print(orders.head())

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, channel='msedge')
    page = browser.new_page()
    page.goto("https://globalchangeimplementation/")

    # Iterate over the dataframe
    for index, row in orders.iterrows():
        page.goto("https://globalchangeimplementation/EcoDecoManagement/Index")
        page.click("#select2-EcoDeco-container")
        
        # Check if the ECO option is available in the dropdown
        eco_option = page.query_selector(f'option[value="{row["ECO"]}"]')
        if eco_option:
            # If the ECO option is found, select it
            page.select_option('#EcoDeco', row['ECO'])
            
            # Check if the Rev option exists in the dropdown
            rev_option = page.query_selector(f'option[value="{row["Rev"]}"]')
            if rev_option:
                page.select_option('#Rev', row['Rev'])
                # If the Rev option exists, continue with the next steps
                page.click("#btnSave")
                time.sleep(3)
                page.click("xpath=//table[@id='lista']//button[text()='SHOW']", timeout=90000)
            else:
                # If the Rev option does not exist, break the loop
                print(f"Revision {row['Rev']} not found for ECO {row['ECO']}, skipping.")
                break
        else:
            # If the ECO option is not found, continue to the next ECO value
            print(f"ECO {row['ECO']} not found in the dropdown, skipping to the next one.")
        time.sleep(1)  # Adjust timing as necessary