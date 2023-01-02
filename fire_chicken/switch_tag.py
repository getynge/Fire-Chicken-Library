from talon import Module, Context
from .tag_utilities import compute_tag_name

class SwitchTag:
    def __init__(self, name: str, description: str):
        module = Module()
        module.tag(name, description)
        self.name = compute_tag_name(name)
        self.context = Context()

    def on(self):
        self.context.tags = [self.name]

    def off(self):
        self.context.tags = []

    def switch(self):
        if len(self.context.tags) == 0:
            self.on()
        else:
            self.off()

    def get_name(self) -> str:
        return self.name
    
    def _get_dot_index(self):
        return self.name.find('.')

    def get_postfix(self) -> str:
        dot_index = self._get_dot_index()
        return self.name[dot_index + 1:]

    def get_prefix(self) -> str:
        dot_index = self._get_dot_index()
        return self.name[:dot_index]
