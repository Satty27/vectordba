from .db_init import Connection
from .schema_analyzer import SchemaAnalyzer
from .premium.agents import NlPAgent
from .query_executor import ExecuteQuery


class VectorAgent:
    def __init__(self, db_session:str, analyzed_schemas: list):
        self.db = db_session
        self.analyzed_schemas = analyzed_schemas



    def initialize_connection(self,connection_string: str, database_name:str):
        try:
            db = Connection.initialize_database(connection_string, database_name)
            #if not db.result:
            self.db = db
            print("initialized connection")
            return {"result": "success", "message":"initialized connection" }
        except Exception as e:
            # Write proper database exception if connectivity fails
            print("database connection initialization failed " + str(e))
            return {"result": "failed", "error": str(e)}

    def analyze_schemas(self, base_collections, query_identifier=None, sample_size=None):
        try:
            schema_analysis = SchemaAnalyzer.analyze_schemas(self.db, base_collections, query_identifier, sample_size)
            if not schema_analysis:
                raise Exception

            self.analyzed_schemas = schema_analysis
            print("schema analysis completed")
            return {"result": "success", "message":"schema analyzed successfully" }
        except Exception as e:
            print("failed to analyze schema " + str(e))
            return {"result": "failed", "error": str(e)}


    def build_nlp_query(self, intent, query_identifier=None, retry=False):
        try:
            nlp_agent = NlPAgent()
            nlp_query = nlp_agent.brain_agent(self.analyzed_schemas, intent, query_identifier, retry)
            return nlp_query
        except Exception as e:
            print("failed to run nlp query " + str(e))
            return {"result": "failed", "error": str(e) }


    def run_query_executor(self, nlp_query, **kwargs):
        try:
            query_executor = ExecuteQuery()
            query_output = query_executor.execute_query(self.db, nlp_query, **kwargs)
            return query_output
        except Exception as e:
            print("failed to run nlp query " + str(e))
            return {"result": "failed", "error": str(e) }

    def run_nlp_query(self, intent, query_identifier=None, retry=False, **kwargs):
        try:
            nlp_agent = NlPAgent()
            nlp_query = nlp_agent.brain_agent(self.analyzed_schemas, intent, query_identifier, retry)

            query_executor = ExecuteQuery()
            query_output = query_executor.execute_query(self.db, nlp_query, **kwargs)
            return query_output
        except Exception as e:
            print("failed to run nlp query " + str(e))
            return {"result": "failed", "error": str(e) }
