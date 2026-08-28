from http import HTTPStatus

from app.core.configGithub import (
    SHIPROCKET_EMAIL,
    SHIPROCKET_PASSWORD,
)

from app.utils.github.httpClient import (
    shiprocketHttpClient,
)

from app.utils.github.tokenManager import (
    getToken,
    setToken,
    clearToken,
)
from sqlalchemy.orm import Session

from app.services.github.orderService import (
    orderService,
)
from app.schemas.github.orderSchema import (
    OrderUpdate,
)


class ShiprocketService:

    async def login(self):

        token = getToken()

        if token:
            return token

        response = await shiprocketHttpClient.post(

            "/auth/login",

            {
                "email": SHIPROCKET_EMAIL,
                "password": SHIPROCKET_PASSWORD
            }

        )

        data = response.json()

        if response.status_code != HTTPStatus.OK:

            raise Exception(

                data.get(
                    "message",
                    "Shiprocket authentication failed."
                )

            )

        token = data.get("token")

        if token is None:

            raise Exception(
                "Authentication token not received."
            )

        setToken(token)

        return token

    async def _request(

        self,

        method,

        endpoint,

        data=None,

        params=None

    ):

        await self.login()

        if method == "GET":

            response = await shiprocketHttpClient.get(

                endpoint,

                params=params

            )

        elif method == "POST":

            response = await shiprocketHttpClient.post(

                endpoint,

                data=data

            )

        elif method == "PUT":

            response = await shiprocketHttpClient.put(

                endpoint,

                data=data

            )

        elif method == "DELETE":

            response = await shiprocketHttpClient.delete(

                endpoint

            )

        else:

            raise Exception(
                "Unsupported HTTP Method"
            )

        if response.status_code == HTTPStatus.UNAUTHORIZED:

            clearToken()

            await self.login()

            if method == "GET":

                response = await shiprocketHttpClient.get(
                    endpoint,
                    params=params
                )

            elif method == "POST":

                response = await shiprocketHttpClient.post(
                    endpoint,
                    data=data
                )

            elif method == "PUT":

                response = await shiprocketHttpClient.put(
                    endpoint,
                    data=data
                )

            elif method == "DELETE":

                response = await shiprocketHttpClient.delete(
                    endpoint
                )

        if response.status_code >= 400:
            raise Exception(
                response.json().get(
                    "message",
                    "Shiprocket API Error"
                )
            )

        return response.json()

    async def createOrder(
        self,
        order
    ):
        return await self._request(
            "POST",
            "/orders/create/adhoc",
            data=order.model_dump(
                mode="json"
            )
        )

    async def checkServiceability(
        self,
        request
    ):
        return await self._request(
            "GET",
            "/courier/serviceability",
            params=request.model_dump(
                mode="json"
            )
        )

    async def getAvailableCouriers(
        self,
        request
    ):
        return await self._request(
            "GET",
            "/courier/serviceability",
            params=request.model_dump(
                mode="json"
            )
        )

    async def generateAwb(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/courier/assign/awb",
            data=request.model_dump(
                mode="json"
            )
        )

    async def requestPickup(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/courier/generate/pickup",
            data=request.model_dump(
                mode="json"
            )
        )

    async def generateLabel(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/courier/generate/label",
            data=request.model_dump(
                mode="json"
            )
        )

    async def generateInvoice(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/courier/generate/invoice",
            data=request.model_dump(
                mode="json"
            )
        )

    async def generateManifest(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/courier/generate/manifest",
            data=request.model_dump(
                mode="json"
            )
        )

    async def trackShipment(
        self,
        awbCode: str
    ):
        return await self._request(
            "GET",
            f"/courier/track/awb/{awbCode}"
        )

    async def cancelOrder(
        self,
        orderIds: list[int]
    ):
        return await self._request(
            "POST",
            "/orders/cancel",
            data={
                "ids": orderIds
            }
        )

    async def getOrders(
        self
    ):
        return await self._request(
            "GET",
            "/orders"
        )

    async def getOrderById(
        self,
        orderId: int
    ):
        return await self._request(
            "GET",
            f"/orders/show/{orderId}"
        )

    async def updateOrder(
        self,
        request
    ):
        return await self._request(
            "PUT",
            "/orders/update",
            data=request.model_dump(
                mode="json"
            )
        )

    async def getPickupLocations(
        self
    ):
        return await self._request(
            "GET",
            "/settings/company/pickup"
        )

    async def addPickupLocation(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/settings/company/addpickup",
            data=request.model_dump(
                mode="json"
            )
        )

    async def getChannels(
        self
    ):
        return await self._request(
            "GET",
            "/channels"
        )

    async def getCourierCompanies(
        self
    ):
        return await self._request(
            "GET",
            "/courier/courierListWithCounts"
        )

    async def getNdrShipments(
        self
    ):
        return await self._request(
            "GET",
            "/ndr"
        )

    async def updateNdr(
        self,
        request
    ):
        return await self._request(
            "POST",
            "/ndr/action",
            data=request.model_dump(
                mode="json"
            )
        )


shiprocketService = ShiprocketService()