import logging

from aiohttp import ClientSession

from gateway.pandora import (
    URL,
    AuthResponseField,
    RequestMethod,
    ResponseStatus,
    excepton,
)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

FORCE_UPDATE_INTERVAL = 300
DENSE_POLLING_INTERVAL = 1
COMMAND_RESPONSE_TIMEOUT = 35

logger = logging.getLogger(__name__)


class BaseClient:
    def __init__(self, username: str, password: str) -> None:
        self._token = None
        self.username = username
        self.password = password
        self.session = ClientSession(
            base_url=URL.BASE_URL, headers={"User-Agent": USER_AGENT}
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        logger.info("Session closed")

    async def __aenter__(self) -> "BaseClient":
        logger.info("Session closed")
        return self

    async def login(self) -> None:
        """Login on gateway"""
        response = await self.session.post(
            url=URL.LOGIN_PATH,
            data={"login": self.username, "password": self.password, "lang": "ru"},
        )
        logger.info(await response.text())
        response_data = await response.json()
        session_id = response_data.get(AuthResponseField.SESSION_ID)
        if session_id is None:
            logger.info("Session " "id not found")
            raise excepton.LoginException(msg=str(response_data))

        self._token = response_data.get(AuthResponseField.SESSION_ID)
        logger.info("Logged in successfully")

    async def request(
        self, url: str, data: dict = None, method: RequestMethod = RequestMethod.GET
    ):
        """Send request to gateway"""
        response = await self.session.request(method=method, url=url, data=data)
        logger.info(await response.text())
        response = await response.json()
        if (
            isinstance(response, dict)
            and response.get(AuthResponseField.STATUS)
            in ResponseStatus.session_expire_statuses()
        ):
            logger.info("Request with relogin")
            return await self.request_with_relogin(url=url, data=data, method=method)
        return response

    async def request_with_relogin(
        self, url: str, data: dict = None, method: RequestMethod = RequestMethod.GET
    ):
        """Sends request to gateway with relogin"""
        await self.login()
        return await self.session.request(method=method, url=url, data=data)
