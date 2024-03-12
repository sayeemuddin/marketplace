from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

options = Options()
options.add_argument('--headless=new')

# prod_url = "https://www.trendyol.com/immunace/original-30-tablet-multivitamin-p-6476572?merchantId=753766"
# product_name=url.split('trendyol.com/')[1].split('/')[0]
# print(product_name)

def get_value(market_place, product_name,url):
    product_name=url.split('trendyol.com/')[1].split('/')[0]
    driver = webdriver.Chrome( )
    try:

        driver.get(url)
        # driver.execute_script("document.body.style.zoom='33%'")
        # other_sellers = driver.find_elements(By.CLASS_NAME,'seller-name-text')
        # other_prices = driver.find_elements(By.CLASS_NAME,'prc-dsc')
        # new_dict = {seller.text: price.text for seller,
        #     price in zip(other_sellers, other_prices)}
        # print(new_dict)
        time.sleep(2)
        driver.maximize_window()
        time.sleep(1)
        policy = driver.find_element(By.ID,'onetrust-accept-btn-handler')
        if True or policy.is_displayed():
            try:
                policy.click()
            except Exception as e:
                print(e)
        else:
            pass
    #     element = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME,'omc-mr-btn'))
    # )
    #     element.click()
        try:
            more = driver.find_element(By.CLASS_NAME,'omc-mr-btn')
            print("More>>>>>>>>> ",more.text)
            while not more.is_displayed():
                print("Scrolling down...")
                driver.execute_script("window.scrollBy(0, 250);")
        except Exception as e:
            print(e)
        
        
        if True:
            print('Button displayed')
            time.sleep(2)
            try:
                more = driver.find_element(By.CLASS_NAME,'omc-mr-btn')
                more.click()
            except Exception as e:
                print(e)
        else:
          pass
        # other_sellers = WebDriverWait(driver, 10).until(
        # EC.element_located_to_be_selected((By.CLASS_NAME,'seller-name-text'))
    # )
        time.sleep(2)
        driver.execute_script("window.scrollBy(0, 250);")
        other_sellers = driver.find_elements(By.CLASS_NAME,'seller-name-text')
        other_sellers.pop(0)
        other_prices = driver.find_elements(By.CLASS_NAME,'prc-dsc')
        other_prices.pop(0)
        other_urls= driver.find_elements(By.CLASS_NAME,'pr-om-lnk-btn')
        data  = list(zip(other_sellers,other_prices,other_urls))
        data =[(seller.text,price.text,url.get_attribute('href')) for seller, price, url in data]
        df = pd.DataFrame(data, columns = ['Seller','Price', 'Product URL'])
        df = df.assign(Product_Name=product_name)
        df.to_csv(f"{time.time()}_output.csv",index=False, encoding='utf-8')
        # df = pd.DataFrame()
        # for seller, price, url in zip(other_sellers,other_prices,other_urls):
    

        # header_list = ['Product Name','Seller','Price', 'Product URL']

        # for seller in other_sellers:
        #     print(f"Other Sellers: Price>>>>>>> ,{seller.text}:{price.text}")
        time.sleep(400)
        driver.quit()
        return True
    except Exception as e:
        print(e)
        time.sleep(400)
        driver.quit()
        return str(e)
    
# import openpyxl

# wb = openpyxl.load_workbook('input.xlsx')
# sheets = wb.sheetnames
# ws = wb[sheets[0]]
# # Deprecation warning
# # ws = wb.get_sheet_by_name('Sheet1')
# # print(ws.cell(row=2, column=1).hyperlink.target)
# t = ws.cell(row=3, column=3).hyperlink
# print(t.target)
input_df =pd.read_excel('input.xlsx', sheet_name='Sheet1', header=0)
# input_df =input_df.reset_index()
list_inp = input_df.values.tolist()
print(list_inp[0])
market_name, prd, p_url =list_inp[0]
get_value(market_name, prd, 'https://www.trendyol.com/immunace/original-30-tablet-multivitamin-p-6476572?boutiqueId=61&merchantId=844385')