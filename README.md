
## Install

```bash
pip install rasa_addons
```

## Reference

### Actions

|class|name|description|
|---|---|---|
|rasa_addons.actions.ActionSessionStartSetMetadata|action_session_start|Set metadata in slot "metadata" on each __session start__|
|rasa_addons.actions.ActionExtractMetadata|action_extract_metadata|Set metadata in slot "metadata" on each __user turn__|
|rasa_addons.actions.ActionExtractLangFromMetadata|action_extract_lang_from_metadata|Set slot "lang" from metadata on each __user turn__|

### Pipeline components

|class|description|
|---|---|
|rasa_addons.components.MultiNLUComponent|Call a external Rasa NLU based on "lang" field in metadata|

### Connectors

|class|description|
|---|---|
|rasa_addons.connectors.RestInputWithMetadata|Connector for rest channel without ignoring metadata|


### Brokers

|class|description|
|---|---|
|rasa_addons.brokers.LoggerEventBroker|Logs all events in json format in file|


#### rasa_addons.brokers.LoggerEventBroker

|parameter|description|
|---|---|
|type|class path|
|name|logger name|
|path|file path where rasa send events|
|nb_file|maximum number of files for logger rotation|

Above a example:

```yaml
event_broker:
  type: rasa_addons.brokers.LoggerEventBroker
  name: rasa_event
  path: "./log/rasa.log"
  nb_file: 10
```


## Example

Below an example for chatbot using nlu and answers depending on the language.

In your config file:

```yaml
pipeline:
  - name: rasa_addons.components.MultiNLUComponent
    endpoints:
      - lang: fr
        endpoint: "http://localhost:5001/model/parse"
      - lang: en
        endpoint: "http://localhost:5002/model/parse"
```


In your credentials file replace "rest:" by "rasa_addons.connectors.RestInputMetadata:"

```yaml
# rest:
rasa_addons.connectors.RestInputMetadata:
```

In yours fronts and requests, you must to add a metadata field with a dict value containing a lang field :
```json
{
  "sender": "test_user",
  "message": "Salut!",
  "metadata": {"lang": "fr"}
}
```
If you want to send a response depending on the language, add the line if below in your action.py :
```python
from rasa_addons.actions import ActionExtractLangFromMetadata
```

```yaml
slots:
  # ... other slots ...
  lang:
    type: text
    influence_conversation: false
    mappings:
    - type: custom
      action: action_extract_lang_from_metadata


responses:
  # ... other responses ...
  utter_greet:
  - text: "Hey! How are you?"
    condition:
      - type: slot
        name: lang
        value: en
  - text: "Hey! Comment vas-tu?"
    condition:
      - type: slot
        name: lang
        value: fr
```