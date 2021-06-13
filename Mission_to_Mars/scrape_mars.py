#!/usr/bin/env python
# coding: utf-8

# In[1]:


from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    
    # Set up Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
    #Visit website
    url = "https://redplanetscience.com/"
    browser.visit(url)


    time.sleep(5) 
    #Set up BeautifulSoup to find what is needed   
    html = browser.html
    soup = bs(html, "html.parser")
    try:
        news_title = soup.find('div', class_='content_title').get_text()
        #print(news_title)
        #scrape for paragraph text for news title
        news_p = soup.find('div', class_='article_teaser_body').get_text()
        #print(news_p)
    except AttributeError:
        return None, None
    

    # # JPL Mars Space Images - Featured Image
    
    #visit website
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    #Set up BeautifulSoup to find what is needed   
    html = browser.html
    soup = bs(html, "html.parser")
    #parsed to find the image source
    header_image = soup.find('img', class_='headerimage')['src']
    print(header_image)
    #added image source to original url to create the full image link
    featured_image_url = url + header_image
    print(featured_image_url)
    

    # # Mars Facts
    #set up url
    url = "https://galaxyfacts-mars.com/"

    #Scrapped tables from URL 
    tables = pd.read_html(url)
    tables
    #Created dataframe from tables list element
    df = tables[0]
    #Renamed columns
    df.columns = ['Description', 'Mars', 'Earth']
    #dropped first row to eleminate unnecessary items
    df = df.iloc[1:]
    df = df.reset_index(drop=True)
    df.set_index('Description', inplace=True)
    df
    #Converted dataframe to HTML Tabls
    html_table = df.to_html(classes=["table", 'table-striped'])
    html_table
    #Stripped unwanted newlines 
    stripped_html_table = html_table.replace('\n', '')

    # # Mars Hemispheres    
    
    #visit website
    url = "https://marshemispheres.com/"
    browser.visit(url)
    #Set up BeautifulSoup to find what is needed   
    html = browser.html
    soup = bs(html, "html.parser")
    #empty list to store links to get to pages to get title and image
    links = []
    #scrap page to get to parent div of each link
    divs = soup.find_all('div', class_='description')
    #looped through divs to find the full link
    for div in divs:
        description = div.find('a', class_='itemLink')['href']
        #print(description)
        full_link = url + description
        #appended links list to add each full link
        links.append(full_link)
    print(links)
    #empty list to hold dictionaries of each result
    hemisphere_image_urls = []
    #looped through each link in link list to find image and title
    for link in links:
        #used to visit each links page
        browser.visit(link)
        #reset BeautifulSoup to new browser
        html = browser.html
        soup = bs(html, "html.parser")
        #parsed to find image url
        img_url = soup.find_all('a', target='_blank')[2]['href']
        #added img_url to the original url to create a full link to image
        full_img = url + img_url
        #parsed to find title
        title = soup.find('h2', class_='title').text
        #saved results to a dictionary
        hem_info = {'title':title,
                    'img':full_img}
        #appended empty list with the dictionary
        hemisphere_image_urls.append(hem_info)
    
    print(hemisphere_image_urls)
    

    #Store data in dictionary
    mars_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_image":featured_image_url,
        "facts_table":stripped_html_table,
        "hemispheres":hemisphere_image_urls
    }
    browser.quit()
    return mars_data

scrape()
