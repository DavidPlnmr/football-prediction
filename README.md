# soccer-pronostic

This application, made in Python, is an application that make prediction on an hypothetic football match or an upcoming match. These predictions are made using the statistics of the previous matches for each team selected. 

## API

The API that I use to get all the data is https://apifootball.com.

## Getting Started

This app uses the third version of Python (so `python3`).



### `pip3`

Firstly, make sure to have pip3 installed to download all the packages to be sure that the app works correctly.
```bash
sudo apt install python3-pip
```
If an error appears, make `sudo apt update && sudo apt upgrade`. Else, you can see if the package has been correctly installed using `pip3 --version`

### Virtual environment

For the beginning, it should be better for you to use a virtual environment for this project and then to install everything.
The virtualenv package helps you to not have problem with other versions of libraries with other python projects.
To setup a virtual environment, you need to install the virtualenv package using
```bash
sudo apt install python3-venv
```
Then to create the venv :
```bash
python3 -m venv venv
```
After doing this, you'll need to activate the environment by doing :
```bash
source venv/bin/activate
```
Now, you can see that your shell is working on your virtual environment for Python. 

Now, make all the `pip3 install` commands in the venv.

### `Requests` package
The package is used to make calls to the API that it's used. Be certain that you have this package downloaded before launching the app.
```bash
pip3 install requests
```

### `Dotenv`
Make sure to have `python-dotenv` installed. Then, you'll need to make a copy of the `.env.example` file and name it `.env` and put your own credentials in the environment variable `API_KEY`. You can get your own key at this link : https://apifootball.com

To install :
```bash
pip3 install python-dotenv
```

### `Database`
The app uses a database. You can find the structure of the DB in the "sql" repository. Don't forget to change the `.env` file with the correct username and password to connect to your DB.

To install the package that permits you to communicate with the DB :
```bash
pip3 install mysql-connector-python
```

### `Python Flask`
For the view, we use Python Flask. To make all the good setup, follow the link down below :
https://flask.palletsprojects.com/en/1.1.x/installation/

OR

```bash
pip3 install Flask
```
And then to run the view make `flask run`

### Dateutil

This package is used to make addition of dates.

Installation : 
```bash
pip3 install python-dateutil
```

## Thanks
I really want to thank the team behind [APIFootball](https://apifootball.com) who generously elevated my plan for the period of this work.
