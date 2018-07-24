from kivy.config import Config
Config.set('graphics', 'fullscreen','auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from datetime import datetime
import glob
from numpy import zeros
from functools import partial

class VotingScreen(Screen):
    # Empty class to connect to definition in kv
    
    def draw(self):
        app = App.get_running_app()
        with self.canvas.before:
            if app.manager.background_image == '':
                Color(rgba=app.manager.background_color)
            Rectangle(size=(app.root_window.width,app.root_window.height), pos=self.pos, source=app.manager.background_image)
            
    def __init__(self, *args, **kwargs):
    
        app = App.get_running_app()
    
        super(VotingScreen, self).__init__(*args, **kwargs)
        
        self.top_layout = BoxLayout(orientation='vertical')
        self.title = Label(text=app.manager.title, halign='center',
                            font_size=50, size_hint=(1,0.35),
                            markup=True, font_name=app.manager.title_font)
        self.button_container = BoxLayout(orientation='horizontal', size_hint=(1,0.4))
        self.subtitle = Label(text=app.manager.subtitle, font_size=35,
                                size_hint=(1,0.25), markup=True, halign='center',
                                font_name=app.manager.subtitle_font)
        
        self.top_layout.add_widget(self.title)
        self.top_layout.add_widget(self.button_container)
        self.top_layout.add_widget(self.subtitle)
        
        self.add_widget(self.top_layout)
        self.draw()
            
class ScreenManagement(ScreenManager):

    # Manages the counting and recording of votes
    
    ticks_blocked = 0 # in 20ths of a second
    blocked = False # If True, button presses ignored
    vote_array = [] # Stores the votes.
    
    # Config variable defaults
    csv_path = 'vote_data.csv'
    title = 'Rate This Experience'  
    subtitle = "Tap a button to give us a score!"
    button_font = 'Roboto-Bold.ttf'
    background_color = (0,0,0,1)
    background_image = ''

    def add_vote(self, value, *args):

        # If a button is pressed, add a correspoinding vote
        if not self.blocked: # To defeat button spamming
            self.vote_array[value] += 1
            self.blocked = True
            
    def record_votes(self, *args):
        # Write the currently recorded votes out to a file
                   
        if sum(self.vote_array) > 0: # Only proceed if there are votes
            # Date string
            date_str = datetime.now().isoformat()

            # Build the line to write
            line_str = date_str
            for i in range(len(self.vote_array)):
                line_str += ', ' + str(int(self.vote_array[i]))
            line_str += '\n'
            
            # Write the line to the file
            with open(self.csv_path, 'a') as f:
                f.write(line_str)
            
            # Reset everything so we don't double record
            self.vote_array = zeros(len(self.vote_array))
    
    def check_for_block(self, dt):
        # If self.block == True, a button was recently pressed and we're ignoring additional presses
        if self.blocked:
            if (self.ticks_blocked + 1) > 20: # Cancel block after 1 second (20 ticks)
                self.ticks_blocked = 0
                self.blocked = False
            else:
                self.ticks_blocked += 1

    def get_config(self):
        # Function to parse arguments from a configuration file
        # dt passed by clock. We ignore it

        with open('config.conf', 'r') as f:
            for line in f:

                line = line.split('#',1)[0] # Check for comment symbol (#)

                if line[0:5].lower() == 'path:': # Where the file is written
                    value = line[5:].strip()
                    if value != '':
                        self.csv_path = value
                elif line[0:6].lower() == 'title:': # The large text at the top
                    self.title = line[6:].strip().replace('\\n', '\n')
                elif line[0:11].lower() == 'font_title:': # Title font
                    self.title_font = line[11:].strip()
                    
                elif line[0:9].lower() == 'subtitle:': # The text at the bottom
                    self.subtitle = line[9:].strip().replace('\\n', '\n')
                elif line[0:14].lower() == 'font_subtitle:': # Subtitle font
                    self.subtitle_font = line[14:].strip()
                elif line[0:17].lower() == 'background_color:': # Screen background color
                    s = line[17:].strip().split(',')
                    self.background_color = (float(s[0])/255,
                                                float(s[1])/255,
                                                float(s[2])/255,
                                                1)                                 

                elif line[0:17].lower() == 'background_image:': # Screen background color
                    self.background_image = line[17:].strip()                    
                            
    def build_screen(self, *args):
        
        self.screen = VotingScreen()
        
        # Find button definition files
        files = glob.glob('buttons/*.conf')
        
        # For each file, add a button to the interface
        index = 0
        for file in files:
            with open(file, 'r', encoding='utf8') as f:
            
                text = ''
                text_font_size = 50
                text_font_name = 'Roboto-Bold.ttf'
                text_font_color = (0,0,0,1)
                label = ''
                label_font_size = 30
                label_font_name = 'Roboto-Regular.ttf'
                label_font_color = (1,1,1,1)
                background_normal = ''
                background_down = ''
                
                for line in f: # Parse the definition file for keywords
                    if line[0:5].lower() == 'text:':
                        text = line[5:].strip().replace('\\n', '\n')
                    if line[0:6].lower() == 'label:':
                        label = line[6:].strip().replace('\\n', '\n')
                    if line[0:15].lower() == 'text_font_size:':
                        text_font_size = float(line[15:].strip())
                    if line[0:16].lower() == 'text_font_size:':
                        label_font_size = float(line[16:].strip())
                    if line[0:15].lower() == 'text_font_name:':
                        text_font_name = line[15:].strip()
                    if line[0:16].lower() == 'label_font_name:':
                        label_font_name = line[16:].strip()
                    if line[0:18].lower() == 'background_normal:':
                        background_normal = line[18:].strip()
                    if line[0:19].lower() == 'background_pressed:':
                        background_down = line[19:].strip()
                        
            pack = BoxLayout(orientation='vertical')
            but = Button(text=text, font_size=text_font_size,
                            size_hint=(1,0.85), markup=True,
                            font_name=text_font_name,
                            color = text_font_color, halign='center',
                            on_release=partial(self.add_vote, index),
                            background_normal=background_normal,
                            background_down=background_down)
            lab = Label(text=label, font_size=label_font_size,
                            size_hint=(1,0.15), markup=True,
                            font_name=label_font_name, halign='center',
                            color = label_font_color)
            pack.add_widget(but)
            pack.add_widget(lab)
            self.screen.button_container.add_widget(pack)
            
            index += 1 # This assigns the next button to the next entry in vote_array
            
        self.vote_array = zeros(len(files))
       
        self.add_widget(self.screen)
      
    def __init__(self):
        super(ScreenManagement, self).__init__()
        
        Clock.schedule_once(self.build_screen, 1)
        Clock.schedule_interval(self.check_for_block, 1./20)
        #Clock.schedule_interval(self.record_votes, 60.)
        
class MainApp(App):
    
    def build(self):
        self.manager = ScreenManagement()
        self.manager.get_config()
        #self.manager.build_screen()
        return(self.manager)
        
    def on_stop(self):
        self.manager.record_votes()

# Start the app
MainApp().run()














