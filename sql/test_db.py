#!/usr/bin/python3
import os
from db_manager import DbManager
from dotenv import load_dotenv

load_dotenv()
db = DbManager("127.0.0.1", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))
#db.delete(6)
#print (db.query())