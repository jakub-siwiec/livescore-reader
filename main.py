from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Livescore_Driver:
    def __init__(self):
        self.PATH = "./chromedriver"
        self.all_day_results = ""
        self.leagues_array = []
        driver = webdriver.Chrome(self.PATH)
        driver.get("https://www.livescore.com/")

        try:
            driver_livescore_read = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-type=\"container\"]")))

            self.all_day_results = driver_livescore_read.text

            results = driver_livescore_read.find_elements_by_css_selector(
                "[data-type=\"stg\"], [data-type=\"evt\"]")

            for item in results:
                if item.get_attribute("data-type") == "stg":
                    self.leagues_array.append({
                        "name": item.text,
                        "games": []
                    })

                if item.get_attribute("data-type") == "evt":
                    self.leagues_array[len(self.leagues_array) -
                                       1]["games"].append(item.text)

        finally:
            driver.quit()

    def get_day_result(self):
        return self.all_day_results

    def get_exp_res(self):
        return self.leagues_array


x = Livescore_Driver()
y = x.get_exp_res()
print(y)
# print(y)
