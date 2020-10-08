from livescore_driver import LivescoreDriver
from results_save import ResultsSave


def main():

    driver20201008 = LivescoreDriver("2020-10-08")
    driver20201008.populate_results()

    file_results2 = ResultsSave(driver20201008.get_json_results())

    file_results2.export_json()


if __name__ == "__main__":
    main()
