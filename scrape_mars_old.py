# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import time
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist

# Define scrape function
def scrape():
    mars_library = {}
    executable_path = {"executable_path": "chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)
    
    # Mars News
    url1 = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url1)
    html = browser.html
    soup1 = bs(html, "html5lib")
    news_title = soup1.find_all("div", class_="content_title")[0].find("a").text.strip()
    news_p = soup1.find_all("div", class_="rollover_description_inner")[0].text.strip()
    mars_library["news_title"] = news_title
    mars_library["news_p"] = news_p

    # Mars Featured Image
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)
    html = browser.html
    soup2 = bs(html, "html5lib")
    partial_address = soup2.find_all("a", class_="fancybox")[0].get("data-fancybox-href").strip()
    featured_image_url = "https://www.jpl.nasa.gov"+partial_address
    mars_library["featured_image_url"] = featured_image_url

    # Mars Weather
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)
    html = browser.html
    soup3 = bs(html, "html5lib")
    mars_weather = soup3.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[0].text
    mars_library["mars_weather"] = mars_weather

    # Mars Facts
    url4 = "https://space-facts.com/mars/"
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns=["description","value"]
    df.set_index("description", inplace=True)
    mars_facts=df.to_html(justify="left")
    mars_library["mars_facts"] = mars_facts

    # Mars Hemisperes
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)
    html = browser.html
    soup5 = bs(html,"html5lib")
    hemisphere_image_urls = []
    dict = {}
    results = soup5.find_all("h3")
    for result in results:
        itema = result.text
        time.sleep(1)    
        browser.click_link_by_partial_text(itema)
        time.sleep(1)
        htmla = browser.html
        soupa = bs(htmla,"html5lib")
        time.sleep(1)
        linka = soupa.find_all("div", class_="downloads")[0].find_all("a")[0].get("href")
        time.sleep(1)
        dict["title"]=itema
        dict["img_url"]=linka 
        hemisphere_image_urls.append(dict)
        dict = {}
        browser.click_link_by_partial_text("Back")
        time.sleep(1)
        
    # Mars Library
    mars_library["hemisphere_image_urls"]=hemisphere_image_urls
    
    # Return Library
    return mars_library
