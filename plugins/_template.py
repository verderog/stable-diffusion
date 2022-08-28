#!/usr/bin/env python3

import scripts.dream
from ldm.dream.promptformatter import PromptFormatter
from plugins._dreamplugin import DreamPlugin
import argparse

plugin_class_name="TemplatePlugin"  # TODO - figure out a robust way to automate class name retrieval

class TemplatePlugin(DreamPlugin):

    def plugin_parser(self):
        parser = argparse.ArgumentParser(
            description='Example: black dragon, flying, color illustration --count 10 --plugin plugins.templateplugin'
        )
        parser.add_argument('--count', type=int, help='number of images to generate',default=1)
        return parser

    #
    # Plugins take a Python list of switches of the form of:
    #
    #    "quote, encapsulated, prompt" -S1 -C2 -F3 ... <more optional switches here>
    #
    def __init__(self, initial_switches=None):
        self.initial_switches=initial_switches
    
    def get_dream_prompt(self):
        pass
    
    def process_dream_output(self,output_list):
        pass
    
