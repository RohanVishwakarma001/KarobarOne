from fastapi import HTTPException

from app.services.github.shiprocketService import (
    shiprocketService,
)


class ShiprocketController:

    async def _execute(
        self,
        callback,
        *args
    ):
        try:
            return await callback(*args)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

    async def login(self):
        return await self._execute(
            shiprocketService.login
        )

    async def createOrder(
        self,
        order
    ):
        return await self._execute(
            shiprocketService.createOrder,
            order
        )

    async def checkServiceability(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.checkServiceability,
            request
        )

    async def getAvailableCouriers(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.getAvailableCouriers,
            request
        )

    async def generateAwb(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.generateAwb,
            request
        )

    async def requestPickup(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.requestPickup,
            request
        )

    async def generateLabel(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.generateLabel,
            request
        )

    async def generateInvoice(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.generateInvoice,
            request
        )

    async def generateManifest(
        self,
        request
    ):
        return await self._execute(
            shiprocketService.generateManifest,
            request
        )

    async def trackShipment(
        self,
        awbCode: str
    ):
        return await self._execute(
            shiprocketService.trackShipment,
            awbCode
        )

    async def cancelOrder(
        self,
        orderIds
    ):
        return await self._execute(
            shiprocketService.cancelOrder,
            orderIds
        )


shiprocketController = ShiprocketController()
async def getOrders(
    self
):
    return await self._execute(
        shiprocketService.getOrders
    )


async def getOrderById(
    self,
    orderId: int
):
    return await self._execute(
        shiprocketService.getOrderById,
        orderId
    )


async def updateOrder(
    self,
    request
):
    return await self._execute(
        shiprocketService.updateOrder,
        request
    )
async def getPickupLocations(
    self
):

    try:
        return await shiprocketService.getPickupLocations()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


async def addPickupLocation(
    self,
    request
):

    try:
        return await shiprocketService.addPickupLocation(
            request
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
async def getChannels(
    self
):

    try:
        return await shiprocketService.getChannels()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


async def getCourierCompanies(
    self
):

    try:
        return await shiprocketService.getCourierCompanies()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
async def getNdrShipments(
    self
):

    try:
        return await shiprocketService.getNdrShipments()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


async def updateNdr(
    self,
    request
):

    try:
        return await shiprocketService.updateNdr(
            request
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )