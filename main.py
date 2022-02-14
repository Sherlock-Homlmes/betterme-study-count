#### main
import os
import discord
import uvicorn
import time
from datetime import datetime,time,date
from discord.utils import get
import asyncio
from discord.ext import commands
from discord_slash import SlashCommand,SlashContext
from discord_slash.utils.manage_commands import create_option

#database
from easy_mongodb import db

#xu ly thoi gian
from timedef import minute,total_time,show_time,time_data,time_converter,leader_board

from dotenv import load_dotenv

#calc time
number =[
  "0","1","2","3","4","5","6","7","8","9"
]


def time_per_day(time1,time2,mem_id):
##check if same date
  mid9_time = time(17, 0)
  mid9 = datetime.combine(time1, mid9_time)

  t1 = 0
  t2 = 0
  if time1 < mid9 and time2 > mid9:
    time_left1 = mid9 - time1
    time_left2 = time2 - mid9
    t1 = time_left1.seconds // 60
    t2 = time_left2.seconds //60

  else:
    time_left = time2 - time1
    t1 = time_left.seconds // 60

##convert time per day
  last_30_day = db[mem_id]["time_per_day"]
  if t2 != 0:

    day = db[mem_id]["date"]
    day_time = time(day[3])
    now = datetime.utcnow()
    now =[now.year, now.month, now.day, now.hour]
    now_time = (now[3])

    date1 = date(day[0], day[1], day[2])
    date2 = date(now[0], now[1], now[2])
    date1 = datetime.combine(date1, mid9_time)
    date2 = datetime.combine(date2, mid9_time)
    date3 = time_converter(date2) - time_converter(date1)
    date3 = date3.days
    if date3 > 30:
      last_30_day = {
          "last_30_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      }
    elif date3 != 0:
      for i in range(29):
        if i + date3 <= 29:
          last_30_day[i] = last_30_day[i+date3] 
        else:
          last_30_day[i] = 0

  #plus to time per day
    last_30_day[28] += t1 
    last_30_day[29] += t2  
    db[mem_id]["date"] = now
  else:
    last_30_day[29] += t1      

  db[mem_id]["time_per_day"] = last_30_day


def plus_money(uid,money):
  db[uid]["h_all_time_transfer"] += money

def minus_money(uid,money):
  db[uid]["h_all_time_transfer"] -= money

#chuyển khoản
def money_ck(var):
  i = 0
  money = ""
  while not var[i] in number and i<=len(var):
    i = i + 1
  while var[i] in number and i<=len(var):
    money = money + var[i]
    i = i + 1
  return money  

def to_user(var):
  i = len(var) - 1
  user = ""
  while not var[i] in number and i>=0:
    i = i - 1
  while var[i] in number and i>=0:
    user = var[i] + user
    i = i - 1
  return user  



# start

#start
intents = discord.Intents().all()
client = commands.Bot(command_prefix=["m,","M,"], intents = intents)
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(' ')

@client.event
async def on_voice_state_update(member, member_before, member_after):

  voice_channel_before = member_before.channel
  voice_channel_after = member_after.channel
  if voice_channel_after != voice_channel_before:
    print("-------"+str(member)+"----------")
    #print(voice_channel_before)
    #print(voice_channel_after)
  

  mem_id = str(member.id)
  mem_name = str(member.name)

  if voice_channel_before == None and voice_channel_after != None:
    if mem_id in db.keys():
      db[mem_id]["name"] = mem_name
      #print("Start count")

      now = datetime.utcnow()
      db[mem_id]["date"] = [now.year,now.month,now.day,now.hour,now.minute]

    else:
      #default_value
      db[mem_id] = {
        "name":"",
        "date":[2020,1,1,1,1],
        "m_all_time":0,
        "time_per_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      }

      db[mem_id]["name"] = mem_name
      #print("Start cre count")

      now = datetime.utcnow()
      db[mem_id]["date"] = [now.year,now.month,now.day,now.hour,now.minute]


  if voice_channel_before != None and voice_channel_after == None:
      if mem_id not in db.keys():
        db[mem_id] = {
          "name":"",
          #date : year-mon-d-h-min
          "date":[0,0,0,0,0],
          "m_all_time":0,
          "time_per_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        }
      else:
        now = datetime.utcnow()
        start_time = time(db[mem_id]["date"][3], db[mem_id]["date"][4])
        stop_time = time(now.hour, now.minute)

        date1 = date(db[mem_id]["date"][0], db[mem_id]["date"][1], db[mem_id]["date"][2])
        date2 = date(now.year, now.month, now.day)

        datetime1 = datetime.combine(date1, start_time)
        datetime2 = datetime.combine(date2, stop_time)

        time_per_day(datetime1,datetime2,mem_id)
        time_per_day(datetime1,datetime2,"server_study_time")

        time_elapsed = datetime2 - datetime1

        #mới
        #print(str(time_elapsed))
        s_cal = time_elapsed.seconds

        #personal time
        m_user = db[mem_id]["m_all_time"]
        db[mem_id]["m_all_time"] = total_time(m_user,s_cal)

        #all server time
        m_sv = db["server_study_time"]["m_all_time"]
        db["server_study_time"]["m_all_time"] = total_time(m_sv,s_cal)

        db[mem_id]["name"] = mem_name

        show = show_time(db[mem_id]["m_all_time"])
        print(member.name + " đã học "+show[0]+" giờ "+show[1]+" phút")    
        show = show_time(db[mem_id]["time_per_day"][29])
        print(member.name + " đã học "+show[0]+" giờ "+show[1]+" phút")          
        today = show_time(db["server_study_time"]["time_per_day"][29])
        print("Hôm nay server đã học: "+str(today[0])+" giờ, "+str(today[1])+" phút")

#var
user_confirm_id = 0 
confirm = False 
user_confirm_ck_id = 0
confirm_ck = False
money = ""
to_user_ck = ""

guild = client.get_guild(880360143768924210)
guild_ids = [880360143768924210]

#################################learn_time/study_time
@slash.slash(
  name="learn_time",
  description="Kiểm tra số giờ đã học",
  guild_ids=guild_ids,
  )
async def _learn_time(ctx:SlashContext):
  member = ctx.author
  mem_id = str(member.id)
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0,
      "time_per_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    }
  elif voice_state != None:
    now = datetime.utcnow()
    start_time = time(db[mem_id]["date"][3], db[mem_id]["date"][4])
    stop_time = time(now.hour, now.minute)

    date1 = date(db[mem_id]["date"][0], db[mem_id]["date"][1], db[mem_id]["date"][2])
    date2 = date(now.year, now.month, now.day)

    datetime1 = datetime.combine(date1, start_time)
    datetime2 = datetime.combine(date2, stop_time)
    time_elapsed = datetime2 - datetime1

    #mới
    s_cal = time_elapsed.seconds

    #personal time
    m_user = db[mem_id]["m_all_time"]
    db[mem_id]["m_all_time"] = total_time(m_user,s_cal)

    db[mem_id]["date"] = [now.year,now.month,now.day,now.hour,now.minute]

  show1 = show_time(db[mem_id]["m_all_time"])
  show2 = show_time(db[mem_id]["time_per_day"][29])
  await ctx.send(member.name + " đã học "+show1[0]+" giờ "+show1[1]+" phút. Hôm nay bạn đã học "+show2[0]+" giờ "+show2[1]+" phút")

@slash.slash(
  name="study_time",
  description="Kiểm tra số giờ đã học",
  guild_ids=guild_ids,
  )
async def _study_time(ctx:SlashContext):
  member = ctx.author
  mem_id = str(member.id)
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0,
      "time_per_day":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    }
  elif voice_state != None:
    now = datetime.utcnow()
    start_time = time(db[mem_id]["date"][3], db[mem_id]["date"][4])
    stop_time = time(now.hour, now.minute)

    date1 = date(db[mem_id]["date"][0], db[mem_id]["date"][1], db[mem_id]["date"][2])
    date2 = date(now.year, now.month, now.day)

    datetime1 = datetime.combine(date1, start_time)
    datetime2 = datetime.combine(date2, stop_time)
    time_elapsed = datetime2 - datetime1

    #mới
    s_cal = time_elapsed.seconds

    #personal time
    m_user = db[mem_id]["m_all_time"]
    db[mem_id]["m_all_time"] = total_time(m_user,s_cal)

    db[mem_id]["date"] = [now.year,now.month,now.day,now.hour,now.minute]

  show = show_time(db[mem_id]["m_all_time"])
  await ctx.send(member.name + " đã học "+show[0]+" giờ "+show[1]+" phút")

###leader board
@slash.slash(
  name="leader_board",
  description="Leader board",
  guild_ids=guild_ids,
  )
async def _leader_board(ctx:SlashContext):
  board = leader_board()
  show = show_time(db["server_study_time"]["m_all_time"])
  await ctx.send("Tổng số giờ học cả server: "+show[0]+" giờ,"+show[1]+" phút\n" + "1:"+str(db[board[1]]["name"])+"\n2:"+str(db[board[2]]["name"])+"\n3:"+str(db[board[3]]["name"])+"\n4:"+str(db[board[4]]["name"])+"\n5:"+str(db[board[5]]["name"]))

#study time
@slash.slash(
  name="server_time_data",
  description="Study data control",
  guild_ids=guild_ids,
  )
async def _study_time(ctx:SlashContext):
  if ctx.channel.name == "take-data":
    tam = time_data()
    await ctx.send("Tổng số người học:"+tam[0])
    await ctx.send("Học trên 1 ngày:"+tam[1])
    await ctx.send("Học trên 1 giờ:"+tam[2])
    await ctx.send("Tổng số giờ học cả server: "+str(db["server_study_time"]["h_all_time"])+" giờ,"+str(db["server_study_time"]["m_all_time"])+"phút")



load_dotenv()
my_secret = os.environ['BOT_TOKEN']
client.run(my_secret) 
