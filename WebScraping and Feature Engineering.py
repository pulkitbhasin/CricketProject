#Web scraping and feature engineering

import bs4
import requests
import io
import lxml
import pandas as pd
import numpy as np

#Function that takes a cricinfo link as an argument and creates a dataframe with data stored in it

def getTableFromLink(link):
    data=requests.get(link)
    data=bs4.BeautifulSoup(data.text, "html.parser")
    tables = data.find_all('table')
    table = tables[0]
    new_table = pd.DataFrame(columns=range(0,14), index = range(len(table.find_all('tr'))))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            new_table.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        row_marker += 1
    return new_table


#Conduct feature engineering on batting data of each player

def feature_engineering_batsmen(dataset):
    
    #Drop empty row and rename column labels
    dataset = dataset.drop([0])
    dataset=dataset.rename(columns = {0 : "Name", 1: "Matches", 2: "Innings", 3: "NO", 4: "Runs"})
    dataset=dataset.rename(columns = {5: "Highest Score", 6: "Average", 7: "Balls Faced", 8: "Strike Rate", 9: "100s", 10: "50s"})
    dataset=dataset.rename(columns = {11: "Ducks", 12: "4s", 13: "6s"})
    
    #Clean Runs column
    runs_arr = np.array([])
    index = 0
    for elem in dataset["Runs"]:
        if (dataset["Innings"].iloc[index] == "-"):
            elem = "0"
        runs_arr = np.append(runs_arr, int(elem))
        index+=1
    dataset["Runs"] = runs_arr
    
    #Clean Average column
    average_arr = np.array([])
    index = 0
    for elem in dataset["Average"]:
        if  elem == "-":
            elem = dataset["Runs"].iloc[index]
        average_arr = np.append(average_arr, float(elem))
        index += 1
    dataset["Average"] = average_arr
    
    #Clean Balls Faced column
    bf_arr = np.array([])
    index = 0
    for elem in dataset["Balls Faced"]:
        if (dataset["Balls Faced"].iloc[index] == "-"):
            elem = "0"
        index+=1
        bf_arr = np.append(bf_arr, int(elem))
    dataset["Balls Faced"] = bf_arr
    
    #Clean Strike Rate column
    index = 0
    sr_arr = np.array([])
    for elem in dataset["Strike Rate"]:
        if (dataset["Strike Rate"].iloc[index] == "-"):
            elem = "0"
        index+=1
        sr_arr = np.append(sr_arr, float(elem))
    dataset["Strike Rate"] = sr_arr
    
    #Clean 100s column
    index = 0
    hundreds_arr = np.array([])
    for elem in dataset["100s"]:
        if (dataset["100s"].iloc[index] == "-"):
            elem = "0"
        index+=1
        hundreds_arr = np.append(hundreds_arr, int(elem))
    dataset["100s"] = hundreds_arr
    
    #Clean 50s column
    fifties_arr = np.array([])
    index = 0
    for elem in dataset["50s"]:
        if (dataset["50s"].iloc[index] == "-"):
            elem = "0"
        index+=1
        fifties_arr = np.append(fifties_arr, int(elem))
    dataset["50s"] = fifties_arr
    
    #Clean 4s column
    fours_arr = np.array([])
    index = 0
    for elem in dataset["4s"]:
        if (dataset["4s"].iloc[index] == "-"):
            elem = "0"
        index+=1
        fours_arr = np.append(fours_arr, int(elem))
    dataset["4s"] = fours_arr
    
    #Clean 6s column
    index = 0
    sixes_arr = np.array([])
    for elem in dataset["6s"]:
        if (dataset["6s"].iloc[index] == "-"):
            elem = "0"
        index+=1
        sixes_arr = np.append(sixes_arr, int(elem))
    dataset["6s"] = sixes_arr
    
    #Clean Highest Score column
    highest_score_arr = np.array([])
    for elem in dataset["Highest Score"]:
        final_elem = ""
        for i in elem: 
            if i != "*" and i != "-":
                final_elem += i
            elif i == "-":
                final_elem = "0"
        highest_score_arr = np.append(highest_score_arr, int(final_elem))
    dataset["Highest Score"] = highest_score_arr
    
    #Sort dataframe by Name column
    dataset = dataset.sort_values(by=["Name"])
    
    #Drop unnecessary columns
    dataset = dataset.drop(columns=["Ducks", "Matches", "Innings", "NO"])
    return dataset


#Create dataframe for each World Cup

dataset_batsmen_2000 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2138;team=1854;type=tournament"))
dataset_batsmen_2002 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2243;team=1854;type=tournament"))
dataset_batsmen_2004 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2391;team=1854;type=tournament"))
dataset_batsmen_2006 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/u19-worldcup/engine/records/averages/batting_bowling_by_team.html?id=2616;team=1854;type=tournament"))
dataset_batsmen_2008 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/u19wc2008/engine/records/averages/batting_bowling_by_team.html?id=3138;team=1854;type=tournament"))
dataset_batsmen_2010 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/u19wc2010/engine/records/averages/batting_bowling_by_team.html?id=5324;team=1854;type=tournament"))
dataset_batsmen_2012 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/icc-under19-world-cup-2012/engine/records/averages/batting_bowling_by_team.html?id=6767;team=1854;type=tournament"))
dataset_batsmen_2014 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/icc-under-19-world-cup-2014/engine/records/averages/batting_bowling_by_team.html?id=8909;team=1854;type=tournament"))
dataset_batsmen_2016 = feature_engineering_batsmen(getTableFromLink("https://stats.espncricinfo.com/icc-under-19-world-cup-2016/engine/records/averages/batting_bowling_by_team.html?id=10799;team=1854;type=tournament"))

#Concatenate all dataframes
batsmen_datasets = [dataset_batsmen_2000, dataset_batsmen_2002, dataset_batsmen_2004, dataset_batsmen_2006, dataset_batsmen_2008, dataset_batsmen_2010, dataset_batsmen_2012, dataset_batsmen_2014, dataset_batsmen_2016]
batsmen_dataset = pd.concat(batsmen_datasets)


#Function to create dataframe with World Cup bowling statistics for each U-19 player

def getTableFromLinkBowler(link):
    data=requests.get(link)
    data=bs4.BeautifulSoup(data.text, "html.parser")
    tables = data.find_all('table')
    table = tables[1]
    new_table = pd.DataFrame(columns=range(0,15), index = range(len(table.find_all('tr'))))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            new_table.iat[row_marker,column_marker] = column.get_text()
            column_marker += 1
        row_marker += 1
    return new_table


#Feature engineering for bowling sattistics of U-19 players

def feature_engineering_bowler(df):
    
    #Rename columns and dropping unnecessary columns
    df=df.rename(columns = {0: "Bowler Name", 3: "Overs Bowled", 6: "Wickets Taken", 8: "Bowling Average", 9: "Economy", 10: "Bowling Strike Rate", 11: "4W"})
    df = df.drop([0])
    df = df.drop(columns = [1, 2, 4, 5, 7, 12, 13, 14])
    
    #Sorting dataframe by bowler name
    df = df.sort_values(by = ["Bowler Name"])
    
    #Cleaning Overs Bowled column
    overs_bowled = np.array([])
    index = 0
    for elem in df["Overs Bowled"]:
        if (df["Overs Bowled"].iloc[index] == "-"):
            elem = "0"
        overs_bowled = np.append(overs_bowled, float(elem))
        index+=1
    df["Overs Bowled"] = overs_bowled
    
    #Cleaning Wickets Taken column
    wickets_taken = np.array([])
    index = 0
    for elem in df["Wickets Taken"]:
        if (df["Wickets Taken"].iloc[index] == "-"):
            elem = "0"
        wickets_taken = np.append(wickets_taken, int(elem))
        index+=1
    df["Wickets Taken"] = wickets_taken
    
    #CLeaning 4W column
    four_wickets = np.array([])
    index = 0
    for elem in df["4W"]:
        if (df["4W"].iloc[index] == "-"):
            elem = "0"
        four_wickets = np.append(four_wickets, int(elem))
        index+=1
    df["4W"] = four_wickets
    
    #Cleaning Bowling Average column
    bowling_average = np.array([])
    index = 0
    for elem in df["Bowling Average"]:
        if (df["Bowling Average"].iloc[index] == "-"):
            elem = "0"
        bowling_average = np.append(bowling_average, float(elem))
        index+=1
    df["Bowling Average"] = bowling_average

    bowling_average = np.array([])
    index = 0
    for elem in df["Bowling Average"]:
        if (df["Bowling Average"].iloc[index] == 0):
            elem = np.max(df["Bowling Average"])
        bowling_average = np.append(bowling_average, elem)
        index+=1
    df["Bowling Average"] = bowling_average
    
    #Cleaning Bowling Strike Rate column
    bowling_sr = np.array([])
    index = 0
    for elem in df["Bowling Strike Rate"]:
        if (df["Bowling Strike Rate"].iloc[index] == "-"):
            elem = "0"
        bowling_sr = np.append(bowling_sr, float(elem))
        index+=1
    df["Bowling Strike Rate"] = bowling_sr
    
    bowling_sr = np.array([])
    index = 0
    for elem in df["Bowling Strike Rate"]:
        if (df["Bowling Strike Rate"].iloc[index] == 0):
            elem = np.max(df["Bowling Strike Rate"])
        bowling_sr = np.append(bowling_sr, elem)
        index+=1
    index = 0
    df["Bowling Strike Rate"] = bowling_sr
    
    #Cleaning Economy column 
    economy = np.array([])
    for elem in df["Economy"]:
        if (df["Economy"].iloc[index] == "-"):
            elem = "0"
        economy = np.append(economy, float(elem))
        index+=1
    df["Economy"] = economy
    
    economy = np.array([])
    index = 0
    for elem in df["Economy"]:
        if (df["Economy"].iloc[index] == 0):
            elem = np.max(df["Economy"])
        economy = np.append(economy, elem)
        index+=1
    df["Economy"] = economy
    return df


#Creating a dataframe for bowling statistics of each player for each World Cup

bowler_2000 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2138;team=1854;type=tournament"))
bowler_2002 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2243;team=1854;type=tournament"))
bowler_2004 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/ci/engine/records/averages/batting_bowling_by_team.html?id=2391;team=1854;type=tournament"))
bowler_2006 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/u19-worldcup/engine/records/averages/batting_bowling_by_team.html?id=2616;team=1854;type=tournament"))
bowler_2008 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/u19wc2008/engine/records/averages/batting_bowling_by_team.html?id=3138;team=1854;type=tournament"))
bowler_2010 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/u19wc2010/engine/records/averages/batting_bowling_by_team.html?id=5324;team=1854;type=tournament"))
bowler_2012 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/icc-under19-world-cup-2012/engine/records/averages/batting_bowling_by_team.html?id=6767;team=1854;type=tournament"))
bowler_2014 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/icc-under-19-world-cup-2014/engine/records/averages/batting_bowling_by_team.html?id=8909;team=1854;type=tournament"))
bowler_2016 = feature_engineering_bowler(getTableFromLinkBowler("https://stats.espncricinfo.com/icc-under-19-world-cup-2016/engine/records/averages/batting_bowling_by_team.html?id=10799;team=1854;type=tournament"))


#Inputting whether each player got into the team or not

bowler_2000.insert(7, "Played for India", False)
bowler_2000["Played for India"][1] = True
bowler_2000["Played for India"][6] = True

bowler_2002.insert(7, "Played for India", False)
bowler_2002["Played for India"][5] = True
bowler_2002["Played for India"][12] = True
bowler_2002["Played for India"][4] = True

bowler_2004.insert(7, "Played for India", False)
bowler_2004["Played for India"][8] = True
bowler_2004["Played for India"][12] = True
bowler_2004["Played for India"][3] = True
bowler_2004["Played for India"][13] = True
bowler_2004["Played for India"][11] = True
bowler_2004["Played for India"][2] = True
bowler_2004["Played for India"][9] = True

bowler_2006.insert(7, "Played for India", False)
bowler_2006["Played for India"][11] = True
bowler_2006["Played for India"][5] = True
bowler_2006["Played for India"][4] = True
bowler_2006["Played for India"][2] = True
bowler_2006["Played for India"][3] = True

bowler_2008.insert(7, "Played for India", False)
bowler_2008["Played for India"][3] = True
bowler_2008["Played for India"][11] = True
bowler_2008["Played for India"][4] = True
bowler_2008["Played for India"][2] = True
bowler_2008["Played for India"][6] = True
bowler_2008["Played for India"][12] = True
bowler_2008["Played for India"][5] = True

bowler_2010.insert(7, "Played for India", False)
bowler_2010["Played for India"][4] = True
bowler_2010["Played for India"][12] = True
bowler_2010["Played for India"][9] = True

bowler_2012.insert(7, "Played for India", False)
bowler_2012["Played for India"][12] = True

bowler_2014.insert(7, "Played for India", False)
bowler_2014["Played for India"][6] = True
bowler_2014["Played for India"][13] = True
bowler_2014["Played for India"][15] = True

bowler_2016.insert(7, "Played for India", False)
bowler_2016["Played for India"][6] = True
bowler_2016["Played for India"][14] = True
bowler_2016["Played for India"][3] = True


#Inputting whether a player was captain or not

bowler_2000.insert(8, "Captain", 0)
bowler_2000["Captain"].iloc[2] = 1

bowler_2002.insert(8, "Captain", 0)
bowler_2002["Captain"].iloc[7] = 1

bowler_2004.insert(8, "Captain", 0)
bowler_2004["Captain"].iloc[1] = 1

bowler_2006.insert(8, "Captain", 0)
bowler_2006["Captain"].iloc[10] = 1

bowler_2008.insert(8, "Captain", 0)
bowler_2008["Captain"].iloc[11] = 1

bowler_2010.insert(8, "Captain", 0)
bowler_2010["Captain"].iloc[0] = 1

bowler_2012.insert(8, "Captain", 0)
bowler_2012["Captain"].iloc[10] = 1

bowler_2014.insert(8, "Captain", 0)
bowler_2014["Captain"].iloc[14] = 1

bowler_2016.insert(8, "Captain", 0)
bowler_2016["Captain"].iloc[3] = 1

bowlers = [bowler_2000, bowler_2002, bowler_2004, bowler_2006, bowler_2008, bowler_2010, bowler_2012, bowler_2014, bowler_2016]
bowling_dataset = pd.concat(bowlers)


#Cleaning indices

bowling_dataset = bowling_dataset.set_index(np.arange(121))
batsmen_dataset = batsmen_dataset.copy(deep = True)
batsmen_dataset = batsmen_dataset.set_index(np.arange(121))


#Column concatentation of batsmen and bowlers statistics

final_dataset = pd.concat([batsmen_dataset, bowling_dataset], axis = 1)
final_dataset = final_dataset.drop(columns = ["Bowler Name"])


#Extracting batsmen and exporting dataset to spreadsheet
battingDataset = final_dataset.take([0, 2, 4, 5, 6, 7, 9, 10, 12, 14, 16, 17, 18, 19, 22, 23, 24, 26, 27, 28, 30, 31, 33, 34, 35, 36, 39, 40, 41, 42, 45, 47, 48, 54, 59, 60, 61, 62, 63, 64, 70, 71, 72, 73, 74, 75, 78, 79, 80, 81, 84, 85, 87, 89, 90, 93, 94, 96, 97, 98, 102, 103, 104, 105, 106, 107, 108, 109, 110, 113, 114, 115, 116, 118])
final_dataset.to_csv("U-19 World Cup Dataset.csv")




