This assignment was created for the class CS 3240, Advanced Software Development Techniques at UVa. It is co-owned by Sierra Shuman, Declan Brady, Vivian Ma, Jake Coughlin, and Sam Jun.

# Setup
To setup this locally run the following commands in your terminal (in the directory you want to house this repository):
```
git clone https://github.com/uva-cs3240-f21/project-a-15.git
python -m venv .venv

# Windows
source .venv/Scripts/activate
# Mac / Linux
source .venv/bin/activate

pip install -r requirements.txt
```
Follow the Google Auth tutorial below for more info on how to set up Google login remotely.

# Templating Our HTML
To make the website more consistent I implemented a `base.html` file that can just be pulled down
in any HTML file. In all new templates the first line should be:
```
{% extends "base.html" %}
```
This will take care of all bootstrap imports so no need to do that. Then, the HTML to follow needs to be contained in:
```
{% block content %}
...HTML Stuff
{% endblock %}
```
See [appindex.html](https://github.com/uva-cs3240-f21/project-a-15/blob/main/assignment_app/templates/appindex.html) for an example.


# Credits
Google Auth Tutorial
   * Title: "User Registration in Django using Google OAuth"
   * Date published: 12/18/2020
   * Author: Geoffrey Mungai
   * URL: https://www.section.io/engineering-education/django-google-oauth/

Calendar Tutorial
   * Title: "How To Create a Calendar Using Django"
   * Date published: 7/29/2018
   * Author: Hui Wen
   * URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html

List of Authenticated Users
   * Title: "How to get the list of the authenticated users?"
   * Date published: 4/27/2010
   * Author: GeReinhart
   * URL: https://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users
