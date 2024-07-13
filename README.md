# qbittorrent-sqlite-plugin

Alpha release, functionality not guaranteed.
Windows support only (TBD)

Current functionality is for a specific (popular) database, code alteration is required for usage with other databases. (TBD)
-----
# How to use?
1. Add the ```.py``` and ```.ico``` files to  Windows: ```%localappdata%\qBittorrent\nova3\engines\```
2. Run qBittorrent
3. View -> Check "Search Engine"
4. Switch to "Search" tab
5. Click "Search plugins..."
6. "Install a new one" -> "Local file" -> select the .py file
7. Attempt to search something using the plugin, a file dialog will pop up asking you to select the SQLite database file
8. Another dialog will ask for exclusion of ONE (TBD) specific category, you can cancel if you don't want to
9. Another dialog will ask for exclusion of ONE (TBD) specific title string (i.e. if you type fort, your searches will never include anything with Fort in it at any place in the title), you can cancel if you don't want to
10. After first time setup (steps 7, 8, 9) your settings are saved to sqliteplugin.json and are editable via text editor. The program will no longer ask you for any of these settings.
11. In case of any problems, delete the sqliteplugin.json file entirely and set it up again

Enjoy
