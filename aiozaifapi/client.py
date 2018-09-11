import asyncio
import aiohttp
import async_timeout
import zaifapi
from zaifapi.api_common import get_api_url
from zaifapi.api_error import ZaifApiError, ZaifApiNonceError


class AsyncHTTPMixin:

    async def _http_get(self, session, url, params={}):
        with async_timeout.timeout(self._timeout):
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def _http_post(self, session, url, data=None, headers=None):
        with async_timeout.timeout(self._timeout):
            async with session.post(url, data=data, headers=headers) as resp:
                return await resp.json()


class ZaifPublicApi(zaifapi.ZaifPublicApi, AsyncHTTPMixin):

    def __init__(self, api_url=None, loop=None):
        super().__init__(get_api_url(api_url, 'api', version=1))
        self._timeout = 3
        self.loop = loop or asyncio.get_event_loop()

    async def _execute_api(self, func_name, schema_keys=None, q_params=None, **kwargs):
        schema_keys = schema_keys or []
        q_params = q_params or {}
        params = self._params_pre_processing(schema_keys, kwargs)
        self._url.add_dirs(func_name, *params.values())
        url = self._url.get_absolute_url()
        self._url.refresh_dirs()
        async with aiohttp.ClientSession(loop=self.loop) as session:
            return await self._http_get(session, url, params=q_params)


class ZaifFuturesPublicApi(zaifapi.ZaifFuturesPublicApi, AsyncHTTPMixin):

    def __init__(self, api_url=None, loop=None):
        super().__init__(get_api_url(api_url, 'api', version=1))
        self._timeout = 3
        self.loop = loop or asyncio.get_event_loop()

    async def _execute_api(self, func_name, schema_keys=None, q_params=None, **kwargs):
        schema_keys = schema_keys or []
        q_params = q_params or {}
        params = self._params_pre_processing(schema_keys, kwargs)
        if params.get('page', None):
            self._url.add_dirs(func_name, params.get('group_id'), params.get('currency_pair'),
                               params.get('page'))
        else:
            self._url.add_dirs(func_name, params.get('group_id'), params.get('currency_pair'))
        url = self._url.get_absolute_url()
        self._url.refresh_dirs()
        async with aiohttp.ClientSession(loop=self.loop) as session:
            return await self._http_get(session, url, params=q_params)


class ZaifTradeApi(zaifapi.ZaifTradeApi, AsyncHTTPMixin):

    def __init__(self, key, secret, api_url=None, loop=None):
        super().__init__(key, secret, get_api_url(api_url, 'tapi'))
        self._timeout = 3
        self.loop = loop or asyncio.get_event_loop()

    async def _execute_api(self, func_name, schema_keys=None, params=None):
        schema_keys = schema_keys or []
        params = params or {}

        _params = self._params_pre_processing(schema_keys, params, func_name)
        header = self._get_header(_params)
        url = self._url.get_absolute_url()
        async with aiohttp.ClientSession(loop=self.loop) as session:
            res = await self._http_post(session, url, data=params, headers=header)

        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']


class ZaifLeverageTradeApi(zaifapi.ZaifLeverageTradeApi, AsyncHTTPMixin):

    def __init__(self, key, secret, api_url=None, loop=None):
        super().__init__(key, secret, get_api_url(api_url, 'tlapi'))
        self._timeout = 3
        self.loop = loop or asyncio.get_event_loop()

    async def _execute_api(self, func_name, schema_keys=None, params=None):
        schema_keys = schema_keys or []
        params = params or {}

        _params = self._params_pre_processing(schema_keys, params, func_name)
        header = self._get_header(_params)
        url = self._url.get_absolute_url()
        async with aiohttp.ClientSession(loop=self.loop) as session:
            res = await self._http_post(session, url, data=params, headers=header)

        if res['success'] == 0:
            if res['error'].startswith('nonce'):
                raise ZaifApiNonceError(res['error'])
            raise ZaifApiError(res['error'])
        return res['return']
