from flask import Flask

app = Flask(__name__)

from app.controller.Main import *
from app.controller.Auth import *
from app.controller.Action_frontend import *
from app.controller.Action import *
from app.controller.Api import *
from app.modul.Scrapping.ScrappingData import *
from app.modul.Preprocessing.Preprocessing import *
from app.config.config import *
from app.config.connect_db import *
from app.modul.Preprocessing.dbmodel import *
from app.modul.Sentimen.Sentimen import *
from app.modul.Sentimen.dbmodel import *
from app.modul.Data.dbmodel import *
from app.modul.Data.Data import *
from app.modul.Smote.Smote import *
from app.modul.Smote.dbmodel import *
from app.modul.Klasifikasi.KlasifikasiKNN import *
from app.modul.Klasifikasi.dbmodel import *
