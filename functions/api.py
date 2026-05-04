import json
import uuid

# In-memory store — replace with DynamoDB or RDS for persistence
_items: dict[str, dict] = {}


def _response(status: int, body: object) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def get_root(event, context):
    return _response(200, {"message": "python-backend API", "version": "1.0.0"})


def get_items(event, context):
    return _response(200, list(_items.values()))


def get_item(event, context):
    item_id = event["pathParameters"]["id"]
    item = _items.get(item_id)
    if item is None:
        return _response(404, {"error": f"Item {item_id} not found"})
    return _response(200, item)


def create_item(event, context):
    try:
        body = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Invalid JSON body"})

    if "name" not in body:
        return _response(400, {"error": "'name' field is required"})

    item_id = str(uuid.uuid4())
    item = {"id": item_id, "name": body["name"], **{k: v for k, v in body.items() if k != "name"}}
    _items[item_id] = item
    return _response(201, item)


def delete_item(event, context):
    item_id = event["pathParameters"]["id"]
    if item_id not in _items:
        return _response(404, {"error": f"Item {item_id} not found"})
    del _items[item_id]
    return _response(200, {"deleted": item_id})
