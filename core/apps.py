from django.apps import AppConfig

<<<<<<< Updated upstream
=======
import os
import psycopg2
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

>>>>>>> Stashed changes

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
