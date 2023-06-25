import json
from flask import url_for
import pandas as pd
import requests
from bs4 import BeautifulSoup
from langdetect import detect



start = 'dp/'
end = '/'

class Amazon():
    def __init__(self, url) -> None:
        self.cookie={}
        self.header={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'
        }
        self.url = url
        self.link = []
        self.reviews=[]
        
        

    def Searchasin(self, asin):
        url="https://www.amazon.com/dp/"+asin
        page=requests.get(url,cookies=self.cookie,headers=self.header)
        if page.status_code==200:
            return page
        else:
            return "Error"

    def Searchreviews(self, review_link):
        url="https://www.amazon.com"+review_link
        page=requests.get(url,cookies=self.cookie,headers=self.header)
        if page.status_code==200:
            return page
        else:
            return "Error"

    def get_title(self):
        data_asin=(self.url.split(start))[1].split(end)[0]
        response=self.Searchasin(data_asin)
        soup2 = BeautifulSoup(response.content, "lxml")
        try:
        # Outer Tag Object
            title = soup2.find("span",
                            attrs={"id": 'productTitle'})
    
            # Inner NavigableString Object
            title_value = title.string
    
            # Title as a string value
            title_string = title_value.strip().replace(',', '')
 
        except AttributeError:
            title_string = "NA"
        return title_string
    
    def get_price(self):
        data_asin=(self.url.split(start))[1].split(end)[0]
        response=self.Searchasin(data_asin)
        soup2 = BeautifulSoup(response.content, "lxml")
        try:
            price = soup2.find(
                "span", attrs={'class': 'a-offscreen'}).string.strip().replace(',', '')
        except AttributeError:
            price = "N/A"
        return price
    def get_image(self):
        data_asin=(self.url.split(start))[1].split(end)[0]
        response=self.Searchasin(data_asin)
        soup2 = BeautifulSoup(response.content, "lxml")
        img_div = soup2.find(id="imgTagWrapperId")
        try:
            imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format
        except AttributeError:
            return url_for("static", filename="images/no_image_avaliable.jpg")
        # convert to a dictionary
        imgs_dict = json.loads(imgs_str)
        #each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
        # num_element = 0 
        first_link = list(imgs_dict.keys())[0]
        return first_link
        

    def get_reviews(self):
        data_asin=(self.url.split(start))[1].split(end)[0]
        response=self.Searchasin(data_asin)
        soup=BeautifulSoup(response.content)
        for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
            self.link.append(i['href'])
        for j in range(len(self.link)):
            for k in range(50):
                response = self.Searchreviews(self.link[j]+'&pageNumber='+str(k))
                soup=BeautifulSoup(response.content)
                for i in soup.findAll("span",{'data-hook':"review-body"}):
                    self.reviews.append(i.text)

        rev={'reviews':self.reviews}
        review_data = pd.DataFrame.from_dict(rev)
        try:
            review_data["reviews"] = review_data["reviews"].apply(lambda x: " ".join([i for i in x.split() if i != "\n" and detect(i) == "en"]))
        except:
            pass
        return review_data
