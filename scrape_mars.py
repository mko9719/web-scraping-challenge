from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
executable_path = {'executable_path':"chromedriver.exe"}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())

    #Create Loop 
    #results_title = soup.find('div', class_="content_title")[1]
    #print(results_title)

    #results = soup.find('div', class_="rollover_description").text
    #print(results)
    for result in soup:
        # Identify and return title of listing
        results_title = soup.find_all("div", class_ = "content_title")[1].text
        # Identify and return price of listing
        results = soup.find_all("div", class_= "rollover_description_inner")[0].text
        # Print results only if title, price, and link are available
        if (results_title and results):
            print('-------------')
            print(results_title)
            print(results)


    #RETRIEVE IMAGES#
    #Retrieve Picture
    url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    response_image = requests.get(url_image)
    soup = BeautifulSoup(response_image.text, 'html.parser')
    print(soup.prettify())

    images = soup.find('img', class_="thumb")
    print(images)

    src = images["src"]
    print(src)

    jpl_images = "https://www.jpl.nasa.gov" + src
    jpl_images

    #retrieve mars data
    url_mars = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url_mars)
    mars_df = mars_table[0]
    mars_df.columns=["Facts", "Data"]
    mars_df

    #convert data to html
    mars_html = mars_df.to_html(header=True, index=False)

    #Mars image retrieval
    url_mars_images = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    #browser.visit(url_mars_images)
    #html = browser.html
    #html
    #hemisphere_image_urls = [
    # {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #{"title": "Cerberus Hemisphere", "": "..."},
    #{"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #{"title": "Syrtis Major Hemisphere", "img_url": "..."},


    # In[122]:


    request = requests.get(url_mars_images)
    soup = BeautifulSoup(request.text, 'html.parser')
    print(soup.prettify())


    # In[123]:


    #cerebus = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"
    #cerebus = soup.find('div', class_="collapsible results")
    #print(cerebus)


    # In[124]:


    #results = cerebus.find('a')
    #results

    cerebus = soup.find_all('div', class_="item")
    print(cerebus)

    image_list = []
    for hemi in cerebus:
        title = hemi.find("h3").text
        image = hemi.find("a", class_="itemLink product-item")["href"]
        full_url = "https://astrogeology.usgs.gov" + image
        request = requests.get(full_url)
        soup = BeautifulSoup(request.text, 'html.parser')
        src = "https://astrogeology.usgs.gov" + soup.find('img', class_="wide-image")["src"]
        image_list.append({"title":title, "image": src})
        print(image_list)
    mars_data_dict = {"Title":results_title, "Paragraph":results, "MarsP": jpl_images, "MarsDT": mars_html,"HemiI":image_list}
    return mars_data_dict
#if __name__ == "__main__":
#      If running as script, print scraped data
#    print(scrape())    




