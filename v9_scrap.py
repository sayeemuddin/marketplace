import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.filterwarnings("ignore")
import pandas as pd
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import SB
from seleniumbase import BaseCase as bc
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session, mapped_column, Mapped, DeclarativeBase
from sqlalchemy import create_engine, String, exc
from dotenv import load_dotenv, find_dotenv
import random

BASEDIR = os.path.abspath(os.path.dirname(__file__))
USER_AGENTS_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2866.71 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2820.59 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2762.73 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36']

load_dotenv(os.path.join(BASEDIR, '.env'))

SQLALCHEMY_DATABASE_URI =os.getenv('SQLALCHEMY_DATABASE_URI')

engine = create_engine(SQLALCHEMY_DATABASE_URI)

class Base(DeclarativeBase):
    pass

class ProductsTable(Base):
    __tablename__ = "products_table"
    Product: Mapped[str] = mapped_column(String(8000),primary_key=True)
    Marketplace: Mapped[str] = mapped_column(String(8000),primary_key=True)
    Seller: Mapped[str] = mapped_column(String(8000),primary_key=True)
    Data_Date: Mapped[str] = mapped_column(String(8000),primary_key=True)
    Data_Time: Mapped[str] = mapped_column(String(8000),primary_key=True)
    Price: Mapped[str] = mapped_column(String(8000))
    Product_price: Mapped[str] = mapped_column(String(8000))
    Product_URL: Mapped[str] = mapped_column(String(8000),primary_key=True)

options = Options()
options.add_argument('--headless=new')
agent=random.choice(USER_AGENTS_LIST)
options.add_argument(f"user-agent={agent}")
options.add_argument('log-level=1')

def trendyol_get_value(market_place, product_name, url):
    driver = webdriver.Chrome(options=options )
    try:
        driver.get(url)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(1)
        try:
            policy = driver.find_element(By.ID,'onetrust-accept-btn-handler')
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
        if self_data:
            self_name = self_data.find('a',class_='seller-name-text').text.replace("\n", "")
        else:
            self_name = None
        self_price_box = soup.find('div',class_='product-price-container')
        if self_price_box:
            self_price = self_price_box.find('span',class_='prc-dsc').text.replace("\n", "")
        else:
            self_price = None
        self_org_price= self_price_box.find('span',class_='prc-org')
        if self_org_price:
            self_org_price=self_org_price.text.replace("\n", "")
        else:
            self_org_price= self_price
        
        data.append((market_place, self_name, self_org_price, self_price, url, product_name))

        more = soup.find_all('div',class_='pr-mc-w')
        if not more:
            print("More sellers button not found")
        
        m_url= url.split('/')[:3]
        separator = "//"
        f_url = separator.join(t for t in m_url if t)

        for item in more:
            o_seller_name= item.find('a', class_='seller-name-text')
            if o_seller_name:
                o_seller_name = o_seller_name.text
            else:
                o_seller_name = None
            o_seller_price = item.find('span','prc-dsc')
            if o_seller_price:
                o_seller_price =o_seller_price.text
            else:
                o_seller_price = None
            try:
                o_seller_url = f"{f_url}{item.find('a','pr-om-lnk-btn')['href']}"
            except:
                o_seller_url = None
            o_seller_org_price = item.find('span','prc-org')
            if o_seller_org_price:
                o_seller_org_price = o_seller_org_price.text
            else:
                o_seller_org_price = o_seller_price

            data.append((market_place, o_seller_name, o_seller_org_price, o_seller_price, o_seller_url,product_name))

        time.sleep(1)
        driver.quit()
        return data
    except Exception as e:
        # print(e)
        time.sleep(1)
        driver.quit()
        return False
    
def hepsiburada_get_value(market_place, product_name, url):
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(3)
        driver.maximize_window()
        time.sleep(2)
        try:
            policy = driver.find_element(By.ID,'onetrust-accept-btn-handler')
            policy.click()
        except Exception as e:
            print("GDPR policy banner not found")

        try:
            more = driver.find_element(By.ID,'merchantTabTrigger')
            more.click()
        except Exception as e:
            print("Show more sellers button not found.")
            
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        more = soup.find_all('tr',class_='merchant-list-item')
        if not more:
            print("More sellers button not found")
        data=[]
        time.sleep(3)

        for item in more:
            o_seller_name= item.find('a', class_='merchant-name')
            if o_seller_name:
                o_seller_name = o_seller_name.text.replace("\n", "")
            else:
                o_seller_name = None
            o_seller_price = item.find('span','product-price')
            if o_seller_price:
                o_seller_price =o_seller_price.text.replace("\n", "")
            else:
                o_seller_price = None
            try:
                prod_url =url.split('?')[0]
                o_seller_url = f"{prod_url}?magaza={o_seller_name}".replace("\n", "")
            except:
                o_seller_url = None
            o_seller_org_price = item.find('del','product-old-price')
            if o_seller_org_price:
                o_seller_org_price = o_seller_org_price.text.replace("\n", "")
            else:
                o_seller_org_price = o_seller_price

            data.append((market_place, o_seller_name, o_seller_org_price, o_seller_price, o_seller_url,product_name))

        time.sleep(1)
        driver.quit()
        # print("199",data)
        return data
    except Exception as e:
        print(e)
        time.sleep(1)
        driver.quit()
        return False
    
def vitaminer_get_value(market_place, product_name, url):
    def verify_success(sb):
        sb.assert_element('div.search-overlay', timeout=8)
        sb.sleep(4)
    data = []
    with SB(uc=True, guest_mode=True,headless=True) as sb:
        sb.open(url)
        try:
            verify_success(sb)
            if sb.is_element_visible('input[value*="Verify"]'):
                sb.click('input[value*="Verify"]')
            elif sb.is_element_visible('iframe[title*="challenge"]'):
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                try:
                    product_price_element = bc.find_element(sb,selector="span#product-price",by="css selector", timeout=15)
                    product_price = f'{product_price_element.text} TL'
                    # print("Product Discounted Price:", product_price)
                except:
                    product_price = None
                try:
                    product_old_price_element = bc.find_element(sb,selector="span.product-old-price",by="css selector", timeout=15)
                    product_old_price = product_old_price_element.text
                    # print("Product Original Price:", product_old_price)
                except:
                    product_old_price = product_price
                data.append((market_place, market_place, product_old_price, product_price, url,product_name))
                return data
            else:
                print("Bot Detected!")
                return False
        except Exception:
            if sb.is_element_visible('input[value*="Verify"]'):
                sb.click('input[value*="Verify"]')
            elif sb.is_element_visible('iframe[title*="challenge"]'):
                sb.switch_to_frame('iframe[title*="challenge"]')
                sb.click("span.mark")
                try:
                    product_price_element = bc.find_element(sb,selector="span#product-price",by="css selector", timeout=15)
                    product_price = f'{product_price_element.text} TL'
                    # print("Product Discounted Price:", product_price)
                except:
                    product_price = None
                try:
                    product_old_price_element = bc.find_element(sb,selector="span.product-old-price",by="css selector", timeout=15)
                    product_old_price = product_old_price_element.text
                    # print("Product Original Price:", product_old_price)
                except:
                    product_old_price = product_price
                data.append((market_place, market_place, product_old_price, product_price, url,product_name))
                return data
            else:
                print("Bot Detected!")
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
        timed = time_stamp.split('_')[1:]
        separator = ":"
        time_data = separator.join(t for t in timed if t)
        
        with Session(engine) as session:
            for record in data:
                if not record[3]:
                    print(f'Could not scrap {product_name} from {record[0]}. Skipping...')
                    return False
                new_product = ProductsTable(
                    Marketplace = record[0],
                    Seller = record[1],
                    Price = record[2],
                    Product_price = record[3],
                    Product_URL = record[4],
                    Product = product_name,
                    Data_Date = time_stamp.split('_')[0],
                    Data_Time = time_data
                )
                session.add(new_product)
                try:
                    session.commit()
                    time.sleep(.2)
                except exc.IntegrityError as e:
                    print(e)
                    session.rollback()
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    from concurrent.futures import ThreadPoolExecutor
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

        if market_name.lower() == 'trendyol':
            result = trendyol_get_value(market_name, prd, p_url)
            if result:
                write_data_to_csv(result,time_stamp)
                write_data_to_db(result,time_stamp,prd)

            else:
                result = trendyol_get_value(market_name, prd, p_url)
                if result:
                    write_data_to_csv(result, time_stamp)
                    write_data_to_db(result,time_stamp,prd)
                else:
                    print(f"There was an error in scrapping {prd}, we may need to modify the script")

        elif market_name.lower() == 'hepsiburada':
            result = hepsiburada_get_value(market_name, prd, p_url)

            if result:
                write_data_to_csv(result,time_stamp)
                write_data_to_db(result,time_stamp,prd)

            else:
                result = hepsiburada_get_value(market_name, prd, p_url)
                if result:
                    write_data_to_csv(result, time_stamp)
                    write_data_to_db(result,time_stamp,prd)
                else:
                    print(f"There was an error in scrapping {prd}, we may need to modify the script")
        elif market_name.lower() == 'vitaminler.com':
            result = vitaminer_get_value(market_name, prd, p_url)
            if result:
                write_data_to_csv(result,time_stamp)
                write_data_to_db(result,time_stamp,prd)
            else:
                result = hepsiburada_get_value(market_name, prd, p_url)
                if result:
                    write_data_to_csv(result, time_stamp)
                    write_data_to_db(result,time_stamp,prd)
                else:
                    print(f"There was an error in scrapping {prd}, we may need to modify the script")
    print(f"Time taken to scrap data:{int(time.time()-start)} seconds")
