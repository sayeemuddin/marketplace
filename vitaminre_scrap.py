from seleniumbase import SB
from seleniumbase import BaseCase as bc
from selenium import webdriver

def verify_success(sb):
    sb.assert_element('div.search-overlay', timeout=8)
    sb.sleep(4)

with SB(uc=True, guest_mode=True,headless=False) as sb:
    sb.open("https://www.vitaminler.com/urun/natures-supreme-tonalin-cla-1250-mg-60-yumusak-kapsul-7315")
    try:
        verify_success(sb)
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.click('input[value*="Verify"]')
        elif sb.is_element_visible('iframe[title*="challenge"]'):
            sb.switch_to_frame('iframe[title*="challenge"]')
            sb.click("span.mark")
            product_price_element = bc.find_element(sb,selector="span#product-price",by="css selector", timeout=15)
            product_price = product_price_element.text
            print("Product Discounted Price:", product_price)
            product_old_price_element = bc.find_element(sb,selector="span.product-old-price",by="css selector")
            product_old_price = product_old_price_element.text
            print("Product Original Price:", product_old_price)
        else:
            raise Exception("Detected!")
    except Exception:
        if sb.is_element_visible('input[value*="Verify"]'):
            sb.click('input[value*="Verify"]')
        elif sb.is_element_visible('iframe[title*="challenge"]'):
            sb.switch_to_frame('iframe[title*="challenge"]')
            sb.click("span.mark")
            product_price_element = bc.find_element(sb,selector="span#product-price",by="css selector", timeout=15)
            product_price = product_price_element.text
            print("Product Discounted Price:", product_price)
            product_old_price_element = bc.find_element(sb,selector="span.product-old-price",by="css selector")
            product_old_price = product_old_price_element.text
            print("Product Original Price:", product_old_price)
        else:
            raise Exception("Detected!")
        # try:
        #     verify_success(sb)
        # except Exception:
        #     raise Exception("Detected!")
        
    
    def fetch_data():
        pass