# Livescore&#46;com reader

The app scraps [Livescore](https://www.livescore.com/) in its football/soccer section and processes the results that they are ready to send by API.

**Purpose:** There was no specific purpose of this project except fun and practicing Selenium with Python.

**Information:** The reader works with the version of the Livescore website which is online on the 8th of October 2020.

**Diclaimer:** The project was done only for educational purposes. Before using this code for any other purposes, please ask Livescore if they allow it.

## Summary

### Technologies

Languages:

* Python

Web browser automation tool:

* Selenium

Driver:

* Chromedriver

Package manager:

* Anaconda

### What it can do

The app reads all the results for a day specified with a parameter. Several days can be combined together into one result. The result is the list of dictionaries at the beginning but later can be converted into JSON string format. The beginning result can be saved as a pickle file and results in strings can be saved in file as a pickle, text (.txt file) or json (.json file).

This is the example of received results (this is a small excerpt of real data received):

```json
  [{
    "competitionPlace": "Brazil",
    "competitions": [
      {
        "name": "Serie A",
        "games": [
          {
            "date": "October 8",
            "currentState": "FT",
            "homeTeam": "Goias",
            "awayTeam": "Fluminense",
            "result": "2 - 4"
          },
          {
            "date": "October 8",
            "currentState": "FT",
            "homeTeam": "Sao Paulo",
            "awayTeam": "Atletico GO",
            "result": "3 - 0"
          },
          {
            "date": "October 8",
            "currentState": "FT",
            "homeTeam": "Botafogo RJ",
            "awayTeam": "Palmeiras",
            "result": "2 - 1"
          },
          {
            "date": "October 8",
            "currentState": "FT",
            "homeTeam": "Fortaleza",
            "awayTeam": "Atletico MG",
            "result": "2 - 1"
          },
          {
            "date": "October 8",
            "currentState": "23:00",
            "homeTeam": "Athletico Paranaense",
            "awayTeam": "Ceara",
            "result": "? - ?"
          },
          {
            "date": "October 9",
            "currentState": "01:00",
            "homeTeam": "Bragantino",
            "awayTeam": "Internacional",
            "result": "? - ?"
          }
        ]
      },
      {
        "name": "Serie B",
        "games": [
          {
            "date": "October 8",
            "currentState": "22:30",
            "homeTeam": "Cruzeiro",
            "awayTeam": "Sampaio Correa",
            "result": "? - ?"
          },
          {
            "date": "October 9",
            "currentState": "20:00",
            "homeTeam": "Figueirense",
            "awayTeam": "Chapecoense AF",
            "result": "? - ?"
          },
          {
            "date": "October 9",
            "currentState": "20:30",
            "homeTeam": "Operario Ferroviario",
            "awayTeam": "Confianca",
            "result": "? - ?"
          },
          {
            "date": "October 9",
            "currentState": "22:30",
            "homeTeam": "Cuiaba",
            "awayTeam": "Ponte Preta",
            "result": "? - ?"
          },
          {
            "date": "October 9",
            "currentState": "23:15",
            "homeTeam": "America MG",
            "awayTeam": "Nautico",
            "result": "? - ?"
          }
        ]
      },
      {
        "name": "U20 Copa Do Brasil",
        "games": [
          {
            "date": "October 8",
            "currentState": "20:00",
            "homeTeam": "Goias U20",
            "awayTeam": "Uniao EC MT U20",
            "result": "? - ?"
          }
        ]
      },
      {
        "name": "Serie C: Grp A",
        "games": [
          {
            "date": "October 9",
            "currentState": "00:00",
            "homeTeam": "Treze",
            "awayTeam": "Imperatriz",
            "result": "? - ?"
          }
        ]
      },
      {
        "name": "Paulista A2: Play-Off",
        "games": [
          {
            "date": "October 9",
            "currentState": "19:00",
            "homeTeam": "Sao Bento",
            "awayTeam": "Sao Caetano",
            "result": "? - ?"
          }
        ]
      }
    ]
  }]
```