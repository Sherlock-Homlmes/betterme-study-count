from datetime import datetime,time,date,timedelta
from easy_mongodb import db
from tpd_database import cre_data, take_data, update_data, delete_data

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

######################time per day##################
#real_time
def real_time(time_value):
  return time_value + timedelta(hours=7)

#check if don't have data
def cre_new_day(udb,time_value):

  if str(time_value.year) not in udb:
    udb[str(time_value.year)] = {}
  if str(time_value.month) not in udb[str(time_value.year)]:
    udb[str(time_value.year)][str(time_value.month)] = {}
  if str(time_value.day) not in udb[str(time_value.year)][str(time_value.month)]:
    udb[str(time_value.year)][str(time_value.month)][str(time_value.day)] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  return udb

#từ thời điểm đó -> giờ tiếp theo
def time_up(time_value):
  next_hour = (time_value + timedelta(hours=1)).replace(microsecond=0, second=0, minute=0)

  wait_seconds = (next_hour - time_value).seconds   

  return minute(wait_seconds)

#từ giờ trước đó -> thời điểm đó
def time_down(time_value):

  past_hour = time_value.replace(microsecond=0, second=0, minute=0)
  wait_seconds = (time_value - past_hour).seconds   
  return minute(wait_seconds)

#time per hour
def time_per_hour(time1,time2,time_val):

  hour1 = time1.hour
  hour2 = time2.hour

  if hour1 == hour2:
    time_del = time2 - time1
    time_del = time_del.seconds
    time_val[hour1] += minute(time_del)
  else:
    if hour2 == 0 and time2.minute == 0:
      for i in range(hour1+1,24):
        time_val[i] = 60

      time_val[hour1] += time_up(time1)
    else:
      for i in range(hour1+1,hour2):
        time_val[i] = 60

      time_val[hour1] += time_up(time1)
      time_val[hour2] += time_down(time2)

  return time_val


#time per day
def time_per_day(member_id, time1, time2):

  time1 = real_time(time1)
  time2 = real_time(time2)

  member_id = str(member_id)
  udb = take_data(member_id)

  if take_data(member_id) == False:
    cre_data(member_id)
    udb = take_data(member_id)

  if time1.day != time2.day:
    udb = cre_new_day(udb,time1)
    udb = cre_new_day(udb,time2)

    mid9 = time2.replace(minute=0,hour=0)

    udb[str(time1.year)][str(time1.month)][str(time1.day)] = time_per_hour(time1,mid9,udb[str(time1.year)][str(time1.month)][str(time1.day)])
    udb[str(time2.year)][str(time2.month)][str(time2.day)] = time_per_hour(mid9,time2,udb[str(time2.year)][str(time2.month)][str(time2.day)])


  else:
    udb = cre_new_day(udb,time1)

    udb[str(time1.year)][str(time1.month)][str(time1.day)] = time_per_hour(time1,time2,udb[str(time1.year)][str(time1.month)][str(time1.day)])


  update_data(member_id,udb)

#time in day
def time_in_day(member_id):
  member_id = str(member_id)
  udb = take_data(member_id) 

  for val in udb[str(time1.year)][str(time1.month)][str(time1.day)]:
    day_time += udb[str(time1.year)][str(time1.month)][str(time1.day)][val]

  return day_time
