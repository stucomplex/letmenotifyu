import os
import configparser
import logging

log = logging.getLogger(__name__)

DIRECTORY_PATH = os.path.join(os.environ['HOME'], '.letmenotifyu')
DATA_FILES_PATH = '/usr/share/letmenotifyu/'

DATABSE_PATH = os.path.join(DIRECTORY_PATH, 'database')
MOVIE_DB = os.path.join(DATABSE_PATH, 'movie.db')
SERIES_DB = os.path.join(DATABSE_PATH, 'series.db')
GENERAL_DB = os.path.join(DATABSE_PATH, 'general.db')

LOG_FILE_PATH = os.path.join(DIRECTORY_PATH, 'letmenotifyu.log')
IMAGES_DIRECTORY = 'images'
IMAGE_PATH = os.path.join(DIRECTORY_PATH, IMAGES_DIRECTORY)
TORRENT_DIRECTORY = os.path.join(DIRECTORY_PATH, 'torrents')
SQLITE_WAL_MODE = "PRAGMA journal_mode=WAL"
config = configparser.ConfigParser()


def logging_dict(log_level):
    levels = {'Logging.DEBUG': logging.DEBUG,
              'Logging.INFO': logging.INFO}
    return levels[log_level]


def create_ini_file():
    """
    Create config file upon install start of application
    """
    config['DIRECTORIES'] = {'CompleteDownloads': os.path.join(DIRECTORY_PATH,
                                                               'complete'),
                             'IncompleteDownloads': os.path.join(DIRECTORY_PATH,
                                                                 'incomplete')}
    config["LOGGING"] = {'LoggingLevel': "Logging.INFO"}
    with open(DIRECTORY_PATH+'/config.ini', 'w') as cfg_file:
        config.write(cfg_file)


def check_db():
    if os.path.exists(MOVIE_DB) and os.path.exists(SERIES_DB) and os.path.exists(GENERAL_DB):
        return True
    else:
        log.error("movie, series or general database does not exist")
        raise ValueError("movie or series database not found")

try:
    config.read(DIRECTORY_PATH+'/config.ini')
    COMPLETE_DIRECTORY = config['DIRECTORIES']['CompleteDownloads']
    INCOMPLETE_DIRECTORY = config['DIRECTORIES']['IncompleteDownloads']
    LOG_LEVEL = logging_dict(config['LOGGING']['LoggingLevel'])
except KeyError:
    os.mkdir(DIRECTORY_PATH)
    os.mkdir(IMAGE_PATH)
    os.mkdir(DATABSE_PATH)
    create_ini_file()
    COMPLETE_DIRECTORY = config['DIRECTORIES']['CompleteDownloads']
    INCOMPLETE_DIRECTORY = config['DIRECTORIES']['IncompleteDownloads']
    LOG_LEVEL = logging_dict(config['LOGGING']['LoggingLevel'])
    os.mkdir(INCOMPLETE_DIRECTORY)
    os.mkdir(COMPLETE_DIRECTORY)
    os.mkdir(TORRENT_DIRECTORY)
