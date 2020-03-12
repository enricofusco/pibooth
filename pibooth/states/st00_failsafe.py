# -*- coding: utf-8 -*-

import pibooth
from pibooth.states import State


class StateFailSafe(State):

    def __init__(self, timeout):
        State.__init__(self, 'failsafe', timeout)

    @pibooth.hookimpl
    def state_failsafe_enter(self, app):
        app.dirname = None
        app.capture_nbr = None
        app.nbr_duplicates = 0
        app.previous_picture = None
        app.previous_animated = []
        app.previous_picture_file = None
        app.camera.drop_captures()  # Flush previous captures
        app.window.show_oops()
        self.timer.start()

    @pibooth.hookimpl
    def state_failsafe_validate(self):
        if self.timer.is_timeout():
            return 'wait'
