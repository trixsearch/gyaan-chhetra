from core.mongo import MongoDBClient
from core.audit import create_audit_fields, update_audit_fields

db = MongoDBClient.get_db()
collection = db["books"]


def create_book(data: dict, user_uuid: str):
    book = {
        "title": data["title"],
        "writer": data["writer"],
        "genre": data["genre"],
        "quantity": data["quantity"],
        "available_quantity": data["quantity"],
        **create_audit_fields(user_uuid),
    }
    collection.insert_one(book)
    return book


def update_book(book_uuid: str, data: dict, user_uuid: str):
    update_data = {
        **data,
        **update_audit_fields(user_uuid),
    }
    result = collection.update_one(
        {"uuid": book_uuid},
        {"$set": update_data},
    )
    return result.matched_count > 0


def delete_book(book_uuid: str):
    result = collection.delete_one({"uuid": book_uuid})
    return result.deleted_count > 0


def list_books():
    return list(collection.find({}, {"_id": 0}))