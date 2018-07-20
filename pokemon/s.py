import json

with open('myjson.json') as rawWeather:
    weather = json.load(rawWeather)

weatherString = ""

for weatherData in weather["Location"]["periods"]:
    weatherString += weatherData["Type"] + ": " + str(weatherData["Index"]) + "\n"

print(weatherString)