import time

from talon import actions, Module


class SleepSetting:
    def __init__(self, name: str, default_amount: float, description: str, provided_module = None):
        module = provided_module
        if module is None:
            module = Module()

        self.setting = module.setting(
            name,
            type = float,
            default = default_amount,
            desc = f'How much to pause when {description}. If any commands using this setting are not working, try increasing this.'
        )

    def sleep(self):
        actions.sleep(self.get())

    def sleep_with_factor(self, factor):
        actions.sleep(self.get() * factor)

    def get(self):
        return self.setting.get()

class DeadlineExceededException(Exception):
    pass

class TimeoutSleeper:
    """An object that does not allow sleeps to exceed the given deadline amount
        :param timeout: number of seconds that sleep must exceed for exception to be thrown
        :param leak_per_second: number of seconds that are subtracted from tracked time per second,
        tracked time never goes below zero
        :raises ValueError: when leak_per_second is less than zero"""
    def __init__(self, timeout: float, leak_per_second: float = 0):
        if leak_per_second < 0:
            raise ValueError("leak_per_second must not be less than zero")
        self.timeout = timeout
        self.leak_per_second = leak_per_second
        self.last_sleep = None
        self.time_slept_minus_leak = 0.0

    def sleep(self, amount: float):
        """
        sleep for specified number of seconds if and only if the supplied amount does not exceed the timeout
        :param amount: number of seconds to sleep, must not be below zero
        """
        elapsed = 0
        if self.last_sleep is not None:
            elapsed = time.time() - self.last_sleep

        self.last_sleep = time.time()
        total_leak = self.leak_per_second * elapsed

        self.time_slept_minus_leak -= total_leak
        if self.time_slept_minus_leak < 0:
            self.time_slept_minus_leak = 0

        if self.time_slept_minus_leak + amount > self.timeout:
            raise DeadlineExceededException(f"deadline of {self.timeout} seconds reached, exceeded by "
                                            f"{self.time_slept_minus_leak + amount - self.timeout}")
        actions.sleep(amount)
        self.time_slept_minus_leak += amount

def sleep_max_setting(* args):
    maximum_delay_amount = 0
    for setting in args:
        if setting.get() > maximum_delay_amount:
            maximum_delay_amount = setting.get()
    actions.sleep(maximum_delay_amount)
