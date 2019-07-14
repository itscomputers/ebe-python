#   numth/config.py
#=============================
import configparser
#=============================

def default(category, data_type=eval):
    config = configparser.ConfigParser()
    config.read('numth.ini')
    return data_type(config['DEFAULT'][category])

