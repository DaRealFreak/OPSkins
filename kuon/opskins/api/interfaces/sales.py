#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import requests

from kuon.common import *
from kuon.opskins import APIResponse, OPSkins
from kuon.opskins.api import HtmlToJsonParser
from kuon.opskins.api.exceptions import *
from kuon.opskins.common import *


class ISales(OPSkins):
    """The ISales interface of OPSkins
    To prevent bot sniping it doesn't list the new items in the first 10 minutes.
    I'll add another option to use a different function to fulfill the functions of the handicapped API options

    common not self explanatory keys:
        app id:
            The Steam AppID of the game which owns this item (e.g. 730 for CS:GO, 440 for TF2, 570 for Dota 2)
        context id:
            (2 for Valve games, 6 for Steam Community items, 1 for H1Z1, etc.).
            When you right-click on an item in your Steam inventory and copy its URL,
            the context ID is the second number after the hash.
        asset id:
            The Steam asset ID of the item. This is also known as just the item's id
        market name:
            The full market name of the item. For example: "AK-47 | Aquamarine Revenge (Field-Tested)"
    """

    def __init__(self, *args, **kwargs):
        """Initializing function"""
        super().__init__(*args, **kwargs)

    def get_sales(self, status_type=ItemStatus.AWAITING_PICKUP, app_id=None, after_saleid=None, page=None,
                  per_page=None, sort=None) -> APIResponse:
        """GetSales v1 implementation
        https://opskins.com/kb/api-isales#method-getsales-v1

        :param status_type:
        :param app_id:
        :param after_saleid:
        :param page:
        :param per_page:
        :param sort:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/GetSales/v1/"

        if not status_type:
            raise MissingArgumentException('The function get_sales requires the argument "status_type"')

        payload = {
            'type': status_type,
        }

        if app_id:
            payload['appid'] = app_id
        if after_saleid:
            payload['after_saleid'] = str(after_saleid)
        if page:
            payload['page'] = str(page)
        if per_page:
            payload['per_page'] = str(per_page)
        if sort:
            payload['sort'] = sort

        link = requests.get(url=api_url, params=payload, headers=self._headers)
        return APIResponse(link.text)

    def get_listing_limit(self) -> APIResponse:
        """GetListingLimit v1 implementation
        https://opskins.com/kb/api-isales#method-getlistinglimit-v1

        :return:
        """
        api_url = "https://api.opskins.com/ISales/GetListingLimit/v1/"

        link = requests.get(url=api_url, headers=self._headers)
        return APIResponse(link.text)

    def list_items(self, items: list) -> APIResponse:
        """ListItems v1 implementation
        https://opskins.com/kb/api-isales#method-listitems-v1

        :param items:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/ListItems/v1/"
        required_keys = ['appid', 'contextid', 'assetid', 'price', 'addons']

        for item in items:
            if any([key not in item for key in required_keys]):
                raise ArgumentIncompleteError("Your passed item doesn't have all required keys({0:s}).".format(
                    ",".join(required_keys)
                ))

        payload = {
            'items': json.dumps(items)
        }

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def edit_price(self, saleid, price: int) -> APIResponse:
        """EditPrice v1 implementation
        https://opskins.com/kb/api-isales#method-editprice-v1

        :param saleid:
        :param price:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/EditPrice/v1/"

        payload = {
            "saleid": str(saleid),
            "price": str(price)
        }

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def edit_price_multi(self, items: list) -> APIResponse:
        """EditPriceMulti v1 implementation
        https://opskins.com/kb/api-isales#method-editpricemulti-v1

        :param items:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/EditPriceMulti/v1/"
        required_keys = ['saleid', 'price']

        for item in items:
            if any([key not in item for key in required_keys]):
                raise ArgumentIncompleteError("Your passed item doesn't have all required keys({0:s}).".format(
                    ",".join(required_keys)
                ))

        payload = {}

        for item in items:
            payload['items[{0:s}]'.format(str(item['saleid']))] = str(item['price'])

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def bump_items(self, items: list) -> APIResponse:
        """BumpItems v1 implementation
        https://opskins.com/kb/api-isales#method-bumpitems-v1

        :param items:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/BumpItems/v1/"

        payload = {
            "items": ",".join([str(item) for item in items])
        }

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def return_items(self, items: list) -> APIResponse:
        """ReturnItems v1 implementation
        https://opskins.com/kb/api-isales#method-returnitems-v1

        :param items:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/ReturnItems/v1/"

        payload = {
            "items": ",".join([str(item) for item in items])
        }

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def get_active_trade_offers(self) -> APIResponse:
        """GetActiveTradeOffers v1 implementation
        https://opskins.com/kb/api-isales#method-getactivetradeoffers-v1

        :return:
        """
        api_url = "https://api.opskins.com/ISales/GetActiveTradeOffers/v1/"

        link = requests.get(url=api_url, headers=self._headers)
        return APIResponse(link.text)

    def search(self, search_item='', app_id=CommonSteamGames.APP_ID_CSGO, price_min=None,
               price_max=None) -> APIResponse:
        """Search v1 implementation
        https://opskins.com/kb/api-isales#method-search-v1

        This endpoint is relatively heavily rate-limited.
        Currently, it is limited to 20 requests per minute.
        To prevent bot sniping, this endpoint will only return listings which have been publicly visible for at least
        ten minutes, and are not currently limited to Buyers Club members.
        This endpoint always returns 100 listings sorted from lowest to highest price.

        :param search_item:
        :param app_id:
        :param price_min:
        :param price_max:
        :return:
        """
        api_url = 'https://api.opskins.com/ISales/Search/v1/'

        if not app_id:
            raise MissingArgumentException('The function search requires the argument "app_id"')

        payload = {
            'app': OPSkins.app_id_to_search_id(app_id),
        }

        if search_item:
            payload['search_item'] = search_item
        if price_min:
            payload['min'] = str(price_min)
        if price_max:
            payload['max'] = str(price_max)

        link = requests.get(url=api_url, params=payload, headers=self._headers)
        return APIResponse(link.text)

    def search_no_delay(self, search_item='', app_id=CommonSteamGames.APP_ID_CSGO, price_min=None, price_max=None,
                        sorting=FilterSorting.PRICE_ASC) -> APIResponse:
        """Custom implementation of the Search v1 API option

        Since items don't appear within the first 10 minutes using the API
        this method is using a normal web request to retrieve the first 18 search results
        Adds an additional option to sort the results by default

        :param search_item:
        :param app_id:
        :param price_min:
        :param price_max:
        :param sorting:
        :return:
        """
        url = "https://opskins.com/"

        payload = {
            "app": OPSkins.app_id_to_search_id(app_id),
            "loc": "shop_search",
            # low to high sorting
            "sort": sorting
        }

        if search_item:
            payload['search_item'] = search_item
        if price_min:
            payload['min'] = str(price_min)
        if price_max:
            payload['max'] = str(price_max)

        link = self.selenium_helper.get(url=url, params=payload)
        return APIResponse(HtmlToJsonParser.search_result(link.page_source))

    def buy_items(self, saleids: list, total) -> APIResponse:
        """BuyItems v1 implementation
        https://opskins.com/kb/api-isales#method-buyitems-v1

        :param saleids:
        :param total:
        :return:
        """
        api_url = "https://api.opskins.com/ISales/BuyItems/v1/"

        payload = {
            "saleids": ",".join([str(saleid) for saleid in saleids]),
            "total": str(total)
        }

        link = requests.post(url=api_url, data=payload, headers=self._headers)
        return APIResponse(link.text)

    def get_last_sales(self, market_name: str, app_id=CommonSteamGames.APP_ID_CSGO, context_id=ContextIds.VALVE_GAMES,
                       val_1=None) -> APIResponse:
        """GetLastSales v1 implementation
        https://opskins.com/kb/api-isales#method-getlastsales-v1

        :param market_name:
        :param app_id:
        :param context_id:
        :param val_1:
        :return:
        """
        api_url = 'https://api.opskins.com/ISales/GetLastSales/v1/'

        if not app_id:
            raise MissingArgumentException('The function get_last_sales requires the argument "app_id"')
        if not context_id:
            raise MissingArgumentException('The function get_last_sales requires the argument "context_id"')

        payload = {
            'appid': str(app_id),
            'contextid': str(context_id),
            'market_name': market_name
        }

        if val_1:
            payload['val_1'] = str(val_1)

        link = requests.get(url=api_url, params=payload, headers=self._headers)
        return APIResponse(link.text)

    def get_last_sales_no_delay(self, market_name: str, app_id=CommonSteamGames.APP_ID_CSGO,
                                context_id=None, val_1=None) -> APIResponse:
        """Custom implementation of the GetLastSales v1 API option

        Since the returned data from the API is sometimes about 1 week old
        This method is using a normal web request to find the item and return the last 20 sales
        in the format of the get_last_sales function

        :param market_name:
        :param app_id:
        :param context_id:
        :param val_1:
        :return:
        """
        if context_id or val_1:
            raise NotImplementedError('The OPSkins web view doesn\'t allow filtering for context_id or val_1')

        # we can freely use the API method here we just need to get one item id with the same market name
        listed_items = self.search(search_item=market_name, app_id=app_id)
        item_id = listed_items.response.sales[0].id

        url = "https://opskins.com/"

        payload = {
            "loc": "shop_view_item",
            # low to high sorting
            "item": item_id
        }

        link = self.selenium_helper.get(url=url, params=payload)
        return APIResponse(HtmlToJsonParser.last_sold(link.page_source))

    def get_sales_status(self) -> APIResponse:
        """GetSaleStatuses v1 implementation
        https://opskins.com/kb/api-isales#method-getsalestatuses-v1

        :return:
        """
        api_url = 'https://api.opskins.com/ISales/GetSaleStatuses/v1/'

        link = requests.get(url=api_url, headers=self._headers)
        return APIResponse(link.text)
