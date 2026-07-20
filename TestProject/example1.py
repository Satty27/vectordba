from vectordba import VectorAgent

class TestProject:
    def testing_nlp(self, db_session, analyzed_schemas):
        self.db = db_session
        self.analyzed_schemas = analyzed_schemas


        connection_string = "mongodb+srv://dbuser:alpahbeta123456@arasthoo-dev.egtuvaa.mongodb.net/?retryWrites=true&w=majority&appName=arasthoo-dev"

        vector_agent = VectorAgent(db_session=db_session, analyzed_schemas=analyzed_schemas)
        database_name = "aristotle"

        status = vector_agent.initialize_connection(connection_string=connection_string, database_name=database_name)

        print(status)

        user_coll = vector_agent.analyze_schemas(base_collections=["users", "wallets", "weekly_leaderboard"])
        print(user_coll)

        #Example 1

        target_email = "test_user_8_fischertimothy@gmail.com"

        intent = {
          "intent": {
            "goal": "Find the preferred_language and name of the user where email=target_email",
            "runtime_inputs":[
                {
                    "email":"${target_email}",
                    "datatype": "string"
                }
            ],
            "projection":["name", "preferred_language"]
          }
        }
        query = vector_agent.build_nlp_query(intent=intent, query_identifier=None, retry=False)
        print(query)

        output = vector_agent.run_query_executor(nlp_query=query, target_email=target_email)
        print(output)


if __name__ == "__main__":
    test_project = TestProject()
    test_project.testing_nlp(db_session=None, analyzed_schemas=[])