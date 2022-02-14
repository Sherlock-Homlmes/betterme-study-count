from datetime import datetime,time,date,timedelta
from easy_mongodb import db

#calc time
d_value = {
  "name":"",
  #date : year-mon-d-h-min
  "date":[2020,1,1,1,1],
  "m_all_time":0,
  "time_per_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}

tpd = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pass_key=["server_study_time"]


##################################def

#convert from second -> minute || minute -> hour
def minute(value):
  return value//60

#show time: hour,minute
def show_time(value):
  return [str(value//60),str(value%60)]

#plus minute and second
#value1: minute, value2: second
def total_time(value1,value2):
  return value1 + value2//60

#time data
def time_data():
  x = len(db.keys()) - 1
  y = 0
  z = 0
  for key in db.keys():
    if key not in pass_key:
      count = minute(db[key]["m_all_time"])
      if count > 24:
        y += 1
      elif count > 1:
        z += 1

  print("Tổng số người học:"+str(x))
  print("Học trên 1 ngày:"+str(y))
  print("Học trên 1 giờ:"+str(z))
  return [str(x),str(y),str(z)]

#leader board
def leader_board():
  a = sorted(db, key=lambda x: (db[x]['m_all_time']) ,reverse = True)
  return a

#time converter
def time_converter(time_val):

  time_hour = time(17, 0) 
  time_day = date(time_val.year,time_val.month,time_val.day)

  mid9 = datetime.combine(time_day, time_hour)

  if mid9 > time_val:
    time_val = mid9
  else:
    time_val = mid9 + timedelta(days=1)

  return time_val

#weekly
def study_time_weekly(mem_id):
  mem_id = str(mem_id)
  day = [0,0,0,0,0,0,0]
  for i in range(7):
    day[i] = db[mem_id]["time_per_day"][23+i]

  all_time = 0
  for i in range(7):
    all_time += day[i]
    print(i,day[i])

  return all_time

def study_time_monthly(mem_id):
  mem_id = str(mem_id)
  day = [0,0,0,0,0,0,0]
  for i in range(30):
    day[i] = db[mem_id]["time_per_day"][23+i]

  all_time = 0
  for i in range(30):
    all_time += day[i]
    print(i,day[i])

  return all_time

def abc():
  pass
