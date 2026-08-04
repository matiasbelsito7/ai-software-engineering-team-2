
from enum import StrEnum

class SourceType(StrEnum):

    FILE = "file"

    MARKDOWN = "markdown"

    PDF = "pdf"

    PYTHON = "python"

    GIT = "git"

    HTTP = "http"

    REPOSITORY = "repository"