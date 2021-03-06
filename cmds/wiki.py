from discord.ext import commands
from core.classes import Cog_Extension
import discord
from mwclient import Site
import json
from fuzzywuzzy import process
from language import language as lang

lang = lang()
lang = lang.langpref()['wiki']

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

zhURL = 'warframe.huijiwiki.com'
tcURL = 'warframe.fandom.com'
enURL = 'warframe.fandom.com'

zh = Site(zhURL,scheme='http')
tc = Site(tcURL, path='/zh-tw/', scheme='http')
en = Site(enURL, path='/', scheme='http')


class wiki(Cog_Extension):
  tag = "Warframe"
  @commands.command(name='update_wiki',brief=lang['update_wiki.brief'],description=lang['update_wiki.description'])
  async def update_wiki(self,ctx,*wiki):
    name = " ".join(wiki)
    if name == "zh"or"all":
      allpages= zh.allpages()
      with open("dict/zh_pages.txt","w") as zh_pages:
        for page in allpages:
          print(page.name,file = zh_pages)
    if name == "tc"or"all":
      allpages= tc.allpages()
      with open("dict/tc_pages.txt","w") as tc_pages:
        for page in allpages:
          print(page.name,file = tc_pages)
    if name == "en"or"all":
      allpages= en.allpages()
      with open("dict/en_pages.txt","w") as en_pages:
        for page in allpages:
          print(page.name,file = en_pages)
  @commands.command(name='wiki',aliases=lang['wiki.aliases'],brief=lang['wiki.brief'],description=lang['wiki.description'])
  async def wiki(self,ctx,*page):
    name = " ".join(page)
    with open("dict/zh_pages.txt","r") as zh_pages:
      zhpage = []
      for page in zh_pages.readlines():
        zhpage.append(page)
    with open("dict/tc_pages.txt","r") as tc_pages:
      tcpage = []
      for page in tc_pages.readlines():
        tcpage.append(page)
    with open("dict/en_pages.txt","r") as en_pages:
      enpage = []
      for page in en_pages.readlines():
        enpage.append(page)
    title,ratio = process.extractOne(name,zhpage)
    if ratio>75:
      footer = lang['wiki.footer.huiji']
      URL = f"https://{zhURL}/wiki/{title}"
    else:
      title,ratio = process.extractOne(name,tcpage)
      if ratio>75:
        footer = lang['wiki.footer.tc']
        URL = f"https://{tcURL}/zh-tw/wiki/{title}"
      else:
        title,ratio = process.extractOne(name,enpage)
        if ratio>75:
          footer = lang['wiki.footer.en']
          URL = f"https://{enURL}/wiki/{title}"
        else:
          await ctx.send(lang['wiki.error.notFound'].format(self=jdata['self'],user=jdata['user']))
          return
    embed = discord.Embed(title=title,url=URL.replace(" ","_"))
    embed.set_footer(text=footer)
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(wiki(bot))