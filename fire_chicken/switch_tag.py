from talon import Module, Context, actions, app


class SwitchTag:
    def __init__(self, name: str, description: str):
        module = Module()
        module.tag(name, description)
        self.name = name
        self.context = Context()
        app.register('ready', self._register)
    def _register(self):
        try:
            actions.user.switch_tag_insert(self)
        except Exception as exception:
            print('Switch tag manager not available', exception)
    def on(self):
        self.context.tags = [self.get_name()]
    def activate(self):
        self.on()
    def off(self):
        self.context.tags = []
    def deactivate(self):
        self.off()
    def switch(self):
        if len(self.context.tags) == 0:
            self.on()
        else:
            self.off()

    def get_name(self) -> str:
        return 'user.' + self.name
    def get_postfix(self) -> str:
        return self.name
