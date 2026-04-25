# Card: Creating Single-Property RANGE Indexes (Neo4j Cypher DDL)
**Source:** https://www.graphacademy.neo4j.com/courses/cypher-indexes-constraints/3-indexes/02-create-index/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Cypher DDL patterns for indexes and how Neo4j uses them in query planning (PROFILE/db hits)

## Key Content
- **List metadata**
  - `SHOW CONSTRAINTS` lists constraints.
  - `SHOW INDEXES` lists indexes and their implementation details.
  - **Uniqueness constraints are implemented as RANGE indexes** (with uniqueness lookup characteristics).
  - A graph always contains a **LOOKUP index**; **do not drop it** (used to quickly find nodes by labels and relationships by types).

- **Create RANGE index (node single property) — Eq. 1**
  - **Syntax:**  
    `CREATE INDEX <index_name> IF NOT EXISTS FOR (x:<node_label>) ON (x.<property_key>)`  
    Variables: `<index_name>` name; `x` variable; `<node_label>` label; `<property_key>` property.
  - **IF NOT EXISTS behavior:**  
    - If same **index name** exists → no index created.  
    - Else if an index already exists for the same **label + property** → no index created.  
    - Otherwise → index is created.

- **Create RANGE index (relationship single property) — Eq. 2**
  - **Syntax:**  
    `CREATE INDEX <index_name> IF NOT EXISTS FOR ()-[x:<RELATIONSHIP_TYPE>]-() ON (x.<property_key>)`  
    Variables: `<RELATIONSHIP_TYPE>` relationship type; others as above.
  - Same `IF NOT EXISTS` rules as nodes (name check, then type+property check).

- **Empirical performance example (PROFILE)**
  - Query: `PROFILE MATCH (m:Movie) WHERE m.title STARTS WITH "Toy" RETURN m.title`
    - Before index: **27,376 total db hits**; plan starts with **node by label scan**.
    - After `CREATE INDEX Movie_title IF NOT EXISTS FOR (x:Movie) ON (x.title)`: **8 total db hits**; plan starts with **NodeIndexSeekByRange()**.
  - Case-insensitive variant uses index but increases db hits due to `toLower(m.title)` transformation.

- **Drop index**
  - `DROP INDEX <index_name>`

- **Testing index usage**
  - Use **`PROFILE`** to confirm index usage and view db hits/elapsed time.

## When to surface
Use when students ask how to create/list/drop Neo4j indexes, what `IF NOT EXISTS` does, why a query plan changes (scan vs `NodeIndexSeekByRange()`), or how to verify index impact with `PROFILE`.