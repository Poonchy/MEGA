import discord
import time
import calendar
import pymysql
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import os
import re
import datetime
import random
from random import randint
import math
import sys
import schedule
import asyncio
from multiprocessing import Process
import numpy as np
import cv2
import requests
import string
from collections import defaultdict
from decouple import config
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType, component

client = discord.Client()
activeUsers = []