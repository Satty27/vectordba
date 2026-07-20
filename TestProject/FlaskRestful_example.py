from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from vectordba import VectorAgent  # Assuming package evolution to VectorDBA

app = Flask(__name__)
api = Api(app)

# 1. Initialize DB and VectorDBA compiler

class AnalyticsQueryEngine(Resource):
    def post(self):
        """
        Expects payload body:

        example 1:
        {
          "intent": {
            "goal": "Find the preferred_language and name of the user where email=test_user_8_fischertimothy@gmail.com",
            "projection":["name", "preferred_language"]
            },
          "collection_name": ["users"]
        }

        example 2:
        {
          "intent": {
            "goal": "Get user balance where email=test_user_8_fischertimothy@gmail.com",
            "projection":["balance"]
            },
          "collection_name": ["wallets"]
        }
        """

        json_data = request.get_json(force=True)
        user_prompt = json_data.get("intent")
        collection_name = json_data.get("collection_name")

        if not user_prompt:
            return {"error": "Missing 'prompt' parameter"}, 400

        if type(collection_name) is not list:
            return {"error": "base collection accept values only in list"}, 400


        try:
            connection_string = "mongodb://localhost:27017"

            vector_agent = VectorAgent(db_session="", analyzed_schemas=[])
            database_name = "test"

            vector_agent.initialize_connection(connection_string=connection_string, database_name=database_name)
            vector_agent.analyze_schemas(base_collections=collection_name)

            query = vector_agent.build_nlp_query(intent=user_prompt, query_identifier=None, retry=False)

            output = vector_agent.run_query_executor(nlp_query=query)

            return {
                "success": True,
                "compiled_pipeline": query,
                "data": output
            }, 200

        except Exception as e:
            return {"error": f"Query generation or execution failed: {str(e)}"}, 500


# 4. Route declaration
api.add_resource(AnalyticsQueryEngine, "/api/v1/nlp_query")

if __name__ == "__main__":
    app.run(debug=True, port=5000)