from pymongo import errors
import re
from typing import Any, Dict, List, Tuple, Set, Union

# 1. Compile the regex pattern globally for significant performance gains during recursion
_PLACEHOLDER_PATTERN = re.compile(r'\${(.*?)}')


def resolve_placeholders(target: Any, strict: bool = False, **kwargs: Any) -> Any:
    """
    Recursively scans data structures and replaces ${key} placeholders with kwargs.

    Args:
        target: The data structure (str, dict, list, tuple, set) to process.
        strict: If True, raises a KeyError when a placeholder is missing from kwargs.
                If False, leaves the unresolved placeholder intact.
        **kwargs: The variables to substitute into the placeholders.

    Returns:
        A new data structure with resolved placeholders.
    """
    # Base Case 1: Strings (Where the actual replacement happens)
    if isinstance(target, str):
        # Scenario A: Exact match (e.g. target == "${user_id}").
        # We do this to preserve native data types like int, bool, or dict from kwargs.
        exact_match = _PLACEHOLDER_PATTERN.fullmatch(target)
        if exact_match:
            var_name = exact_match.group(1)
            if strict and var_name not in kwargs:
                raise KeyError(f"Missing placeholder variable: '{var_name}'")
            return kwargs.get(var_name, target)

        # Scenario B: Inline match (e.g. target == "Hello ${name}!").
        # Everything becomes a string here.
        def replace_match(match: re.Match) -> str:
            var_name = match.group(1)
            if strict and var_name not in kwargs:
                raise KeyError(f"Missing placeholder variable: '{var_name}'")
            # Convert the injected value to string, or keep original placeholder if not strict
            return str(kwargs.get(var_name, match.group(0)))

        return _PLACEHOLDER_PATTERN.sub(replace_match, target)

    # Base Case 2: Dictionaries (Resolves both keys AND values)
    elif isinstance(target, dict):
        return {
            resolve_placeholders(k, strict, **kwargs): resolve_placeholders(v, strict, **kwargs)
            for k, v in target.items()
        }

    # Base Case 3: Iterables (Lists, Tuples, Sets)
    elif isinstance(target, list):
        return [resolve_placeholders(item, strict, **kwargs) for item in target]

    elif isinstance(target, tuple):
        return tuple(resolve_placeholders(item, strict, **kwargs) for item in target)

    elif isinstance(target, set):
        return {resolve_placeholders(item, strict, **kwargs) for item in target}

    # Base Case 4: Primitives (int, float, bool, None) - Return as-is
    return target



class ExecuteQuery:
    @classmethod
    def execute_query(cls, db_session, nlp_query, **kwargs):
        try:
            print("####### EXECUTING QUERY #######")
            operation = nlp_query.get("operation")
            collection = nlp_query.get("collection")


            if operation == "updateOne" or operation == "updateMany":
                query = nlp_query.get("query")
                update_query = nlp_query.get("update")

                query = resolve_placeholders(query, **kwargs)
                update_query = resolve_placeholders(update_query, **kwargs)


                try:
                    coll = db_session.get_collection(collection)
                    result = coll.update_one(query, update_query)
                    if result.acknowledged:
                        if result.matched_count == 0:
                            ret_json = {
                                "operation": operation,
                                "collection": collection,
                                'status': 'success',
                                "message": "no documents found: matched_count = 0",
                            }
                            return ret_json

                        ret_json = {
                            "operation": operation,
                            "collection": collection,
                            'status': 'success',
                            "message": "modified records: " + result.modified_records,
                        }
                        return ret_json

                except errors.DuplicateKeyError as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Duplicate key error: " + str(err),
                    }
                    return ret_json
                except errors.ConnectionFailure as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Failed to establish a connection:  " + str(err),
                    }
                    return ret_json
                except errors.PyMongoError as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Pymongo error:  " + str(err),
                    }
                    return ret_json

            if operation == "find":
                try:
                    query = nlp_query.get("query")
                    print("---unresolved query args---")
                    print(query)
                    print("---resolved query args---")
                    query = resolve_placeholders(query, strict=True ,**kwargs)
                    print(query)

                    projection = nlp_query.get("projection")
                    coll = db_session.get_collection(collection)
                    documents = coll.find(query, projection)

                    return list(documents)

                except errors.OperationFailure as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Failed to perform the operation:  " + str(err),
                    }
                    return ret_json
                except errors.ConnectionFailure as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Failed to establish a connection:  " + str(err),
                    }
                    return ret_json
                except errors.PyMongoError as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Pymongo error:  " + str(err),
                    }
                    return ret_json

            if operation == "aggregate":
                try:
                    pipeline = nlp_query.get("pipeline")
                    pipeline = resolve_placeholders(pipeline, **kwargs)

                    coll = db_session.get_collection(collection)
                    documents = coll.aggregate(pipeline)
                    return list(documents)

                except errors.OperationFailure as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Failed to perform the operation:  " + str(err),
                    }
                    return ret_json
                except errors.ConnectionFailure as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Failed to establish a connection:  " + str(err),
                    }
                    return ret_json
                except errors.PyMongoError as err:
                    ret_json = {
                        "operation": operation,
                        "collection": collection,
                        'status': 'error',
                        "message": "Pymongo error:  " + str(err),
                    }
                    return ret_json

        except Exception as e:
            print("failed to execute nlp query " + str(e))
            return None