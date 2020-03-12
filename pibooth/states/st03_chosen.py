# -*- coding: utf-8 -*-

import pibooth
from pibooth.states.machine import State
from pibooth.utils import timeit


class StateChosen(State):

    def __init__(self, timeout):
        State.__init__(self, 'chosen', timeout)

    @pibooth.hookimpl
    def state_chosen_enter(self, app):
        with timeit("Show picture choice ({} captures selected)".format(app.capture_nbr)):
            app.window.show_choice(app.capture_choices, selected=app.capture_nbr)
        self.timer.start()

    @pibooth.hookimpl
    def state_chosen_validate(self):
        if self.timer.is_timeout():
            return 'capture'

    @pibooth.hookimpl
    def state_chosen_exit(self, app):
        app.led_capture.switch_off()
        app.led_print.switch_off()
