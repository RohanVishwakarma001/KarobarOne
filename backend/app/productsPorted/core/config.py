# Owner - pradhansaikat123@gmail.com

# Application configuration using Pydantic Settings.
# Manages database credentials, image constraints, and JWT settings.

# Import Pydantic Settings to manage application configuration settings
from pydantic_settings import BaseSettings
# Import List from typing for type annotations
from typing import List
# Import Field from pydantic to define settings metadata and validation aliases
from pydantic import Field

class Settings(BaseSettings):
    databaseUrl: str = Field(
        "postgresql+asyncpg://developer_user_1:PwdKarobarOne%402026@ep-mute-morning-aohy3ymu-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?ssl=require",
        validation_alias="DATABASE_URL"
    )
    secretKey: str = Field("your-secret-key-change-in-production", validation_alias="SECRET_KEY")
    algorithm: str = Field("HS256", validation_alias="ALGORITHM")
    accessTokenExpireMinutes: int = Field(30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    dropboxAccessToken: str = Field(
        "sl.u.AGlNn4tXTZKtbMMih4zEPUIPfG4vF7NvJpQlZkriK938FG3rqDJITzkVDvrXjB1THAsQytEC0HcvOBMPo8IloWCe8fMT1qUgGwTSnMew327jPw73BjmyUTR42JoHVK5lN53ig0G-F-E8BoGUKiqeFt6_aMk-svkAhQyNUTWVrMLKFqvAHp6XrXIyFoCBwL906tl5K2ZPK9n8mmNml6SCpc2RSHj5YpKqhP9vqbxDmWCqEHJjM9lXhtsuTRlX0Ol__wLSMBiYEDQ0kLi6eJeOVSZy1Rqa1xD5Db5_sKlNX27DHgNmTD-NaiEzCoESNOG4_bBANcVQq7WZ3enEdpBv56NYQ8HqL_kBdYq0as9VopFdN7Q1dEoRa2oaBdsozNQoF7FfmcoJx7PWNQO4P0Wap_UxraRhxJoW_vGEQZzDt3V83RZYG2ALvxSek7hTxnCmknS5cuyzTXCX4GTTg3EopHTBijEbXu9zxyF4WvRNl2Nuwj_xV3DVuYLEsGc-LGBErrxjrG8UcVW_6ypR0yWPkThqXnlCqNMtyUNeK2rh5PpSCWLVSIe-OJLy1A8JtI7Q0lDsEAriBgyTHwADMxZ5TNaJYHefDVOVsU1lIJVD3zVA0eHqaYq5szNyOOP8-z8Mlzl9KjhIG2nD_78wLuPGL_NyGsF66WJSwIAa3eQOWnHZhZm9s52OgRvfGvCxmoZ_zcxTXwPLPFMpOhJ5J_4yaQgXrb5awv42XdaEPUOuFBpiy9hk174NOdfqkv-rUXAENqDjSCXXiluB9W4ke3M6Ely1zd6xmAOmVCzdOLYrbWnn7WyqNnPU8TjCQj6YMCjqZUNEgFaIXJtyVhsekhdqD0mbSqnXTF1f4uB3v8lotWc7rEFBJ0JT31rhYC8VGPj6Ox5J3FgGIhKm3aOX3xmv0WeXP-N7oSmuBr7NHkoZH6GWYRk4R6HHAPj-AGC9ubqAvuT_toPNbnPzEl78BiFydmRBWLyStjFfLA_8uPsjMf7r5tJNzLpmDOfPbHONJ7mIo_n-C0viOE2YxiSfSoeCKkYpJqXgicF-NJJreUhExuqLTLmnqn2fWKi1S99M7C6eGaYbJE7yjmRWutGGt87I9Kx2rD6vhTszK_W8tRsoS1itTEdH7S6mNewgXlDSm2ITTIPHLrzc4eUzw7hGvJ-pOvkBj_wOTGfN6qXmBM4tn4l-BkT4EKFdjLe8ew5s7ltSkrb86fIQjD_KfE_Vw5DgFSwEkNe3IBC7Q2LuEFFmsbonTXIcIsL-SDHuPpNrY7MfU8pNbNsjQ5rH6hCLt7RYMoJ_YpG6aSbR3ub-8XH_bQalvDRXKfGg-QO1m6qduD0E-WN-8JqBnclPm_96aZ8B0DL9lpuYfrtSHz5s58RT7dGJwO4CicfQGCoyIW2efdJ1MZ5-APK4K-I1BcxlwTSKHMTbsmsD0TZCUcS-udquXRjNNg",
        validation_alias="DROPBOX_ACCESS_TOKEN"
    )

    # Image upload validations
    maxImagesPerProduct: int = Field(5, validation_alias="MAX_IMAGES_PER_PRODUCT")
    maxImageSizeBytes: int = Field(5242880, validation_alias="MAX_IMAGE_SIZE_BYTES")
    allowedImageTypes: List[str] = Field(
        ["image/jpeg", "image/jpg", "image/png", "image/webp"],
        validation_alias="ALLOWED_IMAGE_TYPES"
    )

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
