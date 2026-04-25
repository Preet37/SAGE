# Source: https://www.graphacademy.neo4j.com/courses/cypher-indexes-constraints/3-indexes/02-create-index/
# Title: Creating Single Property Indexes
# Fetched via: trafilatura
# Date: 2026-04-09

Creating RANGE indexes
In this lesson you will learn how to create a single property RANGE index on a node property or relationship property to optimize queries.
Listing indexes
You have already learned how to list the constraints in the graph:
SHOW CONSTRAINTS
There is another command that lists the indexes in the graph:
SHOW INDEXES
SHOW INDEXES
provides information about the implementation of the index.
When you execute SHOW INDEXES
on the current graph you have been working with, you see that the uniqueness constraints defined in the graph are RANGE indexes.
That is, the implementation of a uniqueness constraint in the graph is as a RANGE index, along with the uniqueness lookup characteristics of the index.
Lookup Indexes
A graph will always contain a LOOKUP
index that you see when you list the indexes.
You should never drop this index as it is used to quickly find nodes by their labels and relationships by their types in the graph.
Syntax for creating a RANGE index for a single property of a node
Here is the syntax for creating a RANGE index for a single property of a node:
CREATE INDEX <index_name> IF NOT EXISTS
FOR (x:<node_label>)
ON x.<property_key>
You specify the name of the index, the node label it will be associated with, and the name of the property.
-
If an index already exists in the graph with the same name, no index is created.
-
If an index does not exist in the graph with the same name:
-
No index is created if there already is an index for that node label and property key.
-
Otherwise, the index is created.
-
Creating the RANGE index for a single property of a node
Suppose that we want this type of query to perform its best:
PROFILE MATCH (m:Movie)
WHERE m.title STARTS WITH "Toy"
RETURN m.title
If you execute this query and examine the plan produced by the PROFILE
, you will see that it required 27,376 total db hits.
The query plan begins with a node by label scan.
To test the WHERE m.title STARTS WITH "Toy"
predicate, the query engine must examine all title properties of every Movie node.
To improve the performance of this query, we create a RANGE index on the Movie.title property.
Execute this code to create the RANGE index for the Movie.title property:
CREATE INDEX Movie_title IF NOT EXISTS
FOR (x:Movie)
ON (x.title)
Repeat the above query with the PROFILE
. You should see that with the index, only 8 total db hits occur.
The query plan now starts with the NodeIndexSeekByRange() operation and uses the RANGE index you just created.
Always profile before you deploy your application!
We cannot understate how important it is to profile your queries, especially queries that are most important to your application.
Suppose in our application, we wanted to have the query be case-insensitive. The new query would be:
PROFILE MATCH (m:Movie)
WHERE toLower(m.title) STARTS WITH "toy"
RETURN m.title
Notice that for this query, the index is used but more properties need to be transformed to lower case, making the db hits higher.
Syntax for creating a RANGE index for a single property of a relationship
Here is the syntax for creating a RANGE index for a single property of a relationship:
CREATE INDEX <index_name> IF NOT EXISTS
FOR ()-[x:<RELATIONSHIP_TYPE>]-()
ON (x.<property_key>)
You specify the name of the index, the relationship type it will be associated with, and the name of the property.
-
If an index already exists in the graph with the same name, no index is created.
-
If an index does not exist in the graph with the same name:
-
No index is created if there already is an index for that relationship type and property key.
-
Otherwise, the index is created.
-
You will create a RANGE index on a relationship type property in one of the next Challenges.
Dropping indexes
Previously, you learned how to drop constraints in the graph.
You use DROP INDEX <index_name>
to drop an index by its name.
Check your understanding
1. Creating a RANGE index
Suppose we have a graph that contains Company nodes. One of the properties of a Company node is name. We want to be able to optimize queries that test the names of companies. What is the correct statement to create this RANGE index?
-
❏
CREATE b-tree Company_name IF NOT EXISTS ON (Company.name)
-
❏
CREATE b-tree Company_name IF NOT EXISTS FOR (x:Company) ON (x.name)
-
✓
CREATE INDEX Company_name IF NOT EXISTS FOR (x:Company) ON (x.name)
-
❏
CREATE INDEX Company_name IF NOT EXISTS ON (Company.name)
Hint
You are creating an index. The index type by default is RANGE.
Solution
The correct code for creating the RANGE index is:
CREATE INDEX Company_name IF NOT EXISTS FOR (x:Company) ON (x.name)
2. Testing indexes
What Cypher keyword can you use to confirm that an index is used and also see if the query yields fewer total db hits or has a shorter elapsed time after it executes?
-
❏
EXPLAIN
-
❏
TEST
-
❏
PLAN
-
✓
PROFILE
Hint
You prefix any query with this clause to show the query plan.
Solution
The correct Cypher clause for confirming that the index is used and to show the total db hits and elapsed time when the query executes is:
PROFILE
Summary
In this lesson, you learned how to create a RANGE index for a property of a node. In the next challenge, you will create another RANGE index and test it.