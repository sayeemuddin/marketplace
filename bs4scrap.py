from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from db_conn import engine, ProductsTable, Base
from sqlalchemy.orm import Session

options = Options()
options.add_argument('--headless=new')
options.add_argument('log-level=3')

def get_value(market_place, product_name, url):
    driver = webdriver.Chrome(options=options )
    try:
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(1)
        policy = driver.find_element(By.ID,'onetrust-accept-btn-handler')
        try:
            policy.click()
        except Exception as e:
            print("GDPR policy banner not found")

        try:
            more = driver.find_element(By.CLASS_NAME,'omc-mr-btn')
            more.click()
        except Exception as e:
            print("Show more sellers button not found.")

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        data=[]

        self_data = soup.find('div',class_='product-seller-line')
        self_name = self_data.find('a',class_='seller-name-text').text
        self_price_box = soup.find('div',class_='product-price-container')
        self_price = self_price_box.find('span',class_='prc-dsc').text
        self_org_price= self_price_box.find('span',class_='prc-org')
        if self_org_price:
            self_org_price=self_org_price.text
        else:
            self_org_price= self_price
        
        data.append((market_place, self_name, self_org_price, self_price, url, product_name))


        more = soup.find_all('div',class_='pr-mc-w')
        if not more:
            print("More sellers button not found")
        
        for item in more:
            # sellers_name = soup.find("item", { "class" : "seller-name-text" }).find("a", recursive=False)
            o_seller_name= item.find('a', class_='seller-name-text').text
            o_seller_price = item.find('span','prc-dsc').text
            o_seller_url = item.find('a','pr-om-lnk-btn')['href']
            o_seller_org_price = item.find('span','prc-org')
            if o_seller_org_price:
                o_seller_org_price = o_seller_org_price.text
            else:
                o_seller_org_price = o_seller_price

            # print(o_seller_name, o_seller_price, o_seller_url, o_seller_org_price)

            data.append((market_place, o_seller_name, o_seller_org_price, o_seller_price, o_seller_url,product_name))

        time.sleep(1)
        driver.quit()
        return data
    except Exception as e:
        # print(e)
        time.sleep(1)
        driver.quit()
        return False


def write_data_to_csv(data,time_stamp):
        df = pd.DataFrame(data, columns = ['Market Place','Seller','Original Price','Discounted Price', 'Product URL','Product Name'])

        file_exists = os.path.isfile(f"{time_stamp}_output.csv")
        if file_exists:
            df.to_csv(f"{time_stamp}_output.csv", mode='a', index=False, header=False, encoding='utf-8')
        else:
            df.to_csv(f"{time_stamp}_output.csv", mode='a', index=False, header=True, encoding='utf-8')
        return True

def write_data_to_db(data,time_stamp, product_name):
        with Session(engine) as session:
            for record in data:
                new_product = ProductsTable(
                    Seller = record[1],
                    Price = record[2],
                    Product_price = record[3],
                    Product_URL = record[4],
                    Product = product_name,
                    Data_Date = time_stamp.split('_')[0],
                    Data_Time = time_stamp.split('_')[1]
                )
                session.add(new_product)
            session.commit()

if __name__ == '__main__':

    Base.metadata.create_all(engine)
    start = time.time()
    time_stamp= str(datetime.now()).split('.')[0].replace(':',"_").replace(' ','_')

    if os.path.isfile('input.xlsx'):
        input_df =pd.read_excel('input.xlsx', sheet_name='Sheet1', header=0)
    else:
        print("Could not find input.xlsx file to read, please make sure it exists in the same directory")
        exit(1) 
    list_inp = input_df.values.tolist()

    for record in list_inp:
        header=True
        market_name, prd, p_url = record

        result = get_value(market_name, prd, p_url)
        if result:
            # write_data_to_csv(result,time_stamp)
            write_data_to_db(result,time_stamp,prd)

        else:
            result = get_value(market_name, prd, p_url)
            if result:
                # write_data_to_csv(result, time_stamp)
                write_data_to_db(result,time_stamp,prd)
            else:
                print(f"There was an error in scrapping {prd}, we may need to modify the script")
    print(f"Time taken to scrap data:{int(time.time()-start)} seconds")