from talon import Module, Context

class SwitchTag:
    def __init__(self, name: str, description: str):
        module = Module()
        module.tag(name, description)
        self.name = name
        self.context = Context()
        manager.insert(self)
    def activate(self):
        self.context.tags = [self.get_name()]
    def deactivate(self):
        self.context.tags = []
    def switch(self):
        if len(self.context.tags) == 0:
            self.activate()
        else:
            self.deactivate()

    def get_name(self) -> str:
        return 'user.' + self.name
    def get_postfix(self) -> str:
        return self.name

class TagNotFoundException(Exception):
    pass

class SwitchTagManager:
    def __init__(self):
        self.tags = {}
    def insert(self, Tag: SwitchTag):
        self.tags[Tag.get_postfix()] = Tag
    def get(self, name: str) -> SwitchTag:
        if name in self.tags:
            return self.tags[name]
        raise TagNotFoundException('Tag with name ' + name + ' not found within the switch tag manager!')
manager = SwitchTagManager()

module = Module()
@module.action_class
class Actions:
    def fire_chicken_switch_tag_activate(name: str):
        '''Activates the specified switch tag'''
        manager.get(name).activate()
    def fire_chicken_switch_tag_deactivate(name: str):
        '''Deactivates the specified switch tag'''
        manager.get(name).deactivate()
    def fire_chicken_switch_tag_switch(name: str):
        '''Toggles the specified switch tag'''
        manager.get(name).switch()
