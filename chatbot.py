from weather import Weather, Unit
from textblob import TextBlob
import datetime
import re
from uszipcode import ZipcodeSearchEngine
from chatterbot import ChatBot
import chatterbot
import sys

search = ZipcodeSearchEngine()
weather = Weather(unit=Unit.CELSIUS)
today = datetime.date.today()

chatbot = ChatBot('Ron Obvious',trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

# # Train based on english greetings corpus
chatbot.train("chatterbot.corpus.english.greetings")

# Train based on the english conversations corpus
chatbot.train("chatterbot.corpus.english.conversations")

def weather_condition(txt) :
    city=""
    blob = TextBlob(txt)
    city=blob.noun_phrases
    print(city)
    for c in city:
        if 'tomorrow' in txt:
            # print(datetime.date.today() + datetime.timedelta(1))
            date=datetime.date.today() + datetime.timedelta(1)
            date=date.strftime('%d %b %Y')
            # print(date)
            forecasts = getWeatherbyCity(c)
            for forecast in forecasts:
               if date == forecast.date:
                    print("Forecast for tomorrow would be:",forecast.text)
                   # print(forecast.date)
                    # print("Tomorrow's temperature would go as high up to:",forecast.high+chr(176)+"C")
                    # print("Tomorrow's temperature would go as low up to:",forecast.low+chr(176)+"C")
        else :
            lookup = weather.lookup_by_location(c)
            print("Forecast today  in:",c.upper(),"is: ",lookup.condition.text)

def getWeatherbyCity(city) :
   
   lookup = weather.lookup_by_location(city)
   temp=lookup.condition.temp.strip()+chr(176)+"C"
   print("Weather today in ",city.upper(),"is:",temp)
   return lookup.forecast
   
def weather_function(txt) :
    city,temp,date="","",""
    reg = re.compile('^.*(?P<zipcode>\d{6}).*$')
    reg1 = re.compile('^.*(?P<zipcode>\d{5}).*$')
    if reg.match(txt) == None :
        match = reg1.match(txt)
    else :
        match = reg.match(txt)
    if(match!=None):
        zip=match.groupdict()['zipcode'] # should be 75009
        print(zip)
        zipcode = search.by_zipcode(str(zip))
        if zipcode.City != None :
            a  = getWeatherbyCity(zipcode.City)
        else :
            lookup = weather.lookup(zip)
            condition = lookup.condition	    

    blob = TextBlob(txt)
    city=blob.noun_phrases
    # print(city)
    for c in city:
        if 'tomorrow' in txt:
            # print(datetime.date.today() + datetime.timedelta(1))
            date=datetime.date.today() + datetime.timedelta(1)
            date=date.strftime('%d %b %Y')
            # print(date)
            forecasts = getWeatherbyCity(c)
            for forecast in forecasts:
               if date == forecast.date:
                    print("Forecast for tomorrow would be:",forecast.text)
                   # print(forecast.date)
                    print("Tomorrow's temperature would go as high up to:",forecast.high+chr(176)+"C")
                    print("Tomorrow's temperature would go as low up to:",forecast.low+chr(176)+"C")
        else :
            getWeatherbyCity(c)

txt = input("Bot:Hi there!\nUser:")
list=["rain","rainy","sunny","clear","cloudy","ThunderStorms","windy"]
while(1) :
    if txt.lower() == "bye":
        print("Bye!Take care")
        sys.exit()		
    if 'weather' in txt :
        print("Bot:")
        weather_function(txt)
    elif any(txt.find(s)>=0 for s in list):
        print("Bot:")
        weather_condition(txt)
    else :
        print("Bot:",chatbot.get_response(txt))
    txt = input("User:")

