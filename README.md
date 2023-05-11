# Telegram-parser

## Installation

1. Clone the repository:

```sh
git clone https://github.com/gaponukz/Telegram-parser.git
cd Telegram-parser
```

2. Install pyhton packages
```sh
pip install -r requirements.txt
```

### Configuration

Create a `settings.json` file in the root directory of the project and add the following variables:
```json
{
    "entity_to_parse": "",
    "entity_type": "chat",
    "user_count_limit": 1,
    "account": {
        "session_path": "session",
        "api_id": 0,
        "api_hash": ""
    }
}
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| entity_to_parse | `str` | Chat or channel t.me link or username |
| entity_type | `Literal['chat', 'channel']` | Chat or channel |
| user_count_limit | `int` | Parsed users limit |
| account | `dict` | Telegram API |

## Deployment
To run the app on your local machine, simply execute the server.py file:
```sh
python main.py
```
