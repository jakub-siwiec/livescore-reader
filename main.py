from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Livescore_Driver:
    def __init__(self):
        self._PATH = "./chromedriver"
        self._container_attribute = "[data-type=\"container\"]"
        self._title_attribute = "[data-type=\"stg\"]"
        self._game_attribute = "[data-type=\"evt\"]"
        self._full_games_attributes = self._title_attribute + ", " + self._game_attribute

        # Member variables used later
        self._leagues_array = []
        self._driver = None

    def __run_driver(self):
        self._driver = webdriver.Chrome(self._PATH)
        self._driver.get("https://www.livescore.com/")
        self._driver.implicitly_wait(5)

    def __page_reader(self):
        driver_livescore_read = WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self._container_attribute)))
        results = driver_livescore_read.find_elements_by_css_selector(
            self._full_games_attributes)
        return results

    def __data_conversion(self, results):
        for item in results:
            if item.get_attribute("data-type") == "stg":
                item_text = item.text.split(" - ")
                self._leagues_array.append({
                    "location": item_text[0].title(),
                    "name": item_text[1].split("\n")[0].title(),
                    "games": {
                        "date": item_text[1].split("\n")[1].title(),
                        "list": []
                    }
                })
            if item.get_attribute("data-type") == "evt":
                item_text = item.text.split("\n")
                self._leagues_array[len(self._leagues_array) - 1]["games"]["list"].append({
                    "state": item_text[0],
                    "homeTeam": item_text[1],
                    "awayTeam": item_text[3],
                    "result": item_text[2]
                })

    def __run_data(self):
        self.__run_driver()
        try:
            result = self.__page_reader()
            self.__data_conversion(result)
        finally:
            self._driver.quit()

    def get_results(self):
        self.__run_data()
        return self._leagues_array


x = Livescore_Driver()
y = x.get_results()
print(y)
