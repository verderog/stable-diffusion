#!/usr/bin/env python3
'''
This example plug-in demonstrates how to iterate from the first cfg_scale value through 10.0, re-using the
same prompt, seed, and steps with every iteration

Invocation:

    dream> dragon --plugin plugins.iteratecfgscale --cs_tart 7.5 --cs_stop 10.0 --cs_step 0.5
    
This will produce outputs using "dragon" as a prompt, with config scale ranging from 7.5 -> 10.0 at 0.5 increments.

'''
import shlex
import scripts.dream
import argparse
from ldm.dream.promptformatter import PromptFormatter
from plugins._dreamplugin import DreamPlugin

plugin_class_name="IterateCfgScale" # TODO - figure out a robust way to automate class name retrieval

class IterateCfgScale(DreamPlugin):
    def plugin_parser(self):
        parser = argparse.ArgumentParser(
            description='Example: dragon --plugin .plugins.iteratecfgscale --cs_start 7.5 --cs_stop 10.0 --cs_step 0.5'
        )
        parser.add_argument('--cs_start', type=float, help='config scale start',default=7.5)
        parser.add_argument('--cs_stop', type=float, help='config scale stop',default=10.5)
        parser.add_argument('--cs_step', type=float, help='config scale step',default=3.0)
        return parser

    def __init__(self, initial_switches=None):
        super().__init__(initial_switches)
        
        # process plug-in specific args
        self.plg_parser = self.plugin_parser()
        opt_t=self.plg_parser.parse_known_args(initial_switches) # silently drop any unknowns
        opt=opt_t[0]
        self.cs_start = opt.cs_start
        self.cs_stop = opt.cs_stop
        self.cs_step = opt.cs_step
        self.cfg_scale = self.cs_start
        
        # process dream specific args
        self.cmd_parser = scripts.dream.create_cmd_parser()
        opt_t=self.cmd_parser.parse_known_args(initial_switches)
        opt = opt_t[0]
        self.dream_opt = opt
        self.dream_opt.cfg_scale = self.cfg_scale
        self.dream_opt = opt

    def get_dream_prompt(self):
        if self.cfg_scale <= self.cs_stop: # TODO - bounds check if cfg_scale + cs_step goes beyond desired cs_stop
            self.dream_opt.cfg_scale = self.cfg_scale
            self.cfg_scale += self.cs_step
            command_str = PromptFormatter(opt=self.dream_opt).normalize_prompt() # tee things up for when the dream console is ready for more input
            return command_str
        else:
            return "--terminate-plugin"
    
    def process_dream_output(self,output_list):
        opt_t = self.cmd_parser.parse_known_args(output_list)
        self.dream_opt = opt_t[0] # keep knowns, drop unknowns
    
    
    