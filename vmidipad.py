import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivymd.app import MDApp
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from kivy.properties import ColorProperty
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton, ActionCheck, ActionSeparator
from kivy.uix.popup import Popup


# from kivymd.uix.button import MDIconButton, MDFillRoundFlatIconButton
# from kivymd.uix.screen import MDScreen

from kivy.properties import BooleanProperty

from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout



import mido

import time

PAD_ROWS=4
PAD_COLS=4


# caption: button caption
# midi_msg: # CC | PC | 'NOTE_ON' | 'NOTE_OFF'
button_template = { 
    "caption" : "-",
    "midi_channel" : 0,    
    "midi_msg" : "NONE",  
    "midi_val" : 0
}

buttons_config = [
    {
        "caption": "MSG1",
        "midi_channel" : 1, 
        "midi_msg" : "CC",
        "midi_cc_nr": 10,
        "midi_cc_val" : 1
    },
    { 
        "caption": "MSG2",
        "midi_channel" : 0,
        "midi_msg" : "CC",
        "midi_cc_nr": 20,
        "midi_cc_val" : 100
    },
    { 
        "caption": "MSG3",
        "midi_channel" : 0,
        "midi_msg" : "PC",
        "midi_pc_val" : 12
    }
]



class PadButton(Button):
    
    btn_configuration = {}

    def __init__(self, config, r=20, **kwargs):
        super(PadButton, self).__init__(**kwargs)
        self.btn_configuration = config
        print(config)
        
        

        self.text = config['caption']
        # self.background_normal = ''
        self.background_color = (0.3, 1, 0.5, 1)
        self.font_size = self.width*0.3
        # self.surf=FloatLayout(); self.add_widget(self.surf)
        
       
class ButtonConfigPopup(Popup):
    pass
        
   

class MainPad(GridLayout):
    
    edit_mode = BooleanProperty(False) 

    
    def __init__(self, **kwargs):
        super(MainPad, self).__init__(**kwargs)
        self.padding = 10
        self.midi_port = mido.open_output()
        self.edit_mode = False

        self.cols = PAD_COLS
        self.spacing = 20

        for i in range (0,PAD_COLS*PAD_ROWS):
            if (i < len(buttons_config)):
                btn_config = buttons_config[i]
            else:
                btn_config = button_template

                
            
            pad_button = PadButton( config=btn_config,)
            pad_button.bind(state = self.btn_callback)
            self.add_widget(pad_button)


    def set_edit_mode(self, isediting):
        self.edit_mode = isediting

        print(' Edit mode ', self.edit_mode)
    
    
    def btn_callback(self, instance, touch):
        # print('btn pressed')
        # print('My button <%s> state is <%s>' % (instance, touch))

        
        if (touch == 'down'):
            
            if self.edit_mode:
                self.cfgpopup = ButtonConfigPopup(title='Configure button')
                self.cfgpopup.open()

            else :
                btn_cfg = instance.btn_configuration

                print("### ", btn_cfg)

                if btn_cfg['midi_msg'] == 'CC':
                    midi_msg = mido.Message('control_change', channel=btn_cfg['midi_channel'], control=btn_cfg['midi_cc_nr'], value=btn_cfg['midi_cc_val'], time=0)
                
                elif btn_cfg['midi_msg'] == "PC":
                    midi_msg = mido.Message('program_change', channel=btn_cfg['midi_channel'], program=btn_cfg['midi_pc_val'], time=0)

                else:
                    midi_msg = mido.Message('note_on', channel=btn_cfg['midi_channel'], note=60, velocity=64, time=0)

                self.midi_port.send(midi_msg)
            


class Manager(ScreenManager):
    screen_thermo = ObjectProperty(None)
    screen_light = ObjectProperty(None)
    screen_energy = ObjectProperty(None)
    screen_weather = ObjectProperty(None)


class MainWindow(BoxLayout):
    manager = ObjectProperty(None)


class VMidiPadApp(App):

    title = 'vMIDIPad'
    
    
    def build(self):
        # self.actionbar = ActionBar(    )
        # self.actionview = ActionView()
        # self.actionview.add_widget(ActionButton(text="ss"))
        # self.actionbar.add_widget(self.actionview)

       
        return (
            MainWindow()
            # MainPad()
        )
if __name__ == '__main__':
    VMidiPadApp().run()
    
