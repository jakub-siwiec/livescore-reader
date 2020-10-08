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
        # Using chromedriver
        self._PATH = "./chromedriver"

        # https://www.livescore.com/ shows today games. E.g. https://www.livescore.com/soccer/2021-02-18/ shows the games from 18/02/2021
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

        # Member variables used later. _leagues_array is the main array to which the competitions and games will be added. Driver is a selenium driver
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

    def __create_new_competition_place(self, competition_place, name):
        """ Create new competition place, e.g. England or Champions League

        Args:
            competition_place (string): Competition place to add e.g. England or Champions League
            name (string): Name of the competition to add e.g. Premier League or Group B
        """
        self._leagues_array.append(
            {
                "competitionPlace": competition_place,
                "competitions": [
                    {
                        "name": name,
                        "games": []
                    }
                ]
            }
        )

    def __create_new_competition(self, name, index_competition_place):
        """Creating new competition within competition place. E.g. Premier League within England or Group B within Champions League

        Args:
            name (string): Name of the competition to add e.g. Premier League or Group B
            index_competition_place (integer): The index in self._leagues_array of the particular competition place to which the competition will be added
        """
        self._leagues_array[index_competition_place]["competitions"].append(
            {
                "name": name,
                "games": []
            }
        )

    def __create_new_game(self, date, current_state, home_team, away_team, result, index_competition_place, index_name):
        """Creating new game within competition.

        Args:
            date (string): Date of the game e.g. October 8
            current_state (string): The state of the game which can be: the time when starts, the minute of the game, half-time, full-time or any special event (postponed)
            home_team (string): Full name of the home team
            away_team (string): Full name of the away team
            result (string): The result or in case the game has not been played yet just ' - '
            index_competition_place (integer): The index in self._leagues_array of the particular competition place to which the competition will be added
            index_name (integer): The index in self._leagues_array[index_competition_place]["competitions"] of the particular competition to which the game will be added
        """
        self._leagues_array[index_competition_place]["competitions"][index_name]["games"].append(
            {
                "date": date,
                "currentState": current_state,
                "homeTeam": home_team,
                "awayTeam": away_team,
                "result": result
            }
        )

    def __get_league_array_element(self, index_competition_place, index_name=None, index_game=None):
        """Get a dictionary with specific index. Can be competition place, competition or game

        Args:
            index_competition_place (integer): Number of the competition place index in the list.
            index_name (integer, optional): Number of the competition name index in the list. Defaults to None.
            index_game (integer, optional): Number of the game index in the list. Defaults to None.

        Raises:
            TypeError: Raises an error if the wrong indices or the index for competition place is None.

        Returns:
            dictionary: Element of a self._leagues_array.
        """
        if index_competition_place != None and index_name != None and index_game != None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"][index_game]
        elif index_competition_place != None and index_name != None and index_game == None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]
        elif index_competition_place != None and index_name == None and index_game == None:
            return self._leagues_array[index_competition_place]
        else:
            raise TypeError("Indices cannot be None if not allowed")

    def __get_league_array_list(self, index_competition_place=None, index_name=None):
        """Get a list with a specific index/indices. Can be the list of games, competitions or competition places.

        Args:
            index_competition_place (integer, optional): Number of the competition place index in the list. Defaults to None.
            index_name (integer, optional): Number of the competition name index in the list. Defaults to None.

        Raises:
            TypeError: Something wrong with indices

        Returns:
            list: Array of the elements of choice based on indices in the input.
        """
        if index_competition_place != None and index_name != None:
            return self._leagues_array[index_competition_place]["competitions"][index_name]["games"]
        elif index_competition_place != None and index_name == None:
            return self._leagues_array[index_competition_place]["competitions"]
        elif index_competition_place == None and index_name == None:
            return self._leagues_array
        else:
            raise TypeError("Indices cannot be None if not allowed")

    def __get_competition_place_array_length(self):
        """The length of the list of competition place.

        Returns:
            integer: The length of the array of competition places.
        """
        return len(self._leagues_array)

    def __get_competition_array_length(self, index_competition_place):
        """The length of the list of competition.

        Args:
            index_competition_place (integer): Number of the competition place index in the list.

        Returns:
            integer: The length of the array of competitions.
        """
        return len(self._leagues_array[index_competition_place]["competitions"])

    def __get_games_array_length(self, index_competition_place, index_name):
        """The length of the games list.

        Args:
            index_competition_place (integer): Number of the competition place index in the list.
            index_name (integer): Number of the competition index in the list.

        Returns:
            integer: The length of the array of competitions.
        """
        return len(self._leagues_array[index_competition_place]["competitions"][index_name]["games"])

    def __get_item_index(self, array_to_check, item_to_find, item_title):
        """ Get index of the item (regardless it is a competition place, a name of the competition or a date)

        Args:
            array_to_check (list): List to browse through. 
            item_to_find (string): String of the key to look for whose name is in the next parameter.
            item_title (string): It is a title of the record in dictionary/JSON. For example for date it it "date".

        Returns:
            integer: The number of the element in the list.
        """
        index = None

        for item_index, item in enumerate(array_to_check):
            if item[item_title] == item_to_find:
                index = item_index

        return index

    def __get_item_indices(self, competition_place, name=None):
        """Get dictionary of the indices for competition place and competitions.

        Args:
            competition_place (string): Competition place to add e.g. England or Champions League
            name (string, optional): Name of the competition to add e.g. Premier League or Group B. Defaults to None.

        Returns:
            dictionary: Dictionary of indices in their lists of indexCompetitionPlace and indexName for competitions.
        """
        indices = {"indexCompetitionPlace": None,
                   "indexName": None}
        index_competition_place = self.__get_item_index(
            self.__get_league_array_list(), competition_place, "competitionPlace")
        index_name = None
        indices["indexCompetitionPlace"] = index_competition_place
        if (indices["indexCompetitionPlace"] != None and competition_place != None and name != None):
            index_name = self.__get_item_index(
                self.__get_league_array_list(indices["indexCompetitionPlace"]), name, "name")
            indices["indexName"] = index_name

        return indices

    def __get_game_index(self, date, home_team, away_team, index_competition_place, index_name):
        """Getting the game index in the list of games

        Args:
            date (string): Date of the game e.g. October 8
            home_team (string): Full name of the home team
            away_team (string): Full name of the away team
            index_competition_place (integer): Number of the competition place index in the list
            index_name (integer): Number of the competition index in the list.

        Returns:
            integer: The number of the index of the game in the list of games
        """
        index = None
        if (self.__get_games_array_length(index_competition_place, index_name) != 0):
            games_array = self.__get_league_array_list(
                index_competition_place, index_name)
            for item_index, item in enumerate(games_array):
                if (item["date"] == date and item["homeTeam"] == home_team and item["awayTeam"] == away_team):
                    index = item_index

        return index

    def __check_game_state(self, current_state, result, index_competition_place, index_name, index_game):
        """Checking whether the game state (current state and the results) are the same for the specific game and parameters

        Args:
            current_state (string): The state of the game which can be: the time when starts, the minute of the game, half-time, full-time or any special event (postponed).
            result (string): The result or in case the game has not been played yet just ' - '.
            index_competition_place (integer): Number of the competition place index in the list.
            index_name (integer): Number of the competition index in the list.
            index_game (integer): Number of the game index in the list.

        Returns:
            boolean: True if the current state and result are the same, False if they are different.
        """
        game_to_check = self.__get_league_array_element(
            index_competition_place, index_name, index_game)

        if (game_to_check["currentState"] != current_state or game_to_check["result"] != result):
            return False
        else:
            return True

    def __change_game_state(self, date, current_state, home_team, away_team, result, index_competition_place, index_name, index_game):
        """Change the state (current state or result) of the game which exists in the list and have a certain index.

        Args:
            date (string): Date of the game e.g. October 8
            current_state (string): The state of the game which can be: the time when starts, the minute of the game, half-time, full-time or any special event (postponed)
            home_team (string): Full name of the home team
            away_team (string): Full name of the away team
            result (string): The result or in case the game has not been played yet just ' - '
            index_competition_place (integer): The index in self._leagues_array of the particular competition place to which the competition will be added
            index_name (integer): The index in self._leagues_array[index_competition_place]["competitions"] of the particular competition to which the game will be added
            index_game (integer, optional): Number of the game index in the list. Defaults to None.
        """
        if (self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_game]["date"] == date and self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_game]["homeTeam"] == home_team and self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_game]["awayTeam"] == away_team):
            self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_game]["currentState"] = current_state
            self._leagues_array[index_competition_place]["competitions"][index_name][
                "games"][index_game]["result"] = result

    def __add_title(self, competition_place, name):
        """Add title of the league and competition.

        Args:
            competition_place (string): Competition place to add e.g. England or Champions League
            name (string): Name of the competition to add e.g. Premier League or Group B
        Returns:
            dictionary: The indices of competition place and name of the competition in their lists. Labels: indexCompetitionPlace and indexName.
        """
        indices = self.__get_item_indices(competition_place, name)

        if (indices["indexCompetitionPlace"] != None and indices["indexName"] == None):
            self.__create_new_competition(
                name, indices["indexCompetitionPlace"])
            index_name = self.__get_competition_array_length(
                indices["indexCompetitionPlace"]) - 1
            indices["indexName"] = index_name
        elif (indices["indexCompetitionPlace"] == None and indices["indexName"] == None):
            self.__create_new_competition_place(competition_place, name)
            index_competition_place = self.__get_competition_place_array_length() - 1
            indices["indexCompetitionPlace"] = index_competition_place
            indices["indexName"] = 0

        return indices

    def __add_game(self, date, current_state, home_team, away_team, result, indices):
        """Add game to the competition

        Args:
            date (string): Date of the game e.g. October 8
            current_state (string): The state of the game which can be: the time when starts, the minute of the game, half-time, full-time or any special event (postponed)
            home_team (string): Full name of the home team
            away_team (string): Full name of the away team
            result (string): The result or in case the game has not been played yet just ' - '
            indices (dictionary): The indices of competition place and name of the competition in their lists. Labels: indexCompetitionPlace and indexName.
        """
        index_competition_place = indices["indexCompetitionPlace"]
        index_name = indices["indexName"]
        index_game = self.__get_game_index(
            date, home_team, away_team, index_competition_place, index_name)

        if (index_game == None):
            self.__create_new_game(date, current_state, home_team, away_team,
                                   result, index_competition_place, index_name)
        else:
            if (self.__check_game_state(current_state, result, index_competition_place, index_name, index_game) == False):
                self.__change_game_state(date, current_state, home_team, away_team, result,
                                         index_competition_place, index_name, index_game)

    def __insert(self, results):
        """Inserting results from result list of selenium webelements into self._leagues_array list of dictionaries

        Args:
            results (list): List of selenium webelements with the titles of the competitions and games.
        """
        competition_place = None
        name = None
        date = None
        indices = None
        date = None
        for item in results:
            # Assigning a title
            if item.get_attribute(self._title_attribute_name) == self._title_attribute_value:
                item_text = item.text.replace("\n", " - ").split(" - ")
                competition_place = item_text[0].title()
                name = item_text[1].title()
                date = item_text[2].title()
                indices = self.__add_title(
                    competition_place, name)
            # Assigning a game
            if item.get_attribute(self._game_attribute_name) == self._game_attribute_value:
                item_text = item.text.split("\n")
                current_state = item_text[0]
                home_team = item_text[1]
                away_team = item_text[3]
                result = item_text[2]
                self.__add_game(date, current_state, home_team,
                                away_team, result, indices)

    def __run_data(self):
        """Start the selenium driver, collect the data and quit selenium driver.
        """
        self.__run_driver()
        try:
            result = self.__page_reader()
            self.__insert(result)
        finally:
            self._driver.quit()

    def get_results(self):
        """Populate self._leagues_array and return it

        Returns:
            list: List of dictionaries of self._leagues_array
        """
        self.__run_data()
        # return json.dumps(self._leagues_array)
        return self._leagues_array
