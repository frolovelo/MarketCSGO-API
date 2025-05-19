from typing import Union, List, Final
import requests
from requests.adapters import HTTPAdapter
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type, stop_never


class MarketApi:
    _REQUEST_TIMEOUT: Final[int] = 5

    def __init__(self, key) -> None:
        self._base_url = "https://market.csgo.com/api/"
        self._key = key
        self._session = requests.Session()
        self._session.mount(self._base_url, HTTPAdapter(max_retries=3))

    def _patch(self, url: str, body: dict) -> dict:
        resp = self._session.patch(f'{self._base_url}/{url}?key={self._key}', json=body, timeout=self._REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def _post(self, url: str, body: Union[dict, list]) -> Union[dict, list]:
        resp = self._session.post(f'{self._base_url}/{url}?key={self._key}', json=body, timeout=self._REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def _put(self, url: str, body: Union[dict, list]) -> None:
        resp = self._session.put(f'{self._base_url}/{url}?key={self._key}', json=body, timeout=self._REQUEST_TIMEOUT)
        resp.raise_for_status()

    def _get(self, url: str) -> Union[list, dict]:
        resp = self._session.get(f'{self._base_url}/{url}?key={self._key}', timeout=self._REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def _delete(self, url: str):
        resp = self._session.delete(f'{self._base_url}/{url}?key={self._key}', timeout=self._REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    @retry(
        stop=stop_never,
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def search_item_by_hash_name(self, hash_name: str) -> dict:
        return self._session.get(
            f'{self._base_url}v2/search-item-by-hash-name?key={self._key}&hash_name={hash_name}').json()

    @retry(
        stop=stop_never,
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def get_bid_ask(self, hash_name: str) -> dict:
        resp = self._session.get(f'{self._base_url}v2/bid-ask?key={self._key}&hash_name={hash_name}')
        resp.raise_for_status()
        return resp.json()

    def search_item_by_hash_name_specific(self, hash_name: str) -> dict:
        resp = self._session.get(f'{self._base_url}v2/search-item-by-hash-name-specific?key={self._key}&hash_name={hash_name}&with_stickers=1&lang=en')
        resp.raise_for_status()
        return resp.json()

    def get_list_items_info(self, hash_name: str) -> dict:
        resp = self._session.get(f'{self._base_url}v2/get-list-items-info?key={self._key}&list_hash_name[]={hash_name}')
        resp.raise_for_status()
        return resp.json()

    def get_all_stickers(self):
        resp = self._session.get(f'{self._base_url}v2/stickers?key={self._key}&lang=ru')
        resp.raise_for_status()
        return resp.json()

    def get_money(self) -> dict:
        return self._session.get(f'{self._base_url}v2/get-money?key={self._key}').json()

    def ping_tm(self, body):
        return self._session.post(f'{self._base_url}v2/ping-new?key={self._key}', json=body).json()

    def get_history(self, date_from: str, date_end: str) -> dict:
        resp = self._session.get(
            f'{self._base_url}v2/operation-history?key={self._key}&date={date_from}&date_end={date_end}')
        resp.raise_for_status()
        resp = resp.json()
        return resp

    def send_money(self, amount, user_api_key, pay_pass) -> None:
        return self._session.get(f'{self._base_url}v2/money-send/{amount}/{user_api_key}?key={self._key}&pay_pass={pay_pass}').json()

    def go_offline(self) -> None:
        return self._session.get(f'{self._base_url}v2/go-offline?key={self._key}').json()

    def update_inventory(self) -> None:
        return self._session.get(f'{self._base_url}v2/update-inventory?key={self._key}').json()

    def get_my_steam_id(self) -> dict:
        return self._session.get(f'{self._base_url}v2/get-my-steam-id?key={self._key}').json()

    def my_inventory(self) -> dict:
        return self._session.get(f'{self._base_url}v2/my-inventory?key={self._key}').json()

    @retry(
        stop=stop_never,
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def get_my_orders(self, page: int = 0) -> dict:
        resp = self._session.get(f'{self._base_url}v2/get-orders?key={self._key}')
        resp.raise_for_status()
        return resp.json()

    @retry(
        stop=stop_never,
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def set_order(self, market_hash_name: str, count: int, price: int | None) -> dict:
        if price:
            resp = self._session.post(
                f'{self._base_url}v2/set-order?key={self._key}&market_hash_name={market_hash_name}&count={count}&price={price}')
            resp.raise_for_status()
        else:
            resp = self._session.post(
                f'{self._base_url}v2/set-order?key={self._key}&market_hash_name={market_hash_name}&count={count}')
            resp.raise_for_status()
        return resp.json()

    def buy(self, market_hash_name: str, price: int | None) -> dict:
        return self._session.post(
            f'{self._base_url}v2/buy?key={self._key}&hash_name={market_hash_name}&price={price}').json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.exceptions.RequestException)
    )
    def buy_by_id(self, id: str, price: int | None) -> dict:
        return self._session.post(
            f'{self._base_url}v2/buy?key={self._key}&id={id}&price={price}').json()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
