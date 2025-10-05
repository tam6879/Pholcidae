#The adversary, this basic testing scraper is meant to help test the effectiveness of the scraper tarpit. This scraper recursively scrapes text and images from every page it encounters as a link. It of course completely ignores robots.txt

import asyncio
from playwright.async_api import async_playwright, Playwright
from bs4 import BeautifulSoup
import requests
import re

pages_visited = [] #Keeps track of pages already scraped

#Recursive function, scrapes as many pages as it encounters
async def scrape_all_pages(base_url, page):
    #Get the current URL and append it to the list of pages visited
    current_url = page.url
    pages_visited.append(current_url)
    print("Scraping: " + current_url)
    
    #Remove all troublesome characters from the url so it can be the file name
    file_url = re.sub(r'\W+', '', current_url)
    file_url = file_url[:64]
    soup = BeautifulSoup(await page.content(), "html.parser") #Used to parse for text and image data
    
    #Parse and save text data
    with open("./scraped_text/" + file_url, "w") as f:
        #Save paragraph and span text to the file
        paragraphs = soup.find_all("p")
        for para in paragraphs:
            f.write(para.text)
        spans = soup.find_all("span")
        for span in spans:
            f.write(span.text)
    f.close()

    #Parse and save image data
    image_tags = soup.find_all("img")
    image_urls = [image['src'] for image in image_tags]
    #For each image url, make sure the name is correct, and download it
    for image_url in image_urls:
        file_name = re.search(r'/([\w_-]+[.](jpg|jpeg|gif|png|webp))$', image_url)
        if not file_name:
            print("Regex failed to match url: {}".format(image_url))
            continue
        with open("./scraped_images/" + file_name.group(1), "wb") as f:
            if "http" not in image_url:
                image_url="{}{}".format(base_url, image_url)
            response = requests.get(image_url)
            f.write(response.content)
        f.close()


    
    #Get all of the links on the current page. For each link, if it is not an external link and is not already visited, open the link and call this function again
    links = await page.get_by_role("link").all()
    for link in links:
        if "http" not in await link.get_attribute("href"):
            full_link = base_url + await link.get_attribute("href")
            if full_link not in pages_visited:
                await page.goto(full_link)
                await scrape_all_pages(base_url, page)
        

async def run(playwright: Playwright):
    #base_url is the address of the server you wish to scrape, leave it on this for this test server if running it locally
    base_url = "http://127.0.0.1:8000"
    chromium = playwright.chromium
    #Remove "headless=False" to skip seeing the browser as it runs
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(base_url)
    await scrape_all_pages(base_url, page)
    browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())
