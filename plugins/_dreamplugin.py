import abc

class DreamPlugin(metaclass=abc.ABCMeta):

    #
    # Plugins take a Python list of switches of the form of:
    #
    #    "quote, encapsulated, prompt" -S1 -C2 -F3 ... <more optional switches here>
    #
    def __init__(self, initial_switches=None):
        self.initial_switches=initial_switches
    
    @abc.abstractmethod    
    def get_dream_prompt(self):
        pass
    
    @abc.abstractmethod
    def process_dream_output(self,output):
        pass
    
    def test_plugin(self):
        print("This is class: " + type(self).__name__)
