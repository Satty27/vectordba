import logging
import os
import json
from pymongo import errors


def update_schema(db_session, coll, sample_size=None):

    DEFAULT_SAMPLE_SIZE = 10

    if sample_size is None or sample_size == "":
        sample_size = DEFAULT_SAMPLE_SIZE

    collection = db_session.get_collection(coll)

    print("####### Establish DB Connection ##########")
    try:
        # Comprehensive mapping of Python/BSON types to standard string names
        TYPE_MAPPING = {
            # Native Python types
            "str": "string",
            "int": "integer",
            "float": "double",
            "bool": "boolean",
            "dict": "object",
            "list": "array",
            "NoneType": "null",
            "bytes": "binData",
            "datetime": "date",

            # MongoDB/BSON specific types
            "ObjectId": "objectId",
            "Int64": "long",
            "Decimal128": "decimal",
            "Timestamp": "timestamp",
            "Regex": "regex",
            "Code": "javascript",
            "MinKey": "minKey",
            "MaxKey": "maxKey"
        }

        cursor = None
        try:
            cursor = collection.find().limit(sample_size)
        except errors.OperationFailure as err:
            ret_json = {
                'status': 'error',
                "message": "Failed to perform the operation:  " + str(err),
            }
            return ret_json
        except errors.ConnectionFailure as err:
            ret_json = {
                'status': 'error',
                "message": "Failed to establish a connection:  " + str(err),
            }
            return ret_json
        except errors.PyMongoError as err:
            ret_json = {
                'status': 'error',
                "message": "Pymongo error:  " + str(err),
            }
            return ret_json

        fields_schema = {}
        indexes = []

        for doc in cursor:
            for key, value in doc.items():
                if key == "_id":
                    continue

                raw_type = type(value).__name__
                mapped_type = TYPE_MAPPING.get(raw_type, "string")

                if key not in fields_schema:
                    fields_schema[key] = {
                        "type": mapped_type,
                        "allowed_filter": True,
                        "allowed_output": True,
                    }

            try:
                index_info = collection.index_information()
                for index_name, details in index_info.items():
                    if index_name != "_id_":
                        for key_field, _ in details["key"]:
                            if key_field not in indexes:
                                indexes.append(key_field)
            except Exception as e:
                print(f"Exception while fetching indexes: {e}")

        ret_json ={
                "collection": {
                    coll: {
                        "fields": fields_schema,
                        "indexes": indexes
                    }
                }
            }
        return ret_json
    except Exception as e:
        print(f"[WARNING] Could not check validator: {e}")


class SchemaAnalyzer:
    @staticmethod
    def analyze_schemas(db_session, base_collections, query_identifier, sample_size=None):
        try:
            # 1. Initialize schema_cache.json with an empty list if it doesn't exist
            CACHE_FILE = "schema_cache.json"
            if not os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "w") as file_writer:
                    json.dump([], file_writer)

            # 2. Load the entire schema cache into memory ONCE
            with open(CACHE_FILE, "r") as file:
                try:
                    schema_object = json.load(file)
                    if schema_object is None:
                        schema_object = []
                except json.JSONDecodeError:
                    schema_object = []  # Fallback if the file is empty/corrupted

            base_collection_schema = []
            cache_updated = False  # Track if we actually need to rewrite the file later

            # 3. Process your collections using the in-memory cache
            for coll in base_collections:
                found = False

                # Search for the collection in our current cache
                for schema in schema_object:
                    collection = schema.get("collection")

                    if isinstance(collection, dict) and coll in collection:
                        base_collection_schema.append(collection)
                        found = True
                        break  # Found it, stop looking for this specific 'coll'

                # 4. If not found in cache, fetch it dynamically
                if not found:
                    updated_schema = update_schema(db_session, coll, sample_size)

                    # Ensure updated_schema fits your expected list-of-dicts structure:
                    # e.g., [{"collection": { "coll_name": {...} }}]
                    schema_object.append(updated_schema)

                    # Pull the collection dict out to append to your final results list
                    if isinstance(updated_schema, dict):
                        base_collection_schema.append(updated_schema.get("collection", updated_schema))
                    else:
                        base_collection_schema.append(updated_schema)

                    cache_updated = True  # Flag that the cache has changed

            # 5. Save the updated cache back to the file ONCE (only if changes were made)
            if cache_updated:
                with open(CACHE_FILE, "w") as file_writer:
                    json.dump(schema_object, file_writer, indent=4)

            return base_collection_schema
        except Exception as e:
            logging.critical(f"[WARNING] Could not load schema_cache.json: {e}")
            return False