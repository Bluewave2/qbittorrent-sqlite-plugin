# VERSION: 0.50
# AUTHOR: Bluewave2
# SPECIAL THANKS: To all official qBittorrent plugin repository code contributors and plugin development guide contributors
#
# LICENSING INFORMATION
# THIS SOFTWARE IS PROVIDED AS IS WITH NO WARRANTY OF ANY KIND, USE AT YOUR OWN RISK
#
# 
#  https://github.com/Bluewave2/qbittorrent-sqlite-plugin
#
#

import tkinter as tk
import sqlite3
from tkinter import filedialog
from tkinter import simpledialog
from novaprinter import prettyPrinter # type: ignore
from helpers import retrieve_url # type: ignore
import urllib.parse
import os
import json

CONFIG_FILE = 'sqliteplugin.json'
CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), CONFIG_FILE)
CONFIG_DATA = {
    'DB_PATH': None,
    'EXCLUDED_CAT': None,
    'EXCLUDED_NAME': None,
    'SETUP_DONE': False,
}

def load_configuration():
    global CONFIG_PATH, CONFIG_DATA
    try:
        with open(CONFIG_PATH) as f:
            CONFIG_DATA = json.load(f)
    except Exception:
        save_configuration()

def save_configuration():
    global CONFIG_PATH, CONFIG_DATA
    with open(CONFIG_PATH, 'w') as f:
        f.write(json.dumps(CONFIG_DATA, indent=4, sort_keys=True))

load_configuration()

class sqliteplugin(object):

    url = "Local SQLite Database"
    name = 'SQLite plugin'
    supported_categories = {
        'all': '%',
        'tv': '%tv%',
        'movies': '%movies%',
        'games': '%games%',
        'books': '%ebooks%',
        'music': '%music%',
        'software': '%software%'
    }

    #exclude_cat = "%test%" # (SQL) excluded categories, add whatever you'd like based on the database used (now possible in .json file, don't do it here)
    #exclude_name = "%test%" # (SQL) excluded names (now possible in .json file, don't do it here)

    exclude_cat = None
    exclude_name = None

    staticcon = None
    filepath = None

    dbname = None

    def __init__(self):
        try:
            self.root = tk.Tk()
            self.root.withdraw()
        except Exception as e:
            print(e)

    def search(self, what, cat='all'):
        try:
            sqliteplugin.filepath = CONFIG_DATA['DB_PATH']
            if (sqliteplugin.filepath is None):
                sqliteplugin.filepath = filedialog.askopenfilename()
                sqliteplugin.staticcon = sqlite3.connect(sqliteplugin.filepath)
                CONFIG_DATA['DB_PATH'] = sqliteplugin.filepath
                save_configuration()

            if (CONFIG_DATA['EXCLUDED_CAT'] is not None):
                sqliteplugin.exclude_cat = "%"+CONFIG_DATA['EXCLUDED_CAT'].lower()+"%" # (SQL) for use in like
            elif (CONFIG_DATA['SETUP_DONE'] == False):
                res = simpledialog.askstring("Excluded Category", "Enter ONE category to exclude (string)")
                if (res is not None):
                    CONFIG_DATA['EXCLUDED_CAT'] = res.lower()
                    sqliteplugin.exclude_cat = "%"+CONFIG_DATA['EXCLUDED_CAT'].lower()+"%" # (SQL) for use in like


            if (CONFIG_DATA['EXCLUDED_NAME'] is not None):
                sqliteplugin.exclude_cat = "%"+CONFIG_DATA['EXCLUDED_NAME'].lower()+"%" # (SQL) for use in like
            elif (CONFIG_DATA['SETUP_DONE'] == False):
                res = simpledialog.askstring("Excluded Name", "Enter ONE name (title) to exclude (string, i.e. Fort, no results with fort will show up)")
                if (res is not None):
                    CONFIG_DATA['EXCLUDED_NAME'] = res.lower()
                    sqliteplugin.exclude_name = "%"+CONFIG_DATA['EXCLUDED_NAME'].lower()+"%" # (SQL) for use in like

            CONFIG_DATA['SETUP_DONE'] = True
            save_configuration()

            sqliteplugin.staticcon = sqlite3.connect(sqliteplugin.filepath)
            cur =  sqliteplugin.staticcon.cursor()
            what = what.replace('%20', '.')
            what2 = "%" + what.replace(" ", ".").lower() + "%"
            # print (what)
            # print (what2)

            splitpath = sqliteplugin.filepath.split("/")
            dbname = splitpath[len(splitpath) - 1]

            res = cur.execute("SELECT hash, title, dt, cat, size, imdb from items where lower(cat) like ('{b2}') and lower(title) like ('{b1}') and lower(cat) not like ('{b3}') and lower(title) not like ('{b4}')".format(b1=what2,b2=sqliteplugin.supported_categories[cat],b3=sqliteplugin.exclude_cat,b4=sqliteplugin.exclude_name))
            list = res.fetchall()
            if list is None:
                return
            for row in list:
                rowdict = {
                    "link": "magnet:?xt=urn:btih:{}&dn={}".format(row[0].lower(), urllib.parse.quote(row[1])),
                    "name": row[1],
                    "size": str(row[4]) + " B",
                    "seeds": -1,
                    "leech": -1,
                    "engine_url": str(dbname),
                    "desc_link": str(row[5])
                }
                prettyPrinter(rowdict)
                # Debug
                #
                # print(str(rowdict["link"])+ " " +
                #       str(rowdict["name"])+ " " +
                #       str(rowdict["size"])+ " " +
                #       str(rowdict["seeds"])+ " " +
                #       str(rowdict["leech"])+ " " +
                #       str(rowdict["engine_url"])+ " " +
                #       str(rowdict["desc_link"])
                # )
                # print(rowdict["name"])
        except Exception as e:
            print(e)

    def download_torrent(self, info):
        return "magnet:?xt=urn:btih:{}&dn={}".format(info["info_hash"], info['name'])