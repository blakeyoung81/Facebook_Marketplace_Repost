#facebook marketplace 
from selenium import webdriver
from time import sleep
import pymongo
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

class App:
    def __init__(self, email= "", password= "", 
                 path=r'C:\Users\blake\OneDrive\Desktop\Coding\Python\Projects\Facebook_Marketplace'):
        self.email = "blakeyoung81@gmail.com"
        self.password = "Teancum2011425"
        self.path = path
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r"C:\Users\blake\OneDrive\Desktop\Coding\Python\Projects\Dependencies\chromedriver.exe")
        self.main_url = "https://www.facebook.com"
        self.client = pymongo.MongoClient("localhost", 27017)
        self.driver.get(self.main_url)
        self.log_in()
        self.used_item_links = []
        list = self.scrape_item_links()
        self.scrape_item_details(list)
        self.driver.quit()
        
        
    def log_in(self):
        try:
            email_input = self.driver.find_element_by_id("email")
            email_input.send_keys(self.email)
            #sleep(0.5)
            password_input = self.driver.find_element_by_id("pass")
            password_input.send_keys(self.password)
            #sleep(0.5)
            login_button = self.driver.find_element_by_xpath("//*[@type='submit']")
            login_button.click()
            #sleep(1)
        except:
            print('Some exception occurred while trying to find username or password field')

    def scrape_item_links(self):
        marketplace_button = self.driver.find_element_by_xpath('//div[contains(text(), "Marketplace")]')
        marketplace_button.click()
        #create a list of each section and loop through list
        sections = [
                    self.driver.find_element_by_xpath('//div[contains(text(), "Vehicles")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Rentals")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Electronics")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Home & Garden")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Hobbies")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Entertainment")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Clothing & Accessories")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Classifieds")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Family")]'),
                    self.driver.find_element_by_xpath('//div[contains(text(), "Deals")]'),
                    ]

        for category in sections:
            #self.driver.implicitly_wait(300)
            category.click()
            #Get every single Selenium web item in a list up to 100
            scrolls = 2
            for i in range(scrolls):
                try:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(.5)
                except:
                    pass
                
            full_items_list = self.driver.find_elements_by_xpath("//a[@class='_1oem']")

            if self.used_item_links == 0 or self.used_item_links is None: #False or None?
                self.used_item_links = [item.get_attribute('href') for item in full_items_list]
            else:
                #append or extend or add?
                self.used_item_links = self.used_item_links.extend([item.get_attribute('href') for item in full_items_list])

            #wait = WebDriverWait(self.driver, 10)
            #category_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, category.get_attribute('class'))))
            #category_element.click()
            print("finished making the list range("+str(scrolls)+") is done")
            for item in full_items_list:
                href = item.get_attribute('href')
                print(href)
        print(self.used_item_links)
        return self.used_item_links

    def scrape_item_details(self, used_item_links):
        print("next command started")
        print("the passed in variables are self = ", self, "used item links", used_item_links)
        #db = self.client["LOCAL_USED_ITEMS"]
        #Facebook_Marketplace = db[Facebook]
        # db = self.client["LOCAL_USED_ITEMS"]
        # collection = db["Facebook"]
        # data = {'Name:': "Blake"}
        # collection.insert_one(data)
        for url in used_item_links:
            images = []
            driver.get(url)
            sleep(0.5)
            url = url
            try:
                image_element = driver.find_element_by_xpath('//img[contains(@class, "_5m")]')
                images = [image_element.get_attribute('src')]
            except:
                images = ""
            try:
                title = driver.find_element_by_xpath('//div[contains(@class, " _50f")]/span').text
            except:
                title = ""
            try:
                date_time = driver.find_element_by_xpath('//a[@class="_r3j"]').text
            except:
                date_time = ""
            try:
                location =  driver.find_element_by_xpath('//span[@class="_7yi"]').text
            except:
                location = ""
            try:
                price = driver.find_element_by_xpath('//div[contains(@class, "_5_md")]').text
            except:
                price = ""
            try:
                if driver.find_element_by_xpath("//a[@title='More']").is_displayed():
                    driver.find_element_by_xpath("//a[@title='More']").click()
                description = driver.find_element_by_xpath('//p[@class="_4etw"]/span').text
            except:
                description = ""

            try:
                previous_and_next_buttons = driver.find_elements_by_xpath("//i[contains(@class, '_3ffr')]")
                next_image_button = previous_and_next_buttons[1]
                while next_image_button.is_displayed():
                    next_image_button.click()
                    image_element = driver.find_element_by_xpath('//img[contains(@class, "_5m")]')
                    sleep(1)   
                    if image_element.get_attribute('src') in images:
                        break
                    else:
                        images.append(image_element.get_attribute('src'))
            except:
                pass
     
             
                 
        db.Facebook_items.insert({ 'Url': url,
                         'Images': images,
                         'Title': title,
                         'Description': description,
                         'Date_Time': date_time,
                         'Location': location,
                         'Price': price,          
                        })
                 
        print({ 'Url': url,
                         'Images': images,
                         'Title': title,
                         'Description': description,
                         'Date_Time': date_time,
                         'Location': location,
                         'Price': price,
                        })



if __name__ == '__main__':
    app = App()