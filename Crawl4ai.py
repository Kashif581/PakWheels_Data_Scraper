import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import JsonCssExtractionStrategy
import json




async def main():

    c4a_script = """
                CLICK `.dropdown`                        # open dropdown menu
                WAIT `a[title="Used Cars for sale in Pakistan"]` 15
                CLICK `a[title="Used Cars Search"]`   # click the link
                WAIT `.car-name` 15
                """
    schema = {
        "name":"Cars",
        "baseSelector":"div.name-price",
        "fields":[
        {
            "name": "Car_Name",
            "selector": "h3",
            "type": "text"
        }
        ]
     
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    config = CrawlerRunConfig(
        c4a_script=c4a_script,
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
        
    )

    browser_config = BrowserConfig(headless=False, java_script_enabled=True)

    # create an instance of asyncWebCrawler
    async with AsyncWebCrawler(config=browser_config, close_on_exit=False) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(
            url='https://www.pakwheels.com/',
            config=config
            )
        if not result.success:
            print("Crawl failed:", result.error_message)
            return
        
        data = json.loads(result.extracted_content)

        # print the extracted content
        print(data)
        # print(result.extracted_content)

asyncio.run(main())



