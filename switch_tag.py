from talon import Module, Context

class SwitchTag:
    def __init__(self, name: str, description: str):
        module = Module()
        module.tag(name, description)
        self.name = name
        self.context = Context()
    def activate(self):
        self.context.tags = [self.get_name()]
    def deactivate(self):
        self.context.tags = []
    def switch(self):
        if len(self.context.tags) == 0:
            self.activate()
        else:
            self.deactivate()

    def get_name(self):
        return 'user.' + self.name