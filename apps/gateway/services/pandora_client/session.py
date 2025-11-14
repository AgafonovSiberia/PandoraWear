import asyncio
import logging
import time

from aiohttp import ClientResponse, ClientSession, CookieJar, TCPConnector

from apps.common.dao.config import PandoraCredDomain
from apps.gateway.services.pandora_client import excepton
from apps.gateway.services.pandora_client.field import AuthResponseField
from apps.gateway.services.pandora_client.url import URL

TTL_LOGIN = 5
LOGIN_TIMEOUT = 10
SESSION_LIFE_TIME = 60 * 60 * 3

logger = logging.getLogger(__name__)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"


class PandoraSession:
    def __init__(self, connector: TCPConnector, cred: PandoraCredDomain) -> None:

        self._session = ClientSession(
            base_url=URL.base_url,
            headers={"User-Agent": USER_AGENT},
            connector=connector,  # общий коннектор
            connector_owner=False,
            cookie_jar=CookieJar(),
        )
        self._login_lock = asyncio.Lock()
        self._last_login_ts = 0.0
        self._last_used_ts = time.time()

        self._pandora_cred = cred
        self.session_id = None
        self.user_id = None

    @property
    def last_used_ts(self) -> float:
        return self._last_used_ts

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.last_used_ts) > SESSION_LIFE_TIME

    async def close(self) -> None:
        await self._session.close()

    async def login(self) -> None:
        async with self._login_lock:
            if time.time() - self._last_login_ts < TTL_LOGIN:
                return

            response = await self._session.post(
                url=URL.login,
                data={
                    "login": self._pandora_cred.email,
                    "password": self._pandora_cred.password,
                    "lang": "ru",
                },
                timeout=LOGIN_TIMEOUT,
            )
            logger.info(await response.json())
            response_data = await response.json()
            session_id = response_data.get(AuthResponseField.SESSION_ID)
            if session_id is None:
                logger.info("Session id not found")
                raise excepton.LoginException(msg=str(response_data))

            self.session_id = response_data.get(AuthResponseField.SESSION_ID)
            self.user_id = response_data.get(AuthResponseField.USER_ID)
            logger.info(f"Logged in successfully. SessionId: {self.session_id}")

            self._last_login_ts = time.time()

    async def request(self, method: str, path: str, **kwargs) -> ClientResponse:
        self._last_used_ts = time.time()
        response = await self._session.request(method, path, **kwargs)
        if response.status not in (401, 403):
            return response

        response.release()
        return await self._request_with_relogin(method=method, path=path, **kwargs)

    async def _request_with_relogin(self, method: str, path: str, **kwargs) -> ClientResponse:
        self._last_login_ts = 0.0
        await self.login()
        return await self._session.request(method, path, **kwargs)
