# Source: https://milvus.io/docs/ivf.md
# Title: IVF_FLAT | Milvus Documentation
# Fetched via: search
# Date: 2026-04-10

# Welcome to Milvus Docs!
## Here you will learn about what Milvus is, and how to install, use, and deploy Milvus to build an application according to your business need.
...
Learn how to install Milvus using either Docker Compose or on Kubernetes.
Quick Start
Learn how to quickly run Milvus with sample code.
...
Learn how to build vector similarity search applications with Milvus.
...
- Single-Vector Search
- Hybrid Search
- Get & Scalar Query
- Milvus for AI Agents
...
- Added Milvus for AI Agents section with prompt guides.
- Added guidance on how to use Gemini embedding function.
- Added guidance on how to search by primary keys.
- Added guidance on how to use text highlighter in search results.
- Added descriptions of geometry field, timestamptz field, tiered storage, and array of structs.
...
Learn what it is, how OpenAI used it, and why it requires hybrid search.

## Overview

In Milvus, indexes are specific to fields, and the applicable index types vary according to the data types of the target fields. As a professional vector database, Milvus focuses on enhancing both the performance of vector searches and scalar filtering, which is why it offers various index types.

The following table lists the mapping relationship between field data types and applicable index types.
|Field Data Type|Applicable Index Types|
|--|--|
|- FLOAT_VECTOR - FLOAT16_VECTOR - BFLOAT16_VECTOR - INT8_VECTOR|- FLAT - IVF_FLAT - IVF_SQ8 - IVF_PQ - IVF_RABITQ - HNSW - HNSW_SQ - HNSW_PQ - HNSW_PRQ - DISKANN - SCANN - AISAQ - GPU_CAGRA - GPU_IVF_FLAT - GPU_IVF_PQ - GPU_BRUTE_FORCE|
|BINARY_VECTOR|- BIN_FLAT - BIN_IVF_FLAT - MINHASH_LSH|
|SPARSE_FLOAT_VECTOR|SPARSE_INVERTED_INDEX|
|VARCHAR|- INVERTED (Recommended) - BITMAP - Trie|
|BOOL|- BITMAP (Recommended) - INVERTED|
|- INT8 - INT16 - INT32 - INT64|- INVERTED - STL_SORT|
|- FLOAT - DOUBLE|INVERTED|
|ARRAY ^(elements of the BOOL, INT8/16/32/64, and VARCHAR types)^|BITMAP (Recommended)|
|ARRAY ^(elements of the BOOL, INT8/16/32/64, FLOAT, DOUBLE, and VARCHAR types)^|INVERTED|
|JSON|INVERTED|

…

## Vector Index anatomy

As demonstrated in the diagram below, an index type in Milvus consists of three core components, namely **data structure**, **quantization**, and **refiner**. Quantization and refiner are optional, but are widely used because of a significant gains-better-than-costs balance.

Vector Index Anatomy
During index creation, Milvus combines the chosen data structure and quantization method to determine an optimal **expansion rate**. At query time, the system retrieves `topK × expansion rate` candidate vectors, applies the refiner to recalculate distances with higher precision, and finally returns the most accurate `topK` results. This hybrid approach balances speed and accuracy by restricting resource-intensive refinement to a filtered subset of candidates.

### Data structure

The data structure forms the foundational layer of the index. Common types include:
- **Inverted File (IVF)**

  IVF-series index types allow Milvus to cluster vectors into buckets through centroid-based partitioning. It is generally safe to assume that all vectors in a bucket are likely to be close to the query vector if the bucket centroid is close to the query vector. Based on this premise, Milvus scans only the vector embeddings in those buckets where the centroids are near the query vector, rather than examining the entire dataset. This strategy reduces computational costs while maintaining acceptable accuracy.

  This type of index data structure is ideal for large-scale datasets requiring fast throughput.
- **Graph-based structure**

  A graph-based data structure for vector search, such as Hierarchical Navigable Small World (HNSW), constructs a layered graph where each vector connects to its nearest neighbors. Queries navigate this hierarchy, starting from coarse upper layers and switching through lower layers, enabling efficient logarithmic-time search complexity.

  This type of index data structure excels in high-dimensional spaces and scenarios demanding low-latency queries.

### Quantization

Quantization reduces memory footprint and computational costs through a coarser representation:

- **Scalar Quantization** (e.g. **SQ8**) enables Milvus to compress each vector dimension into a single byte (8-bit), reducing memory usage by 75% compared to 32-bit floats while preserving reasonable accuracy.
- **Product Quantization** (**PQ**) enables Milvus to split vectors into subvectors and encode them using codebook-based clustering. This achieves higher compression ratios (e.g., 4-32x) at the cost of marginally reduced recall, making it suitable for memory-constrained environments.

…

### Summary

This tiered architecture – coarse filtering via data structures, efficient computation through quantization, and precision tuning via refinement – allows Milvus to optimize the accuracy-performance tradeoff adaptively.

…

- **Graph-based index types** usually outperform **IVF variants** in terms of **QPS**.
- **IVF variants** particularly fit in the scenarios with **a large topK (for example, over 2,000)**.
- **PQ** typically offers a better recall rate at similar compression rates when compared to **SQ**, though the latter provides faster performance.

…

### Recall

The recall usually involves the filter ratio, which refers to the data that is filtered out before searches. When dealing with recall, consider the following:

- If the filter ratio is less than 85%, graph-based index types outperform IVF variants.
- If the filter ratio is between 85% and 95%, use IVF variants.
- If the filter ratio is over 98%, use Brute-Force (FLAT) for the most accurate search results.

…

### Performance

The performance of a search usually involves the top-K, which refers to the number of records that the search returns. When dealing with performance, consider the following:

- For a search with a small top-K (e.g., 2,000) requiring a high recall rate, graph-based index types outperform IVF variants.
- For a search with a great top-K (compared with the total number of vector embeddings), IVF variants are a better choice than graph-based index types.
- For a search with a medium-sized top-K and a high filter ratio, IVF variants are better choices.

…

|Scenario|Recommended Index|Notes|
|--|--|--|
|Raw data fits in memory|HNSW, IVF + Refinement|Use HNSW for low-`k`/high recall.|
|Raw data on disk, SSD|DiskANN|Optimal for latency-sensitive queries.|
|Raw data on disk, limited RAM|IVFPQ/SQ + mmap|Balances memory and disk access.|
|High filter ratio (>95%)|Brute-Force (FLAT)|Avoids index overhead for tiny candidate sets.|
|Large `k` (≥1% of dataset)|IVF|Cluster pruning reduces computation.|

…

The memory consumption of an index is influenced by its data structure, compression rate through quantization, and the refiner in use. Generally speaking, graph-based indices typically have a higher memory footprint due to the graph’s structure (e.g., **HNSW**), which usually implies a noticeable per-vector space overhead. In contrast, IVF and its variants are more memory-efficient because less per-vector space overhead applies. However, advanced techniques such as **DiskANN** allow parts of the index, like the graph or the refiner, to reside on disk, reducing memory load while maintaining performance.

…

### IVF index memory usage

IVF indexes balance memory efficiency with search performance by partitioning data into clusters. Below is a breakdown of the memory used by 1 million 128-dimensional vectors indexed using IVF variants.

1. **Calculate the memory used by centroids.**

   IVF-series index types enable Milvus to cluster vectors into buckets using centroid-based partitioning. Each centroid is included in the index in raw vector embedding. When you divide the vectors into 2,000 clusters, the memory usage can be calculated as follows:

…

2. **Calculate the memory used by cluster assignments.**

   Each vector embedding is assigned to a cluster and stored as integer IDs. For 2,000 clusters, a 2-byte integer suffices. The memory usage can be calculated as follows:

…

3. **Calculate the compression caused by quantization.**

   IVF variants typically use PQ and SQ8, and the memory usage can be estimated as follows:

   - Using PQ with 8 subquantizers

…

|Configuration|Memory Estimation|Total Memory|
   |--|--|--|
   |IVF-PQ (no refinement)|1.0 MB + 2.0 MB + 8.0 MB|11.0 MB|
   |IVF-PQ + 10% raw refinement|1.0 MB + 2.0 MB + 8.0 MB + 51.2 MB|62.2 MB|
   |IVF-SQ8 (no refinement)|1.0 MB + 2.0 MB + 128 MB|131.0 MB|
   |IVF-FLAT (full raw vectors)|1.0 MB + 2.0 MB + 512 MB|515.0 MB|
4. **Calculate the refinement overhead.**

   IVF variants often pair with a refiner to re-rank candidates. For a search retrieving the top 10 results with an expansion rate of 5, the refinement overhead can be estimated as follows:

…

This achieves a 64-times compression rate when compared to the raw vector embeddings, and the total memory used by the **HNSWPQ** index type would be **128 MB (graph) + 8 MB (compressed vector) = 136 MB**.
4. **Calculate the refinement overhead.**

   Refinement, such as re-ranking with raw vectors, temporarily loads high-precision data into memory. For a search retrieving the top 10 results with an expansion rate of 5, the refinement overhead can be estimated as follows:

…

#### Memory-mapped files (mmap)

Memory mapping (Mmap) enables direct memory access to large files on disk, allowing Milvus to store indexes and data in both memory and hard drives. This approach helps optimize I/O operations by reducing the overhead of I/O calls based on access frequency, thereby expanding storage capacity for collections without significantly impacting search performance.

Specifically, you can configure Milvus to memory-map the raw data in certain fields instead of fully loading them into memory. This way, you can gain direct memory access to the fields without worrying about memory issues and extend the collection capacity.

## 2. Schema

#### 2.1 Collection Schema

```
type CollectionSchema struct {
	Name string
	Description string
	AutoId bool
	Fields []*FieldSchema
}
```

#### 2.2 Field Schema

```
type FieldSchema struct {
	FieldID int64
	Name string
	IsPrimaryKey bool
	Description string
	DataType DataType
	TypeParams []*commonpb.KeyValuePair
	IndexParams []*commonpb.KeyValuePair
	AutoID bool
}
```

###### 2.2.1 Data Types

**DataType**
```
enum DataType {
  NONE = 0;
  BOOL = 1;
  INT8 = 2;
  INT16 = 3;
  INT32 = 4;
  INT64 = 5;

  FLOAT = 10;
  DOUBLE = 11;

  STRING = 20;

  VECTOR_BINARY = 100;
  VECTOR_FLOAT = 101;
}
```

###### 2.2.2 Type Params

###### 2.2.3 Index Params

# Intro to Index

For more detailed information about indexes, please refer to Milvus documentation index chapter.

To learn how to choose an appropriate index for your application scenarios, please read How to Select an Index in Milvus.

To learn how to choose an appropriate index for a metric, see Similarity Metrics.

Different index types use different index params in construction and query. All index params are represented by the structure of the map. This doc shows the map code in python.

…

## IVF_FLAT

**IVF** (*Inverted File*) is an index type based on quantization. It divides the points in space into `nlist` units by the clustering method. During searching vectors, it compares the distance between the target vector and the center of all units, and then selects the `nprobe` nearest unit. Afterwards, it compares all the vectors in these selected cells to get the final result.
IVF_FLAT is the most basic IVF index, and the encoded data stored in each unit is consistent with the original data.

- building parameters:

  **nlist**: Number of cluster units.
```
# IVF_FLAT
{
    "index_type": "IVF_FLAT",
    "metric_type": "L2", # one of L2, IP

    #Special for IVF_FLAT
    "nlist": 100 # int. 1~65536
}
```

…

```
# IVF_FLAT
{
    "topk": top_k,
    "query": queries,
    "metric_type": "L2", # one of L2, IP

    #Special for IVF_FLAT
    "nprobe": 8 # int. 1~nlist(cpu), 1~min[2048, nlist](gpu)
}
```

…

```
# BIN_IVF_FLAT
{
    "index_type": "BIN_IVF_FLAT",
    "metric_type": "jaccard", # one of jaccard, hamming, tanimoto

    #Special for BIN_IVF_FLAT
    "nlist": 100 # int. 1~65536
}
```

…

```
# BIN_IVF_FLAT
{
    "topk": top_k,
    "query": queries,

  	#Special for BIN_IVF_FLAT
    "metric_type": "jaccard", # one of jaccard, hamming, tanimoto
    "nprobe": 8 # int. 1~nlist(cpu), 1~min[2048, nlist](gpu)
}
```

## IVF_PQ

**PQ** (*Product Quantization*) uniformly decomposes the original high-dimensional vector space into Cartesian products of `m` low-dimensional vector spaces and then quantizes the decomposed low-dimensional vector spaces. Instead of calculating the distances between the target vector and the center of all the units, product quantization enables the calculation of distances between the target vector and the clustering center of each low-dimensional space and greatly reduces the time complexity and space complexity of the algorithm.
IVF_PQ performs IVF index clustering, and then quantizes the product of vectors. Its index file is even smaller than IVF_SQ8, but it also causes a loss of accuracy during searching.

…

**GPU-enabled** Milvus: `m` ∈ {1, 2, 3, 4, 8, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 96}, and (dim / m) ∈ {1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32}. (`m` x 1024) ≥ `MaxSharedMemPerBlock` of your graphics card.
```
# IVF_PQ
{
    "index_type": "IVF_PQ",
    "metric_type": "L2", # one of L2, IP

		#Special for IVF_PQ
    "nlist": 100, # int. 1~65536
    "m": 8
}
```

…

```
# IVF_PQ
{
    "topk": top_k,
    "query": queries,
    "metric_type": "L2", # one of L2, IP

    #Special for IVF_PQ
    "nprobe": 8 # int. 1~nlist(cpu), 1~min[2048, nlist](gpu)
}
```

## IVF_SQ8

**IVF_SQ8** does scalar quantization for each vector placed in the unit based on IVF. Scalar quantization converts each dimension of the original vector from a 4-byte floating-point number to a 1-byte unsigned integer, so the IVF_SQ8 index file occupies much less space than the IVF_FLAT index file. However, scalar quantization results in a loss of accuracy during searching vectors.

…

```
# IVF_SQ8
{
    "topk": top_k,
    "query": queries,
    "metric_type": "L2", # one of L2, IP

    #Special for IVF_SQ8
    "nprobe": 8 # int. 1~nlist(cpu), 1~min[2048, nlist](gpu)
}
```

## IVF_SQ8_HYBRID

An optimized version of IVF_SQ8 that requires both CPU and GPU to work. Unlike IVF_SQ8, IVF_SQ8H uses a GPU-based coarse quantizer, which greatly reduces the time to quantize.

IVF_SQ8H is an IVF_SQ8 index that optimizes query execution.
The query method is as follows:

- If `nq` ≥ `gpu_search_threshold`, GPU handles the entire query task.
- If `nq` < `gpu_search_threshold`, GPU handles the task of retrieving the `nprobe` nearest unit in the IVF index file, and CPU handles the rest.
- building parameters:

  **nlist**: Number of cluster units.

…

```
# IVF_SQ8_HYBRID
{
    "topk": top_k,
    "query": queries,
    "metric_type": "L2", # one of L2, IP

    #Special for IVF_SQ8_HYBRID
    "nprobe": 8 # int. 1~nlist(cpu), 1~min[2048, nlist](gpu)
}
```

…

When searching for vectors, ANNOY follows the tree structure to find subspaces closer to the target vector, and then compares all the vectors in these subspaces (The number of vectors being compared should not be less than `search_k`) to obtain the final result. Obviously, when the target vector is close to the edge of a certain subspace, sometimes it is necessary to greatly increase the number of searched subspaces to obtain a high recall rate.

…

## HNSW

**HNSW** (*Hierarchical Navigable Small World Graph*) is a graph-based indexing algorithm. It builds a multi-layer navigation structure for an image according to certain rules. In this structure, the upper layers are more sparse and the distances between nodes are farther; the lower layers are denser and the distances between nodes are closer. The search starts from the uppermost layer, finds the node closest to the target in this layer, and then enters the next layer to begin another search. After multiple iterations, it can quickly approach the target position.
To improve performance, HNSW limits the maximum degree of nodes on each layer of the graph to `M`.
In addition, you can use `efConstruction` (when building index) or `ef` (when searching targets) to specify a search range.

- building parameters:

  **M**: Maximum degree of the node.

  **efConstruction**: Take the effect in the stage of index construction.

…

## RHNSW_PQ

**RHNSW_PQ** is a variant index type combining PQ and HNSW. It first uses PQ to quantize the vector, then uses HNSW to quantize the PQ quantization result to get the index.

- building parameters:

  **M**: Maximum degree of the node.

  **efConstruction**: Take effect in the stage of index construction.

  **PQM**: m for PQ.

…

## RHNSW_SQ

**RHNSW_SQ** is a variant index type combining SQ and HNSW. It uses SQ to quantize the vector, then uses HNSW to quantize the SQ quantization result to get the index.

- building parameters:

  **M**: Maximum degree of the node.

  **efConstruction**: Take effect in the stage of index construction, search scope.

# How to Pick a Vector Index in Your Milvus Instance: A Visual Guide

May 14, 20249 min read

In this post, we'll explore several vector indexing strategies that can be used to efficiently perform similarity search, even in scenarios where we have large amounts of data and multiple constraints to consider.

By Ruben Winastwan

Read the entire series

…

- Efficiently Deploying Milvus on GCP Kubernetes: A Guide to Open Source Database Management
- Building RAG with Snowflake Arctic and Transformers on Milvus
- Vectorizing JSON Data with Milvus for Similarity Search
- Building a Multimodal RAG with Gemini 1.5, BGE-M3, Milvus Lite, and LangChain
Similarity search has emerged as one of the most popular real-world use cases of data science and AI applications. Tasks such as recommendation systems, information retrieval, and document clustering rely on similarity search as their core algorithm.

A sound similarity search system must provide accurate results quickly and efficiently. However, as the volume of data grows, meeting all of these requirements becomes increasingly challenging. Therefore, approaches and techniques are necessary to improve the scalability of similarity search tasks.

…

## What is a Vector Index?

Similarity search, a crucial real-world application of Natural Language Processing (NLP), is particularly significant when dealing with text as our input data. Since machine learning models cannot directly process raw text, these texts need to be transformed into vector embeddings.

Several models, including BM25, Sentence Transformers, OpenAI, BG3, and SPLADE, can transform raw texts into embeddings.
Once we have a collection of vector embeddings, the distance between one embedding and another can be computed using various distance metrics, such as inner product, cosine distance, Euclidean distance, Hamming distance, Jaccard distance, and more.

The common workflow of similarity search is as follows:
1. We store a collection of embeddings inside a database (typically a dedicated vector database).
2. Given a user query, we transform that query into an embedding.
3. Perform a similarity search between the query embedding and each of the embeddings inside the database by calculating the distance.
4. The embedding inside the database with the smallest distance is the most relevant to the user's query.
A special data structure called an index is built on top of each embedding inside a vector database during the storing process to facilitate efficient searching and retrieval of similar embeddings.

Several indexing strategies can be applied to fit our specific use case. In general, there are four categories of indexing strategies: tree-based, graph-based, hash-based, and quantization-based indexing.

…

| | | | | | | |
|--|--|--|--|--|--|--|
|**Category**|**Index**|**Accuracy**|**Latency**|**Throughput**|**Index Time**|**Cost**|
|Graph-based|Cagra (GPU)|High|Low|Very High|Fast|Very High|
| |HNSW|High|Low|High|Slow|High|
| |DiskANN|High|High|Mid|Very Slow|Low|
|Quantization-based or cluster-based|ScaNN|Mid|Mid|High|Mid|Mid|
| |IVF_FLAT|Mid|Mid|Low|Fast|Mid|

…

## Popular Index Types Supported by Milvus

Milvus supports several indexing algorithms that you can choose based on your specific use case. Let's begin with the most basic one, known as the FLAT index.

### FLAT Index

The FLAT index is a straightforward and elementary similarity search algorithm that utilizes the k-nearest neighbors (kNN) algorithm.

Consider a database with a collection of 100 embeddings and a query embedding Q. To find the most similar embedding to Q, kNN calculates the distance between Q and each embedding in the database using a specified distance metric. It then identifies the embedding with the smallest distance as the most similar to Q.

…

### Inverted File FLAT (IVF-FLAT) Index

The Inverted File FLAT (IVF-FLAT) index aims to improve the search performance of the basic FLAT index by implementing approximate nearest neighbors (ANNs) algorithm instead of the native kNN. IVF_FLAT works by dividing the embeddings in the database into several non-intersecting partitions. Each partition has a center point called a centroid, and every vector embedding in the database is associated with a specific partition based on the nearest centroid.
When a query embedding Q is provided, IVF-FLAT only needs to calculate the distance between Q and each centroid rather than the entire set of embeddings in the database. The centroid with the smallest distance is then selected, and the embeddings associated with that partition are used as candidates for the final search.

This indexing method speeds up the search process, but it comes with a potential drawback: the candidate found as the nearest to the query embedding Q may not be the exact nearest one. This can happen if the nearest embedding to Q resides in a partition different from the one selected based on the nearest centroid (see visualization below).
To address this issue, IVF-FLAT provides two hyperparameters that we can tune:

1. `nlist`: Specifies the number of partitions to create using the k-means algorithm.
2. `nprobe`: Specifies the number of partitions to consider during the search for candidates.

Now if we set `nprobe` to 3 instead of 1, we get the following result:
By increasing the `nprobe` value, you can include more partitions in the search, which can help ensure that the nearest embedding to the query is not missed, even if it resides in a different partition. However, this comes at the cost of increased search time, as more candidates need to be evaluated.

### Inverted File Index with Quantization (IVF-SQ8 and IVF-PQ)

The IVF-FLAT indexing algorithm mentioned earlier accelerates the vector search process. However, when memory resources are limited, using the FLAT strategy may not be optimal as it does not compress the values of the embeddings.

To address memory constraints, an additional step can be combined with IVF, which involves mapping the values in each vector dimension to lower-precision integer values. This mapping strategy is commonly known as quantization, and there are two main quantization approaches: scalar quantization and product quantization.
**Inverted File Index and Scalar Quantization (IVF-SQ8)**

Scalar quantization involves mapping floating-point numbers representing each vector dimension to integers.

In scalar quantization, the first step is to determine and store the maximum and minimum values of each dimension of the vectors in the database to calculate the step size. This step size is crucial for scaling the floating-point number in each dimension to its integer representation. For example, converting a 32-bit floating-point number to an 8-bit integer typically involves splitting the range into 256 buckets. The step size can be calculated as:
step size formula.png

The quantized version of the n-th vector dimension is obtained by subtracting the value of the n-th dimension from its minimum value and then dividing the result by the step size.

**Inverted File Index and Product Quantization (IVF-PQ)**

Product quantization addresses the limitation of scalar quantization by considering the distribution of each dimension.
Product quantization divides vector embeddings into subvectors, performs clustering within each subvector to create centroids, and encodes each subvector with the ID of the nearest centroid. This method creates non-intersecting partitions within subvectors, similar to IVF-FLAT.

The ID of the centroid, known as the PQ code, represents an 8-bit integer, resulting in memory-efficient encoding of vector embeddings.
Product quantization offers more powerful memory compression compared to scalar quantization, making it a highly useful method for handling massive memory constraints in similarity search applications.

### Hierarchical Navigable Small World (HNSW)

HNSW is a graph-based indexing algorithm that combines two key concepts: skip lists and Navigable Small World (NSW) graphs.

A skip list is a probabilistic data structure composed of multiple layers of linked lists. The lowest layer contains the original linked list with all elements. As we move to higher layers, the linked lists progressively skip over more elements, resulting in fewer elements at each higher layer.
During the search process, we start from the highest layer and gradually descend to lower layers until we find the desired element. Because of this, skip lists can significantly speed up the search process.

Let’s say we have a skip list with 3 layers and 8 elements in the original linked list. If we want to find element 7, the searching process will look something like this:
On the other hand, an NSW graph is built by randomly shuffling data points and inserting them one by one, with each point connected to a predefined number of edges (M). This creates a graph structure that exhibits the "small world" phenomenon, where any two points are connected through a relatively short path.

As an example, let’s say we have 5 data points and then we set the M=2. The step-by-step process of building an HSW graph is shown below:
The "Hierarchical" terms in HNSW refers to the combination of the skip list and NSW graph concepts. HNSW consists of a multi-layered graph, where the lower layers contain the complete set of data points, and the higher layers contain only a small fraction of the points.
HNSW starts by assigning a random integer number from 0 to l to each data point (can be referred to as “node”—as we call it in graph algorithm), where l is the maximum layer at which that data point can be present in a multi-layered graph. If a data point has l=2 and the total number of layers in the graph is 5, then that data point should only be present up until the second layer, and shouldn’t be available in layer 3 upwards.
During the search process, HNSW starts by selecting an entry point, and this should be the data point present in the highest layer. It then searches for the neighbor closest to the query point and recursively continues the search in lower layers until the nearest data point is found.

HNSW has two key hyperparameters that we can tune to improve search accuracy:
1. `efConstruction`: The number of neighbors considered to find the nearest neighbor at each layer. Higher values result in more thorough searches and better accuracy, but with increased computation time.
2. `efSearch`: The number of nearest neighbors to consider as the entry point in each layer.

By leveraging the concepts of skip lists and NSW graphs, HNSW can significantly speed up the similarity search process by skipping over many unpromising data points.

…

For precise searches that guarantee 100% accuracy, the FLAT index is the ideal choice. However, if speed is a priority and exact accuracy is not that critical, other indexing algorithms can be selected.

If memory resources are a concern, consider using quantized indexing algorithms like IVF-SQ8 or IVF-PQ. Otherwise, options like IVF-FLAT or HNSW can be suitable. For smaller datasets (less than 2GB), IVF-FLAT may suffice, while larger datasets (over 2GB) can benefit from HNSW for improved search speed, whilst still maintaining high recall.
In cases of exceptionally large datasets, combining IVF with a quantization method remains a preferred approach to prevent memory overload.

- Created by Vsevolod Kovalev, last modified by Maksim Timonin on Nov 16, 2025

- **DESCRIPTION** - Architecture
  - Concepts
- **Vector Fields Types**
- **Examples of create collection**
- **DATA** - Data Structures in Segments
  - Compaction

…

- **Proxy:** Stateless gateway, a single entry point for clients. Handles validation, request routing, and **reduce**/aggregation of results (role description).
- **Worker Nodes:** Perform the actual data work. Divided into three types:

  - **Streaming Node:** Processes streaming inserts/deletes, maintains WAL
  - **Query Node:** Executes search queries, loading segments/indexes from object storage; can build a **temporary index** for growing segments (parameter).
  - **Data Node:** Performs background tasks: compaction and index building (triggered by DataCoord, compaction).
- **Storage Layer:** Stores data and indexes in MinIO/S3 object storage (general description).

### Concepts

|Term in Milvus|Essence in Milvus|
|--|--|
|**Collection**|A logical group of vector and scalar data (analogous to a table).|
|**Segment**|A physical fragment of a collection’s data; the unit of management for flush, compaction, and indexing.|
|**Growing Segment**|An "active" segment receiving current inserts. Data is in memory, an index is often not yet built.|
|**Sealed Segment**|A segment whose data has been flushed to object storage (S3/MinIO) and is immutable; sealed segments carry raw vectors and any built indexes on disk.|
|**Vector Index (IVF_PQ, HNSW)**|Specialized data structures for ANN. Built asynchronously for **each** sealed segments; until the index is ready, QueryNode falls back to brute-force on raw vectors.|
|**HNSW**|Graph-based multi-layer proximity index (via Knowhere). Key build params: **M** (neighbors per node) and **efConstruction** (candidate pool). High recall, higher memory.|
|**IVF**|K-means partitions vectors into **nlist** clusters (typ. 128). Search probes **nprobe** clusters (typ. 8). IVF_FLAT stores raw vectors; IVF_PQ compresses them.|
|**IVF_PQ**|IVF with product quantization: split D-dim vector into **m** sub-vectors and encode each with **nbits**-bit codebooks. Stores coarse centroids, PQ codebooks, and codes.|

…

### Vector Field Types

Milvus supports **multi-vector** schemas so you can combine dense, binary, and sparse embeddings in one collection (default **up to 4** vector fields; configurable to **10** via `proxy.maxVectorFieldNum`). See Multi-Vector Hybrid Search and `proxy` config.

…

- **`FLOAT_VECTOR` (dense, fp32)** — standard dense embeddings; `dim` is required. .
- **`FLOAT16_VECTOR` (dense, fp16)** — half-precision dense vectors; `dim` required. .
- **`BFLOAT16_VECTOR` (dense, bfloat16)** — bfloat16 dense vectors; `dim` required.
- **`INT8_VECTOR` (dense, int8)** — quantized dense embeddings; `dim` is required.
- **`BINARY_VECTOR` (bit vectors)** — `dim` **must be a multiple of 8** (bits are packed into bytes). Metrics: Hamming/Jaccard/MH-Jaccard. See Binary Vector.

…

### Vector Index Storage & Lifecycle

#### Where indexes live
- **Growing segments (in-memory):** fresh inserts land in a *growing* segment in DataNode RAM and are mirrored to QueryNodes so the newest data is searchable immediately. By default, growing data has **no on-disk index**; searches fall back to in-memory scan, optionally accelerated by a transient in-memory “growing” index. This acceleration is ephemeral and rebuilt as the segment evolves. In newer versions, the index is not built initially, but once the segment exceeds a configurable threshold (e.g. number of rows or pages), a temporary in-memory index may be built.
- **Sealed segments (persistent):** when a flush/threshold triggers, Milvus **seals** the segment, writes **binlogs** (columnar, per-field) to object storage (S3/MinIO), and schedules an **asynchronous index build** (HNSW or IVF/IVF_PQ). The resulting **index artifacts** are also stored in object storage. QueryNodes **load on demand** (often via `mmap`) and start using the index once available; until then, they search the raw vectors. See docs on data processing & sealing and object storage.

…

#### Data structures & serialization

Milvus integrates optimized ANN implementations via **Knowhere** (wrapping FAISS, hnswlib, etc.), exposing a unified `Serialize()/Load()` for each index. See Knowhere.
- **HNSW:** a multi-layer proximity graph: every vector is a node with up to **M** neighbors per layer; upper layers are sparse for long hops; layer 0 contains all points. The serialized artifact stores the entry point and per-node adjacency. Milvus typically keeps **original vectors in binlogs**, not the graph file, which keeps the index compact; distances can be recomputed against resident/raw data as needed. Common knobs: `M` (~30) and `efConstruction` (~360), with query-time `ef`. See HNSW.
- **IVF_FLAT:** k-means partitions the space into **`nlist`** coarse centroids, then each vector is assigned to the nearest list. At query time, Milvus probes **`nprobe`** lists and scans their raw vectors (no compression). The index artifact persists centroids and inverted lists; raw vectors remain in binlogs. See IVF_FLAT.
- **IVF_PQ:** IVF plus **product quantization** of residuals/vectors for large memory savings. The artifact stores the coarse centroids, **PQ codebooks** and the compact codes. Common knobs include `nlist`, `m` (sub-vectors), and `nbits` (often 8). Distance is computed via asymmetric tables. See IVF_PQ.
> **Takeaway:** indexes persist **IDs/graph/centroids/codes**, not full originals; **original vectors + PKs are in binlogs**. QueryNodes load whichever artifacts are needed for a given search and consistency level.

#### Build & update lifecycle (async, non-blocking)
1. **Sealing:** DataNode flushes the growing segment (per size/time/manual triggers), writes binlogs to object storage, and marks the segment **sealed**. QueryCoord performs a **handoff** so QueryNodes begin treating it as sealed. See data processing.
2. **Index scheduling:** DataCoord enqueue an **asynchronous build task** (DataNode can execute). Build reads the sealed segment’s data, constructs the index (HNSW/IVF_PQ), and persists artifacts to object storage.
3. **Availability during build:** the sealed segment remains **queryable** using brute-force until its index is built and **loaded** on QueryNodes; other segments are unaffected. The Proxy/QueryCoord merge results across segments.

#### Consistency, concurrency & failure

Milvus provides timestamped snapshots (TSO) and configurable consistency (Strong/Bounded/Session/Eventual); searches align to a **guarantee timestamp**. Index builds proceed in parallel and **do not block** reads; if a build fails, the segment remains searchable via brute-force until the task is retried or rebuilt. See consistency and timestamping.

#### Eviction, spill & tiering (sealed artifacts)

Milvus treats sealed artifacts as read-mostly and manages them across three tiers:

…

- **Memory / OS page cache** — hottest pages live in RAM; with `mmap`, the **OS decides** which pages to reclaim; sealed data is immutable so no write-back is required. Operators bound mmap usage (e.g., `queryNode.mmap.maxDiskUsagePercentageForMmapAlloc`) and warmup behavior.
> Persistent index files live in object storage; QueryNodes **stage + `mmap`** what they need; **OS page cache handles eviction**. GC retires obsolete sealed artifacts after compaction/drop.

#### Mapping index hits to primary keys

Indexes return **internal IDs/positions**. Milvus stores **PKs and vectors as separate columns** in binlogs/in-RAM buffers and maintains a strict **row-aligned** mapping: the *i-th* PK corresponds to the *i-th* vector. After an ANN scan returns candidate row-IDs, QueryNodes resolve them to PKs (and any requested scalar fields) before reduction. See primary field and your earlier “PK mapping” notes.

…

**Serialize/Load Mechanics:** Milvus uses **Knowhere** to save indexes as opaque binary files backed by FAISS/HNSWlib implementations. For an **HNSW** index, the on-disk file records the graph’s *entry point* and per-node adjacency (layered small-world graph). For **IVF_PQ**, the file contains the coarse **centroids** (inverted lists) plus PQ **codebooks** and compact **codes**.
In both cases the format is the underlying FAISS/HNSWlib binary layout rather than a human-readable schema. Milvus does **not** duplicate full vectors in the index file—the original vectors stay in **binlogs** (object storage). Conceptually, the file has a small header of metadata (dimensions, parameters, etc.) followed by sections for centroids or graph links and code arrays. During `Load()`, Knowhere reads or **memory-maps** the file and reconstructs the internal index structure.

…

- **Operational Availability:** Because indexing is asynchronous, segments remain **queryable** throughout. While a segment’s index is being built or loaded, that segment falls back to **brute-force (IDMAP)** search on raw vectors; after loading completes, queries automatically switch to the indexed method. The Proxy/QueryCoord layer merges results across segments, so queries on one segment never block others.
- **Milvus Integration:** QueryNode fetches serialized index files from **object storage** and invokes Knowhere `Load()`; by default it stages artifacts on local disk and often uses **mmap** for efficient access. Once loaded, the segment’s `Search()` uses Knowhere routines; configuration flags under **queryNode.mmap.** govern what is memory-mapped. This end-to-end flow (seal → build index → write artifact → QueryNode load) ties into the normal segment lifecycle.

…

**Step 2: Sharding and Routing**

- The **Proxy** determines which **shard (vchannel)** to send the data to, based on the hash of the primary key (PK) or the partition key value.
- At any given moment, the shard is served by a specific **Streaming Node**, and the distribution can change due to load balancing.

…

- For the sealed segment, the **Data Node** initiates an asynchronous process to build the vector index (e.g., **IVF_PQ** or **HNSW**) (index building and node roles).
- The finished index files are saved to **object storage (S3/MinIO)** (where indexes are stored).

…

#### Vector Search Inside a Segment

Milvus uses an index per segment. **Indexes store structural metadata and internal row IDs—not full vectors.** Original vectors always live in the segment’s binlog and are accessed via mmap during scoring/refinement (see the IVF overview and HNSW overview). After a segment search, the engine returns top-K *(distance, internalID)* pairs.

#### IVF
1. **Coarse routing.** The query compares to all coarse centroids and selects the *nprobe* closest inverted lists (`nprobe`).
2. **Candidate scan.** Within those lists, IVF retrieves the **internal IDs** of member vectors from the index artifact and evaluates exact (IVF_FLAT) or code-table (IVF_PQ) distances using the **vectors mapped from binlog** (IVF overview).

…

#### Vector/PK mapping

Indexes operate on **internal row positions**. Milvus stores the primary key column separately but row-aligned with the vector column. After ANN returns internalIDs, QueryNode looks up the corresponding **user PKs** (and any payload fields) by these positions before emitting results (ASF summary).

**Step 4: Local shard reduction**

…

> Use `ignore_growing` to trade off freshness vs. latency; use partitions/filters to limit segment fan-out.
> HNSW is controlled by `ef`; IVF by `nprobe`.
> Growing-segment acceleration uses a temporary index when enabled; otherwise it’s a linear scan.

…

**2. How is the link between a vector and its primary key implemented in Milvus?**

The link is ensured by a **strict index-based binding** within the segment. Data is stored in columns: separate arrays for PKs, vectors, and scalar fields. The i-th element in the primary key array always corresponds to the i-th element in the vector array. During index-based search, the engine returns an internal identifier (position), which the system uses to unambiguously find the corresponding PK and vector (column-oriented storage · data/segment organization).

…

- **HNSW:** Graph-based algorithm. **Application:** High-speed search with maximum accuracy for data that fits in RAM. **Pros:** Highest speed and quality. **Cons:** High memory consumption.
- **IVF:** Clustering-based algorithm (index overview and scenarios · IVF_FLAT). **Application:** Search in very large collections (billions of vectors). **Pros:** High speed by narrowing the search scope. **Cons:** Requires pre-training (clustering); accuracy is lower than HNSW.
- **PQ:** Compression method (IVF_PQ). **Application:** Significant memory savings for huge datasets. **Pros:** Drastically reduces data volume. **Cons:** Reduces accuracy. Often used in combination (e.g., IVF_PQ).

**5. Does Milvus use a two-level index architecture (e.g., to combine speed and accuracy)?**
Yes, it does. A fast but approximate algorithm (first level) creates a shortlist of candidates, which is then rechecked and refined by a more accurate method (second level).

- **Example:** IVF quickly finds ~200 candidates, then exact distances are calculated for them using uncompressed vectors to return the top-100 most accurate results (reranking/refine).
- **Example:** Index types like `HNSW_PQ` (graph built on compressed data) with a `refine` option for recalculating distances.

…

- **IVF:** `nlist` (number of clusters, affects accuracy and memory), `nprobe` (number of clusters probed during search, affects search speed and accuracy).
- **HNSW:** `M` (number of connections, affects accuracy and memory), `efConstruction` (affects graph build quality), `ef` (search depth, affects search speed and accuracy).

…

1. **Local Search:** Each **QueryNode** performs a search on its segments, finding a local top-K list of candidates (multi-level reduction).
2. **Shard Aggregation:** The **Streaming Node** aggregates results from different QueryNodes within its shard (description of the Streaming Node role and shard-level reduction).