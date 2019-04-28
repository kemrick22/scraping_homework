# Dependencies
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import re
from splinter import Browser
from bs4 import BeautifulSoup

scrape_dict={}

def scrape():
    # Read NASA HTML
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Pull first headline available
    news_title=soup.find_all("div", "content_title")[0].text

    #Pull first description available
    news_p=soup.find_all("div", class_="article_teaser_body")[0].text

    #Visit JPL Site
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Create a Beautiful Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Find image
    result=soup.find("div",class_="img")
    path=result.img['src']

    #Store Featured Image
    featured_image_url=str('https://www.jpl.nasa.gov')+path

    #Visit Twitter
    url='https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Pull Latest Tweet
    result=soup.find("p",class_="tweet-text")
    temp=result.text

    #Remove Image Link
    mars_weather=temp[:temp.index('hPapic')-1]

    #Pull Table from Space Facts
    url='https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df=tables[0]

    #Format as html
    html_table = df.to_html(index=False, header=False)

    #Visit USGS
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Find List of Hemispheres
    hemispheres=soup.find_all("div",class_="item")


    #Create Empty Dictionary
    hemisphere_image_urls=[]
    hemisphere_titles=[]



    #Loop Through Hemispheres
    for i in hemispheres:
        
        #Store Title
        title=i.find('h3').text
        hemisphere_titles.append(title)
        
        #Visit Sub Url for Image
        ending=i.find('a')['href']
        start='https://astrogeology.usgs.gov'
        sub_url=start+ending
        response = requests.get(sub_url)
        sub_soup = BeautifulSoup(response.text, 'html.parser')
        
        #Pull Full Image
        img_url=sub_soup.find(href=re.compile("\.tif$"))['href']
        
        #Append Hemisphere to List
        hemisphere_image_urls.append(img_url)

    scrape_dict={"nasa_news":[news_title,news_p],
            "jpl_image":featured_image_url,
            "mars_weather":mars_weather,
            "mars_table":html_table,
            "hemisphere_titles":hemisphere_titles,
            "hemisphere_images":hemisphere_image_urls,
            }

    return scrape_dict
    


