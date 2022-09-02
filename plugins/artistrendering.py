#!/usr/bin/env python3

'''
This example plug-in demonstrates how to generate prompts that have iterate through a list of artist names as found in artistlist.txt.  '{}' portions
of the text will be replaced by random values.

Reference: https://old.reddit.com/r/StableDiffusion/comments/x32dif/study_of_500_artists_using_the_same_prompt/

'''


import scripts.dream
from ldm.dream.promptformatter import PromptFormatter
from plugins._dreamplugin import DreamPlugin
import argparse
from pathlib import Path
import random

plugin_class_name="ArtistRenderingPlugin"  # TODO - figure out a robust way to automate class name retrieval

class ArtistRenderingPlugin(DreamPlugin):

    def plugin_parser(self):
        parser = argparse.ArgumentParser(
            description='Example: a beautiful elf princess, ethereal face. Painted by {} --plugin plugins.artistrendering'
        )
        parser.add_argument('--outputfile', type=str, help='Internal switch for parsing dream output results')
        parser.add_argument('--random', type=int, help='Use prompt against <N> random artists', default=None)
        parser.add_argument('--phelp', action="store_true")
        return parser

    #
    # Plugins take a Python list of switches of the form of:
    #
    #    "quote, encapsulated, prompt" -S1 -C2 -F3 ... <more optional switches here>
    #
    def __init__(self, initial_switches=None):
        super().__init__(initial_switches)
        self.initial_switches=initial_switches
        
        # process plug-in specific args
        self.plg_parser = self.plugin_parser()
        opt_t=self.plg_parser.parse_known_args(initial_switches)
        opt=opt_t[0] # only grab known parms
        
        self.artistlist = []
        self.randartistlist=[]
        # create array from the artistlist
        with open('plugins/artistlist.txt', 'r') as fd:
            for line in fd:
                self.artistlist.append(line.strip())
            
        if opt.random and opt.random < len(self.artistlist):
            for _ in range(0,opt.random):
                artist = self.artistlist.pop(random.randint(0,len(self.artistlist)))
                print(f"Queue'ing random artist: {artist}") 
                self.randartistlist.append(artist)
            self.artistlist.clear() # using the random list, so clear out the full list
        else:
            print(f"*** Sampling all {len(self.artistlist)} artists! ***")

        if opt.phelp:
            self.plg_parser.print_help()
        
        # process dream specific args
        self.cmd_parser = scripts.dream.create_cmd_parser()
        opt_t=self.cmd_parser.parse_known_args(initial_switches)
        opt = opt_t[0]
        self.prompt_baseline=opt.prompt
        self.dream_opt=opt
        self.default_seed = self.dream_opt.seed
                
        self.currentartist=''
    
    def get_dream_prompt(self):
        if len(self.randartistlist) > 0:
            self.currentartist = self.randartistlist.pop(0)
        elif len(self.artistlist) > 0:
            self.currentartist = self.artistlist.pop(0)
        else:
            return "--terminate-plugin"
        
        self.dream_opt.prompt = self.prompt_baseline.format(self.currentartist) # populate the random fields
        command_str = PromptFormatter(opt=self.dream_opt).normalize_prompt() # tee things up for when the dream console is ready for more input
        return command_str
    
    def process_dream_output(self,output_list):
        opt_t = self.cmd_parser.parse_known_args(output_list)
        self.dream_opt = opt_t[0] # keep knowns, drop unknowns
        if self.default_seed:
            self.dream_opt.seed = self.default_seed
            
        # rename the file to include the artist
        opt_t = self.plg_parser.parse_known_args(output_list)
        opt = opt_t[0]
        p = Path(opt.outputfile)
        condensedname = ''.join(self.currentartist.split(" "))
        newfilepath = Path(p.parent, f"{p.stem}.{condensedname}{p.suffix}")
        
        print(f"Rename: {opt.outputfile} -> {newfilepath}")
        
        p.rename(newfilepath)
    
