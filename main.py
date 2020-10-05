from livescore_driver import LivescoreDriver
import pickle


def main():

    # with open("livescore", "rb") as f:
    # today_results_get = pickle.load(f)

    # print("\n")
    # print(today_results_get)
    # print("\n")

    print("\n\n\n-----TODAY RESULTS-----\n")
    today_results = LivescoreDriver("2020-10-06")
    today_results_get = today_results.get_results()
    print(today_results_get)

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
