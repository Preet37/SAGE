# Card: Neo4j Cypher Constraints (data integrity for KG canonicalization)
**Source:** https://neo4j.com/docs/cypher-manual/current/constraints/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Constraint semantics (uniqueness, existence, type, key), where to create/list/drop, and schema/operational implications

## Key Content
- **Purpose (schema/data quality):** Neo4j constraints “ensure the quality and integrity of data in a graph.”
- **Constraint types available (semantics):**
  - **Property uniqueness constraints:** ensure that **combined property values are unique** for:
    - all **nodes with a specific label**, or
    - all **relationships with a specific type**.
  - **Property existence constraints (Enterprise Edition):** ensure that a property **exists** for:
    - all nodes with a specific label, or
    - all relationships with a specific type.
  - **Property type constraints (Enterprise Edition):** ensure that a property has the **required property type** for:
    - all nodes with a specific label, or
    - all relationships with a specific type.
  - **Key constraints (Enterprise Edition):** ensure **both**:
    - all specified properties **exist**, and
    - the **combined property values are unique**
    for nodes with a specific label or relationships with a specific type.
- **Operational workflow pointers (where to look next in the manual):**
  - “Create constraints”, “Show constraints”, “Drop constraints” pages contain details on **index-backed constraints**, **creation failures**, and **data violation scenarios**.
  - Cypher command reference: **Syntax → Constraints**.
- **Design rationale / schema management guidance:**
  - Constraints created with the older `CREATE CONSTRAINT` syntax are **automatically added to the graph type** of a database.
  - Neo4j **recommends defining a schema using a graph type** because it provides **more sophisticated constraint types** and a **more holistic/simplified** way to constrain and maintain data shape as constraints grow.

## When to surface
Use when students ask how to enforce KG canonical IDs, prevent duplicates, require mandatory properties, or validate property types in Neo4j; also when discussing schema-first vs ad-hoc constraint management (graph types vs many individual constraints).