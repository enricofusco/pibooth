# -*- coding: utf-8 -*-

import pygame
import pibooth
from pibooth.states.machine import State
from pibooth.utils import timeit


class StateChoose(State):

    def __init__(self, timeout):
        State.__init__(self, 'choose', timeout)

    @pibooth.hookimpl
    def state_choose_enter(self, app):
        with timeit("Show picture choice (nothing selected)"):
            app.window.set_print_number(0)  # Hide printer status
            app.window.show_choice(app.capture_choices)
        app.capture_nbr = None
        app.led_capture.blink()
        app.led_print.blink()
        self.timer.start()

    @pibooth.hookimpl
    def state_choose_do(self, app, events):
        event = app.find_choice_event(events)
        if event:
            if event.key == pygame.K_LEFT:
                app.capture_nbr = app.capture_choices[0]
            elif event.key == pygame.K_RIGHT:
                app.capture_nbr = app.capture_choices[1]

    @pibooth.hookimpl
    def state_choose_validate(self, app):
        if app.capture_nbr:
            return 'chosen'
        elif self.timer.is_timeout():
            return 'wait'

    @pibooth.hookimpl
    def state_choose_exit(self, app):
        if app.capture_nbr == app.capture_choices[0]:
            app.led_capture.switch_on()
            app.led_print.switch_off()
        elif app.capture_nbr == app.capture_choices[1]:
            app.led_print.switch_on()
            app.led_capture.switch_off()
        else:
            app.led_print.switch_off()
            app.led_capture.switch_off()
