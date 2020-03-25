from __future__ import print_function
import sys
if sys.version_info[0] < 3 :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
    #from BitField import BitFieldWordDesc, BitFieldWordValue
else :
    from DataFormat.BitField import BitFieldWordDesc, BitFieldWordValue
    #from .BitField import BitFieldWordDesc, BitFieldWordValue
from DataFormat.DataFormatIO import SubwordUnpacker
from DataFormat import DataFormat

from event_parse import decoder

class EventTable :

    def __init__(self) :
        self._l0ids = set()
        self._l0id_idx_map = {}
        self._events = []

    def clear(self) :
        self._l0ids = set()
        self._l0id_idx_map = {}
        self._events = []

    @property
    def l0ids(self) :
        return self._l0ids

    @property
    def events(self) :
        return self._events

    def event_at_l0id(self, l0id) :

        if l0id in self._l0id_idx_map :
            idx = self._l0id_idx_map[l0id]
            return self._events[idx]
        return None

    def add_events(self, event_list) :

        for event in event_list :
            self.add_event(event)
        self.sort_events_by_l0id()

    def add_event(self, event) :

        if event.header_l0id in self.l0ids :
            print("WARNING Already encountered event data for this L0ID = {}, skipping!".format(hex(event.header_l0id)))
        else :
            this_event_idx = len(self._events)
            self._events.append(event)
            self._l0ids.add(event.header_l0id)
            self._l0id_idx_map[event.header_l0id] = this_event_idx

    def n_words_total(self) :
        return sum([e.n_words_total for e in self.events])

    def sort_events_by_l0id(self) :

        self._events.sort(key = lambda event : event.header_l0id, reverse = False)
        self._l0id_idx_map = {}
        for ievent, event in enumerate(self._events) :
            self._l0id_idx_map[event.header_l0id] = ievent

    def events_gen(self) :

        for event in self._events :
            yield event
