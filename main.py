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
from tpd_database import take_data,cre_data

#xu ly thoi gian
from timedef import minute, total_time, show_time, time_data, leader_board, time_per_day, time_in_day

from dotenv import load_dotenv

#calc time
number =[
  "0","1","2","3","4","5","6","7","8","9"
]

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
bot = commands.Bot(command_prefix=["m,","M,"], intents = intents)
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(' ')

@bot.event
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
        "m_all_time":0
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
          "m_all_time":0
        }
      else:
        now = datetime.utcnow()
        start_time = time(db[mem_id]["date"][3], db[mem_id]["date"][4])
        stop_time = time(now.hour, now.minute)

        date1 = date(db[mem_id]["date"][0], db[mem_id]["date"][1], db[mem_id]["date"][2])
        date2 = date(now.year, now.month, now.day)

        datetime1 = datetime.combine(date1, start_time)
        datetime2 = datetime.combine(date2, stop_time)

        time_per_day(mem_id,datetime1,datetime2)
        time_per_day("server_study_time",datetime1,datetime2)

        s_cal = (datetime2 - datetime1).seconds

        #mới

        #personal time
        m_user = db[mem_id]["m_all_time"]
        db[mem_id]["m_all_time"] = total_time(m_user,s_cal)

        #all server time
        m_sv = db["server_study_time"]["m_all_time"]
        db["server_study_time"]["m_all_time"] = total_time(m_sv,s_cal)

        db[mem_id]["name"] = mem_name

        show = show_time(db[mem_id]["m_all_time"])
        print(member.name + " đã học "+show[0]+" giờ "+show[1]+" phút")    


#var
user_confirm_id = 0 
confirm = False 
user_confirm_ck_id = 0
confirm_ck = False
money = ""
to_user_ck = ""

guild = bot.get_guild(880360143768924210)
guild_ids = [880360143768924210]
##################################################################command##########################################
#################################learn_time/study_time
@bot.command(name="learn_time",description="Kiểm tra số giờ đã học")
async def _learn_time(ctx):
  member = ctx.author
  mem_id = str(member.id)
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
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
  await ctx.send(member.name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")

@bot.command(name="study_time",description="Kiểm tra số giờ đã học",)
async def _study_time(ctx):
  member = ctx.author
  mem_id = str(member.id)
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
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
@bot.command(name="leader_board",description="Leader board")
async def _leader_board(ctx):
  board = leader_board()
  show = show_time(db["server_study_time"]["m_all_time"])
  await ctx.send("Tổng số giờ học cả server: "+show[0]+" giờ,"+show[1]+" phút\n" + "1:"+str(db[board[1]]["name"])+"\n2:"+str(db[board[2]]["name"])+"\n3:"+str(db[board[3]]["name"])+"\n4:"+str(db[board[4]]["name"])+"\n5:"+str(db[board[5]]["name"]))

#study time
@bot.command(name="server_time_data",description="Study data control")
async def _study_time(ctx):
  if ctx.channel.name == "take-data":
    tam = time_data()
    await ctx.send("Tổng số người học:"+tam[0])
    await ctx.send("Học trên 1 ngày:"+tam[1])
    await ctx.send("Học trên 1 giờ:"+tam[2])
    await ctx.send("Tổng số giờ học cả server: "+str(db["server_study_time"]["h_all_time"])+" giờ,"+str(db["server_study_time"]["m_all_time"])+"phút")

##################################################################slash##########################################
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
      "m_all_time":0
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
  await ctx.send(member.name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")

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
      "m_all_time":0
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
#bot.loop.create_task(time_per_day_data())
bot.run(my_secret)
