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
* [MORE TKINTER](https://www.w3schools.com/python/ref_module_tkinter.asp)



# What I am most proud of in the assignment

Making the gui was the hardest but in my opinion the most fun due to my parser being mostly finished my by From [labs](https://github.com/lentenamen/DCP_C24383676) and most of the OS work was done in the starter code. I also liked calling a lot of my functions in other functions even while it was confusing.

# What I learned

I learned that making something like this modularly worked well but calling functions inside off functions needed a lot of bandwidth in my brain. 

## Below is how to use Markdown. You can delete this:

## This is how to markdown text:

This is *emphasis*

This is a bulleted list

- Item
- Item

This is a numbered list

1. Item
1. Item

This is a [hyperlink](http://bryanduggan.org)

# Headings
## Headings
#### Headings
##### Headings

This is code:

```Java
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

So is this without specifying the language:

```
public void render()
{
	ui.noFill();
	ui.stroke(255);
	ui.rect(x, y, width, height);
	ui.textAlign(PApplet.CENTER, PApplet.CENTER);
	ui.text(text, x + width * 0.5f, y + height * 0.5f);
}
```

This is an image using a relative URL:

![An image](images/p8.png)

This is an image using an absolute URL:

![A different image](https://bryanduggandotorg.files.wordpress.com/2019/02/infinite-forms-00045.png?w=595&h=&zoom=2)

This is a youtube video:

[![YouTube](http://img.youtube.com/vi/J2kHSSFA4NU/0.jpg)](https://www.youtube.com/watch?v=J2kHSSFA4NU)

This is a table:

| Heading 1 | Heading 2 |
|-----------|-----------|
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |
|Some stuff | Some more stuff in this column |

|Some stuff | Some more stuff in this column |
