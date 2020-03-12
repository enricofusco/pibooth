# -*- coding: utf-8 -*-

import pluggy

hookspec = pluggy.HookspecMarker('pibooth')


#--- FailSafe State -----------------------------------------------------------


@hookspec
def state_failsafe_enter(config, app):
    """Actions performed when application enter in FailSafe state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_failsafe_do(config, app, events):
    """Actions performed when application is in FailSafe state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_failsafe_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_failsafe_exit(config, app):
    """Actions performed when application exit FailSafe state.

    :param config: application config
    :param app: application instance
    """


#--- Wait State ---------------------------------------------------------------


@hookspec
def state_wait_enter(config, app):
    """Actions performed when application enter in Wait state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_wait_do(config, app, events):
    """Actions performed when application is in Wait state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_wait_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_wait_exit(config, app):
    """Actions performed when application exit Wait state.

    :param config: application config
    :param app: application instance
    """


#--- Choose State -------------------------------------------------------------


@hookspec
def state_choose_enter(config, app):
    """Actions performed when application enter in Choose state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_choose_do(config, app, events):
    """Actions performed when application is in Choose state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_choose_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_choose_exit(config, app):
    """Actions performed when application exit Choose state.

    :param config: application config
    :param app: application instance
    """


#--- Chosen State -------------------------------------------------------------


@hookspec
def state_chosen_enter(config, app):
    """Actions performed when application enter in Chosen state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_chosen_do(config, app, events):
    """Actions performed when application is in Chosen state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_chosen_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_chosen_exit(config, app):
    """Actions performed when application exit Chosen state.

    :param config: application config
    :param app: application instance
    """


#--- Capture State ------------------------------------------------------------


@hookspec
def state_capture_enter(config, app):
    """Actions performed when application enter in Capture state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_capture_do(config, app, events):
    """Actions performed when application is in Capture state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_capture_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_capture_exit(config, app):
    """Actions performed when application exit Capture state.

    :param config: application config
    :param app: application instance
    """


#--- Processing State ---------------------------------------------------------


@hookspec
def state_processing_enter(config, app):
    """Actions performed when application enter in Processing state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_processing_do(config, app, events):
    """Actions performed when application is in Processing state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_processing_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_processing_exit(config, app):
    """Actions performed when application exit Processing state.

    :param config: application config
    :param app: application instance
    """


#--- PrintView State ----------------------------------------------------------


@hookspec
def state_print_enter(config, app):
    """Actions performed when application enter in Print state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_print_do(config, app, events):
    """Actions performed when application is in Print state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_print_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_print_exit(config, app):
    """Actions performed when application exit Print state.

    :param config: application config
    :param app: application instance
    """


#--- Finish State -------------------------------------------------------------


@hookspec
def state_finish_enter(config, app):
    """Actions performed when application enter in Finish state.

    :param config: application config
    :param app: application instance
    """


@hookspec
def state_finish_do(config, app, events):
    """Actions performed when application is in Finish state.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec(firstresult=True)
def state_finish_validate(config, app, events):
    """Return the next state name if application can switch to it
    else return None.

    :param config: application config
    :param app: application instance
    :param events: pygame events generated since last call
    """


@hookspec
def state_finish_exit(config, app):
    """Actions performed when application exit Finish state.

    :param config: application config
    :param app: application instance
    """
