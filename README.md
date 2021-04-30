# soccer-pronostic

This application, made in Python, is an application that make prediction on an hypothetic football match or an upcoming match. These predictions are made using the statistics of the previous matches for each team selected. 

## API

The API that I use to get all the data is https://apifootball.com. Make sure to have an API_KEY on this API before starting the project.

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

To disable the venv just make `deactivate`.

### Requirements

Once, you have installed the `pip3` and `python3-venv`, the last thing you have to do is :

```bash
pip3 install -r requirements.txt

This command will installed all the packages that the project needs.

**/ ! \\** Do not touch this file.

### Database

Firstly, create DB called `footballPrediction`,  (respect the name, else it won't work), then run the sql script which is located in `/lib/sql/db.sql`

### .env

For the environment variables, make a copy of the `.env.example` file in the root repository. Once, you have done it, include the `API_KEY` that you get in from [APIFootball](https://apifootball.com), the name of the user from the DB with his password, and the host.

```
API_KEY=[YOUR_API_KEY]
DB_USER=[YOUR_USERNAME]
DB_PASSWORD=[YOUR_PASSWORD]
DB_HOST=[THE_HOST_WHERE_THE_DB_IS]
```

## Thanks

I really want to thank the team behind [APIFootball](https://apifootball.com) who generously elevated my plan for the period of this work.

