from typing import Any, Text, Dict, List
from pyrsistent import v
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SessionStarted, ActionExecuted, SlotSet


class ActionSessionStartSetMetadata(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        metadata = tracker.get_slot("session_started_metadata")
        return [SessionStarted(), SlotSet("metadata", metadata), ActionExecuted("action_listen")]



class ActionExtractLangFromMetadata(Action):
    def name(self) -> Text:
        return "action_extract_lang_from_metadata"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        print(tracker.slots)

        meta = tracker.latest_message.get('metadata', None)

        if meta:
            lang = tracker.latest_message['metadata'].get('lang', None)
            return [SlotSet("lang", lang)]

        return [SlotSet("lang", None)]


class ActionExtractMetadata(Action):
    def name(self) -> Text:
        return "action_extract_metadata"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        meta = tracker.latest_message.get('metadata', None)
        return [SlotSet("metadata", meta)]


