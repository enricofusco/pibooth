# -*- coding: utf-8 -*-

from pibooth.states.machine import State, StateMachine
from pibooth.states.st00_failsafe import StateFailSafe
from pibooth.states.st01_wait import StateWait
from pibooth.states.st02_choose import StateChoose
from pibooth.states.st03_chosen import StateChosen
from pibooth.states.st04_capture import StateCapture
from pibooth.states.st05_processing import StateProcessing
from pibooth.states.st06_print import StatePrint
from pibooth.states.st07_finish import StateFinish
