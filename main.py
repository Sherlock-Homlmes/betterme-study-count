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

# start

#start
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=["m,","M,"], intents = intents)
slash = SlashCommand(bot, sync_commands=True)

def time_caculate(mem_id,mem_name):
  mem_id = str(mem_id)

  now = datetime.utcnow()
  start_time = time(db[mem_id]["date"][3], db[mem_id]["date"][4])
  stop_time = time(now.hour, now.minute)

  date1 = date(db[mem_id]["date"][0], db[mem_id]["date"][1], db[mem_id]["date"][2])
  date2 = date(now.year, now.month, now.day)

  datetime1 = datetime.combine(date1, start_time)
  datetime2 = datetime.combine(date2, stop_time)

  #time per day count
  time_per_day(mem_id,datetime1,datetime2)
  time_per_day("server_study_time",datetime1,datetime2)


  s_cal = (datetime2 - datetime1).seconds

  #personal time
  m_user = db[mem_id]["m_all_time"]
  db[mem_id]["m_all_time"] = total_time(m_user,s_cal)

  #all server time
  m_sv = db["server_study_time"]["m_all_time"]
  db["server_study_time"]["m_all_time"] = total_time(m_sv,s_cal)


  db[mem_id]["date"] = [now.year, now.month, now.day,now.hour, now.minute]
  db["server_study_time"]["date"] = [now.year, now.month, now.day,now.hour, now.minute]
  db[mem_id]["name"] = mem_name

  show = show_time(db[mem_id]["m_all_time"])
  print(mem_name + " đã học "+show[0]+" giờ "+show[1]+" phút")    


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
        time_caculate(mem_id,mem_name)  


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
  mem_name = member.name
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
    }
  elif voice_state != None:
    time_caculate(mem_id,mem_name)

  show1 = show_time(db[mem_id]["m_all_time"])
  await ctx.send(mem_name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")

@bot.command(name="study_time",description="Kiểm tra số giờ đã học",)
async def _study_time(ctx):
  member = ctx.author
  mem_id = str(member.id)
  mem_name = member.name
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
    }
  elif voice_state != None:
    time_caculate(mem_id,mem_name)

  show1 = show_time(db[mem_id]["m_all_time"])
  await ctx.send(mem_name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")


###leader board
@bot.command(name="leader_board",description="Leader board")
async def _leader_board(ctx):
  board = leader_board()
  show = show_time(db["server_study_time"]["m_all_time"])

  def number(mem_id,pos):
    show = show_time(db[mem_id]["m_all_time"])
    return str(pos)+": "+str(db[mem_id]["name"])+": "+str(show[0])+" giờ,"+str(show[1])+" phút"

  lead_board =""
  for i in range(1,11):
    lead_board += "\n"+number(board[i],i)

  await ctx.send("Tổng số giờ học cả server: "+show[0]+" giờ,"+show[1]+" phút\n" +lead_board)


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
  mem_name = member.name
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
    }
  elif voice_state != None:
    time_caculate(mem_id,mem_name)

  show1 = show_time(db[mem_id]["m_all_time"])
  await ctx.send(mem_name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")

@slash.slash(
  name="study_time",
  description="Kiểm tra số giờ đã học",
  guild_ids=guild_ids,
  )
async def _study_time(ctx:SlashContext):
  member = ctx.author
  mem_id = str(member.id)
  mem_name = member.name
  voice_state = member.voice
  if mem_id not in db.keys():
    db[mem_id] = {
      "name":"",
      "date":[0,0,0,0,0],
      "m_all_time":0
    }
  elif voice_state != None:
    time_caculate(mem_id,mem_name)

  show1 = show_time(db[mem_id]["m_all_time"])
  await ctx.send(mem_name + " đã học "+show1[0]+" giờ "+show1[1]+" phút")
###leader board
@slash.slash(
  name="leader_board",
  description="Leader board",
  guild_ids=guild_ids,
  )
async def _leader_board(ctx:SlashContext):
  board = leader_board()
  show = show_time(db["server_study_time"]["m_all_time"])

  def number(mem_id,pos):
    show = show_time(db[mem_id]["m_all_time"])
    return str(pos)+": "+str(db[mem_id]["name"])+": "+str(show[0])+" giờ,"+str(show[1])+" phút"

  lead_board =""
  for i in range(1,11):
    lead_board += "\n"+number(board[i],i)

  await ctx.send("Tổng số giờ học cả server: "+show[0]+" giờ,"+show[1]+" phút\n" +lead_board)

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

#hstc
@bot.command(name = "hstc",description = "mua role hstc")
async def _hstc(ctx):

  hstc = ctx.guild.get_role(882810506824515615)

  if hstc in ctx.author.roles:
    await ctx.send("Bạn đã có role HSTC")
  elif db[str(ctx.author.id)]["m_all_time"] >= 12000:

    message = await ctx.send("Xác nhận mua role(200 coins)\nNếu không xác nhận sau 30 giây, giao dịch sẽ bị hủy bỏ")

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    try:
      reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.emoji in ['✅','❌'],timeout = 30.0)

      if reaction.emoji == '❌':
        await ctx.send("Giao dịch đã bị hủy bỏ")
      elif reaction.emoji == '✅':

        from transfer_history_database import cre_tdb, take_tdb, update_tdb

        his = take_tdb(str(ctx.author.id))
        if his != False:
          his["Mua role HSTC"] = 200
        else:
          cre_tdb(str(ctx.author.id))
          his = {}
          his["Mua role HSTC"] = 200
        update_tdb(str(ctx.author.id),his)


        await ctx.author.add_roles(hstc)
        await ctx.send("Chúc mừng {} đã có role HSTC".format(ctx.author.mention))

    except:
      await ctx.send("Có lỗi trong quá trình cấp role, hãy liên hệ với AD để giải quyết")


  else:
    await ctx.send("Bạn cần ít nhất 200 coin(tương đương với 200 giờ học để mua role HSTC")
    
#hstc
#study time
@slash.slash(
  name="hstc",
  description="hstc",
  guild_ids=guild_ids,
  )
async def _hstc(ctx:SlashContext):

  hstc = ctx.guild.get_role(882810506824515615)

  if hstc in ctx.author.roles:
    await ctx.send("Bạn đã có role HSTC")
  elif db[str(ctx.author.id)]["m_all_time"] >= 12000:

    message = await ctx.send("Xác nhận mua role(200 coins)\nNếu không xác nhận sau 30 giây, giao dịch sẽ bị hủy bỏ")

    await message.add_reaction('✅')
    await message.add_reaction('❌')

    try:
      reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.emoji in ['✅','❌'],timeout = 30.0)

      if reaction.emoji == '❌':
        await ctx.send("Giao dịch đã bị hủy bỏ")
      elif reaction.emoji == '✅':

        from transfer_history_database import cre_tdb, take_tdb, update_tdb

        his = take_tdb(str(ctx.author.id))
        if his != False:
          his["Mua role HSTC"] = 200
        else:
          cre_tdb(str(ctx.author.id))
          his = {}
          his["Mua role HSTC"] = 200
        update_tdb(str(ctx.author.id),his)


        await ctx.author.add_roles(hstc)
        await ctx.send("Chúc mừng {} đã có role HSTC".format(ctx.author.mention))

    except:
      await ctx.send("Có lỗi trong quá trình cấp role, hãy liên hệ với AD để giải quyết")


  else:
    await ctx.send("Bạn cần ít nhất 200 coin(tương đương với 200 giờ học để mua role HSTC")
  


@bot.command(name="print",description="Kiểm tra số giờ đã học")
async def _learn_time(ctx):
  take1 = take_data(str(ctx.author.id))
  await ctx.send("```"+str(take1)+"```")

  take2 = take_data("server_study_time")
  await ctx.send("```"+str(take2)+"```")

load_dotenv()
my_secret = os.environ['BOT_TOKEN']
###bot.loop.create_task(time_per_day_data())
bot.run(my_secret)
