#!/usr/bin/env python3
'''
This plugin chains img2img operations together using an adjustable strength.  The output of the previous step
is fed into the input of the current step.  This is done for "--count" iterations.  It uses the initial seed
(if there is one) on the very first iteration, then uses random ones from there on out.
'''

import scripts.dream
from ldm.dream.promptformatter import PromptFormatter
from plugins._dreamplugin import DreamPlugin
import argparse

plugin_class_name="Img2ImgChain"  # TODO - figure out a robust way to automate class name retrieval

class Img2ImgChain(DreamPlugin):

    def plugin_parser(self):
        parser = argparse.ArgumentParser(
            description='Example: --chain_base <name-of-initial-image> --chain_str 0.1 --count 10 --plugin plugins.img2imgchain'
        )
        parser.add_argument('--count', type=int, help='number of img2img generations to process',default=1)
        parser.add_argument('--chain_base', type=str, help='Base image for chained generation')
        parser.add_argument('--chain_strength', type=float,help='Chain strength, similar to --strength, but kept separate to allow run-time modification',default=0.5)
        parser.add_argument('--outputfile', type=str, help='Internal switch for parsing dream output results')
        return parser

    #
    # Plugins take a Python list of switches of the form of:
    #
    #    "quote, encapsulated, prompt" -S1 -C2 -F3 ... <more optional switches here>
    #
    def __init__(self, initial_switches=None):
        super().__init__(initial_switches)
        
        print(str(initial_switches))
        
        # process plug-in specific args
        self.plg_parser = self.plugin_parser()
        opt_t=self.plg_parser.parse_known_args(initial_switches)
        opt=opt_t[0] # only grab known parms
        self.count = opt.count
        self.base_image = opt.chain_base
        self.chain_strength = opt.chain_strength
        
        # process dream specific args
        self.cmd_parser = scripts.dream.create_cmd_parser()
        opt_t=self.cmd_parser.parse_known_args(initial_switches)
        opt = opt_t[0]
        opt.init_img = self.base_image
        opt.strength = self.chain_strength
        self.dream_opt = opt
    
    def get_dream_prompt(self):
        print("*")
        print("* img2imgchain iteration countdown: " + str(self.count))
        print("*")
        if self.count >= 1:
            self.dream_opt.strength = self.chain_strength # TODO: Add start/stop/step operations
            command_str = PromptFormatter(opt=self.dream_opt).normalize_prompt() # tee things up for when the dream console is ready for more input
            self.count -= 1
            return command_str
        else:
            return "--terminate-plugin"
    
    def process_dream_output(self,output_list):
        opt_t = self.cmd_parser.parse_known_args(output_list)
        self.dream_opt = opt_t[0] # accept knowns, drop unknowns
        opt_t = self.plg_parser.parse_known_args(output_list)
        opt = opt_t[0]
        self.dream_opt.init_img = opt.outputfile

        if self.dream_opt.seed: # ensure a new seed is generated
            self.dream_opt.seed=None
    
