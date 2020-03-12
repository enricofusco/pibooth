# -*- coding: utf-8 -*-

import os.path as osp
import pibooth
from pibooth.states.machine import State
from pibooth.pictures import get_picture_maker
from pibooth.utils import timeit


class StateProcessing(State):

    def __init__(self):
        State.__init__(self, 'processing')

    @pibooth.hookimpl
    def state_processing_enter(self, app):
        app.window.show_work_in_progress()
        app.makers_pool.clear()
        app.previous_animated = []

    @pibooth.hookimpl
    def state_processing_do(self, config, app):
        with timeit("Creating the final picture"):
            captures = app.camera.get_captures()

            backgrounds = config.gettuple('PICTURE', 'backgrounds', ('color', 'path'), 2)
            if app.capture_nbr == app.capture_choices[0]:
                background = backgrounds[0]
            else:
                background = backgrounds[1]

            overlays = config.gettuple('PICTURE', 'overlays', 'path', 2)
            if app.capture_nbr == app.capture_choices[0]:
                overlay = overlays[0]
            else:
                overlay = overlays[1]

            texts = [config.get('PICTURE', 'footer_text1').strip('"'),
                     config.get('PICTURE', 'footer_text2').strip('"')]
            colors = config.gettuple('PICTURE', 'text_colors', 'color', len(texts))
            text_fonts = config.gettuple('PICTURE', 'text_fonts', str, len(texts))
            alignments = config.gettuple('PICTURE', 'text_alignments', str, len(texts))

            def _setup_maker(m):
                m.set_background(background)
                if any(elem != '' for elem in texts):
                    for params in zip(texts, text_fonts, colors, alignments):
                        m.add_text(*params)
                if config.getboolean('PICTURE', 'captures_cropping'):
                    m.set_cropping()
                if overlay:
                    m.set_overlay(overlay)
                if config.getboolean('GENERAL', 'debug'):
                    m.set_outlines()

            maker = get_picture_maker(captures, config.get('PICTURE', 'orientation'))
            _setup_maker(maker)
            app.previous_picture = maker.build()

        app.previous_picture_file = osp.join(app.savedir, osp.basename(app.dirname) + "_pibooth.jpg")
        maker.save(app.previous_picture_file)

        if config.getboolean('WINDOW', 'animate') and app.capture_nbr > 1:
            with timeit("Asyncronously generate pictures for animation"):
                for capture in captures:
                    maker = get_picture_maker((capture,), config.get('PICTURE', 'orientation'), force_pil=True)
                    _setup_maker(maker)
                    app.makers_pool.add(maker)

    @pibooth.hookimpl
    def state_processing_validate(self, config, app):
        if app.printer.is_installed() and config.getfloat('PRINTER', 'printer_delay') > 0 \
                and not app.printer_unavailable:
            return 'print'
        else:
            return 'finish'  # Can not print
