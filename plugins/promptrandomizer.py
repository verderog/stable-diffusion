#!/usr/bin/env python3
'''
This example plug-in demonstrates how to generate prompts that have randomized portions associated with them.  '*' portions
of the text will be replaced by random values. 

Example invocation:

dream> an elephant walking on {} another planet {} -S 385838583 -count 10 --plugin plugins.promptrandomizer

Plugin specific options:

-count : # of iterations to perform

Other notes:

Seed, cfg, etc. will be reused after each invocation

'''
import scripts.dream
from ldm.dream.promptformatter import PromptFormatter

from plugins._dreamplugin import DreamPlugin

import argparse
import random

plugin_class_name="PromptRandomizer" # TODO - figure out a robust way to automate class name retrieval

class PromptRandomizer(DreamPlugin):
    def plugin_parser(self):
        parser = argparse.ArgumentParser(
            description='Example: an elephant walking on {} another planet {} -S 385838583 --count 10 --plugin plugins.promptrandomizer'
        )
        parser.add_argument('--count', type=int, help='number of images to generate',default=1)
        return parser
        
    
    def __init__(self, initial_switches=None):
        super().__init__(initial_switches)
        
        # process plug-in specific args
        self.plg_parser = self.plugin_parser()
        opt_t=self.plg_parser.parse_known_args(initial_switches)
        opt=opt_t[0] # only grab known parms
        self.count = opt.count
        
        # process dream specific args
        self.cmd_parser = scripts.dream.create_cmd_parser()
        opt_t=self.cmd_parser.parse_known_args(initial_switches)
        opt = opt_t[0]
        self.prompt_baseline=opt.prompt
        self.dream_opt=opt
        
        self.field_count = self.prompt_baseline.count("{}") # count the number of random fields
        
        self.sys_rand = random.SystemRandom() # maintain separate generator so dream's seeds don't affect this plugin

    def get_dream_prompt(self):
        if self.count >= 1:
            rfields=tuple(self.sys_rand.randint(0,10000) for _ in range(0,self.field_count)) # define random field values
            self.dream_opt.prompt = self.prompt_baseline.format(*rfields) # populate the random fields
            command_str = PromptFormatter(opt=self.dream_opt).normalize_prompt() # tee things up for when the dream console is ready for more input
            self.count -= 1
            return command_str
        else:
            return "--terminate-plugin"
        
    def process_dream_output(self,output_list):
        opt_t = self.cmd_parser.parse_known_args(output_list)
        self.dream_opt = opt_t[0] # accept knowns, drop unknowns
    
    