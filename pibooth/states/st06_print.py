# -*- coding: utf-8 -*-

import time
import pibooth
from pibooth.states.machine import State
from pibooth.utils import timeit


class StatePrint(State):

    def __init__(self, timeout):
        State.__init__(self, 'print', timeout)
        self.printed = False

    @pibooth.hookimpl
    def state_print_enter(self, cfg, app):
        self.printed = False

        with timeit("Display the final picture"):
            app.window.set_print_number(len(app.printer.get_all_tasks()), app.printer_unavailable)
            app.window.show_print(app.previous_picture)

        app.led_print.blink()
        # Reset timeout in case of settings changed
        self.timer.timeout = cfg.getfloat('PRINTER', 'printer_delay')
        self.timer.start()

    @pibooth.hookimpl
    def state_print_do(self, cfg, app, events):
        if app.find_print_event(events) and app.previous_picture_file:

            with timeit("Send final picture to printer"):
                app.led_print.switch_on()
                app.printer.print_file(app.previous_picture_file,
                                       cfg.getint('PRINTER', 'pictures_per_page'))

            time.sleep(1)  # Just to let the LED switched on
            app.nbr_duplicates += 1
            app.led_print.blink()
            self.printed = True

    @pibooth.hookimpl
    def state_print_validate(self, app):
        if self.timer.is_timeout() or self.printed:
            if self.printed:
                app.window.set_print_number(len(app.printer.get_all_tasks()), app.printer_unavailable)
            return 'finish'
