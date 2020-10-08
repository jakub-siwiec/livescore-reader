from livescore_driver import LivescoreDriver


def main():

    driver20201008 = LivescoreDriver("2020-10-08")
    results2020108 = driver20201008.get_results()
    driver20201009 = LivescoreDriver("2020-10-09", results2020108)
    results2020100709 = driver20201009.get_results()
    print(results2020100709)


if __name__ == "__main__":
    main()
