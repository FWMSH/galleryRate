from kivy.config import Config
Config.set('graphics', 'fullscreen','auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import time
from datetime import datetime

class VoteButton(Button):
    # Empty class to connect to definition in kv
    pass

class VoteLabel(Label):
    # Empty class to connect to definition in kv
    pass
           
class VotingScreen(Screen):
    # Empty class to connect to definition in kv
    pass
            
class ScreenManagement(ScreenManager):

    # Manages the counting and recording of votes
    
    ticks_blocked = 0 # in 20ths of a second
    blocked = False # If True, button presses ignored
    vote_array = [0, 0, 0, 0, 0, 0] # Stores the votes. Ignore index 0
    
    # Config variable defaults
    csv_path = 'vote_data.csv'
    title = 'Rate This Experience'
    title_font = 'Roboto-Bold.ttf'
    label_5 = 'Loved it'
    label_4 = ''
    label_3 = ''
    label_2 = ''
    label_1 = 'Needs work'
    label_font = 'Roboto-Regular.ttf'
    subtitle = "Tap a button to give us a score!"
    subtitle_font = 'Roboto-Bold.ttf'
    date_string = True
    button_font = 'Roboto-Bold.ttf'

    def add_vote(self, value):
        # If a button is pressed, add a correspoinding vote
        if not self.blocked: # To defeat double presses
            self.vote_array[value] += 1
            self.blocked = True
            
    def record_votes(self, dt):
        # Write the currently recorded votes out to a file
        # dt is passed from the Clock. We ignore it.
                   
        if sum(self.vote_array) > 0: # Only proceed if there are votes
            # Date string
            if self.date_string:
                date_str = datetime.now().isoformat()
            else:
                        
                date_str = str(time.time())

            # Build the line to write
            line_str = date_str + ',' + \
                str(self.vote_array[5])+','+str(self.vote_array[4]) + \
                ','+str(self.vote_array[3])+','+str(self.vote_array[2])+ \
                ','+str(self.vote_array[1]) + '\n'
            
            # Write the line to the file
            with open(self.csv_path, 'a') as f:
                f.write(line_str)
            
            # Reset everything so we don't double record
            self.vote_array = [0, 0, 0, 0, 0, 0] 
    
    def check_for_block(self, dt):
        # If self.block == True, a button was recently pressed and we're ignoring additional presses
        if self.blocked:
            if self.ticks_blocked + 1 > 20: # Cancel block after 1 second (20 ticks)
                self.ticks_blocked = 0
                self.blocked = False
            else:
                self.ticks_blocked += 1

    def get_config(self):
        # Function to parse arguments from a configuration file
        
        with open('config.conf', 'r') as f:
            for line in f:

                line = line.split('#',1)[0] # Check for comment symbol (#)

                if line[0:5].lower() == 'path:':
                    self.csv_path = line[5:].strip()
                elif line[0:6].lower() == 'title:':
                    self.title = line[6:].strip()
                elif line[0:11].lower() == 'font_title:':
                    self.title_font = line[11:].strip()
                elif line[0:6].lower() == 'label_':
                    temp = line[6]
                    if int(temp) == 1:
                        self.label_1 = line[8:].strip()
                    if int(temp) == 2:
                        self.label_2 = line[8:].strip()
                    if int(temp) == 3:
                        self.label_3 = line[8:].strip()
                    if int(temp) == 4:
                        self.label_4 = line[8:].strip()
                    if int(temp) == 5:
                        self.label_5 = line[8:].strip()
                elif line[0:12].lower() == 'font_label:':
                    self.label_font = line[12:].strip()
                elif line[0:9].lower() == 'subtitle:':
                    self.subtitle = line[9:].strip()
                elif line[0:14].lower() == 'font_subtitle:':
                    self.subtitle_font = line[14:].strip()
                elif line[0:12].lower()  == 'date_string:':
                    if line[12:].strip().lower() == 'false':
                        self.date_string = False
                elif line[0:12].lower() == 'font_button:':
                    self.button_font = line[12:].strip()             
        
    def __init__(self):
        Clock.schedule_interval(self.check_for_block, 1./20)
        Clock.schedule_interval(self.record_votes, 60.)
        super(ScreenManagement, self).__init__()
        self.get_config()

class MainApp(App):
    # Empty class to connect to definition in kv
    pass

# Start the app
MainApp().run()














