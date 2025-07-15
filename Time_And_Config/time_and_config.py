import datetime
from enum import Enum

# Define Enum for themes (optional for future use)
class ThemeMode(Enum):
    DARK = "dark"
    LIGHT = "light"

class Config:
    #Configuration class for the application including title, version, window size, and theme.
    __APP_TITLE = "Bank Account Management System"
    __APP_VERSION = "1.0.0"
    __DEFAULT_WINDOW_SIZE = "1200x700"
    __MIN_WINDOW_SIZE = (800, 500)
    __MAX_WINDOW_SIZE = (1200, 900)
    __THEME_SETTINGS = {
        "mode": "#000000",  
        "color_theme": "blue"
    }

    
    @classmethod
    def get_app_title(cls):
        #Return the application title.
        return cls.__APP_TITLE

    @classmethod
    def get_app_version(cls):
        #Return the application version.
        return cls.__APP_VERSION

    @classmethod
    def get_default_window_size(cls):
        #Return the default window size.
        return cls.__DEFAULT_WINDOW_SIZE

    @classmethod
    def get_min_window_size(cls):
        #Return the minimum window size.
        return cls.__MIN_WINDOW_SIZE

    @classmethod
    def get_max_window_size(cls):
        #Return the maximum window size.
        return cls.__MAX_WINDOW_SIZE

    @classmethod
    def get_theme_settings(cls):
        #Return the theme settings.
        return cls.__THEME_SETTINGS

class DateTimeUtils:
    #Date and time utilities to get the current time and date.
    
    @staticmethod
    def get_current_time():
        #Get the current time in HH:MM:SS format.
        
        return datetime.datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def get_current_date():
        #Get the current date in YYYY-MM-DD format.
        return datetime.datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_full_datetime():
        #Get the full current date and time in YYYY-MM-DD HH:MM:SS format.
        
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
