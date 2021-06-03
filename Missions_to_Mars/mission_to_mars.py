#!/usr/bin/env python
# coding: utf-8

# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def Scrape():
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    # NASA Mars News
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text


    # JPL Mars Space Images - Featured Image

    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    core_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
    img_line = str(soup.select('img')[1])
    img = img_line.split("=")[2][1:-3]
    featured_image_url = core_url+img


    # Mars Facts
    url = 'https://space-facts.com/mars/'

    Mars_df = pd.read_html('https://space-facts.com/mars/')[0]

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    ''' --------------------------'''

    base_url = 'https://astrogeology.usgs.gov'

    hem_names = []

    mydivs = soup.find_all("a", {"class": "itemLink product-item"})

    x=0
    for i in mydivs:
        if x % 2 == 0:
            x += 1
            continue
        else:
            i = i.text
            i = i.split()[:-1]
            i = " ".join(i)
            hem_names.append(i)
            x += 1

    ''' --------------------------'''

    base_url = 'https://astrogeology.usgs.gov'

    url_adds = []

    mydivs = soup.find_all("a", {"class": "itemLink product-item"})
    x = 0
    for i in mydivs:
        if x%2 != 0:
            x+=1
            continue
        
        else:
            i = str(i).split(" ")[3][6:-6]
            url_adds.append(i)
            x+=1
            
    urls = [str(base_url+x) for x in url_adds]

    ''' --------------------------'''

    hemisphere_image_urls = []

    x = 0
    for url in urls:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        img_line = str(soup.select(".wide-image")[0])
        img = img_line.split("=")[2][1:-3]
        img = url+img
        
        hemisphere_image_urls.append(dict({'title':hem_names[x], 'img_url':img}))

        x += 1


    scrape_dict = {'news_title':news_title,'news_p':news_p,'featured_image_url':featured_image_url,'Mars_df':Mars_df,
                'hemisphere_image_urls':hemisphere_image_urls}

    return scrape_dict