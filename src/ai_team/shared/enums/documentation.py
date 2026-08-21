from enum import StrEnum


class DocumentationType(StrEnum):

    README = "readme"

    ARCHITECTURE = "architecture"

    API = "api"

    DATABASE = "database"

    DEPLOYMENT = "deployment"

    ADR = "adr"

    USER_GUIDE = "user_guide"
