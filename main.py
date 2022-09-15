# This file sets up the app as a tangible window with buttons, layouts, styling and text
# The app's Kivy components are defined primarily in the obsmusicwidget.kv file, with few functionalities partially implemented within this file
# Other functionalities are implemented via seperate .py files



import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

import sys
import os
from multiprocessing import Process
from decouple import config

from server.app import start_widget

import spotipy
from spotipy.oauth2 import SpotifyPKCE


kivy.require("2.1.0")
log = open('log.txt', 'w')
sys.stdout = log
sys.stderr = log
new_environ = os.environ.copy()



# Set environment variables
os.environ['SPOTIPY_CLIENT_ID'] = config('SPOTIFY_CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = config('SPOTIFY_CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = config('REDIRECT')


# Define the different screens/windows of the app, and a manager for the screens
class Controller(Screen):
    
    # enable starting and stopping the widget
    def start(self):
        global p1
        p1 = Process(target=start_widget)
        p1.daemon = True
        p1.start()
        print("The widget is successfully launched (initiated via button id='start_widget_button')")

    def stop(self):
        global p1
        p1.terminate()
        print("The widget is successfully shut down (initiated via button id='stop_widget_button'")

    def restart(self):
        self.stop()
        self.start()
        print("The widget is successfully restarted (initiated via button id='restart_widget_button')")

    # Let users give access to their third-party account information via authentication
    # Spotify
    def spotify_connect_account(self):
        # Set the scope
        scope = "user-library-read"
        print(scope)

        # Initiate spotify with an authentication manager
        sp = spotipy.Spotify(auth_manager=SpotifyPKCE(scope=scope, open_browser=True))
        print("a")

        # Some test code 
        results = sp.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " - ", track['name'])



class Guide(Screen):
    pass


class About(Screen):
    pass


class WindowManager(ScreenManager):
    pass


# Setup the entire app as a class that inherits from Kivy's App class
class OBSMusicWidgetApp(App):
    pass






# On file launch, start the UI
if __name__ == "__main__":
    print("The app is now active")
    OBSMusicWidgetApp().run()
