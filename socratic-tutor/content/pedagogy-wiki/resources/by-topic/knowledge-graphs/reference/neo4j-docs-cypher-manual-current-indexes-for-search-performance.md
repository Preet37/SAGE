# Source: https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/
# Title: Neo4j Cypher Manual — Indexes for search performance
# Fetched via: jina
# Date: 2026-04-09

Title: Search-performance indexes - Cypher Manual


# Search-performance indexes - Cypher Manual

This website uses cookies

We use cookies to offer you a better browsing experience, analyze site traffic, personalize content and serve targeted ads. Learn about how we use cookies and how you can control them in [Cookie Settings](https://neo4j.com/neo4j-cookie-and-tracking-policy/). By using our site. you consent to our use of cookies.

[Accept Cookies](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/#)[Use necessary cookies only](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/#)


[Docs](https://neo4j.com/docs/)

Neo4j DBMS
*   [Getting Started](https://neo4j.com/docs/getting-started/current/)
*   [Operations](https://neo4j.com/docs/operations-manual/current/)
*   [Migration and Upgrade](https://neo4j.com/docs/migration-guide/current/)
*   [Status Codes](https://neo4j.com/docs/status-codes/current/)
*   [Java Reference](https://neo4j.com/docs/java-reference/current/)
*   [Kerberos Add-on](https://neo4j.com/docs/kerberos-add-on/current/)

[Neo4j Aura](https://neo4j.com/docs/aura/)

Neo4j Tools
*   [Neo4j Bloom](https://neo4j.com/docs/bloom-user-guide/current/)
*   [Neo4j Browser](https://neo4j.com/docs/browser/)
*   [Neo4j Data Importer](https://neo4j.com/docs/data-importer/current/)
*   [Neo4j Desktop](https://neo4j.com/docs/desktop-manual/current/)
*   [Neo4j Ops Manager](https://neo4j.com/docs/ops-manager/current/)
*   [Neodash commercial](https://neo4j.com/docs/neodash-commercial/current/)

Neo4j Graph Data Science
*   [Neo4j Graph Data Science Library](https://neo4j.com/docs/graph-data-science/current/)
*   [Neo4j Graph Data Science Client](https://neo4j.com/docs/graph-data-science-client/current/)

Cypher Query Language
*   [Cypher](https://neo4j.com/docs/cypher-manual/current/)
*   [Cypher Cheat Sheet](https://neo4j.com/docs/cypher-cheat-sheet/current/)
*   [APOC Library](https://neo4j.com/docs/apoc/current/)

Generative AI
*   [Neo4j GraphRAG for Python](https://neo4j.com/docs/neo4j-graphrag-python/current/)
*   [Embeddings and vector indexes tutorial](https://neo4j.com/docs/genai/tutorials/embeddings-vector-indexes/)
*   [GenAI integrations](https://neo4j.com/docs/cypher-manual/current/genai-integrations/)
*   [Vector search indexes](https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/)
*   [Vector search functions](https://neo4j.com/docs/cypher-manual/current/functions/vector/)
*   [GraphQL vector index search documentation](https://neo4j.com/docs/graphql/5/directives/indexes-and-constraints/#_vector_index_search)

Create applications
*   [Python Driver](https://neo4j.com/docs/python-manual/current/)
*   [Go Driver](https://neo4j.com/docs/go-manual/current/)
*   [Java Driver](https://neo4j.com/docs/java-manual/current/)
*   [JDBC Driver](https://neo4j.com/docs/jdbc-manual/current/)
*   [JavaScript Driver](https://neo4j.com/docs/javascript-manual/current/)
*   [.Net Driver](https://neo4j.com/docs/dotnet-manual/current/)
*   [Neo4j GraphQL Library](https://neo4j.com/docs/graphql-manual/current/)
*   [Neo4j Visualization Library](https://neo4j.com/docs/nvl/current/)
*   [OGM Library](https://neo4j.com/docs/ogm-manual/current/)
*   [Spring Data Neo4j](https://docs.spring.io/spring-data/neo4j/docs/current/reference/html/#reference)
*   [HTTP API](https://neo4j.com/docs/http-api/current/)
*   [Neo4j Query API](https://neo4j.com/docs/query-api/current/)
*   [Bolt](https://neo4j.com/docs/bolt/current/)

Connect data sources
*   [Neo4j Connector for Apache Spark](https://neo4j.com/docs/spark/current/)
*   [Neo4j Connector for Apache Kafka](https://neo4j.com/docs/kafka/)
*   [Change Data Capture (CDC)](https://neo4j.com/docs/cdc/)
*   [BigQuery to Neo4j](https://neo4j.com/docs/dataflow-bigquery/)
*   [Google Cloud to Neo4j](https://neo4j.com/docs/dataflow-google-cloud/)

[Labs](https://neo4j.com/labs/)

[GenAI Ecosystem](https://neo4j.com/labs/genai-ecosystem/)
*   [LLM Knowledge Graph Builder](https://neo4j.com/labs/genai-ecosystem/llm-graph-builder/)
*   [Vector Index & Search](https://neo4j.com/labs/genai-ecosystem/vector-search/)
*   [LangChain](https://neo4j.com/labs/genai-ecosystem/langchain/)
*   [LangChain.js](https://neo4j.com/labs/genai-ecosystem/langchain-js/)
*   [LlamaIndex](https://neo4j.com/labs/genai-ecosystem/llamaindex/)
*   [Haystack](https://neo4j.com/labs/genai-ecosystem/haystack/)
*   [DSPy](https://neo4j.com/labs/genai-ecosystem/dspy/)

**Developer Tools**
*   [APOC Extended](https://neo4j.com/labs/apoc/)
*   [Aura CLI](https://neo4j.com/labs/aura-cli/)
*   [arrows.app](https://neo4j.com/labs/arrows/)
*   [Cypher Workbench](https://neo4j.com/labs/cypher-workbench/)
*   [ETL Tool](https://neo4j.com/labs/etl-tool/)
*   [NeoDash](https://neo4j.com/labs/neodash/)

**Frameworks & Integrations**
*   [Needle Starter Kit](https://neo4j.com/labs/neo4j-needle-starterkit/)
*   [Neo4j Plugin for Liquibase](https://neo4j.com/labs/liquibase/)
*   [Neo4j Migrations](https://neo4j.com/labs/neo4j-migrations/)
*   [neomodel](https://neo4j.com/labs/neomodel/)

[RDF & Linked Data](https://neo4j.com/labs/neosemantics/)
*   [Neosemantics (Java)](https://neo4j.com/labs/neosemantics/)
*   [RDFLib-Neo4j (Python)](https://neo4j.com/labs/rdflib-neo4j/)

[Get Help](https://neo4j.com/developer/resources/)

[Community Forum](https://dev.neo4j.com/forum)

[Discord Chat](https://dev.neo4j.com/chat)

[Product Support](http://support.neo4j.com/)

[Neo4j Developer Blog](https://neo4j.com/blog/developer/)

[Neo4j Videos](https://neo4j.com/videos/)

[GraphAcademy](https://graphacademy.neo4j.com/?ref=docs-nav)

[Beginners Courses](https://graphacademy.neo4j.com/categories/beginners/?ref=docs-nav)
*   [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/?ref=docs-nav)
*   [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/?ref=docs-nav)
*   [Importing Data Fundamentals](https://graphacademy.neo4j.com/courses/importing-fundamentals/?ref=docs-nav)
*   [Importing CSV Data](https://graphacademy.neo4j.com/courses/importing-csv-data/?ref=docs-nav)
*   [Graph Data Modeling](https://graphacademy.neo4j.com/courses/modeling-fundamentals/?ref=docs-nav)

[Data Scientist Courses](https://graphacademy.neo4j.com/categories/data-scientist/?ref=docs-nav)
*   [Into to Graph Data Science](https://graphacademy.neo4j.com/courses/gds-product-introduction/?ref=docs-nav)
*   [Graph Data Science Fundamentals](https://graphacademy.neo4j.com/courses/graph-data-science-fundamentals/?ref=docs-nav)
*   [Path Finding](https://graphacademy.neo4j.com/courses/gds-shortest-paths/?ref=docs-nav)

[Generative AI Courses](https://graphacademy.neo4j.com/categories/llms/?ref=docs-nav)
*   [Neo4j & LLM Fundamentals](https://graphacademy.neo4j.com/courses/llm-fundamentals/?ref=docs-nav)
*   [Vector Indexes & Unstructured Data](https://graphacademy.neo4j.com/courses/llm-vectors-unstructured/?ref=docs-nav)
*   [Build a Chatbot with Python](https://graphacademy.neo4j.com/courses/llm-chatbot-python/?ref=docs-nav)
*   [Build a Chatbot with TypeScript](https://graphacademy.neo4j.com/courses/llm-chatbot-typescript/?ref=docs-nav)

[Neo4j Certification](https://graphacademy.neo4j.com/certification/?ref=docs-nav)
*   [Neo4j Certified Professional](https://graphacademy.neo4j.com/certifications/neo4j-certification/?ref=docs-nav)
*   [Neo4j Graph Data Science Certification](https://graphacademy.neo4j.com/certifications/gds-certification/?ref=docs-nav)

[Get Started Free](https://console.neo4j.io/?ref=docs-nav-get-started)

[Search](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/#search)


Cypher Manual

Product Version

*       *   [Introduction](https://neo4j.com/docs/cypher-manual/introduction/)
        *   [Overview](https://neo4j.com/docs/cypher-manual/introduction/cypher-overview/)
        *   [Cypher and Neo4j](https://neo4j.com/docs/cypher-manual/introduction/cypher-neo4j/)
        *   [Cypher and Aura](https://neo4j.com/docs/cypher-manual/introduction/cypher-aura/)

    *   [Queries](https://neo4j.com/docs/cypher-manual/queries/)
        *   [Core concepts](https://neo4j.com/docs/cypher-manual/queries/concepts/)
        *   [Basic queries](https://neo4j.com/docs/cypher-manual/queries/basic/)
        *   [Select Cypher version](https://neo4j.com/docs/cypher-manual/queries/select-version/)
        *   [Composed queries](https://neo4j.com/docs/cypher-manual/queries/composed-queries/)
            *   [Combined queries (`UNION`)](https://neo4j.com/docs/cypher-manual/queries/composed-queries/combined-queries/)
            *   [Conditional queries (`WHEN`)](https://neo4j.com/docs/cypher-manual/queries/composed-queries/conditional-queries/)
            *   [Sequential queries (`NEXT`)](https://neo4j.com/docs/cypher-manual/queries/composed-queries/sequential-queries/)

    *   [Clauses](https://neo4j.com/docs/cypher-manual/clauses/)
        *   [Clause composition](https://neo4j.com/docs/cypher-manual/clauses/clause-composition/)
        *   [CALL procedure](https://neo4j.com/docs/cypher-manual/clauses/call/)
        *   [CREATE](https://neo4j.com/docs/cypher-manual/clauses/create/)
        *   [DELETE](https://neo4j.com/docs/cypher-manual/clauses/delete/)
        *   [FILTER](https://neo4j.com/docs/cypher-manual/clauses/filter/)
        *   [FINISH](https://neo4j.com/docs/cypher-manual/clauses/finish/)
        *   [FOREACH](https://neo4j.com/docs/cypher-manual/clauses/foreach/)
        *   [LET](https://neo4j.com/docs/cypher-manual/clauses/let/)
        *   [LIMIT](https://neo4j.com/docs/cypher-manual/clauses/limit/)
        *   [LOAD CSV](https://neo4j.com/docs/cypher-manual/clauses/load-csv/)
        *   [MATCH](https://neo4j.com/docs/cypher-manual/clauses/match/)
        *   [MERGE](https://neo4j.com/docs/cypher-manual/clauses/merge/)
        *   [OPTIONAL MATCH](https://neo4j.com/docs/cypher-manual/clauses/optional-match/)
        *   [ORDER BY](https://neo4j.com/docs/cypher-manual/clauses/order-by/)
        *   [REMOVE](https://neo4j.com/docs/cypher-manual/clauses/remove/)
        *   [RETURN](https://neo4j.com/docs/cypher-manual/clauses/return/)
        *   [SEARCH](https://neo4j.com/docs/cypher-manual/clauses/search/)
        *   [SET](https://neo4j.com/docs/cypher-manual/clauses/set/)
        *   [SHOW FUNCTIONS](https://neo4j.com/docs/cypher-manual/clauses/listing-functions/)
        *   [SHOW PROCEDURES](https://neo4j.com/docs/cypher-manual/clauses/listing-procedures/)
        *   [SHOW SETTINGS](https://neo4j.com/docs/cypher-manual/clauses/listing-settings/)
        *   [SHOW TRANSACTIONS](https://neo4j.com/docs/cypher-manual/clauses/transaction-clauses/#query-listing-transactions)
        *   [SKIP](https://neo4j.com/docs/cypher-manual/clauses/skip/)
        *   [TERMINATE TRANSACTIONS](https://neo4j.com/docs/cypher-manual/clauses/transaction-clauses/#query-terminate-transactions)
        *   [UNWIND](https://neo4j.com/docs/cypher-manual/clauses/unwind/)
        *   [USE](https://neo4j.com/docs/cypher-manual/clauses/use/)
        *   [WHERE](https://neo4j.com/docs/cypher-manual/clauses/where/)
        *   [WITH](https://neo4j.com/docs/cypher-manual/clauses/with/)

    *   [Subqueries](https://neo4j.com/docs/cypher-manual/subqueries/)
        *   [CALL subqueries](https://neo4j.com/docs/cypher-manual/subqueries/call-subquery/)
        *   [CALL subqueries in transactions](https://neo4j.com/docs/cypher-manual/subqueries/subqueries-in-transactions/)
        *   [COLLECT subqueries](https://neo4j.com/docs/cypher-manual/subqueries/collect/)
        *   [COUNT subqueries](https://neo4j.com/docs/cypher-manual/subqueries/count/)
        *   [EXISTS subqueries](https://neo4j.com/docs/cypher-manual/subqueries/existential/)

    *   [Patterns](https://neo4j.com/docs/cypher-manual/patterns/)
        *   [Primer](https://neo4j.com/docs/cypher-manual/patterns/primer/)
        *   [Fixed-length patterns](https://neo4j.com/docs/cypher-manual/patterns/fixed-length-patterns/)
        *   [Variable-length patterns](https://neo4j.com/docs/cypher-manual/patterns/variable-length-patterns/)
        *   [Shortest paths](https://neo4j.com/docs/cypher-manual/patterns/shortest-paths/)
        *   [Non-linear patterns](https://neo4j.com/docs/cypher-manual/patterns/non-linear-patterns/)
        *   [Match modes](https://neo4j.com/docs/cypher-manual/patterns/match-modes/)
        *   [Path modes](https://neo4j.com/docs/cypher-manual/patterns/path-modes/)
        *   [Syntax and semantics](https://neo4j.com/docs/cypher-manual/patterns/reference/)

    *   [Values and types](https://neo4j.com/docs/cypher-manual/values-and-types/)
        *   [Property, structural, and constructed values](https://neo4j.com/docs/cypher-manual/values-and-types/property-structural-constructed/)
        *   [Boolean, numeric, and string literals](https://neo4j.com/docs/cypher-manual/values-and-types/boolean-numeric-string/)
        *   [Temporal values](https://neo4j.com/docs/cypher-manual/values-and-types/temporal/)
        *   [Spatial values](https://neo4j.com/docs/cypher-manual/values-and-types/spatial/)
        *   [Lists](https://neo4j.com/docs/cypher-manual/values-and-types/lists/)
        *   [Maps](https://neo4j.com/docs/cypher-manual/values-and-types/maps/)
        *   [Vectors](https://neo4j.com/docs/cypher-manual/values-and-types/vector/)
        *   [Graph references](https://neo4j.com/docs/cypher-manual/values-and-types/graph-references/)
        *   [Working with `null`](https://neo4j.com/docs/cypher-manual/values-and-types/working-with-null/)
        *   [Casting data values](https://neo4j.com/docs/cypher-manual/values-and-types/casting-data/)
        *   [Equality, ordering, and comparison of value types](https://neo4j.com/docs/cypher-manual/values-and-types/ordering-equality-comparison/)

    *   [Expressions](https://neo4j.com/docs/cypher-manual/expressions/)
        *   [Predicates](https://neo4j.com/docs/cypher-manual/expressions/predicates/)
            *   [Boolean operators](https://neo4j.com/docs/cypher-manual/expressions/predicates/boolean-operators/)
            *   [Comparison operators](https://neo4j.com/docs/cypher-manual/expressions/predicates/comparison-operators/)
            *   [List operators](https://neo4j.com/docs/cypher-manual/expressions/predicates/list-operators/)
            *   [String operators](https://neo4j.com/docs/cypher-manual/expressions/predicates/string-operators/)
            *   [Label expression predicates](https://neo4j.com/docs/cypher-manual/expressions/predicates/label-expression-predicates/)
            *   [Path pattern expressions](https://neo4j.com/docs/cypher-manual/expressions/predicates/path-pattern-expressions/)
            *   [Type predicate expressions](https://neo4j.com/docs/cypher-manual/expressions/predicates/type-predicate-expressions/)

        *   [Node and relationship operators](https://neo4j.com/docs/cypher-manual/expressions/node-relationship-operators/)
        *   [Mathematical operators](https://neo4j.com/docs/cypher-manual/expressions/mathematical-operators/)
        *   [String concatenation operators](https://neo4j.com/docs/cypher-manual/expressions/string-operators/)
        *   [Temporal operators](https://neo4j.com/docs/cypher-manual/expressions/temporal-operators/)
        *   [List expressions](https://neo4j.com/docs/cypher-manual/expressions/list-expressions/)
        *   [Map expressions](https://neo4j.com/docs/cypher-manual/expressions/map-expressions/)
        *   [Conditional expressions (CASE)](https://neo4j.com/docs/cypher-manual/expressions/conditional-expressions/)

    *   [Functions](https://neo4j.com/docs/cypher-manual/functions/)
        *   [Aggregating functions](https://neo4j.com/docs/cypher-manual/functions/aggregating/)
        *   [Database functions](https://neo4j.com/docs/cypher-manual/functions/database/)
        *   [Graph functions](https://neo4j.com/docs/cypher-manual/functions/graph/)
        *   [List functions](https://neo4j.com/docs/cypher-manual/functions/list/)
        *   [LOAD CSV functions](https://neo4j.com/docs/cypher-manual/functions/load-csv/)
        *   Mathematical functions
            *   [Logarithmic functions](https://neo4j.com/docs/cypher-manual/functions/mathematical-logarithmic/)
            *   [Numeric functions](https://neo4j.com/docs/cypher-manual/functions/mathematical-numeric/)
            *   [Trigonometric functions](https://neo4j.com/docs/cypher-manual/functions/mathematical-trigonometric/)

        *   [Predicate functions](https://neo4j.com/docs/cypher-manual/functions/predicate/)
        *   [Scalar functions](https://neo4j.com/docs/cypher-manual/functions/scalar/)
        *   [Spatial functions](https://neo4j.com/docs/cypher-manual/functions/spatial/)
        *   [String functions](https://neo4j.com/docs/cypher-manual/functions/string/)
        *   Temporal functions
            *   [Duration functions](https://neo4j.com/docs/cypher-manual/functions/temporal/duration/)
            *   [Instant type functions](https://neo4j.com/docs/cypher-manual/functions/temporal/)
            *   [Format functions](https://neo4j.com/docs/cypher-manual/functions/temporal/format/)

        *   [User-defined functions](https://neo4j.com/docs/cypher-manual/functions/user-defined/)
        *   [Vector functions](https://neo4j.com/docs/cypher-manual/functions/vector/)

    *   [Indexes](https://neo4j.com/docs/cypher-manual/current/)
        *   [Search-performance indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/)
            *   [Create indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/)
            *   [Show indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/list-indexes/)
            *   [Drop indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/drop-indexes/)
            *   [The impact of indexes on query performance](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/using-indexes/)
            *   [Index hints for the Cypher planner](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/index-hints/)

        *   [Semantic indexes](https://neo4j.com/docs/cypher-manual/current/semantic-indexes/)
            *   [Full-text indexes](https://neo4j.com/docs/cypher-manual/current/semantic-indexes/full-text-indexes/)
            *   [Vector indexes](https://neo4j.com/docs/cypher-manual/current/semantic-indexes/vector-indexes/)

        *   [Syntax](https://neo4j.com/docs/cypher-manual/current/syntax/)

    *   [Schema](https://neo4j.com/docs/cypher-manual/schema/)
        *   [Graph types (Preview feature)](https://neo4j.com/docs/cypher-manual/schema/graph-types/)
            *   [Set graph types](https://neo4j.com/docs/cypher-manual/schema/graph-types/set-graph-types/)
            *   [Extend graph types](https://neo4j.com/docs/cypher-manual/schema/graph-types/extend-graph-types/)
            *   [Alter element types](https://neo4j.com/docs/cypher-manual/schema/graph-types/alter-element-types/)
            *   [Show graph types](https://neo4j.com/docs/cypher-manual/schema/graph-types/list-graph-types/)
            *   [Drop graph type elements](https://neo4j.com/docs/cypher-manual/schema/graph-types/drop-graph-type-elements/)

        *   [Constraints](https://neo4j.com/docs/cypher-manual/schema/constraints/)
            *   [Create constraints](https://neo4j.com/docs/cypher-manual/schema/constraints/create-constraints/)
            *   [Show constraints](https://neo4j.com/docs/cypher-manual/schema/constraints/list-constraints/)
            *   [Drop constraints](https://neo4j.com/docs/cypher-manual/schema/constraints/drop-constraints/)

        *   [Syntax](https://neo4j.com/docs/cypher-manual/schema/syntax/)

    *   [Execution plans and query tuning](https://neo4j.com/docs/cypher-manual/planning-and-tuning/)
        *   [Understanding execution plans](https://neo4j.com/docs/cypher-manual/planning-and-tuning/execution-plans/)
        *   [Operators](https://neo4j.com/docs/cypher-manual/planning-and-tuning/operators/)
            *   [Operators in detail](https://neo4j.com/docs/cypher-manual/planning-and-tuning/operators/operators-detail/)

        *   [Cypher runtimes](https://neo4j.com/docs/cypher-manual/planning-and-tuning/runtimes/)
            *   [Concepts](https://neo4j.com/docs/cypher-manual/planning-and-tuning/runtimes/concepts/)
            *   [Parallel runtime: reference](https://neo4j.com/docs/cypher-manual/planning-and-tuning/runtimes/reference/)

        *   [Query tuning](https://neo4j.com/docs/cypher-manual/planning-and-tuning/query-tuning/)

    *   [Query caches](https://neo4j.com/docs/cypher-manual/query-caches/)
        *   [Unifying query caches](https://neo4j.com/docs/cypher-manual/query-caches/unified-query-caches/)

    *   [Administration](https://neo4j.com/docs/cypher-manual/administration/)
    *   [Syntax](https://neo4j.com/docs/cypher-manual/syntax/)
        *   [Parsing](https://neo4j.com/docs/cypher-manual/syntax/parsing/)
        *   [Naming rules and recommendations](https://neo4j.com/docs/cypher-manual/syntax/naming/)
        *   [Variables](https://neo4j.com/docs/cypher-manual/syntax/variables/)
        *   [Keywords](https://neo4j.com/docs/cypher-manual/syntax/keywords/)
        *   [Parameters](https://neo4j.com/docs/cypher-manual/syntax/parameters/)
        *   [Comments](https://neo4j.com/docs/cypher-manual/syntax/comments/)

    *   [Additions, deprecations, removals, and compatibility](https://neo4j.com/docs/cypher-manual/deprecations-additions-removals-compatibility/)
    *   Appendix
        *   [Cypher styleguide](https://neo4j.com/docs/cypher-manual/styleguide/)
        *   [GQL conformance](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/)
            *   [Supported mandatory GQL features](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/supported-mandatory/)
            *   [Currently unsupported mandatory GQL features](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/unsupported-mandatory/)
            *   [Supported optional GQL features](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/supported-optional/)
            *   [Optional GQL features and analogous Cypher](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/analogous-cypher/)
            *   [Additional Cypher features](https://neo4j.com/docs/cypher-manual/appendix/gql-conformance/additional-cypher/)

        *   [Tutorials and extended examples](https://neo4j.com/docs/cypher-manual/appendix/tutorials/)
            *   [Basic query tuning example](https://neo4j.com/docs/cypher-manual/appendix/tutorials/basic-query-tuning/)
            *   [Advanced query tuning example](https://neo4j.com/docs/cypher-manual/appendix/tutorials/advanced-query-tuning/)

**Is this page helpful?**

[](https://neo4j.com/docs)
*   [Cypher Manual](https://neo4j.com/docs/cypher-manual/introduction/)
*   [Indexes](https://neo4j.com/docs/cypher-manual/current/)
*   [Search-performance indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/)

[Raise an issue](https://github.com/neo4j/docs-cypher/issues/new/?title=Docs%20Feedback%20modules/ROOT/pages/indexes/search-performance-indexes/index.adoc%20(ref:%20cypher-25)&body=%3E%20Do%20not%20include%20confidential%20information,%20personal%20data,%20sensitive%20data,%20or%20other%20regulated%20data.)

# Search-performance indexes

Search-performance indexes enable quicker retrieval of exact matches between an index and the primary data storage. There are four different search-performance indexes available in Neo4j:

*   [**Range indexes**](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/#create-range-index): Neo4j’s default index. Supports most types of predicates.

*   [**Text indexes**](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/#create-text-index): solves predicates operating on `STRING` values. Optimized for queries filtering with the `STRING` operators `CONTAINS` and `ENDS WITH`.

*   [**Point indexes**](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/#create-point-index): solves predicates on spatial `POINT` values. Optimized for queries filtering on distance or within bounding boxes.

*   [**Token lookup indexes**](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/#create-lookup-index): only solves node label and relationship type predicates (i.e. they cannot solve any predicates filtering on properties). Two token lookup indexes (one for node labels and one for relationship types) are present when a database is created in Neo4j.

To learn more about creating, listing, and deleting these indexes, as well as more details about the predicates supported by each index type, see [Create indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/), [Show indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/list-indexes/) and [Drop indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/drop-indexes/).

For information about how search-performance indexes are used in Cypher® queries, how they impact their performance, as well as some heuristics for when to use (and not to use) a search-performance index, see [The impact of indexes on query performance](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/using-indexes/).

Search-performance indexes are used automatically, and if several indexes are available, the [Cypher planner](https://neo4j.com/docs/cypher-manual/planning-and-tuning/execution-plans/) tries to use the index (or indexes) that can most efficiently solve a particular predicate. It is, however, possible to explicitly force a query to use a particular index with the `USING` keyword. For more information, see [Index hints for the Cypher planner](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/index-hints/).

[Indexes](https://neo4j.com/docs/cypher-manual/current/)[Create indexes](https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/create-indexes/)

[## Cypher Indexes and Constraints Learn how to make your graph more performant with Cypher constraints and indexes Take course](https://graphacademy.neo4j.com/courses/cypher-indexes-constraints/?ref=docs-ad-cypher-indexes-constraints)

## Learn

*   [Sandbox](https://neo4j.com/sandbox/?ref=developer-footer)
*   [Neo4j Community Site](https://community.neo4j.com/?ref=developer-footer)
*   [Neo4j Developer Blog](https://medium.com/neo4j)
*   [Neo4j Videos](https://www.youtube.com/neo4j)
*   [GraphAcademy](https://neo4j.com/graphacademy/?ref=developer-footer)
*   [Neo4j Labs](https://neo4j.com/labs/?ref=developer-footer)

## Social

*   [Twitter](https://twitter.com/neo4j)
*   [Meetups](https://www.meetup.com/Neo4j-Online-Meetup/)
*   [Github](https://github.com/neo4j/neo4j)
*   [Stack Overflow](https://stackoverflow.com/questions/tagged/neo4j)
*   [Want to Speak?](https://docs.google.com/forms/d/e/1FAIpQLSdEcNnMruES5iwvOVYovmS1D_P1ZL_HdUOitFrwrvruv5PZvA/viewform)

## [Contact Us →](https://neo4j.com/contact-us/?ref=footer)

*   US: 1-855-636-4532
*   Sweden +46 171 480 113
*   UK: +44 20 3868 3223
*   France: +33 (0) 1 88 46 13 20

© 2026 Neo4j, Inc.

[Terms](https://neo4j.com/terms/) | [Privacy](https://neo4j.com/privacy-policy/) | [Sitemap](https://neo4j.com/sitemap/)

Neo4j®, Neo Technology®, Cypher®, Neo4j® Bloom™ and Neo4j® Aura™ are registered trademarks of Neo4j, Inc. All other marks are owned by their respective companies.

AI search

###### AI SEARCH

Ask Neo4j anything or try one of the following questions

How do I model data for a graph database?How do I use the MATCH clause in Cypher?How do I use Neo4j with Python?How do I get started with graph algorithms? 

This is an experimental AI chatbot. All information should be verified.