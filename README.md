# VectorDBA: Agentic MongoDB NLP Database Interface 🤖🍃

[![PyPI version](https://img.shields.io/pypi/v/vectordba.svg)](https://pypi.org/project/vectordba/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**VectorDBA is the Secure AI Data Gateway for Enterprise MongoDB **.
We provide a deterministic middleware layer that enables AI agents and software applications to safely read from MongoDB clusters using natural language.
We provide a deterministic middleware gateway that allows AI agents and applications to safely query MongoDB clusters using plain text—without sacrificing speed, security, or predictability.
By leveraging the reasoning capabilities of `gpt-4o-mini`, VectorDBA instantly translates plain English into precise MongoDB standard queries or complex multi-stage aggregation pipelines—complete with dynamic runtime variables.

Stop building, maintaining, and debugging dozens of rigid, single-purpose CRUD endpoints. Consolidate your data fetching layer into a single, highly flexible, intelligent NLP endpoint.

```mermaid
graph TD
    classDef payload fill:#e2e8f0,stroke:#475569,stroke-width:2px,color:#0f172a,font-weight:bold;
    classDef stage fill:#f8fafc,stroke:#2563eb,stroke-width:2px,color:#1e3a8a;
    classDef output fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d,font-weight:bold;

    Input["📥 User Intent Payload<br>(Natural Language + Base Collections)"]:::payload

    subgraph VectorDBA_Engine ["VectorDBA Open-Source Compilation Engine"]
        S1["<b>1. Prompt-to-Task Decomposition</b><br>• Deconstructs intent into filtering, grouping, & projection targets"]:::stage
        S2["<b>2. Schema Resolver & Type Isolation</b><br>• Validates keys against schema & isolates BSON data types"]:::stage
        S3["<b>3. Relationship-to-Schema Mapping</b><br>• Resolves multi-collection references & constructs $lookup joins"]:::stage
        S4["<b>4. Deterministic Pipeline Construction</b><br>• Enforces optimal stage ordering ($match ➔ $lookup ➔ $group)"]:::stage
        S5["<b>5. BSON Query Generator & Validator</b><br>• Binds dynamic kwargs & compiles executable BSON syntax"]:::stage
    end

    Output[("🚀 Executable MongoDB BSON Query<br>(PyMongo / Motor Driver)")]:::output

    Input --> S1
    S1 --> S2
    S2 --> S3
    S3 --> S4
    S4 --> S5
    S5 --> Output
```
---

## ✨ Features

*   🗣️ **Text-to-NoSQL Translation:** Write complex database requests in plain English. VectorDBA handles the heavy lifting, translating intent into native MongoDB query syntax.
*   🧠 **Agentic Query Planning:** Powered by `gpt-4o-mini`, VectorDBA deeply understands context, deeply nested structures, and relationships to construct highly accurate operations.
*   🔒 **Privacy-First Schema Isolation:** VectorDBA connects to your database, infers the shape of your collections, and caches the structure locally. **Only the schema metadata is sent to the LLM**—your actual database records are never exposed to the agent.
*   ⚡ **Secure Runtime Variables:** Safely inject dynamic inputs into your natural language prompts at runtime, eliminating string-concatenation and prompt-injection vulnerabilities.
*   🛠️ **Complex Aggregations Out-of-the-Box:** Seamlessly generates standard `find()` queries as well as advanced `aggregate()` pipelines (`$lookup`, `$unwind`, `$group`, etc.).
*   🎯 **Single Endpoint Architecture:** Perfect for building AI agents, chatbots, or highly dynamic applications that require flexible, ad-hoc data retrieval without writing code for every new UI view.

---

## 📦 Installation

VectorDBA is available on PyPI. Install it cleanly using `pip`:

```bash
pip install vectordba
```

## ⚙️ Prerequisites

To run VectorDBA, ensure you have:
1. A valid MongoDB Connection String URI.
2. An OpenAI API Key configured in your environment variables (OPENAI_API_KEY).

## 🚀 Quick Start
Here is how easily you can initialize VectorDBA, map your schema, and execute a natural language query with dynamic runtime bindings:


### ⚡ How Runtime Variables Work (`**kwargs` Resolution)

To prevent string-concatenation vulnerabilities and prompt injection, VectorDBA uses a strict declarative variable binding system. When you define an intent, you declare placeholders using the `${variable_name}` syntax. 

When executing the query via `run_query_executor`, you must pass these exact variables as Python keyword arguments (`**kwargs`).

### The Golden Rule of Mappings
The variable key identifier defined inside your **`runtime_inputs` object template** must match the **Python parameter key** exactly. 

| Location | Key Syntax                                                     | Example |
| :--- |:---------------------------------------------------------------| :--- |
| **1. Inside Intent JSON:** | `"runtime_inputs": [{"email": "${target_email}"}]`             | Uses `${target_email}` placeholder |
| **2. Inside `run_query_executor`:** | `vector_agent.run_query_executor(plan, target_email=variable)` | `target_email=target_email` |

---

### Detailed Breakdown Example

Here is exactly how the mapping connects from your JSON definition to execution:

```Python
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
```

## 🏗️ How It Works

```mermaid
graph TD
    %% Styling and Color Palettes (Enterprise Vibe)
    classDef client fill:#eef2f7,stroke:#3b82f6,stroke-width:2px,color:#1e3a8a;
    classDef engine fill:#eff6ff,stroke:#2563eb,stroke-width:2px,color:#1e40af,font-weight:bold;
    classDef security fill:#fff1f2,stroke:#f43f5e,stroke-width:2px,color:#9f1239;
    classDef database fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#14532d;
    classDef structural fill:#fafafa,stroke:#71717a,stroke-width:1px,color:#27272a;

    %% 1. Ingestion Layer
    subgraph Client_Layer ["Application Interface"]
        API_Call["POST /api/v1/nlp_query<br>(Payload: Intent + Base Collections)"]:::client
    end

    %% 2. Orchestration Layer
    subgraph VectorDBA_Engine ["VectorDBA Agent Engine Core"]
        Init["VectorAgent Initialization<br>(Target Database Setup)"]:::engine
        SchemaAnalzer["vector_agent.analyze_schemas()<br>(Extracts Schemas)"]:::engine
        Builder["vector_agent.build_nlp_query()<br>(Deterministic Query Construction)"]:::engine
    end

    %% 3. Security & Validation Layer
    subgraph Security_Guardrails ["Enterprise Safety Controls"]
        IntentRouter{"Intent Routing<br>& Field Validation"}:::security
        Sanitize{"Injection Scanning<br>& Operator Isolation"}:::security
    end

    %% 4. Data Execution Target
    subgraph Infrastructure ["Enterprise Storage Target"]
        MongoCluster[("NoSQL Cluster<br>(MongoDB)")]:::database
    end

    %% Data Pipeline Connections Flow
    API_Call -->|1. Transmit Payload| Init
    Init -->|2. Scrape Structure Constraints| SchemaAnalzer
    SchemaAnalzer -->|3. Establish Pipeline Context Boundaries| Builder
    
    
    Builder -->|4. Inspect Fields Against Schema| IntentRouter
    IntentRouter -->|Passed: Valid Fields| Sanitize
    IntentRouter -.->|Failed: Reject Intent| API_Call
    
    Sanitize -->|5. Compile Secure BSON Native Pipeline| MongoCluster
    
    MongoCluster -->|6. Standard Isolated Output Cursor| API_Call

    %% Apply Styles to classes
    class Builder,SchemaAnalzer,Init engine;
  
```

## 📖 Supported Operations

VectorDBA features a strict read-only routing engine. It translates natural language exclusively into data-fetching operations, ensuring your production data remains completely safe from AI hallucinations or unauthorized modifications.

| Operation | Status | Capabilities | Natural Language Example | Generated Native Syntax |
| :--- | :--- | :--- | :--- | :--- |
| **`find()`** | ✅ Supported | Standard filtering, sorting, limits, and explicit field projections. | *"Find active users registered after 2025, sorted by latest."* | `{ "status": "active", "reg_date": { "$gt": "2025-01-01" } }` |
| **`aggregate()`** | ✅ Supported | Multi-stage transformations, relational joins, unwinding arrays, and grouping. | *"Join weekly leaderboards with user wallets and get top 10 scores."* | `[{ "$lookup": {...} }, { "$unwind": ... }, { "$sort": ... }]` |
| **`insert()`** | ❌ Blocked | Prevent dynamic data insertion via the NLP endpoint. | *"Add a new user to the database..."* | **Operation Denied** (Read-Only Guardrail) |
| **`update() / delete()`** | ❌ Blocked | Prevent unauthorized mutations, bulk updates, or accidental collections drops. | *"Delete all users who haven't logged in..."* | **Operation Denied** (Read-Only Guardrail) |

### 🔒 The Read-Only Safety Guarantee
> **Security Note:** Write operations are intentionally restricted at the core library layer. Even if an LLM structure attempts to formulate a mutation pipeline, VectorDBA's execution engine will intercept and reject the command before it ever hits your MongoDB driver. This makes it completely safe for exposed API endpoints.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! If you'd like to extend support for custom database engines, optimize pipeline construction routing, or suggest features, feel free to open a pull request or check the Issues Page.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


[//]: # (# **VectorDBA**: Advanced Natural Language Database Interface 🤖🍃 )

[//]: # (## Build exclusively for MongoDB development)

[//]: # (VectorDBA &#40;Advanced Natural Language Database Interface&#41; is an agentic Python library that transforms your MongoDB database into a natural language interface. By leveraging the reasoning capabilities of gpt-4o-mini, VectorDBA allows you to generate and execute complex MongoDB queries—including dynamic runtime variables—using plain English.)

[//]: # ()
[//]: # (Instead of writing rigid CRUD endpoints, consolidate your data fetching into a single, intelligent NLP endpoint.)

[//]: # ()
[//]: # ()
[//]: # (## ✨ Features)

[//]: # ()
[//]: # (* 🗣️ Natural Language to NoSQL: Write your database queries in plain English. VectorDBA translates your intent into precise MongoDB syntax.)

[//]: # (* 🧠 Agentic Solution: Powered by gpt-4o-mini, VectorDBA understands context and constructs highly accurate database operations.)

[//]: # (* 🔒 Privacy-First Schema Management: VectorDBA connects via your MongoDB URI, infers the collection schema, and caches it locally. Only the schema structure is shared with the LLM—your actual database records are never exposed to the agent.)

[//]: # (* ⚡ Runtime Variables: Safely inject dynamic variables into your natural language prompts at runtime without string-concatenation vulnerabilities.)

[//]: # (* 🛠️ Advanced Operations: Currently supports standard find queries and complex aggregate pipelines out of the box.)

[//]: # (* 🎯 Single Endpoint Architecture: Replace dozens of rigid REST API routes with a single, flexible natural language data-fetching endpoint.)

[//]: # ()
[//]: # (## 📦 Installation)

[//]: # (Available on PyPI. Install VectorDBA using pip: )

[//]: # ()
[//]: # (pip install VectorDBA-ai)

[//]: # ()
[//]: # (## ⚙️ Prerequisites)

[//]: # (To use VectorDBA, you will need:)

[//]: # (1. A valid MongoDB Connection String URL. &#40;check TestProject&#41;)

[//]: # (2. An OpenAI API Key &#40;with access to the gpt-4o-mini model&#41;. Configure in .env &#40;check TestProject&#41;)

[//]: # ()
[//]: # (## 🚀 Quick Start)

[//]: # (Here is a basic example of how to initialize VectorDBA and run a natural language query against your database.)

[//]: # (Refers test directory)

[//]: # ()
[//]: # (`class TestProject:)

[//]: # ()
[//]: # (    def testing_nlp&#40;self&#41;:)

[//]: # (        self.db = db_session)

[//]: # (        self.analyzed_schemas = analyzed_schemas)

[//]: # ()
[//]: # (        connection_string = Connection.get_connection&#40;&#41;)

[//]: # (        print&#40;connection_string&#41;)

[//]: # ()
[//]: # (        VectorDBA_instance = VectorDBA&#40;db_session=db_session, analyzed_schemas=analyzed_schemas&#41;)

[//]: # (        database_name = "aristotle")

[//]: # ()
[//]: # (        status = VectorDBA_instance.initialize_connection&#40;connection_string=connection_string, database_name=database_name&#41;)

[//]: # ()
[//]: # (        print&#40;status&#41;)

[//]: # ()
[//]: # (        user_coll = VectorDBA_instance.analyze_schemas&#40;base_collections=["users", "wallets", "weekly_leaderboard"]&#41;)

[//]: # (        print&#40;user_coll&#41;)

[//]: # (        email = "test_user_8_fischertimothy@gmail.com")

[//]: # ()
[//]: # (        intent = {)

[//]: # (          "intent": {)

[//]: # (            "goal": "Find preferred_language of user where email=email",)

[//]: # (            "runtime_inputs":[)

[//]: # (                {)

[//]: # (                    "email":"${email}",)

[//]: # (                    "datatype": "string")

[//]: # (                })

[//]: # (            ],)

[//]: # (            "projection":["name", "preferred_language"])

[//]: # (          })

[//]: # (        })

[//]: # (        query = VectorDBA_instance.build_nlp_query&#40;intent, query_identifier=None, retry=False&#41;)

[//]: # (        print&#40;query&#41;)

[//]: # ()
[//]: # (        query_output = VectorDBA_instance.run_query_executor&#40;query, email=email&#41;)

[//]: # (        print&#40;query_output&#41;)

[//]: # ()
[//]: # (if __name__ == "__main__":)

[//]: # (    test_project = TestProject&#40;&#41;)

[//]: # (    test_project.testing_nlp&#40;db_session=None, analyzed_schemas=[]&#41;)

[//]: # (`)

[//]: # ()
[//]: # (## 🏗️ How It Works)

[//]: # (1. Schema Extraction & Caching: When you connect VectorDBA to your MongoDB instance, it scans the specified collections to map out the document structures, data types, and nested fields. This schema is saved locally &#40;e.g., in a .VectorDBA_schema.json file&#41;.)

[//]: # (2. Prompt Construction: When a query is initiated, VectorDBA feeds your natural language prompt, the mapped variables, and the locally cached schema to gpt-4o-mini.)

[//]: # (3. Agentic Translation: The LLM generates the exact MongoDB find dictionary or aggregate pipeline required to satisfy the request.)

[//]: # (4. Execution: VectorDBA securely executes the generated query against your MongoDB database and returns the raw Python dictionaries.)

[//]: # ()
[//]: # (## 📖 Supported Operations)

[//]: # (VectorDBA's LLM routing engine currently supports the generation and execution of:)

[//]: # (* find&#40;&#41;: For standard filtering, sorting, and projection operations.)

[//]: # (* aggregate&#40;&#41;: For complex data transformations, grouping, unwinding, and multi-stage pipelines.)

[//]: # ()
[//]: # (&#40;Note: Write operations like insert, update, and delete are intentionally restricted in this version to ensure read-only safety for data-fetching endpoints&#41;.)

[//]: # ()
[//]: # (## 🤝 Contributing)

[//]: # (Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.)

[//]: # ()
[//]: # (## 📄 License)

[//]: # (This project is licensed under the MIT License - see the LICENSE file for details.)