from django.db import models
import uuid
from datetime import datetime
from bson import ObjectId

class BaseModel:
    """
    Base model for all MongoDB collections.
    """
    
    def __init__(self, collection):
        self.collection = collection
    
    def insert(self, data, user_uuid):
        """
        Insert a document with audit fields.
        """
        now = datetime.utcnow()
        document = {
            '_id': ObjectId(),
            'uuid': str(uuid.uuid4()),
            'created_by': user_uuid,
            'updated_by': user_uuid,
            'created_at': now,
            'updated_at': now,
            **data
        }
        result = self.collection.insert_one(document)
        return self.collection.find_one({'_id': result.inserted_id})
    
    def update(self, query, data, user_uuid):
        """
        Update a document and set updated_at and updated_by.
        """
        now = datetime.utcnow()
        data['updated_at'] = now
        data['updated_by'] = user_uuid
        result = self.collection.update_one(query, {'$set': data})
        return result
    
    def delete(self, query):
        """
        Delete a document.
        """
        result = self.collection.delete_one(query)
        return result
    
    def find_one(self, query):
        """
        Find a single document.
        """
        return self.collection.find_one(query)
    
    def find(self, query, sort=None, skip=0, limit=0):
        """
        Find multiple documents with optional sorting and pagination.
        """
        cursor = self.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        if limit:
            cursor = cursor.limit(limit)
        return list(cursor)
    
    def count(self, query):
        """
        Count documents.
        """
        return self.collection.count_documents(query)