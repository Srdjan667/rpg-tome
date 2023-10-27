# Overview
The idea for this project was to enable Players and Dungeon Masters alike to store all their items and spells in one place.

## Requirements
    python 3.7 or greater

    requirements.txt

## Installation
Upon the installation navigate to root folder (folder that contains `manage.py`) and run from Command Prompt (Windows), or Terminal (Linux) following commands:

### Create virtual environment
    python -m venv venv

### Activate virtual environment
#### Windows:
    venv\Scripts\activate
#### Linux:
    source venv/bin/activate

### Install requirements
    pip install -r requirements.txt

### Apply the migrations to the database
    python manage.py migrate

## Development server
After installing requirements, you can run the testing server from root folder:

    python manage.py runserver

After that you should be able to see webpage in your browser by entering the following address:

    localhost:8000/

Every time you make a change and save a file, refresh the browser and change will show up.
In rare cases when your change don't show up immediately, just restart the server by pressing CTRL-C and run the server again.

You know your server is running succesfully when text similar to the one below appears:

    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    March 15, 2023 - 14:29:32
    Django version 4.1.5, using settings 'RPG_Tome.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
