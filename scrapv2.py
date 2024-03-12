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
            while not more.is_displayed():
                driver.execute_script("window.scrollBy(0, 250);")
        except Exception as e:
            print("Show more sellers button not found.")
        
        # time.sleep(2)
        try:
            more = driver.find_element(By.CLASS_NAME,'omc-mr-btn')
            more.click()
        except Exception as e:
            print("Show more sellers button not found.")

        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 250);")
        time.sleep(2)
        data=[]
        o_sellers = driver.find_elements(By.CLASS_NAME,'pr-mc-w')
        self_data = driver.find_element(By.CLASS_NAME,'product-seller-line')
        self_name = self_data.find_element(By.CLASS_NAME,'seller-name-text').text
        self_price_tag = driver.find_element(By.CLASS_NAME,'product-price-container')
        self_price = self_price_tag.find_element(By.CLASS_NAME,'prc-dsc').text
        try:
            self_org_pric= self_price_tag.find_element(By.CLASS_NAME,'prc-org').text
        except Exception as e:
            self_org_pric = self_price

        data.append((market_place, self_name, self_org_pric, self_price, url, product_name))
        
        for o_seller in o_sellers:
            o_seller_name= o_seller.find_element(By.CLASS_NAME,'seller-name-text').text
            o_seller_price = o_seller.find_element(By.CLASS_NAME,'prc-dsc').text
            o_seller_url = o_seller.find_element(By.CLASS_NAME,'pr-om-lnk-btn')
            o_seller_url = o_seller_url.get_attribute('href')
            try:
                o_seller_org_price = o_seller.find_element(By.CLASS_NAME,'prc-org').text
            except Exception as e:
                o_seller_org_price = o_seller_price

            data.append((market_place, o_seller_name, o_seller_org_price, o_seller_price, o_seller_url,product_name))

        df = pd.DataFrame(data, columns = ['Market Place','Seller','Original Price','Discounted Price', 'Product URL','Product Name'])

        file_exists = os.path.isfile(f"{time_stamp}_output.csv")
        if file_exists:
            df.to_csv(f"{time_stamp}_output.csv", mode='a', index=False, header=False, encoding='utf-8')
        else:
            df.to_csv(f"{time_stamp}_output.csv", mode='a', index=False, header=True, encoding='utf-8')

        time.sleep(1)
        driver.quit()
        return True
    except Exception as e:
        # print(e)
        time.sleep(1)
        driver.quit()
        return False
    
if __name__ == '__main__':

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
        retry=False
        result = get_value(market_name, prd, p_url)

        if not result and retry:
            result = get_value(market_name, prd, p_url)
            if not result:
                print(f"There was an error in scrapping {prd}, we may need to modify the script")
