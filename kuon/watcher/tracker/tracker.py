#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from kuon.api_response import LockedDict, LockedList
from kuon.watcher.tracker.json_manager import JsonManager


class TrackConditions:
    BELOW_VALUE = 0
    BELOW_AVERAGE_LAST_SOLD = 1
    BELOW_CHEAPEST_LAST_SOLD = 2


class Tracker(object):
    """Class to track search terms with conditions"""

    ITEM_REQUIRED_KEYWORDS = ('search_item', 'conditions')

    def __init__(self, log_level: int = logging.ERROR) -> None:
        """Initializing function"""
        logging.basicConfig(level=log_level,
                            format='[%(asctime)s.%(msecs)03d %(levelname)s %(name)s] %(message)s',
                            datefmt="%H:%M:%S")
        self.logger = logging.getLogger("watcher_tracker")

        self._json_manager = JsonManager()
        self._tracked_items = self._json_manager.get_tracked_items(self.ITEM_REQUIRED_KEYWORDS)

    @property
    def tracked_items(self) -> LockedList:
        """Get the tracked items as LockedList

        :return:
        """
        return LockedList(self._tracked_items)

    def add_item(self, item: LockedDict) -> None:
        """Adds an item to the tracking list

        :type item: LockedDict
        :return:
        """
        if not all([key in item for key in Tracker.ITEM_REQUIRED_KEYWORDS]):
            self.logger.error('Not all required keywords ({keywords}) are in the added item'.format(
                keywords=",".join(Tracker.ITEM_REQUIRED_KEYWORDS)))
            return

        if item not in self._tracked_items:
            self._tracked_items.append(item)
            self._json_manager.save_tracked_items(self._tracked_items)

    def remove_item(self, item: LockedDict) -> None:
        """Removes an item from the tracking list

        :type item: LockedDict
        :return:
        """
        if item in self._tracked_items:
            self._tracked_items.remove(item)
            self._json_manager.save_tracked_items(self._tracked_items)
