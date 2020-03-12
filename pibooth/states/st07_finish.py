# -*- coding: utf-8 -*-

import pibooth
from pibooth.states.machine import State


class StateFinish(State):

    def __init__(self, timeout):
        State.__init__(self, 'finish', timeout)

    @pibooth.hookimpl
    def state_finish_enter(self, app):
        app.window.show_finished()
        self.timer.start()

    @pibooth.hookimpl
    def state_finish_validate(self):
        if self.timer.is_timeout():
            return 'wait'
