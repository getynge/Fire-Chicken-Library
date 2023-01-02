from talon import Module, Context
from .tag_utilities import compute_tag_name_with_proper_prefix, deactivate_tags_in_context, make_tag_only_active_tag_in_context, compute_postfix, compute_prefix

class SwitchTag:
    def __init__(self, name: str, description: str):
        self.name = compute_tag_name_with_proper_prefix(name)
        module = Module()
        module.tag(self.get_postfix(), description)
        self.context = Context()

    def on(self):
        make_tag_only_active_tag_in_context(self.name, self.context)

    def off(self):
        deactivate_tags_in_context(self.context)

    def switch(self):
        if len(self.context.tags) == 0:
            self.on()
        else:
            self.off()

    def get_name(self) -> str:
        return self.name

    def get_postfix(self) -> str:
        return compute_postfix(self.name)

    def get_prefix(self) -> str:
        return compute_prefix(self.name)
