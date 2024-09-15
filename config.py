# config.py

import os

class Config:
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = 'mysql://root:arb12345@localhost/stackithq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
