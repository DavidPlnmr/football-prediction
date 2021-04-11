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
If an error appears, make `sudo apt install`. Else, you can see if the package has been correctly installed using `pip3 --version`

### `Requests` package
The package is used to make calls to the API that it's used. Be certain that you have this package downloaded before launching the app.
```bash
pip3 install requests
```

### `Dotenv`
Make sure to have `python-dotenv` installed. Then, you'll need to make a copy of the `.env.example` file and name it `.env` and put your own credentials in the environment variable `API_KEY`. You can get your own key at this link : https://apifootball.com

### Database
The app uses a database. You can find the structure of the DB in the "sql" repository. Don't forget to change the `.env` file with the correct username and password to connect to your DB.