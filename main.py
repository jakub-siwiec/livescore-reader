from livescore_driver import LivescoreDriver
import pickle


def main():

    # with open("livescore", "rb") as f:
    # today_results_get = pickle.load(f)

    # print("\n")
    # print(today_results_get)
    # print("\n")

    print("\n\n\n-----TODAY RESULTS-----\n")
    driver20201007 = LivescoreDriver("2020-10-07")
    results2020107 = driver20201007.get_results()
    driver20201008 = LivescoreDriver("2020-10-08", results2020107)
    results2020100708 = driver20201008.get_results()
    print(results2020100708)

    # with open("livescore", "wb") as f:
    #     pickle.dump(today_results_get, f)

    # print("\n\n\n-----TOMORROW RESULTS-----\n")
    # tomorrow_results = LivescoreDriver("2020-10-04")
    # tomorrow_results_get = tomorrow_results.get_results()
    # print(tomorrow_results_get)
    # print("\n\n\n-----COMBINED RESULTS-----\n")
    # combined_results = {**today_results_get, **tomorrow_results_get}
    # print(combined_results)
    # print("\n\n\n")


if __name__ == "__main__":
    main()
