#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
import hashlib
import os
from heightconverter import *
from recruitMeasureablePredictorWeight import *
import webbrowser


def save_html_to_file(content, filename):
    with open(filename, 'wb') as file:
        file.write(content)


def load_html_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read()


def recruitSearchFunction(wantedYear, wantedRegion, recruited, developmentDiff, min_potential, min_si, min_height, min_wingspan, min_vertical,
                 inside_shooting, outside_shooting, rangeVal, rebounding, plus_defense, inside_defense, perimeter_defense, iq, passing, handling, speed, far_home,early_commit,close_home, min_measureableDiff):

    hardwoodBeginnerUrl = "http://onlinecollegebasketball.org"

    schoolYear = {
        "HSFR": "1",
        "HSSO": "2",
        "HSJR": "3",
        "HSSR": "4",
        "INT": "6",
        "JCFR": "11",
        "JCSO": "12"
    }
    playerRegion = {"All": "0", "NE": "6", "MA": "MA", "MW": "4", "WI": "WI", "CE":"2", "IN":"IN"}
    playerLengthSearch = 700
    if wantedRegion == "All":
        playerLengthSearch = 3000

    url = hardwoodBeginnerUrl + "/" + "top_prospects/" + schoolYear[wantedYear] + "/" + playerRegion[wantedRegion] + "/" + str(playerLengthSearch)

    file_name = wantedYear + wantedRegion + ".html"
    folder_name = "RecruitSearchHTML"

    try:
        html_content = load_html_from_file(os.path.join(folder_name, file_name))
    except FileNotFoundError:
        response = requests.get(url)
        html_content = response.content
        os.makedirs(folder_name, exist_ok=True)
        save_html_to_file(html_content, os.path.join(folder_name, file_name))

    soup = BeautifulSoup(html_content, "html.parser")
    infoList = soup.find_all("tr")[1:]

    heights = ["5'4", "5'5", "5'6", "5'7", "5'8", "5'9", "5'10", "5'11", "6'", "6'1", "6'2", "6'3", "6'4", "6'5", "6'6", "6'7", "6'8", "6'9", "6'10", "6'11", "7'"]

    InsideShooting = {
        "Great": {"Could be a good post player", "Could be a very good post player", "Could be a dominating post player"},
        "Good": {"Above average post moves", "Could be a good post player", "Could be a very good post player", "Could be a dominating post player"},
        "Bad": ""
    }
    OutsideShooting = {
        "Great" : {"Could be a good shooter", "Could be an excellent shooter"},
        "Good": {"Could be an above average shooter", "Could be a good shooter", "Could be an excellent shooter"},
        "Bad": {"Does not have much of a shooting touch"}
    }
    Range = {"Good": {"Could really be a long-range shooter"}, "Bad": {}}
    Rebounding = {
        "Great": {"Can be a monster on the boards"},
        "Good": {"Can be a decent rebounder", "Can be a monster on the boards"},
        "Bad": {"Can never be a good rebounder"}
    }
    PlusDefense = {
        "Great": {"Can be a great all-around defensive player"},
        "Good": {"Can be a good all-around defensive player", "Can be a great all-around defensive player"},
        "Bad": {}
    }
    InsideDefense = {
        "Good": {"Will never be a good perimeter defender"},
        "Bad": {"Will never be a good interior defender"}
    }
    PerimeterDefense = {
        "Good": {"Will never be a good interior defender"},
        "Bad": {"Will never be a good perimeter defender"}
    }
    IQ = {
        "Great": {"Can be a really smart player"},
        "Good": {"Can be a smart player", "Can be a really smart player"},
        "Bad": {"Can be prone to a lot of mental mistakes"}
    }
    Passing = {
        "Great": {"Can be a skilled passer with exceptional court vision"},
        "Good": {"Can be a skilled passer", "Can be a skilled passer with exceptional court vision"},
        "Bad": {}
    }
    Handling = {
        "Great": {"Can be a really good ball handler"},
        "Good": {"Can be a decent ball handler", "Can be a really good ball handler"},
        "Bad": {"Will be a below average ball handler"}
    }
    Speed = {
        "Great": {"Will be very quick", "Will be quick as lightning"},
        "Good": {"Can be a speedy player", "Will be very quick", "Will be quick as lightning"},
        "Bad": {"Will always be a bit sluggish"}
    }
    FarHome = {"Good": {"Has no preference"}, "Bad": {}}
    EarlyCommit = {"Good": {"Is eager to commit early"}, "Bad": {}}
    CloseHome = {"Good": {"Would prefer to play close to home"}, "Bad": {}}

    preferenceArr = [min_potential, min_si, min_height, min_wingspan, min_vertical, inside_shooting, outside_shooting, rangeVal, rebounding, plus_defense, inside_defense, perimeter_defense, iq, passing, handling, speed, far_home,early_commit,close_home]

    preference_keys = ["", "", "", "", "", "InsideShooting", "OutsideShooting", "Range", "Rebounding","PlusDefense", "InsideDefense", "PerimeterDefense", "IQ", "Passing", "Handling", "Speed", "FarHome","EarlyCommit","CloseHome"]

    resultDic = {}
    for i in range(5, len(preferenceArr)):
        user_input = preferenceArr[i]
        preference_key = preference_keys[i]
        if preference_key and preference_key in locals():
            corresponding_dict = locals()[preference_key]
            if user_input == 'G':
                resultDic.setdefault(preference_key, set()).update(("Great", item) for item in corresponding_dict["Great"])
            elif user_input == 'Y':
                resultDic.setdefault(preference_key, set()).update(("Good", item) for item in corresponding_dict["Good"])
            elif user_input == 'N':
                resultDic.setdefault(preference_key, set()).update(("Bad", item) for item in corresponding_dict["Bad"])

    playersFound = []

    for player in infoList:
        try:
            recEval = player.find("td", colspan="4").text
        except:
            continue

        if "Isn't much of a student and may not qualify academically" in recEval or "Is a troubled kid and may not be college material" in recEval:
            continue

        for key, values in resultDic.items():
            positive_values = [value for qualifier, value in values if qualifier in {"Good", "Great"}]
            bad_values = [value for qualifier, value in values if qualifier == "Bad"]

            if not any(value in recEval for value in positive_values) and positive_values:
                break
            elif any(bad_value in recEval for bad_value in bad_values):
                break
        else:
            playersFound.append(player)

    return playersFound