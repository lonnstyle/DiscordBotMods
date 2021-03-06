from discord.ext import commands
from core.classes import Cog_Extension
from core.time import time_info
from datetime import datetime,timedelta
import json
import os
import requests
import re
import discord
from language import language as lang

lang = lang()
lang = lang.langpref()['event']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

emojimap = requests.get("http://gist.githubusercontent.com/Vexs/629488c4bb4126ad2a9909309ed6bd71/raw/416403f7080d1b353d8517dfef5acec9aafda6c3/emoji_map.json").text
emojimap = json.loads(emojimap)
emojimap = {x: y for y, x in emojimap.items()}

class event(Cog_Extension):
  tag = "common"
  @commands.command(name="reactionRole", aliases=["rr"],brief="指定自動身份組訊息",description="指定可自動分發身份組的訊息")
  async def rr(self,ctx,message:int):
    with open("role/rr.txt","a") as rr:
      rr.write(f"{message}\n")
      await ctx.message.add_reaction("✅")
      await ctx.message.delete(delay=5)
   

  @commands.command(name='role', aliases=lang['role.aliases'],brief=lang['role.brief'],description=lang['role.description'])
  async def role(self,ctx,role:str,emoji):
    match = re.match(r'<(a?):([a-zA-Z0-9\_]+):([0-9]+)>$', emoji)
    if (emojimap.get(emoji,None)!=None or match) and ctx.author.guild_permissions.administrator == True:
      with open("role/roles.txt","a") as roles:
        roles.write(f"{emoji},{role}\n")
      await ctx.message.add_reaction("✅")
      await ctx.message.delete(delay=5)
    else:
      await ctx.message.delete()
      await ctx.send(embed=discord.Embed(title=lang['role.error.title'],description=lang['role.error.description']))

  @commands.Cog.listener()
  async def on_raw_reaction_add(self,payload): 
    roles = {}
    message = []
    raw = open("role/roles.txt","r")
    rr = open("role/rr.txt","r")
    for line in raw.readlines():
      emoji,role = line.split(",")
      roles[emoji] = role.replace("\n","")
    for line in rr.readlines():
      message.append(line.replace("\n",""))
    for role in payload.member.guild.roles:
      if (role.name == roles.get(payload.emoji.name) or role.name == roles.get(f"<:{payload.emoji.name}:{payload.emoji.id}>")) and str(payload.message_id) in message:
        await payload.member.add_roles(role)
  
  @commands.Cog.listener()
  async def on_message(self,msg):
    if str(msg.channel.type) == 'private' and msg.author != self.bot.user:
      print(time_info.UTC_8() + str(msg.author) + lang['onMessage.say'] + msg.content)
      fp = open('./log/' + 'Private.log', 'a',encoding='utf8')
      fp.write(time_info.UTC_8() + str(msg.author) + lang['onMessage.say'] + msg.content+'\n')
      fp.close()
    else:
      if str(msg.channel.type) == 'text' and msg.author != self.bot.user:
        print(time_info.UTC_8_CH() + str(msg.author) + lang['onMessage.say'] + msg.content)
        for items in msg.attachments:
          print(items)
        a = str(msg.guild)
        b = str(msg.channel)
        fp = open('./log/' + a + '-' + b + '.log', 'a',encoding='utf8')
        fp.write(time_info.UTC_8() + str(msg.author) + lang['onMessage.say'] + msg.content+'\n')
        fp.close()
    pass

def setup(bot):
  if not os.path.exists('log'):
    os.mkdir('log')
  bot.add_cog(event(bot))