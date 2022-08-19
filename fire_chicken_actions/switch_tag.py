from talon import Module

from ..fire_chicken.switch_tag import SwitchTag

class TagNotFoundException(Exception):
    pass

class SwitchTagManager:
    def __init__(self):
        self.tags = {}
    def insert(self, Tag: SwitchTag):
        print('inserting into the tag manager: ', Tag.get_postfix())
        self.tags[Tag.get_postfix()] = Tag
        print('the tag manager: ', str(self.tags))
    def get(self, name: str) -> SwitchTag:
        if name in self.tags:
            return self.tags[name]
        raise TagNotFoundException('Tag with name ' + name + ' not found within the switch tag manager: ' + str(self.tags) + '!')

manager = SwitchTagManager()

module = Module()
@module.action_class
class Actions:
    def switch_tag_on(name: str):
        '''Activates the specified switch tag'''
        manager.get(name).on()
    def switch_tag_off(name: str):
        '''Deactivates the specified switch tag'''
        manager.get(name).off()
    def switch_tag_switch(name: str):
        '''Toggles the specified switch tag'''
        manager.get(name).switch()
    def switch_tag_insert(tag: SwitchTag):
        '''Inserts the specified switch tag into the switch tag manager'''
        manager.insert(tag)
