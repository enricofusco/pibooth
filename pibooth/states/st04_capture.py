# -*- coding: utf-8 -*-

import time
import os
import os.path as osp
import pygame
import pibooth
from pibooth.states.machine import State
from pibooth.utils import LOGGER, timeit


class StateCapture(State):

    def __init__(self):
        State.__init__(self, 'capture')
        self.count = 0

    @pibooth.hookimpl
    def state_capture_enter(self, app):
        LOGGER.info("Start new captures sequence")
        app.nbr_duplicates = 0
        app.previous_picture = None
        app.previous_picture_file = None
        app.dirname = osp.join(app.savedir, "raw", time.strftime("%Y-%m-%d-%H-%M-%S"))
        os.makedirs(app.dirname)
        app.led_preview.switch_on()

        self.count = 0
        app.window.set_capture_number(self.count, app.capture_nbr)
        app.camera.preview(app.window)

    @pibooth.hookimpl
    def state_capture_do(self, config, app):
        app.window.set_capture_number(self.count + 1, app.capture_nbr)
        pygame.event.pump()

        if config.getboolean('WINDOW', 'preview_countdown'):
            app.camera.preview_countdown(config.getint('WINDOW', 'preview_delay'))
        else:
            app.camera.preview_wait(config.getint('WINDOW', 'preview_delay'))

        capture_path = osp.join(app.dirname, "pibooth{:03}.jpg".format(self.count))

        if config.getboolean('WINDOW', 'preview_stop_on_capture'):
            app.camera.stop_preview()

        effects = config.gettyped('PICTURE', 'captures_effects')
        if not isinstance(effects, (list, tuple)):
            # Same effect for all captures
            effect = effects
        elif len(effects) >= app.capture_nbr:
            # Take the effect corresponding to the current capture
            effect = effects[self.count]
        else:
            # Not possible
            raise ValueError("Not enough effects defined for {} captures {}".format(
                app.capture_nbr, effects))

        with timeit("Take a capture and save it in {}".format(capture_path)):
            if config.getboolean('WINDOW', 'flash'):
                with app.window.flash(2):
                    app.camera.capture(capture_path, effect)
            else:
                app.camera.capture(capture_path, effect)

        self.count += 1

        if config.getboolean('WINDOW', 'preview_stop_on_capture') and self.count < app.capture_nbr:
            # Restart preview only if other captures needed
            app.camera.preview(app.window)

    @pibooth.hookimpl
    def state_capture_validate(self, app):
        if self.count >= app.capture_nbr:
            return 'processing'

    @pibooth.hookimpl
    def state_capture_exit(self, app):
        app.camera.stop_preview()
        app.led_preview.switch_off()
