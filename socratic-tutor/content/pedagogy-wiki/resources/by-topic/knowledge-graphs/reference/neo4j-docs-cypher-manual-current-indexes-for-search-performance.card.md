# Card: Neo4j search-performance index types (overview)
**Source:** https://neo4j.com/docs/cypher-manual/current/indexes-for-search-performance/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official Cypher Manual overview of search-performance index types + what predicates they solve + planner behavior and hints

## Key Content
- **Definition (Search-performance indexes):** Enable quicker retrieval of **exact matches** between an index and the **primary data storage**.
- **There are 4 search-performance index types in Neo4j (Section “Search-performance indexes”):**
  1. **Range indexes** (default index): *Supports most types of predicates.*
  2. **Text indexes:** Solve predicates operating on `STRING` values; **optimized** for filtering with string operators **`CONTAINS`** and **`ENDS WITH`**.
  3. **Point indexes:** Solve predicates on spatial `POINT` values; **optimized** for filtering on **distance** or **within bounding boxes**.
  4. **Token lookup indexes:** Solve **only** node label and relationship type predicates; **cannot** solve predicates filtering on properties.
- **Defaults / built-ins:**
  - **Range index is Neo4j’s default index.**
  - **Two token lookup indexes** are present when a database is created: **one for node labels** and **one for relationship types**.
- **Planner behavior / rationale:**
  - Indexes are **used automatically**.
  - If multiple indexes are available, the **Cypher planner** attempts to use the index (or indexes) that can **most efficiently solve** a predicate.
  - You can **force** use of a particular index with the **`USING`** keyword (index hints).

## When to surface
Use when students ask which Neo4j index type to use for a predicate (string/spatial/label/type/property), what indexes exist by default, or how the Cypher planner chooses/can be forced to use indexes.