from bs4 import BeautifulSoup
import requests
import telebot
import sqlite3

bot = telebot.TeleBot("1903435250:AAHYl9sTuclgFOqPcbLCppD3TVUINjpIas0")  # bot token
# @webmetry_bot - insert into telegram


def req(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "lxml")
    return soup


@bot.message_handler(commands=["start"])
def start_message(message):
    cn = sqlite3.connect("database.db")
    cur = cn.cursor()
    cur.execute("DROP TABLE IF EXISTS saveps")
    cur.execute("CREATE TABLE IF NOT EXISTS saveps(link TEXT, price TEXT)")
    # searchOzone()
    searchJarcomputers()
    searchOzone()
    printPs(message)


def searchJarcomputers():
    cn = sqlite3.connect("database.db")
    cur = cn.cursor()
    url = "https://www.jarcomputers.com/PlayStation/Konzoli_cat_257.html"
    soup = req(url)
    for y in soup.find_all("a", class_="plttl"):
        title = y.get("title")
        if title.find("playstation 4"):
            price = "xx.xx лв"
            link = y.get("href")

            data = [link, price]
            cur.execute("INSERT INTO saveps VALUES(?, ?)", data)
    cn.commit()
    cn.close()


def searchOzone():
    cn = sqlite3.connect("database.db")
    cur = cn.cursor()
    url = "https://www.ozone.bg/gaming/console-and-accessories/playstation-5/"
    soup = req(url)

    for y in soup.find_all("a", class_="product-box"):
        # title = y.find("span", class_="title")
        # print(title)
        # if(title.find("комплект") != -1):
        price = y.find("span", class_="price")
        link = y.get("href")
        data = [link, price.text]
        cur.execute("INSERT INTO saveps VALUES(?, ?)", data)
    cn.commit()
    cn.close()


def printPs(message):
    cn = sqlite3.connect("database.db")
    cur = cn.cursor()
    for y in cur.execute("SELECT * FROM saveps GROUP BY link"):
        sendingMessage = y[0] + " - " + y[1]
        bot.send_message(message.chat.id, sendingMessage)


# jarcomputers.com - https://www.jarcomputers.com/PlayStation/Konzoli_cat_257.html 1
# ardes.bg - no
# polycomp.bg - no
# emag.bg - https://www.emag.bg/search/playstation%205?ref=effective_search
# plesio.bg - https://plesio.bg/konzoli-ps5-c-69981732.html
# laptop.bg - no
# also.bg - need a company
# ozone.bg - https://www.ozone.bg/gaming/console-and-accessories/playstation-5/

bot.polling()
