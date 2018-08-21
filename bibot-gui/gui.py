#!/usr/bin/python
#coding: utf8


##
## => Graphical User interface for BIBOT
##
## TODO:
##  - Temporary welcome Screen => [DONE]
##  - Make the code clear
##  - Check importation
##  - Run BIBOT-analyser => [DONE]
##  - Get a logo image => [DONE]
##  - Export kv builder in a kv file => [DONE]
##  - Implement a session system
##  - Generate and display html report
##  - "Download" meta table
##  - Deal with meta_information.pkl generation
##



##-------------##
## IMPORTATION #################################################################
##-------------##
from kivy.app import App
from kivy.uix.pagelayout import PageLayout
from kivy.uix.filechooser import FileChooser
from kivy.uix.filechooser import FileChooserIconLayout
from kivy.uix.filechooser import FileChooserListLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from os.path import sep, expanduser, isdir, dirname
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


##---------##
## BUILDER #####################################################################
##---------##

## load kv template
Builder.load_file('interface.kv')


class Screen1App(Screen):
    """
    Temporary Screen for dev,
    choose betwwen Analyser module and search module
    """

    def switch_to_analyser(self):
        print "Tardis"
        self.manager.current = 'Screen2'

    def switch_to_search(self):
        print "WORK STILL IN PROGRESS, NO SCREEN AVAILABLE"


class Screen2App(Screen):
    """
    Temporary Screen for dev,
    Run the analyser module
    """

    ## importation trick
    import sys
    sys.path.append('../bibot-analyser')

    def collect_info(self):
        """
        Run the online search for meta
        information

        TODO:
            - progress bar
            - provide pmid
        """

        ## importation
        import analyser

        ## Run the retrieval
        analyser.collect_meta_informations()


    def create_figures(self):
        """
        IN PROGRESS
        TODO:
            - progress bar

        """

        ## importation
        import analyser

        ## generate all figures
        analyser.generate_all_figures()

        ## switch to figure screen
        self.manager.current = 'Screen3'



class Screen3App(Screen):
    """
    Temporary Screen for dev,
    Display figures screen
    TODO:
        - adjust figure size
        - dynamic figures ?
    """

    pass


##----------------##
## INITIALISATION ##############################################################
##----------------##


# Create the screen manager
sm = ScreenManager()
sm.add_widget(Screen1App(name='Screen1'))
sm.add_widget(Screen2App(name='Screen2'))
sm.add_widget(Screen3App(name='Screen3'))



class TestApp(App):
    title = "BIBOT"

    def build(self):

    	return sm
    	"""
        menu = Screen1App()
        #menu.test_user_request()
        print "value =",menu.myslider.value # <---- value here
        print "min =",menu.myslider.min # <--- min here
        return menu
		"""

if __name__ == "__main__":
    TestApp().run()
