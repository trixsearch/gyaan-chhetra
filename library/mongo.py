"""
MongoDB connection and base utilities using PyMongo.
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from django.conf import settings
import logging
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger(__name__)

class MongoDBConnection:
    """
    Singleton MongoDB connection manager.
    """
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance
    
    def _connect(self):
        """Establish MongoDB connection."""
        try:
            self._client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            
            # Test connection
            self._client.admin.command('ping')
            
            self._db = self._client[settings.MONGODB_DB_NAME]
            
            logger.info(f"Connected to MongoDB: {settings.MONGODB_URI}")
            logger.info(f"Database: {settings.MONGODB_DB_NAME}")
            
            # Create indexes on startup
            self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    def _create_indexes(self):
        """Create necessary indexes for collections."""
        try:
            # Books collection indexes
            self._db.books.create_index([("title", ASCENDING)])
            self._db.books.create_index([("writer", ASCENDING)])
            self._db.books.create_index([("genre", ASCENDING)])
            self._db.books.create_index([("uuid", ASCENDING)], unique=True)
            self._db.books.create_index([("is_available", ASCENDING)])
            
            # Issues collection indexes
            self._db.issues.create_index([("borrower_uuid", ASCENDING)])
            self._db.issues.create_index([("book_uuid", ASCENDING)])
            self._db.issues.create_index([("status", ASCENDING)])
            self._db.issues.create_index([("due_date", ASCENDING)])
            self._db.issues.create_index([("uuid", ASCENDING)], unique=True)
            
            # Penalties collection indexes
            self._db.penalties.create_index([("borrower_uuid", ASCENDING)])
            self._db.penalties.create_index([("issue_uuid", ASCENDING)])
            self._db.penalties.create_index([("status", ASCENDING)])
            self._db.penalties.create_index([("uuid", ASCENDING)], unique=True)
            
            # Audit logs collection indexes
            self._db.audit_logs.create_index([("collection", ASCENDING)])
            self._db.audit_logs.create_index([("action", ASCENDING)])
            self._db.audit_logs.create_index([("user_uuid", ASCENDING)])
            self._db.audit_logs.create_index([("timestamp", DESCENDING)])
            
            logger.info("MongoDB indexes created successfully")
            
        except OperationFailure as e:
            logger.error(f"Failed to create indexes: {e}")
    
    @property
    def db(self):
        """Get database instance."""
        if self._db is None:
            self._connect()
        return self._db
    
    @property
    def client(self):
        """Get client instance."""
        if self._client is None:
            self._connect()
        return self._client
    
    def get_collection(self, collection_name):
        """Get a specific collection."""
        return self.db[collection_name]
    
    def close(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

# Singleton instance
mongo_db = MongoDBConnection()

class BaseMongoModel:
    """
    Base class for all MongoDB models with audit fields.
    """
    
    # Collection name must be defined in subclasses
    collection_name = None
    
    @classmethod
    def get_collection(cls):
        """Get the MongoDB collection for this model."""
        if cls.collection_name is None:
            raise ValueError("collection_name must be defined in subclass")
        return mongo_db.get_collection(cls.collection_name)
    
    @staticmethod
    def add_audit_fields(data, user_uuid, is_update=False):
        """
        Add audit fields to document data.
        
        Args:
            data: Document data (dict)
            user_uuid: UUID of the user performing the action
            is_update: Whether this is an update operation
        
        Returns:
            dict: Document data with audit fields
        """
        now = datetime.utcnow()
        
        if not is_update:
            # For new documents
            data['uuid'] = str(uuid4())
            data['created_by'] = user_uuid
            data['updated_by'] = user_uuid
            data['created_at'] = now
            data['updated_at'] = now
        else:
            # For updates, only update updated fields
            data['updated_by'] = user_uuid
            data['updated_at'] = now
        
        return data
    
    @staticmethod
    def add_audit_query(query, user_uuid):
        """
        Add audit fields to update query.
        
        Args:
            query: MongoDB update query
            user_uuid: UUID of the user performing the action
        
        Returns:
            dict: Update query with audit fields
        """
        now = datetime.utcnow()
        
        # Ensure $set exists
        if '$set' not in query:
            query['$set'] = {}
        
        query['$set']['updated_by'] = user_uuid
        query['$set']['updated_at'] = now
        
        return query
    
    @classmethod
    def log_audit(cls, action, document_id, user_uuid, collection, changes=None):
        """
        Log an audit entry.
        
        Args:
            action: Action performed (create, update, delete)
            document_id: ID of the document affected
            user_uuid: UUID of the user performing the action
            collection: Collection name
            changes: Dictionary of changes made (optional)
        """
        audit_log = {
            'uuid': str(uuid4()),
            'action': action,
            'collection': collection,
            'document_id': str(document_id),
            'user_uuid': user_uuid,
            'changes': changes or {},
            'timestamp': datetime.utcnow()
        }
        
        try:
            mongo_db.get_collection('audit_logs').insert_one(audit_log)
        except Exception as e:
            logger.error(f"Failed to log audit entry: {e}")

# Collection names as constants
BOOKS_COLLECTION = 'books'
ISSUES_COLLECTION = 'issues'
PENALTIES_COLLECTION = 'penalties'
AUDIT_LOGS_COLLECTION = 'audit_logs'