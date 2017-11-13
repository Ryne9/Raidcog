import json

file = open ("C:/Users/cupca/Documents/Raidcog/gamecog/data/blackcards.csv")
blackcards = []
whitecards = []
for item in file.readlines():
    blackcards.append(item.rstrip())
file.close()

file = open ("C:/Users/cupca/Documents/Raidcog/gamecog/data/whitecards.csv")
for item in file.readlines():
    whitecards.append(item.rstrip())
file.close()


with open('gamecog/whitecards.json', 'w') as outfile:
    json.dump(whitecards, outfile)
with open('gamecog/blackcards.json', 'w') as outfile:
    json.dump(blackcards, outfile)