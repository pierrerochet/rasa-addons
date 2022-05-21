
from typing import Text

from rasa.core.channels import RestInput
from sanic.request import Request


class RestInputWithMetadata(RestInput):
    def name(self) -> str:
        """Name of your custom channel."""
        return "rest"

    def get_metadata(self, req: Request) -> Text:
        return req.json.get("metadata", None)
