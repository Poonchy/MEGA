import discord
import time
import calendar
import pymysql
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import os
import re
import random
from random import randint
import math
import schedule
import asyncio
from multiprocessing import Process
import numpy as np
import requests
import string
from collections import defaultdict
from discord_components import DiscordComponents, Button, Select, SelectOption, ActionRow
from discord.ext.commands import Bot
def mixedCase(*args):
  total = []
  import itertools
  for string in args:
    a = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in       string)))
    for x in list(a): total.append(x)
  return list(total)
activeUsers = []
activity = discord.Activity(type=discord.ActivityType.listening, name="mega help")
bot = Bot(case_insensitive=True, activity=activity, help_command=None, command_prefix = mixedCase("mega "))