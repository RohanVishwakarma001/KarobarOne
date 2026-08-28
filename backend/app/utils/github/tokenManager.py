from datetime import datetime, timedelta

shiprocketToken = None
tokenExpiry = None


def getToken():

    global shiprocketToken
    global tokenExpiry

    if (
        shiprocketToken is None
        or tokenExpiry is None
    ):
        return None

    if datetime.utcnow() >= tokenExpiry:

        clearToken()

        return None

    return shiprocketToken


def setToken(
    token: str,
    expiryHours: int = 240
):

    global shiprocketToken
    global tokenExpiry

    shiprocketToken = token

    tokenExpiry = (
        datetime.utcnow()
        + timedelta(hours=expiryHours)
    )


def clearToken():

    global shiprocketToken
    global tokenExpiry

    shiprocketToken = None
    tokenExpiry = None