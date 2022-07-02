from tkinter import *
import pandas as pd

root = Tk()
root.title("HLTV")
root.geometry("1000x600")
filtered = 0
csv_file = pd.read_csv("..//data//MatchesResults.csv", sep=",", decimal=".")
data = csv_file["MatchStatus"]
def filterData():
    if FilterButton.cget("text") == "Filtered!":
        FilterButton.config(text="Filter")
        filtered = 0
        for i in range(len(csv_file["MatchStatus"])):
            if i == "W":
                listbox.insert(END, csv_file["MatchStatus"][i])
    else:
        FilterButton.config(text="Filtered!")
        filtered = 1
    FilterButton.place(x=0, y=0)

MatchesStatustext = Label(root, text="Matches status")
MatchesIndex = Label(root, text="index")

FilterButton = Button(root, text="Filter", command=filterData, padx=50, pady=20)
FilterButton.place(x=0, y=0)

MatchesStatustext.grid(row = 1, column=1)
MatchesIndex.grid(row = 1, column=0)
height = len(csv_file["MatchStatus"])
width = 2
scrollbar = Scrollbar(root)


listbox = Listbox(root)

listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)
scrollbar.place(x=280, y=0)
listbox.place(x=155, y=0)
if not filtered:
    for i in range(len(csv_file["MatchStatus"])):
        listbox.insert(END, csv_file["MatchStatus"][i])


root.mainloop()



