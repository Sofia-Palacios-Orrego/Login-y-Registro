from flask import Flask
import re

app = Flask(__name__)
app.secret_key = "esto es secreto"

BASE_DE_DATOS = "bded_usuarios"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[A-Z]{1}[a-zA-Z\.]+$')