from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import argparse


def main(brand="transtion", model="spur"):
    with webdriver.Chrome("/usr/local/bin/chromedriver") as driver:
        search = f"{brand}+{model}"
        distance = 135
        url = (
            f"https://modesto.craigslist.org/search/farmington-ca/bia?query="
            f"{search}&lat=38.04809106745726&lon=-120.88256835937501&"
            f"search_distance={distance}"
        )
        driver.get(url)

        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

    product_id = []
    product_name = []
    product_price = []
    product_location = []
    product_distance = []
    pub_date = []
    pub_link = []

    for li in soup.findAll('li', href=False, attrs={'class': 'result-row'}):
        title = li.find("div", attrs={"class": "result-info"}).find(
            "a", attrs={"class": "result-title hdrlnk"}
        )
        date = li.find("div", attrs={"class": "result-info"}).find(
            "time", attrs={"class": "result-date"}
        )

        price = li.find("div", attrs={"class": "result-info"}).find(
            "span", attrs={"class": "result-price"}
        )
        location = li.find("div", attrs={"class": "result-info"}).find(
            "span", attrs={"class": "nearby"}
        )
        distance = li.find("div", attrs={"class": "result-info"}).find(
            "span", attrs={"class": "maptag"}
        )

        if brand in title.text.lower() and model in title.text.lower():
            product_name.append(title.text)
            product_id.append(title.attrs["data-id"])
            pub_link.append(title.attrs["href"])
            pub_date.append(date.attrs["datetime"])
            product_price.append(price.text)
            product_location.append(location.text)
            product_distance.append(distance.text)

    df = pd.DataFrame(
        [
            product_id,
            product_name,
            product_price,
            product_location,
            product_distance,
            pub_date,
            pub_link,
        ],
        index=["id", "name", "price", "location", "distance", "date", "url"],
    ).T

    if df.shape[0] > 0:
        print("I found the following ads:")
        for k, row in df.iterrows():
            print(f"Result ({k+1})")
            print("\tAd   : ", row["name"])
            print("\tPrice: ", row["price"])
            print("\tDist : ", row["distance"])
            print("\tLoc  : ", row["location"])
            print("\tLink : ", row["url"])

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Check Craglist")
    parser.add_argument(
        "--brand",
        dest="brand",
        type=str,
        default="transition",
        help="Bike model",
    )
    parser.add_argument(
        "--model",
        dest="model",
        type=str,
        default="spur",
        help="Brand model",
    )
    args = parser.parse_args()
    main(brand=args.brand, model=args.model)
