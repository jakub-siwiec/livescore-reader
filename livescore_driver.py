from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class LivescoreDriver:
    def __init__(self, games_date=""):
        self._PATH = "./chromedriver"
        self._LIVESCORE_ADDRESS = "https://www.livescore.com/" + \
            (games_date if games_date == "" else "soccer/" + games_date + "/")
        self._container_attribute_name = "data-type"
        self._container_attribute_value = "container"
        self._container_attribute = "[" + self._container_attribute_name + \
            "=\"" + self._container_attribute_value + "\"]"
        self._title_attribute_name = "data-type"
        self._title_attribute_value = "stg"
        self._title_attribute = "[" + self._title_attribute_name + \
            "=\"" + self._title_attribute_value + "\"]"
        self._game_attribute_name = "data-type"
        self._game_attribute_value = "evt"
        self._game_attribute = "[" + self._game_attribute_name + \
            "=\"" + self._game_attribute_value + "\"]"
        self._full_games_attributes = self._title_attribute + ", " + self._game_attribute

        # Member variables used later
        self._leagues_array = []
        self._driver = None

    def __run_driver(self):
        self._driver = webdriver.Chrome(self._PATH)
        self._driver.get(self._LIVESCORE_ADDRESS)
        self._driver.implicitly_wait(5)

    def __page_reader(self):
        driver_livescore_read = WebDriverWait(self._driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self._container_attribute)))
        results = driver_livescore_read.find_elements_by_css_selector(
            self._full_games_attributes)
        return results

    def __create_new_competition_place(self, competition_place, name, date):
        self._leagues_array.append(
            {
                "competitionPlace": competition_place,
                "competitions": [
                    {
                        "name": name,
                        "games": [
                            {
                                "date": date,
                                "listGames": []
                            }
                        ]
                    }
                ]
            }
        )

    def __create_new_competition(self, name, date, index_competition_place):
        self._leagues_array[index_competition_place]["competitions"].append(
            {
                "name": name,
                "games": [
                    {
                        "date": date,
                        "listGames": []
                    }
                ]
            }
        )

    def __create_new_date(self, date, index_competition_place, index_competition):
        self._leagues_array[index_competition_place]["competitions"][index_competition]["games"].append(
            {
                "date": date,
                "listGames": []
            }
        )

    def __create_new_game(self, current_state, home_team, away_team, result, index_competition_place, index_competition, index_date):
        self._leagues_array[index_competition_place]["competitions"][index_competition]["games"][index_date]["listGames"].append(
            {
                "currentState": current_state,
                "homeTeam": home_team,
                "awayTeam": away_team,
                "result": result
            }
        )

######### START NEW #########

    def __get_league_array_element(self, index_competition_place, index_name=None, index_date=None):
        if index_competition_place != None and index_name != None and index_date != None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_date]
        elif index_competition_place != None and index_name != None and index_date == None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]
        elif index_competition_place != None and index_name == None and index_date == None:
            return self._leagues_array[index_competition_place]
        else:
            raise TypeError("Indices cannot be None if not allowed")

    def __get_competition_place_array_length(self):
        return len(self._leagues_array)

    def __get_competition_array_length(self, index_competition_place):
        return len(self._leagues_array[index_competition_place]["competitions"])

    def __get_date_array_length(self, index_competition_place, index_competition):
        return len(self._leagues_array[index_competition_place]["competitions"][index_competition]["games"])

    def __get_item_index(self, array_to_check, item_to_find):
        index = None

        for item_index, item in enumerate(array_to_check):
            if item["competitionPlace"] == item_to_find:
                index = item_index

        return index

######### END NEW #########

    def __get_competition_place_index(self, competition_place, name, date):
        index = None

        for index_competition_place, place in enumerate(self._leagues_array):
            if (place["competitionPlace"] == competition_place):
                index = index_competition_place

        return index

    def __get_competition_index(self, competition_place, name, date):
        index = None

        index_competition_place = self.__get_competition_place_index(
            competition_place, name, date)

        if index_competition_place == None:
            return None
        else:
            for index_competition, competition in enumerate(self._leagues_array[index_competition_place]["competitions"]):
                if (competition["name"] == name):
                    index = index_competition

        return {"indexCompetitionPlace": index_competition_place, "indexCompetition": index}

    def __get_date_index(self, competition_place, name, date):
        index = None
        index_competition_place = None
        index_competition = None
        indices_competition = self.__get_competition_index(
            competition_place, name, date)
        if indices_competition != None:
            index_competition_place = indices_competition["indexCompetitionPlace"]
            index_competition = indices_competition["indexCompetition"]

        if indices_competition == None:
            return None
        elif index_competition_place != None and index_competition == None:
            return {"indexCompetitionPlace": index_competition_place, "indexCompetition": None, "indexDate": None}
        else:
            for index_date, game in enumerate(self._leagues_array[index_competition_place]["competitions"][index_competition]["games"]):
                if (game["date"] == date):
                    index = index_date

        return {"indexCompetitionPlace": index_competition_place, "indexCompetition": index_competition, "indexDate": index}

    def __insert_data_title(self, competition_place, name, date):
        index_competition_place = None
        index_competition = None
        index_date = None
        indices = self.__get_date_index(competition_place, name, date)
        if indices != None:
            index_competition_place = indices["indexCompetitionPlace"]
            index_competition = indices["indexCompetition"]
            index_date = indices["indexDate"]

        if indices == None:
            self.__create_new_competition_place(competition_place, name, date)
        elif index_competition_place != None and index_competition == None:
            self.__create_new_competition(name, date, index_competition_place)
        elif index_competition_place != None and index_competition != None and index_date == None:
            self.__create_new_date(
                date, index_competition_place, index_competition)

        return indices

    def __insert_data(self, results):
        _competition_place = None
        _competition = None
        _date = None
        _indices = None
        for item in results:
            # Assigning a title
            if item.get_attribute(self._title_attribute_name) == self._title_attribute_value:
                item_text = item.text.split(" - ")
                _competition_place = item_text[0].title()
                _competition = item_text[1].split("\n")[0].title()
                _date = item_text[1].split("\n")[1].title()
                _indices = self.__insert_data_title(
                    _competition_place, _competition, _date)
            # Assigning a game
            if item.get_attribute(self._game_attribute_name) == self._game_attribute_value:
                item_text = item.text.split("\n")
                _current_state = item_text[0]
                _home_team = item_text[1]
                _away_team = item_text[3]
                _result = item_text[2]
                _index_competition_place = len(
                    self._leagues_array) - 1 if _indices == None else _indices["indexCompetitionPlace"]
                _index_competition = len(
                    self._leagues_array[_index_competition_place]["competitions"]) - 1 if _indices == None or _indices["indexCompetition"] == None else _indices["indexCompetition"]
                # if _indices == None:
                #     _max_index_competition_place = len(self._leagues_array) - 1
                #     _max_index_competition = len(
                #         self._leagues_array[_max_index_competition_place]["competitions"])
                #     _max_index_date = len(
                #         self._leagues_array[_max_index_competition_place]["competitions"][_max_index_competition]["games"])
                #     self.__create_new_game(
                #         _current_state, _home_team, _away_team, _result, _max_index_competition_place, _max_index_competition, _max_index_date)
                # elif _indices != None:
                #     _max_index_competition_place = _indices["indexCompetitionPlace"]
                #     if _indices["indexCompetition"] == None:
                #         _max_index_competition = len(
                #             self._leagues_array[_max_index_competition_place]["competitions"])
                #         _max_index_date = len(
                #             self._leagues_array[_max_index_competition_place]["competitions"][_max_index_competition]["games"])

    def __data_conversion(self, results):
        # Predeclaring variables because of necessary access in various scopes
        _location = None
        _name = None
        _date = None
        for item in results:
            if item.get_attribute(self._title_attribute_name) == self._title_attribute_value:
                item_text = item.text.split(" - ")
                _location = item_text[0].title()
                _name = item_text[1].split("\n")[0].title()
                _date = item_text[1].split("\n")[1].title()
                self._leagues_array.append({
                    "competitionPlace": _location,
                    "name": _name,
                    "games": {
                        "date": _date,
                        "list": []
                    }
                })
            if item.get_attribute(self._game_attribute_name) == self._game_attribute_value:
                item_text = item.text.split("\n")
                self._leagues_array[len(self._leagues_array) - 1]["games"]["list"].append({
                    "currentState": item_text[0],
                    "homeTeam": item_text[1],
                    "awayTeam": item_text[3],
                    "result": item_text[2]
                })

    def __data_insert(self, results):
        _competition_place = None
        _name = None
        _date = None

        for item in results:
            if item.get_attribute(self._title_attribute_name) == self._title_attribute_value:
                item_text = item.text.split(" - ")
                _competition_place = item_text[0].title()
                _name = item_text[1].split("\n")[0].title()
                _date = item_text[1].split("\n")[1].title()
                self._leagues_array

    def __run_data(self):
        self.__run_driver()
        try:
            result = self.__page_reader()
            # self.__data_conversion(result)
            self.__insert_data(result)
        finally:
            self._driver.quit()

    def get_results(self):
        self.__run_data()
        # return json.dumps(self._leagues_array)
        return self._leagues_array
