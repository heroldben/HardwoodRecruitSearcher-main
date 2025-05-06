#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from bs4 import BeautifulSoup
import requests
import hashlib
import os
from heightconverter import convert_to_feet, convert_to_inches, height_pred, Vert_convert_to_inches
from recuritMeasurablePredictor import vertical_pred, vertical_pred_nonFresh, height_pred, wingspan_pred, wingspan_pred_nonFresh
import webbrowser


def save_html_to_file(content, filename):
    with open(filename, 'wb') as file:
        file.write(content)


def load_html_from_file(filename):
    with open(filename, 'rb') as file:
        return file.read()


hardwoodBeginnerUrl = "http://onlinecollegebasketball.org"
wantedYear = input("What Recruit Year (HSFR,HSSO,HSJR,HSSR,INT,JCFR,JCSO): ")
wantedRegion = input("What Region?(All,NE,MA,MW,WI): ")
#schoolYear= ["HSFR","HSSO","HSJR","HSSR"]

#url = "http://onlinecollegebasketball.org/top_prospects/1/6/700"  # Replace this URL with the one you want to scrape
'''
if wantedYear == "INT":
    url = hardwoodBeginnerUrl + "/top_prospects/6/0/700"
else:
    if wantedYear == "JCFR":
        wantedYearIndex = 11
    elif wantedYear == "JCSO":
        wantedYearIndex = 12
    else:
        wantedYearIndex = schoolYear.index(wantedYear) + 1
    url = hardwoodBeginnerUrl + "/"+ "top_prospects/" + str(wantedYearIndex) + "/6/700"
'''

schoolYear = {
    "HSFR": "1",
    "HSSO": "2",
    "HSJR": "3",
    "HSSR": "4",
    "INT": "6",
    "JCFR": "11",
    "JCSO": "12"
}
playerRegion = {"All": "0", "NE": "6", "MA": "MA", "MW": "4", "WI": "WI"}
playerLengthSearch = 700
if wantedRegion == "All":
    playerLengthSearch = 2200

url = hardwoodBeginnerUrl + "/" + "top_prospects/" + schoolYear[
    wantedYear] + "/" + playerRegion[wantedRegion] + "/" + str(playerLengthSearch)



# Generate a unique filename from the URL using hashlib
#file_name = hashlib.md5(url.encode()).hexdigest() + ".html"
file_name = wantedYear + wantedRegion + ".html"
folder_name = "RecruitSearchHTML"  # Corrected folder name

try:
    html_content = load_html_from_file(os.path.join(folder_name, file_name))
    #print("Content loaded from file.")
except FileNotFoundError:
    response = requests.get(url)
    html_content = response.content
    os.makedirs(folder_name,
                exist_ok=True)  # Create folder if it doesn't exist
    save_html_to_file(html_content, os.path.join(folder_name, file_name))
    #print("Content fetched from URL and saved to file.")

soup = BeautifulSoup(html_content, "html.parser")
infoList = soup.find_all("tr")[1:]

# In[ ]:

#allEvals = ['Recruiting Evaluation', 'Could be a good post player', '\nRecruiting Evaluation', 'Could be an above average shooter', 'Could really be a long-range shooter', 'Can never be a good rebounder', 'Can be a really smart player', 'Can be a good all-around defensive player', 'Will never be a good interior defender', 'Projected Height', '6\' 3"', '', 'Could be a good shooter', 'Can be a smart player', 'Can be a great all-around defensive player', 'Can be a really good ball handler', 'Will be very quick', 'Excellent all-around player', '6\' 7"', 'Will never be a good perimeter defender', 'Can be a skilled passer', 'Will be a below average ball handler', 'Will struggle in a fast pace offense', '6\' 5"', 'Can be a decent ball handler', 'Can be a speedy player', 'Will be quick as lightning', '5\' 10"', '6\' 2"', 'Above average post moves', 'Could be an excellent shooter', 'Can be a skilled passer with exceptional court vision', '6\' 1"', '5\' 9"', 'Will always be a poor defender', "7' ", 'Will flourish in a fast pace offense', 'Can be a monster on the boards', 'Will always be a bit sluggish', 'Good all-around player', '6\' 10"', "6' ", '6\' 8"', 'Could be a very good post player', '6\' 11"', '6\' 6"', 'Does not have much of a shooting touch', 'Can be a decent rebounder', 'Will flourish in a slower tempo offense', '6\' 4"', 'Can be prone to a lot of mental mistakes', 'Has no preference to play close to home', 'Will struggle in a slower tempo offense', '5\' 8"', '6\' 9"', '5\' 11"', 'Could be a dominating post player', '5\' 5"', 'Would prefer to play close to home', '5\' 6"']

heights = [
    "5'4", "5'5", "5'6", "5'7", "5'8", "5'9", "5'10", "5'11", "6'", "6'1",
    "6'2", "6'3", "6'4", "6'5", "6'6", "6'7", "6'8", "6'9", "6'10", "6'11",
    "7'"
]

InsideShooting = {
    "Good": {
        "Above average post moves", "Could be a good post player",
        "Could be a very good post player", "Could be a dominating post player"
    },
    "Bad": ""
}
OutsideShooting = {
    "Good": {
        "Could be an above average shooter", "Could be a good shooter",
        "Could be an excellent shooter"
    },
    "Bad": {"Does not have much of a shooting touch"}
}
Range = {"Good": {"Could really be a long-range shooter"}, "Bad": {}}
Rebounding = {
    "Good": {"Can be a decent rebounder", "Can be a monster on the boards"},
    "Bad": {"Can never be a good rebounder"}
}
PlusDefense = {
    "Good": {"Can be a good all-around defensive player", "Can be a great all-around defensive player"},
    "Bad": {}
}
InsideDefense = {
    "Good": {"Will never be a good perimeter defender"},
    "Bad": {"Will never be a good interior defender",}
}
PerimeterDefense = {
    "Good": {"Will never be a good interior defender"},
    "Bad": {"Will never be a good perimeter defender",}
}
IQ = {
    "Good": {"Can be a smart player", "Can be a really smart player"},
    "Bad": {
        "Can be prone to a lot of mental mistakes",
    }
}
Passing = {
    "Good": {
        "Can be a skilled passer",
        "Can be a skilled passer with exceptional court vision"
    },
    "Bad": {}
}
Handling = {
    "Good":
    {"Can be a decent ball handler", "Can be a really good ball handler"},
    "Bad": {"Will be a below average ball handler"}
}
Speed = {
    "Good": {
        "Can be a speedy player", "Will be very quick",
        "Will be quick as lightning"
    },
    "Bad": {"Will always be a bit sluggish"}
}
#Pace = {"Good":{"Will flourish in a slower tempo offense","Will flourish in a fast pace offense"},"Bad":{"Will struggle in a slower tempo offense","Will struggle in a fast pace offense"}}
####
FarHome = {"Good": {"Has no preference"}, "Bad": {}}
####

recruited = input("Is Recruited?: (Y,L,N)")  # gets if player is recruited or not


#Asks for Deve Difference

developmentDiff = int(input("Minimum Developmment: "))



preferenceArr = [
    int(input("Minimum Potential: ")),
    int(input("Minimum SI: ")),
    input("Minimum Height (ex: 6'3 or 6'): "),
    input("Minimum Wingspan (ex: 6'3 or 6'): "),
    input("Minimum Vertical (ex: 27):  "),
    input("InsideShooting: "),
    input("OutsideShooting: "),
    input("Range: "),
    input("Rebounding: "),
    input("PlusDefense: "),
    input("InsideDefense: "),
    input("PerimeterDefense: "),
    input("IQ: "),
    input("Passing: "),
    input("Handling: "),
    input("Speed: "),
    input("FarHome: ")
]

#Finds the links of every player with the minimum inputted Potential and SI values

if recruited == "Y":
    #Includes Recruited players
    playerLinks = [
        hardwoodBeginnerUrl +
        infoList[i].find_all("td")[2].find("a").get("href")
        for i in range(len(infoList))
        if (int(infoList[i].find_all("td")[7].text) >= preferenceArr[0]) and (
            int(infoList[i].find_all("td")[6].text) >= preferenceArr[1])
    ]
elif recruited == "L":
    #Only "Low" interested Recruited players  & None
    playerLinks = [
        hardwoodBeginnerUrl +
        infoList[i].find_all("td")[2].find("a").get("href")
        for i in range(len(infoList))
        if (int(infoList[i].find_all("td")[7].text) >= preferenceArr[0]) and (
            int(infoList[i].find_all("td")[6].text) >= preferenceArr[1]) and (
                not any(substring in infoList[i].find_all("td")[11].text for substring in ["High", "Medium", "Committed"])

            )
    ] 
else:
    #Excludes Recruited Players
    playerLinks = [
        hardwoodBeginnerUrl +
        infoList[i].find_all("td")[2].find("a").get("href")
        for i in range(len(infoList))
        if (int(infoList[i].find_all("td")[7].text) >= preferenceArr[0]) and (
            int(infoList[i].find_all("td")[6].text) >= preferenceArr[1]) and (
                infoList[i].find_all("td")[11].text == "none")
    ]
    

#Maps Inputted Answers w/ Asked 
preference_keys = [
    "", "", "", "", "", "InsideShooting", "OutsideShooting", "Range", "Rebounding","PlusDefense",
    "InsideDefense", "PerimeterDefense", "IQ", "Passing", "Handling", "Speed",
    "FarHome"
]

resultDic = {}

for i in range(5, len(preferenceArr)):
    #print(i,preferenceArr[i])
    user_input = preferenceArr[i]
    preference_key = preference_keys[i]#preference_keys[i - 1]  # Adjust index to match preference_keys

    if preference_key and preference_key in globals(
    ) and preference_key != "":  # Exclude empty keys
        corresponding_dict = globals()[preference_key]
        if user_input == 'Y':
            resultDic.setdefault(preference_key, set()).update(
                ("Good", item) for item in corresponding_dict["Good"])
        elif user_input == 'N':
            resultDic.setdefault(preference_key, set()).update(
                ("Bad", item) for item in corresponding_dict["Bad"])

#
playersFound = [] #Array that holds players printed
# In[ ]:

#Searches and returns links of players who fit preferences
for player in playerLinks:
    #if player == playerLinks[-1]:
        #print("DONE")
    file_name = hashlib.md5(player.encode()).hexdigest() + ".html"
    folder_name = "PlayersHTML"  # Corrected folder name

    try:
        #checks if Player is already in PlayersHTML folder
        html_content = load_html_from_file(os.path.join(
            folder_name, file_name))
        #print("Content loaded from file.")
    except FileNotFoundError:
        response = requests.get(player)
        html_content = response.content
        os.makedirs(folder_name,
                    exist_ok=True)  # Create folder if it doesn't exist
        save_html_to_file(html_content, os.path.join(folder_name, file_name))
        #print("Content fetched from URL and saved to file.")

    soup2 = BeautifulSoup(html_content, "html.parser")


    
    #checks To see Development Difference
    if wantedYear not in ["INT","JCFR","JCSO"]:
        table = soup2.find("table", class_="stats-table-medium_font")
        positions = [(1, 35)]
        schoolYearWantedInt = int(int(schoolYear[wantedYear]))
        if schoolYearWantedInt == 2:
            positions.append((2,35))
        elif schoolYearWantedInt != 1:
            positions.append((2,35))
            positions.append((3, 35))
        '''
        elif schoolYearWantedInt == 4:
            positions.append((4, 35))
        '''
        
        siValues = []
        rows = table.find_all('tr')

        
        try:
            for row_idx, col_idx in positions:
                cell = rows[row_idx].find_all('td')[col_idx]
                siValues.append(int(cell.get_text(strip=True)))
        except IndexError:
            continue
        
        if schoolYearWantedInt == 2:
            if (siValues[1] - siValues[0]) < developmentDiff:
                continue
        elif schoolYearWantedInt != 1:
            if (siValues[2] - siValues[0]) < developmentDiff:
                continue

###############################################################################################################    
    #For Vert and Wingspan Searching            


    if wantedYear not in ["INT","JCFR","JCSO"]:
        table = soup2.find("table", class_="stats-table-medium_font")
        schoolYearWantedInt = int(int(schoolYear[wantedYear]))

        if schoolYearWantedInt == 1:
            positions = [(1, 33)]
        else:
            positions = [(1, 33), (schoolYearWantedInt, 33)]
        height_values = []
        rows = table.find_all('tr')
        for row_idx, col_idx in positions:
            cell = rows[row_idx].find_all('td')[col_idx]

            height_values.append(float(convert_to_inches(cell.get_text(strip=True)))) #for finding height (have to convert to inches)
        
        fresh_height = height_values[0]
        curr_height = height_values[-1]

        str_vert = soup2.find("table").find_all("tr")[9].find("td").text.split("  ")[-1]
        str_wingspan = soup2.find("table").find_all("tr")[8].find("td").text.split("  ")[-1]
        
        curr_vert = Vert_convert_to_inches(str_vert)
        curr_wingspan = convert_to_inches(str_wingspan)

        pred_vert = vertical_pred_nonFresh(fresh_height,curr_height,curr_vert)
        pred_wingspan = wingspan_pred_nonFresh(fresh_height,curr_height,curr_wingspan)

        #Convert asked measureables to inches 
        wanted_wingspan = convert_to_inches(preferenceArr[3])
        wanted_vert = Vert_convert_to_inches(preferenceArr[4])

###############################################################################################################    


    #Finds the recuriting Eval
    try:
        recEval = soup2.find("table").find_all("tr")[15].text
    except AttributeError:
        continue
    
    

    playerEvalheight = ""
    
    # Check the entire recEval string for unwanted phrases
    if "poor defender" in recEval or "Isn't much of a student and may not qualify academically" in recEval:
        continue  # Skip this player if they have the poor eval comment

    # Proceed with the height extraction only if the unwanted phrases aren't present
    for i in recEval:
        if i.isdigit():
            if len(playerEvalheight) == 0:
                playerEvalheight += i
                playerEvalheight += "'"
            else:
                playerEvalheight += i


    #Checks if player's height is above or equal to user's preference and if player's evaluation matches user's criteria.
    try:
        # Attempt to find indices and compare heights
        if wantedYear not in ["INT","JCFR","JCSO"]:

            ########################################## ADDING HEIGHT CHECKING USING FRESHMEN HEIGHTS #################################################
            playerFreshmanHeight = convert_to_inches((rows[1].find_all('td')[33]).text)
            playerPredictedHeight = height_pred(playerFreshmanHeight)
            wantedMinHeight = convert_to_inches(preferenceArr[2])

            if (playerPredictedHeight >= wantedMinHeight - .5) and  (pred_wingspan + 2 > wanted_wingspan) and (pred_vert + 2 > wanted_vert):
                for key, values in resultDic.items():
                    good_values = [
                        value for qualifier, value in values if qualifier == "Good"
                    ]
                    bad_values = [
                        value for qualifier, value in values if qualifier == "Bad"
                    ]
                    if not any(good_value in recEval
                            for good_value in good_values) and good_values != []:
                        break
                    elif any(bad_value in recEval for bad_value in bad_values):
                        break
                else:            
                    print(player)
                    playersFound.append(player)
        else:

            playerEvalIndex = heights.index(playerEvalheight)
            preferenceIndex = heights.index(preferenceArr[2])

            if playerEvalIndex >= preferenceIndex:
                for key, values in resultDic.items():
                    good_values = [
                        value for qualifier, value in values if qualifier == "Good"
                    ]
                    bad_values = [
                        value for qualifier, value in values if qualifier == "Bad"
                    ]
                    if not any(good_value in recEval
                            for good_value in good_values) and good_values != []:
                        break
                    elif any(bad_value in recEval for bad_value in bad_values):
                        break
                else:            
                    print(player)
                    playersFound.append(player)
                
                

    except ValueError as e:
        # Handle the error and continue with the next iteration
        continue

    



print("DONE")

if len(playersFound) != 0:
    ans = input("Open Links? ")
    if ans == "Y":
        for pl in playersFound:
            webbrowser.open(pl)