# -*- coding: utf-8 -*-

import time
import itertools
import pibooth
from pibooth.states import State
from pibooth.utils import LOGGER, PoolingTimer, timeit


class StateWait(State):

    def __init__(self, timeout):
        State.__init__(self, 'wait', timeout)
        self.final_display_timer = None

    @pibooth.hookimpl
    def state_wait_enter(self, config, app):
        if config.getfloat('WINDOW', 'final_image_delay') < 0:
            self.final_display_timer = None
        else:
            self.final_display_timer = PoolingTimer(config.getfloat('WINDOW', 'final_image_delay'))

        animated = app.makers_pool.get()
        if config.getfloat('WINDOW', 'final_image_delay') < 0:
            self.final_display_timer = None
        else:
            self.final_display_timer = PoolingTimer(config.getfloat('WINDOW', 'final_image_delay'))

        if self.final_display_timer and self.final_display_timer.is_timeout():
            previous_picture = None
        elif app.config.getboolean('WINDOW', 'animate') and animated:
            app.previous_animated = itertools.cycle(animated)
            previous_picture = next(app.previous_animated)
            self.timer.timeout = config.getfloat('WINDOW', 'animate_delay')
            self.timer.start()
        else:
            previous_picture = app.previous_picture

        app.window.show_intro(previous_picture, app.printer.is_installed() and
                              app.nbr_duplicates < config.getint('PRINTER', 'max_duplicates') and
                              not app.printer_unavailable)
        app.window.set_print_number(len(app.printer.get_all_tasks()), app.printer_unavailable)

        app.led_capture.blink()
        if app.previous_picture_file and app.printer.is_installed() and not app.printer_unavailable:
            app.led_print.blink()

    @pibooth.hookimpl
    def state_wait_do(self, config, app, events):
        if config.getboolean('WINDOW', 'animate') and app.previous_animated and self.timer.is_timeout():
            previous_picture = next(app.previous_animated)
            app.window.show_intro(previous_picture, app.printer.is_installed() and
                                  app.nbr_duplicates < config.getint('PRINTER', 'max_duplicates') and
                                  not app.printer_unavailable)
            self.timer.start()
        else:
            previous_picture = app.previous_picture

        if app.find_print_event(events) and app.previous_picture_file and app.printer.is_installed()\
                and not (self.final_display_timer and self.final_display_timer.is_timeout()):

            if app.nbr_duplicates >= app.config.getint('PRINTER', 'max_duplicates'):
                LOGGER.warning("Too many duplicates sent to the printer (%s max)",
                               config.getint('PRINTER', 'max_duplicates'))
                return

            elif app.printer_unavailable:
                LOGGER.warning("Maximum number of printed pages reached (%s/%s max)", app.printer.nbr_printed,
                               config.getint('PRINTER', 'max_pages'))
                return

            with timeit("Send final picture to printer"):
                app.led_print.switch_on()
                app.printer.print_file(app.previous_picture_file,
                                       config.getint('PRINTER', 'pictures_per_page'))

            time.sleep(1)  # Just to let the LED switched on
            app.nbr_duplicates += 1

            if app.nbr_duplicates >= config.getint('PRINTER', 'max_duplicates') or app.printer_unavailable:
                app.window.show_intro(previous_picture, False)
                app.led_print.switch_off()
            else:
                app.led_print.blink()

        event = app.find_print_status_event(events)
        if event:
            app.window.set_print_number(len(event.tasks), app.printer_unavailable)

        if self.final_display_timer and self.final_display_timer.is_timeout():
            app.window.show_intro(None, False)

    @pibooth.hookimpl
    def state_wait_validate(self, app, events):
        if app.find_capture_event(events):
            if len(app.capture_choices) > 1:
                return 'choose'
            else:
                app.capture_nbr = app.capture_choices[0]
                return 'capture'

    @pibooth.hookimpl
    def state_wait_exit(self, app):
        app.led_capture.switch_off()
        app.led_print.switch_off()

        # Clear currently displayed image
        app.window.show_image(None)
