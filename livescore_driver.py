from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


class LivescoreDriver:
    def __init__(self, games_date="", base_array=[]):
        """Class which scraps and order the data collected from Livescore

        Args:
            games_date (string, optional): The date of the competitions in the format YYYY-MM-DD. If default then it collects data about today. Defaults to "".
            base_array (list, optional): The array of the games to which we want to add games. If default then we start with an empty array. Defaults to [].
        """
        self._PATH = "./chromedriver"
        self._LIVESCORE_ADDRESS = "https://www.livescore.com/" + \
            (games_date if games_date == "" else "soccer/" + games_date + "/")
        # Attributes in the source code responsible for collection of the right data. Div with data-type container chooses
        # the container of games. Div with data-type stg is the title of the competition and data-type evt of event (game)
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
        self._leagues_array = base_array
        self._driver = None

    def __run_driver(self):
        """ Start selenium webdriver
        """
        self._driver = webdriver.Chrome(self._PATH)
        self._driver.get(self._LIVESCORE_ADDRESS)
        self._driver.implicitly_wait(5)

    def __page_reader(self):
        """ Get data from the website

        Returns:
            list of selenium webelements: The list of selenium elements chosen by data-types stg and evt
        """
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

    def __get_league_array_element(self, index_competition_place, index_name=None, index_date=None, index_game=None):
        if index_competition_place != None and index_name != None and index_date != None and index_game != None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_date]["listGames"][index_game]
        elif index_competition_place != None and index_name != None and index_date != None and index_game == None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_date]
        elif index_competition_place != None and index_name != None and index_date == None and index_game == None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]
        elif index_competition_place != None and index_name == None and index_date == None and index_game == None:
            return self._leagues_array[index_competition_place]
        else:
            raise TypeError("Indices cannot be None if not allowed")

    def __get_league_array_list(self, index_competition_place=None, index_name=None, index_date=None):
        if index_competition_place != None and index_name != None and index_date != None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_date]["listGames"]
        elif index_competition_place != None and index_name != None and index_date == None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"]
        elif index_competition_place != None and index_name == None and index_date == None:
            return self._leagues_array[index_competition_place]["competitions"]
        elif index_competition_place == None and index_name == None and index_date == None:
            return self._leagues_array
        else:
            raise TypeError("Indices cannot be None if not allowed")

    def __get_competition_place_array_length(self):
        return len(self._leagues_array)

    def __get_competition_array_length(self, index_competition_place):
        return len(self._leagues_array[index_competition_place]["competitions"])

    def __get_date_array_length(self, index_competition_place, index_competition):
        return len(self._leagues_array[index_competition_place]["competitions"][index_competition]["games"])

    def __get_games_array_length(self, index_competition_place, index_name, index_date):
        return len(self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_date]["listGames"])

    def __get_item_index(self, array_to_check, item_to_find, item_title):
        """ Get index of the item (regardless it is a competition place, a name of the competition or a date)

        Args:
            array_to_check ([type]): [description]
            item_to_find ([type]): [description]
            item_title (string): It is a title of the record in JSON. For example for date it it "date"

        Returns:
            [type]: [description]
        """
        index = None

        for item_index, item in enumerate(array_to_check):
            if item[item_title] == item_to_find:
                index = item_index

        return index

    def __get_item_indices(self, competition_place, name=None, date=None):
        indices = {"indexCompetitionPlace": None,
                   "indexName": None, "indexDate": None}

        index_competition_place = self.__get_item_index(
            self.__get_league_array_list(), competition_place, "competitionPlace")
        index_name = None
        index_date = None
        indices["indexCompetitionPlace"] = index_competition_place
        if (indices["indexCompetitionPlace"] != None and competition_place != None and name != None):
            index_name = self.__get_item_index(
                self.__get_league_array_list(indices["indexCompetitionPlace"]), name, "name")
            indices["indexName"] = index_name
            if (indices["indexName"] != None and date != None):
                index_date = self.__get_item_index(self.__get_league_array_list(
                    indices["indexCompetitionPlace"], indices["indexName"]), date, "date")
                indices["indexDate"] = index_date

        return indices

    def __get_game_index(self, home_team, away_team, index_competition_place, index_name, index_date):
        index = None

        if (self.__get_games_array_length(index_competition_place, index_name, index_date) != 0):
            games_array = self.__get_league_array_list(
                index_competition_place, index_name, index_date)
            for item_index, item in enumerate(games_array):
                if (item["homeTeam"] == home_team and item["awayTeam"] == away_team):
                    index = item_index

        return index

    def __check_game_state(self, current_state, result, index_competition_place, index_name, index_date, index_game):
        game_to_check = self.__get_league_array_element(
            index_competition_place, index_name, index_date, index_game)

        if (game_to_check["currentState"] != current_state or game_to_check["result"] != result):
            return False
        else:
            return True

    def __change_game_state(self, current_state, home_team, away_team, result, index_competition_place, index_name, index_date, index_game):

        if (self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_date]["listGames"][index_game]["homeTeam"] == home_team and self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_date]["listGames"][index_game]["awayTeam"] == away_team):
            self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_date]["listGames"][index_game]["currentState"] = current_state
            self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_date]["listGames"][index_game]["result"] = result

    def __add_title(self, competition_place, name, date):

        indices = self.__get_item_indices(competition_place, name, date)

        if (indices["indexCompetitionPlace"] != None and indices["indexName"] != None and indices["indexDate"] == None):
            self.__create_new_date(
                date, indices["indexCompetitionPlace"], indices["indexName"])
            index_date = self.__get_date_array_length(
                indices["indexCompetitionPlace"], indices["indexName"]) - 1
            indices["indexDate"] = index_date
        elif (indices["indexCompetitionPlace"] != None and indices["indexName"] == None and indices["indexDate"] == None):
            self.__create_new_competition(
                name, date, indices["indexCompetitionPlace"])
            index_name = self.__get_competition_array_length(
                indices["indexCompetitionPlace"]) - 1
            indices["indexName"] = index_name
            indices["indexDate"] = 0
        elif (indices["indexCompetitionPlace"] == None and indices["indexName"] == None and indices["indexDate"] == None):
            self.__create_new_competition_place(competition_place, name, date)
            index_competition_place = self.__get_competition_place_array_length() - 1
            indices["indexCompetitionPlace"] = index_competition_place
            indices["indexName"] = 0
            indices["indexDate"] = 0

        return indices

    def __add_game(self, current_state, home_team, away_team, result, indices):
        index_competition_place = indices["indexCompetitionPlace"]
        index_name = indices["indexName"]
        index_date = indices["indexDate"]
        index_game = self.__get_game_index(
            home_team, away_team, index_competition_place, index_name, index_date)

        if (index_game == None):
            self.__create_new_game(current_state, home_team, away_team,
                                   result, index_competition_place, index_name, index_date)
        else:
            if (self.__check_game_state(current_state, result, index_competition_place, index_name, index_date, index_game) == False):
                self.__change_game_state(current_state, home_team, away_team, result,
                                         index_competition_place, index_name, index_date, index_game)

    def __insert(self, results):
        competition_place = None
        name = None
        date = None
        indices = None
        for item in results:
            # Assigning a title
            if item.get_attribute(self._title_attribute_name) == self._title_attribute_value:
                item_text = item.text.replace("\n", " - ").split(" - ")
                competition_place = item_text[0].title()
                name = item_text[1].title()
                date = item_text[2].title()
                indices = self.__add_title(
                    competition_place, name, date)
            # Assigning a game
            if item.get_attribute(self._game_attribute_name) == self._game_attribute_value:
                item_text = item.text.split("\n")
                current_state = item_text[0]
                home_team = item_text[1]
                away_team = item_text[3]
                result = item_text[2]
                self.__add_game(current_state, home_team,
                                away_team, result, indices)

    def __run_data(self):
        self.__run_driver()
        try:
            result = self.__page_reader()
            self.__insert(result)
        finally:
            self._driver.quit()

    def get_results(self):
        self.__run_data()
        # return json.dumps(self._leagues_array)
        return self._leagues_array
