from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


driver = webdriver.Chrome("/usr/local/bin/chromedriver")


driver.get("https://modesto.craigslist.org/search/farmington-ca/bia?query=transition&lat=38.04809106745726&lon=-120.88256835937501&search_distance=135")


content = driver.page_source
soup = BeautifulSoup(content)


product_id = []
product_name = []
product_price = []
product_location = []
product_distance = []
pub_date = []
pub_link = []

for li in soup.findAll('li', href=False, attrs={'class':'result-row'}):
    title = li.find("div", attrs={"class": "result-info"}).find("a", attrs={"class": "result-title hdrlnk"})
    date = li.find("div", attrs={"class": "result-info"}).find("time", attrs={"class": "result-date"})

    price = li.find("div", attrs={"class": "result-info"}).find("span", attrs={"class": "result-price"})
    location = li.find("div", attrs={"class": "result-info"}).find("span", attrs={"class": "nearby"})
    distance = li.find("div", attrs={"class": "result-info"}).find("span", attrs={"class": "maptag"})
    
    if "transition" in title.text.lower() and "spur" in title.text.lower():
        print("Hola")
        product_name.append(title.text)
        product_id.append(title.attrs["data-id"])
        pub_link.append(title.attrs["href"])
        pub_date.append(date.attrs["datetime"])
        product_price.append(price.text)
        product_location.append(location.text) 
        product_distance.append(distance.text)



product_name


df = pd.DataFrame([product_id, product_name, product_price, product_location, product_distance, pub_date, pub_link], index=["id", "name", "price", "location", "distance", "date", "url"]).T
print(df.name.values)


def pretty_print():
    


if df.shape[0] > 0:
    print("I found the following ads:")
    for k, row in df.iterrows():
        print(f"Result ({k+1})")
        print("\tAd   : ", row["name"])
        print("\tPrice: ", row["price"])
        print("\tDist : ", row["distance"])
        print("\tLoc  : ", row["location"])
        print("\tLink : ", row["url"])
        



