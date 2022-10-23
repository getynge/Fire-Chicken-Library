from talon import actions, Module

class SleepSetting:
    def __init__(self, name: str, default_amount: int, description: str, units: str = 'ms'):
        module = Module()
        self.setting = module.setting(
            name,
            type = int,
            default = default_amount,
            desc = f'How much to pause when {description}. If any commands using this setting are not working, try increasing this.'
        )
        self.units = units

    def sleep(self):
        actions.sleep(f'{self.get()}' + self.units)
    
    def get(self):
        return self.setting.get()

