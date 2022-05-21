
from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData


import requests


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER], is_trainable=False
)
class MultiNLUComponent(GraphComponent):

    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
    ) -> None:
        self._config = config
        self._name = name
  
    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, execution_context.node_name)


    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        return training_data

    def _get_endpoint(self, lang: Text):
        for ep in self._config['endpoints']:
            if ep['lang'] == lang:
                return ep['endpoint']
  
    def process(self, messages: List[Message]) -> List[Message]:
        
        for m in messages:
            lang = m.data['metadata']["lang"]
            endpoint = self._get_endpoint(lang)
            response = requests.post(url=endpoint, json=m.data)  
            response = response.json()

            m.set("intent", response.get('intent', None), add_to_output=True)
            m.set("intent_ranking", response.get('intent_ranking', None), add_to_output=True)
            m.set("entities", response.get('entities', None), add_to_output=True)
            # m.set("text_tokens", response.get('text_tokens', None), add_to_output=True)
            m.set("response_selector", response.get('response_selector', None), add_to_output=True)

        return messages