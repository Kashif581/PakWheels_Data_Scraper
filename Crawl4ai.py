import gspread
import json
import asyncio
import os
from google.oauth2.service_account import Credentials
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode, JsonCssExtractionStrategy

async def crawl_data():
    c4a_script = """
                CLICK `.dropdown`
                WAIT `a[title="Used Cars for sale in Pakistan"]` 15
                CLICK `a[title="Used Cars Search"]`
                WAIT `.car-name` 15
                """
    schema = {
        "name": "Cars",
        "baseSelector": "div.col-md-9.grid-style",
        "fields": [
            {"name": "Name", "selector": "h3", "type": "text"},
            {"name": "Price", "selector": "div.price-details", "type": "text"},
            {"name": "City", "selector": "ul.search-vehicle-info", "type": "text"},
            {"name": "Year", "selector": "ul.search-vehicle-info-2 li:nth-child(1)", "type": "text"},
            {"name": "Mileage", "selector": "ul.search-vehicle-info-2 li:nth-child(2)", "type": "text"},
            {"name": "Fuel", "selector": "ul.search-vehicle-info-2 li:nth-child(3)", "type": "text"},
            {"name": "Engine", "selector": "ul.search-vehicle-info-2 li:nth-child(4)", "type": "text"},
            {"name": "Transmission", "selector": "ul.search-vehicle-info-2 li:nth-child(5)", "type": "text"}
        ]
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    config = CrawlerRunConfig(
        c4a_script=c4a_script,
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )
    browser_config = BrowserConfig(headless=True, java_script_enabled=True)

    async with AsyncWebCrawler(config=browser_config, close_on_exit=False) as crawler:
        result = await crawler.arun(url='https://www.pakwheels.com/', config=config)
        if not result.success:
            print("Crawl failed:", result.error_message)
            return []
        return json.loads(result.extracted_content)

def upload_to_sheets(data):
    # Google API scope
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    if creds_json is None:
        raise ValueError("Missing GOOGLE_SHEETS_CREDENTIALS env var")

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)

    # Open Sheet2
    sheet = client.open("PakWheelsCarData").worksheet("Sheet2")
    sheet.clear()

    # Prepare data for bulk update
    headers = ["Name", "Price", "City", "Year", "Mileage", "Fuel", "Engine", "Transmission"]
    rows = [[car.get("Name",""), car.get("Price",""), car.get("City",""),
             car.get("Year",""), car.get("Mileage",""), car.get("Fuel",""),
             car.get("Engine",""), car.get("Transmission","")] for car in data]

    # Bulk insert: header + all rows
    sheet.update([headers] + rows)

if __name__ == "__main__":
    cars_data = asyncio.run(crawl_data())
    if cars_data:
        upload_to_sheets(cars_data)
        print("Data uploaded to Google Sheets successfully!")
