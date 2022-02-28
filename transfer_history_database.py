from threading import Thread
import os
import time
######database
#
from pymongo import MongoClient

from threading import Thread
from waiting import wait

from dotenv import load_dotenv

## thuộc tính: account, password, key1, key2
load_dotenv()
database_url = os.getenv('database_url', "value does not exist")
cluster = MongoClient(database_url)
dtbs = cluster["discord_betterme"]
dtb = dtbs["transfer_history"]
#start
#########################################advance#####################################
#cre_data
def cre_tdb(name):
  name = str(name)
  tests = dtb.find({ "id":name })
  i = 0
  for test in tests:
    i += 1

  if i == 0:
  	default_data ={
    "id": name,
  	"history":{}
  	}
  	dtb.insert_one(default_data)
  else:
    print("already have "+name)

#take_data
def take_tdb(name):
  tests = dtb.find( { "id":name } )
  i = 0
  for test in tests:
    i += 1
    return test["history"]

  if i == 0: return False

#update_data
def update_tdb(name,value):
  global dtb
  dtb.update_one({ "id": name },  {'$set': {'history':value}} )

#delete_data
def delete_data(name):
  database = dtb.find({ "id": name })
  for elements in database:
    dtb.delete_many(elements)

#delete all
def delete_all_data():
  database = dtb.find()
  for elements in database:
    dtb.delete_many(elements)

    