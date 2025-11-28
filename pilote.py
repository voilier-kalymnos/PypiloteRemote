"""
control pypilot via signalk
"""

import toga
import time

from functools import partial
import asyncio

from inspect import currentframe, getframeinfo
from .pypilot.client import pypilotClient
from .style  import Style

class Pilote(toga.App):
        

        MODE_COMPAS       = "compass"
        MODE_GPS          = "gps"
        MODE_WIND         = "wind"
        MODE_TRUE_WIND    = "true wind"
        MODE_NAV          = "nav"

        MODE              = 'ap.mode'
        COMMAND           = 'ap.heading_command'
        ENABLED           = 'ap.enabled'
        HEADING           = 'ap.heading'
        
        def __init__(self, dialog ):
                
                self.__dialog  = dialog
                
                self.style = Style()
                self.__initialize_pilote_box()
                asyncio.create_task(self.__initialize_client())
                pass
                
                        
        async def __initialize_client(self):
                self.client = False
                self.__connect()
 
                while True:
                        
                        if self.client :
                                self.__getMessages()

                        else:
                                self.__connect()
                        
                        print("sleep 0.5 Second")
                        await asyncio.sleep(0.5)
                pass
                
        def __initialize_pilote_box(self):
                
                self.__label_target     = toga.Label("NA"         ,                                                        style=self.style.target)
                self.__button_engage    = toga.Button("AUTO"      , on_press=self.__engage,                                style=self.style.button)
                self.__button_disengage = toga.Button("STANBY"    , on_press=self.__disengage,                             style=self.style.button)
                self.__button_m1        = toga.Button("-1"        , on_press=partial(self.__set_target,val=-1),            style=self.style.button)
                self.__button_p1        = toga.Button("+1"        , on_press=partial(self.__set_target,val=1),             style=self.style.button)
                self.__button_m10       = toga.Button("-10"       , on_press=partial(self.__set_target,val=-10),           style=self.style.button)
                self.__button_p10       = toga.Button("+10"       , on_press=partial(self.__set_target,val=10),            style=self.style.button)
                self.__button_compass   = toga.Button("Compas"    , on_press=partial(self.__mode,val=self.MODE_COMPAS),    style=self.style.button)
                self.__button_nav       = toga.Button("Nav"       , on_press=partial(self.__mode,val=self.MODE_NAV),       style=self.style.button)
                self.__button_wind      = toga.Button("Wind"      , on_press=partial(self.__mode,val=self.MODE_WIND),      style=self.style.button)
                self.__button_true_wind = toga.Button("True Wind" , on_press=partial(self.__mode,val=self.MODE_TRUE_WIND), style=self.style.button)
                self.__button_gps       = toga.Button("Gps"       , on_press=partial(self.__mode,val=self.MODE_GPS),       style=self.style.button)

                child_box1 = toga.Box(style=self.style.child_box, children=[self.__label_target])
                child_box2 = toga.Box(style=self.style.child_box, children=[self.__button_engage,  self.__button_disengage])
                child_box3 = toga.Box(style=self.style.child_box, children=[self.__button_m1,      self.__button_p1])
                child_box4 = toga.Box(style=self.style.child_box, children=[self.__button_m10,     self.__button_p10])
                child_box5 = toga.Box(style=self.style.child_box, children=[self.__button_compass, self.__button_nav])
                child_box6 = toga.Box(style=self.style.child_box, children=[self.__button_wind,    self.__button_true_wind])
                child_box7 = toga.Box(style=self.style.child_box, children=[self.__button_gps])
                
                self.__box = toga.Box("Pilote", style=self.style.main_box, children=[child_box1,child_box2,child_box3,child_box4,child_box5,child_box6,child_box7])
                pass
        
        def __mode(self, button, val):
                if self.client:
                        match val:
                                case self.MODE_COMPAS:
                                        self.__button_compass.background_color   = self.style.COLOR_PUSH
                                case self.MODE_GPS:
                                        self.__button_gps.background_color       = self.style.COLOR_PUSH
                                case self.MODE_NAV:
                                        self.__button_nav.background_color       = self.style.COLOR_PUSH
                                case self.MODE_TRUE_WIND:
                                        self.__button_true_wind.background_color = self.style.COLOR_PUSH
                                case self.MODE_WIND:
                                        self.__button_wind.background_color      = self.style.COLOR_PUSH
                                        
                        self.__label_target.color = self.style.COLOR_PUSH
                        self.__set(self.MODE, val)
                pass
                
        def __set_target(self, button, val):
                if self.client:
                        self.__label_target.color = self.style.COLOR_PUSH
                        command = round(self.__last_val(self.COMMAND)) + val
                        self.__set(self.COMMAND,command)
                pass
                
        def __engage(self, widget):
                if self.client:
                        self.__button_engage.background_color = self.style.COLOR_PUSH
                        heading = round(self.__last_val(self.HEADING))
                        self.__set(self.COMMAND,heading)
                        self.__set(self.ENABLED, True)
                pass
                
        def __disengage(self, widget):
                if self.client:
                        self.__button_disengage.background_color = self.style.COLOR_PUSH
                        self.__set(self.ENABLED, False)
                pass
                
        def __update_target(self,target):
                
                self.__label_target.text=str(round(target))
                self.__label_target.color = self.style.COLOR_TEXT
                pass    
                
        def __update_enable(self, enabled):
                
                if enabled:
                        self.__button_engage.background_color     = self.style.COLOR_ON
                        self.__button_disengage.background_color  = self.style.COLOR_OFF	
                        self.__button_m10.background_color        = self.style.COLOR_TARGET		
                        self.__button_m1.background_color         = self.style.COLOR_TARGET		
                        self.__button_p1.background_color         = self.style.COLOR_TARGET		
                        self.__button_p10.background_color        = self.style.COLOR_TARGET
                        
                else:
                        self.__button_engage.background_color     = self.style.COLOR_OFF
                        self.__button_disengage.background_color  = self.style.COLOR_ON
                        self.__button_m10.background_color        = self.style.COLOR_OFF
                        self.__button_m1.background_color         = self.style.COLOR_OFF	
                        self.__button_p1.background_color         = self.style.COLOR_OFF	
                        self.__button_p10.background_color        = self.style.COLOR_OFF
                pass

        def __update_mode(self, mode):

                self.__label_target.color = self.style.COLOR_TEXT
                self.__button_compass.background_color   = self.style.COLOR_OFF
                self.__button_gps.background_color       = self.style.COLOR_OFF
                self.__button_wind.background_color      = self.style.COLOR_OFF
                self.__button_true_wind.background_color = self.style.COLOR_OFF
                self.__button_nav.background_color       = self.style.COLOR_OFF
                if   mode == self.MODE_COMPAS:
                        self.__button_compass.background_color   = self.style.COLOR_ON
                elif mode == self.MODE_GPS:
                        self.__button_gps.background_color       = self.style.COLOR_ON
                elif mode == self.MODE_WIND:
                        self.__button_wind.background_color      = self.style.COLOR_ON
                elif mode == self.MODE_TRUE_WIND:
                        self.__button_true_wind.background_color = self.style.COLOR_ON
                elif mode == self.MODE_NAV:
                        self.__button_nav.background_color       = self.style.COLOR_ON
                pass
                
######################## Other ###########################                                
                
        def __print_debug(self, frameinfo, mess):
                
                #logging.warning( "pilote.py line " + str(frameinfo.lineno) + " : " + mess)
                print( "pilote.py line " + str(frameinfo.lineno) + " : " + mess)
                pass
        
        def __errorDialog(self, message):
                
                modal = toga.ErrorDialog("Signalk", message)
                task = asyncio.create_task(self.__dialog(modal))
                

########################### MyClient ###########################

        def __connect(self):
                watchlist = [self.ENABLED, self.MODE, self.COMMAND, self.HEADING]
                self.last_msg = {}

                try:
                    self.client = pypilotClient()

                    for name in watchlist:
                        self.client.watch(name)

                    print('connected')

                    
                except Exception as e:
                    print(e)
                    self.client = False
                    time.sleep(1)


        def __last_val(self, name):
                if name in self.last_msg:
                    return self.last_msg[name]
                return 'N/A'


        def __set(self, name, value):
                if self.client:
                    print ("setting {} to {}".format(name, value))
                    self.client.set(name, value)

                
        def __getMessages(self):
                
                try:
                        msgs = self.client.receive()

                except Exception as e:
                        print('disconnected', e)
                        self.__errorDialog("disconnected")
                        self.client = False

                if not msgs:
                        print("no msgs")
                        return False

                #print("msgs" + str(msgs))
                for name, value in msgs.items():
                        self.last_msg[name] = value

                        match name:
                                case self.COMMAND:
                                        self.__update_target(value)
                                        print("Command : "+ str(value))
                                        
                                case self.MODE:
                                        self.__update_mode(value)
                                        
                                case self.ENABLED:
                                        self.__update_enable(value)
                                        
                                case self.HEADING:
                                        print("Heading : " + str(value))
                return True
                                
                        
############################ Public ############################# 
                
        def get_box(self):
                return self.__box
