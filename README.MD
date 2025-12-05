# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name:Allen Lapitan

Student Number: C24383676

# Screenshots
![UI](https://github.com/lentenamen/dcp25-assignment/blob/main/images/dcp1.png)
![UI showing all of info](https://github.com/lentenamen/dcp25-assignment/blob/main/images/dcp2.png)
![Search bar works](https://github.com/lentenamen/dcp25-assignment/blob/main/images/dcp3.png)

# Description of the project
Program designed to read 2 folders containing ABC files representing different books in a main folder abc_books. The program parses and stores the tunes in a dictionary which then gets stored into a list. A database is created using sqlite and is used to store a table with all of the contents in the abc_books. This data is accessed using a GUI. Pandas was used to create a dataframe to store all of the tunes.

# Instructions for use
Run a program and a window will be opened it lets you search by text but there are filters for each feature. If you click on the row where the tune is on it gives you all of the information and the notation underneath.

# How it works:
Parsing part:
This project is a project that reads in abc files from abc_books and goes through each of the subfolders in the root folder and detects that if the file ends with .abc then it will parse it based off of the start of the string and output a dictionary similar to lab 5. My analysis queries get queried. All of the tunes get inputted into the dataframe.

SQLite:
Inputs the tunes into abc_tunes.db using the list of dictionaries, no duplicate IDs are allowed if tune exists its replaced.

TKINTER :( :
Main window is created. Search and sort controls are created. User clicks filter and data is loaded into table. Table is created and displayed. When user clicks a tune details are shown.

# List of files in the project

| Files | Source |
|-----------|-----------|
| parser.py | Self written |
| big_red_button.py | Self written |
| tkintertst.py (meant to say test) | From [reference](https://coderslegacy.com/python-tkinter-gui-with-sqlite-tutorial/) |


# References
* [TKinter & Sqlite ui](https://coderslegacy.com/python-tkinter-gui-with-sqlite-tutorial/)
* [TKinter & sqlite ui](https://www.youtube.com/watch?v=gdDI_GhIRGo)
* [Parser](https://github.com/skooter500/dcp25)
* [Parser](https://github.com/lentenamen/DCP_C24383676)
* [Whole playlist](https://www.youtube.com/watch?v=fEBzetetV94&list=PLs3IFJPw3G9KL3huzPS7g-0PCbS7Auc7I&index=2)
* [MORE TKINTER](https://www.w3schools.com/python/ref_module_tkinter.asp)
* [BROCODE for TKINTER](https://www.youtube.com/watch?v=TuLxsvK4svQ)
* [TKInter reference](https://docs.python.org/3/library/tkinter.html)


# What I am most proud of in the assignment

Making the gui was the hardest but in my opinion the most fun due to my parser being mostly finished my by From [labs](https://github.com/lentenamen/DCP_C24383676) and most of the OS work was done in the starter code. I also liked calling a lot of my functions in other functions even while it was confusing. I was happy that I could use the knowledge from attending a good bit of classes with ai assistance e.g calling functions in functions, was something that I saw Bryan Dugann do in Week 5 on the Friday class and it changed the way I coded. These scaled up projects based off of the labs made be grateful for doing most of the labs. 

# What I learned

I learned that making something like this modularly worked well but calling functions inside off functions needed a lot of bandwidth in my brain to process everything. Overall it was fairly complicated but I think the way I did the parsing was the most efficient even if I had to draw maps for my functions. I think that in hindsight making a CLI is probably a lot easier than a GUI so I might do that next time given the chance. The TKinter was evidently very challenging seeing as how it was 6/8 of my references. This assignment taught me how to work with real world text formats and new data. I learned a good bit on how to use SQLite databases and inputting them into the tkinter gui. I learned how to work with the frontend and backend and how to connect them.