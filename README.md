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

# Admin Login
To login into admin use the following credentials:
```
Username: superuser
Password: assignment_org
```

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


# Credits
Google Auth Tutorial
   * Title: "User Registration in Django using Google OAuth"
   * Date published: 12/18/2020
   * Author: Geoffrey Mungai
   * URL: https://www.section.io/engineering-education/django-google-oauth/

