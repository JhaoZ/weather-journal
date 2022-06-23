from plumbum import cli, colors
from pyfiglet import Figlet
import questionary
from questionary import prompt
import yaml, ruamel.yaml
import os, fnmatch
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import textwrap
import sys
import shutil

author = ""
journal_name = ""

def save_config(filename, config):
    yaml = ruamel.yaml.YAML()
    with open(filename, "w") as file:
        yaml.dump(config, file)

def load_config(filename):
    global author, journal_name
    if not os.path.exists(filename):
        save_config(filename, 
        {
            "author": '',
            "journal_name": '',
        }
        )

    with open(filename, "r") as file:
        data = yaml.safe_load(file)
    author = data['author']
    journal_name = data['journal_name']

def open_journal():
    today_entry = str(datetime.today().strftime('%Y-%m-%d')) + ".txt"
    if not os.path.basename(os.getcwd()) == journal_name:
        os.chdir(journal_name)
    journal_list = os.listdir()

    #looping through the list of journals to check if there is an entry for today
    if not journal_list:
        add_page()
    for journal in journal_list:
        if fnmatch.fnmatch(journal, today_entry):
            add_content(today_entry)
            return
    add_page()

def print_banner(text):
    with colors['LIGHT BLUE']:
        print(Figlet(font = 'slant').renderText(text))

def init_folder(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError:
        print(f"Creating the directory {folder_name} has failed.")

    os.chdir(journal_name)
    add_page()

def add_page():
    today_entry = str(datetime.today().strftime('%Y-%m-%d'))+ ".txt"
    open(today_entry, 'x')
    print("Created Entry" + today_entry)
    add_content(today_entry)

def add_content(title):
    city = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("Which city weather data to add?").ask())
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]

    with open(title, 'a') as entry:
        writing = questionary.text("What notes do you want to add?").ask()
        text = 'Location: ' + city +  '\n'  + 'Temperature: ' + temp + '\n' + 'Time: ' + time + '\n' + 'Sky: ' + sky + '\n' + 'Other: ' + other_data + '\n'
        prettier_writing = textwrap.fill(text) + '\n' + textwrap.fill(writing) + '\n'
        entry.write(prettier_writing)

def create_journal():
    global author, journal_name
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    
    #find the place to save the journal
    journal_name = ruamel.yaml.scalarstring.DoubleQuotedScalarString(author + "-Journal")

    my_dict = dict(author=author, journal_name=journal_name)

    save_config("config.yaml", my_dict)
    init_folder(journal_name)

def view_weather():
    city = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("Which city?").ask())
    url = "https://www.google.com/search?q="+"weather"+city
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
    str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
    data = str.split('\n')
    time = data[0]
    sky = data[1]
    listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
    strd = listdiv[5].text
    pos = strd.find('Wind')
    other_data = strd[pos:]
    print("Temperature is", temp)
    print("Time: ", time)
    print("Sky Description: ", sky)
    print(other_data)

def read_entries():
    global journal_name
    if not os.path.basename(os.getcwd()) == journal_name:
        os.chdir(journal_name)
    journal_list = os.listdir()

    question = [{
        "type": "select",
        "name": "select_entry",
        "message": "Choose an entry to read",
        "choices": journal_list
    },]
    entry = prompt(question)['select_entry']
    with open(entry, 'r') as e:
        print(e.read())

class weather_journal(cli.Application):
    VERSION = "0.0"

    delete = cli.Flag(['d', 'delete'], help = 'Deletes your journal (Warning: There is no confirmation message)')

    def main(self):
        load_config("config.yaml")

        if self.delete:
            if not journal_name == "":
                shutil.rmtree(journal_name)
                save_config("config.yaml", {
                    "author":"",
                    "journal_name":"",
                })
                print("Successfully deleted!")
                return
            else:
                print("You don't have any journals to delete!")

        print_banner('Weather Journal')

       

        end = False
        while not end:
            choice = questionary.select(
            "What would you like to do",
            choices=[
                'View Weather',
                'Write',
                'Read Entries',
                'Quit'
            ]).ask()
            if choice == 'Write':
                if journal_name == "":
                    create_journal()
                else:
                    open_journal()
            elif choice == "View Weather":
                view_weather()
            elif choice == 'Read Entries':
                read_entries()
            elif choice == 'Quit':
                print("Program ended!")
                end = True
                break
                
        
                

if __name__ == "__main__":
    weather_journal()