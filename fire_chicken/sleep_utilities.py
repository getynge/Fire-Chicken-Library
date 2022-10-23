from talon import actions, Module

class SleepSetting:
    def __init__(self, name: str, default_amount: float, description: str):
        module = Module()
        self.setting = module.setting(
            name,
            type = float,
            default = default_amount,
            desc = f'How much to pause when {description}. If any commands using this setting are not working, try increasing this.'
        )

    def sleep(self):
        actions.sleep(self.get())
    
    def get(self):
        return self.setting.get()
