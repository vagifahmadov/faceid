from flask import Flask, jsonify, request, Blueprint, json, Response, url_for, render_template, redirect, make_response, session
from flask_pymongo import PyMongo, DESCENDING, ASCENDING
from flask_cors import CORS
import requests, json, bson
import calendar
from calendar import monthrange, weekday, SUNDAY, monthcalendar
from bson.objectid import ObjectId
from datetime import datetime, timedelta, date
from time import gmtime, strftime, localtime
from jsondiff import diff
import random
from hashlib import sha256, md5
import urllib.parse as urlparse
from copy import deepcopy
import time
import pymongo
import os
import base64
import PIL.Image
import PIL.ImageTk
import face_recognition
import cv2
import io
import numpy as np
from werkzeug.utils import secure_filename
import ast
from tqdm import tqdm
import glob
import re
from deepface import DeepFace
import pyodbc
import pandas as pd
# from sklearn.metrics import accuracy_score, recall_score, f1_score, fbeta_score
from dateutil.relativedelta import relativedelta
import jwt
from functools import wraps

upload_folder = 'uploads'
app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['SECRET_KEY'] = 'Aze19051985'
