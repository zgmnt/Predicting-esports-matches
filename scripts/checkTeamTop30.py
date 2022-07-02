import pandas as pd

top30 = pd.read_csv("..//data//TeamRanking.csv", sep=",")
upcomingMatches = pd.read_csv("..//data//UpcomingMatches.csv", sep=",")

for i in range(len(upcomingMatches["Team A"])):
    if upcomingMatches["Team A"][i] in list(top30["name"]):
        print(upcomingMatches["Team B"][i] in list(top30["name"]))





