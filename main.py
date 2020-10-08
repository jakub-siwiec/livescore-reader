from livescore_driver import LivescoreDriver
from results_save import ResultsSave


def main():

    # Reading the results from today
    driver = LivescoreDriver()
    driver_results = driver.populate_results()

    # Reading the results from 2020-10-09 and appening them to the results from today then printing the list of dictionaries in the console
    driver_1 = LivescoreDriver("2020-10-09", driver_results)
    driver_results_1 = driver_1.populate_results()
    print(driver_results_1)

    # Getting the results in json/string format
    json_results = driver_1.get_json_results()

    # Saving file of list of dictionaries with a custom name
    variable_results = ResultsSave(driver_results_1)
    variable_results.export_pickle()

    # Saving a string file with a chosen name
    string_results = ResultsSave(json_results, "results_json")
    string_results.export_pickle()
    string_results.export_txt()
    string_results.export_json()


if __name__ == "__main__":
    main()
