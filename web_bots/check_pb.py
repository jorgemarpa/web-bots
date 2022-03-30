from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from bs4 import BeautifulSoup
import pandas as pd
import argparse


def main(brand="transtion", model="spur"):

    brand_ = brand.replace(" ", "%20") if " " in brand else brand
    model_ = model.replace(" ", "%20") if " " in model else model
    search = f"{brand_}%20{model_}"
    distance = 135
    url = (
        f"https://www.pinkbike.com/buysell/list/?lat=37.8292&"
        f"lng=-121.0305&distance={distance}&"
        f"q={search}&category=2"
    )
    with webdriver.Chrome(service=Service("/usr/local/bin/chromedriver")) as driver:
        driver.get(url)

        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")

    product_id = []
    product_name = []
    product_condition = []
    frame_size = []
    product_price = []
    pub_link = []
    product_location = []

    for div in soup.findAll('div', href=False, attrs={'class': 'bsitem'}):
        title = div.find(
            "a", attrs={"style": "font-size: 18px;font-weight:bold;color:#000000"}
        ).text
        link = div.find("a").attrs["href"]
        condition = div.findAll("div")[1].text.split(":")[-1].strip()
        fsize = div.findAll("b")[1].next_sibling.strip()

        price = div.findAll("b")[-2].text

        location = div.findAll("img")[-1].next_element.strip()

        if brand in title.lower() and model in title.lower():
            product_id.append(div.attrs["id"])
            product_name.append(title)
            product_condition.append(condition)
            frame_size.append(fsize)

            pub_link.append(link)

            product_price.append(price)
            product_location.append(location)

    df = pd.DataFrame(
        [
            product_id,
            product_name,
            product_condition,
            product_price,
            product_location,
            pub_link,
        ],
        index=["id", "name", "condition", "price", "location", "url"],
    ).T

    if df.shape[0] > 0:
        print(f"I found the following ads for {brand} {model} in PinkBike:")
        for k, row in df.iterrows():
            print(f"Result ({k+1})")
            print("\tAd       : ", row["name"])
            print("\tPrice    : ", row["price"])
            print("\tCondition: ", row["condition"])
            print("\tLoc      : ", row["location"])
            print("\tLink     : ", row["url"])
            print("_______________________________" * 2)
    else:
        print(f"I found no ads for {brand} {model}:")

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
