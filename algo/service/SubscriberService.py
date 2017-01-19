from algo.strategy.strategyEntry import *

def subscribeInstrument(instrument):
    """
    create event
    """
    global_event_engine.put(AQIStrategyEvent(EVENT_MARKETDATA, instrument))


