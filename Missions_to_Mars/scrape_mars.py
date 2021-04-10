# Import dependencies 
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import time

# Define scrape function
def mars_scrape(): 

    # Import ChromeDriver: 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape the NASA Mars News Site (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.

    # Open and let load
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)

    # Grab HTML 
    html = browser.html 
    news_soup = soup(html, 'html.parser')

    # Grabbing the pieces using the classes
    mars_news_result = news_soup.find_all('div', class_='list_text')[0]
    news_title = mars_news_result.find('div', class_="content_title").text
    news_p = mars_news_result.find('div', class_="article_teaser_body").text

    # Visit the url for JPL Featured Space Image here: https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    # and assign the url string to a variable called featured_image_url.

    # Open and let load
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(2)

    # Grab HTML 
    html = browser.html 
    spaceimage_soup = soup(html, 'html.parser')

    # Grabbing the pieces using the classes
    spaceimage_soup_result = spaceimage_result = spaceimage_soup.find_all('div', class_='floating_text_area')[0]
    featured_image_url_href = spaceimage_soup_result.find('a', class_='showimg fancybox-thumbs').get('href')

    # Connect this href to the base url to get the full size image 
    featured_image_url = url + featured_image_url_href
    featured_image_url

    # Visit the Mars Facts webpage here (https://space-facts.com/mars/) and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.
    mars_table = pd.read_html('https://space-facts.com/mars/')[0]

    # Changing column names 
    mars_table.columns = ['Description', 'Metrics']
    mars_table_html = mars_table.to_html()

    # Visit the USGS Astrogeology site for images for each of Mars' hemispheres: https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

    # Open and let load
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)

    # Grab HTML 
    html = browser.html 
    hemisphere_soup = soup(html, 'html.parser')

    # Grabbing the href using the classes
    hemisphere_img_list = hemisphere_soup.find_all('a', class_='itemLink product-item')

    # Prepare for the next step 
    hrefs = []

    for img_url in hemisphere_img_list: 
        print(img_url)
        hrefs.append(img_url.get('href'))

    hrefs = hrefs[:-1]
    hrefs = list(set(hrefs)) 

    # Make empty list for final urls and titles
    hemisphere_img_urls = []

    for img_url in hrefs:
        secondary_link = url + img_url
        
        # Visit and let load
        browser.visit(secondary_link)
        time.sleep(2)
        
        # Grab HTML 
        html = browser.html
        secondary_link_soup = soup(html, 'html.parser')
        
        # Find the title
        img_title = secondary_link_soup.find('h2', class_='title').text 
        img_title = img_title.replace(' Enhanced','')
        
        # Append sample url to final urls
        final_url = secondary_link_soup.find('a', text = 'Sample').get('href')
        final_url = url + final_url # combine with base url
        
        d = {"title": img_title, "img_url": final_url}
        hemisphere_img_urls.append(d)
        
    # Close it
    browser.quit()

    # Combining into one dictionary for Mongo

    mars_dictionary = {'news_title': news_title, 
                    'news_p': news_p, 
                    'featured_image_url': featured_image_url, 
                    'mars_table_html': mars_table_html,
                    'hemisphere_img_urls': hemisphere_img_urls}
    print(mars_dictionary)
    return mars_dictionary 
