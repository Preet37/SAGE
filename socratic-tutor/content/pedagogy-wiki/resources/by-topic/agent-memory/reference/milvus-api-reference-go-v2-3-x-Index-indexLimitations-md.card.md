# Source: https://milvus.io/api-reference/go/v2.3.x/Index/indexLimitations.md
# Title: Index Parameter Range - Milvus go sdk v2.3.x/Index
# Fetched via: jina
# Date: 2026-04-10

Title: Index Parameter Range - Milvus go sdk v2.3.x/Index


# Index Parameter Range - Milvus go sdk v2.3.x/Index

[🚀 Zilliz Cloud: fully managed Milvus — 10x faster. Zero hassle. Built for AI.Try Free Now →](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_top_banner&utm_content=api-reference/go/v2.3.x/Index/indexLimitations.md)


*   
Why Milvus

    *   [What is Milvus](https://milvus.io/intro)
    *   [Use Cases](https://milvus.io/use-cases)

*   [Docs](https://milvus.io/docs)
*   
Tutorials

    *   [Bootcamp](https://milvus.io/bootcamp)
    *   [Demos](https://milvus.io/milvus-demos)
    *   [Video](https://www.youtube.com/c/MilvusVectorDatabase)

*   
Tools

    *   [Attu](https://github.com/zilliztech/attu)
    *   [Milvus CLI](https://github.com/zilliztech/milvus_cli)
    *   [Sizing Tool](https://milvus.io/tools/sizing)
    *   [Milvus Backup](https://github.com/zilliztech/milvus-backup)
    *   [VTS](https://github.com/zilliztech/vts)
    *   [Deep Searcher](https://github.com/zilliztech/deep-searcher)
    *   [Claude Context](https://github.com/zilliztech/claude-context)

*   [Blog](https://milvus.io/blog)
*   
Community

    *   [Milvus Office Hours](https://meetings.hubspot.com/chloe-williams1/milvus-office-hour?uuid=4cb203e5-482a-47e0-90a6-7acc511d61f4)
    *   [Discord](https://milvus.io/discord)
    *   [GitHub](https://github.com/milvus-io/milvus/discussions)
    *   [More Channels](https://milvus.io/community)

[Star 43.7K](https://github.com/milvus-io/milvus)[Book a Demo](https://milvus.io/contact)[Try Managed Milvus](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_nav_right&utm_content=api-reference/go/v2.3.x/Index/indexLimitations.md)


*   [Docs](https://milvus.io/docs)

* * *

*   Tutorials

* * *

*   Tools

* * *

*   [Blog](https://milvus.io/blog)

* * *

*   Community

[Book a Demo](https://milvus.io/contact)[Try Managed Milvus](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_nav_right&utm_content=api-reference/go/v2.3.x/Index/indexLimitations.md)

[< Docs](https://milvus.io/docs)

v2.3.x
*   [v2.6.x](https://milvus.io/api-reference/go/v2.6.x/About.md)
*   [v2.5.x](https://milvus.io/api-reference/go/v2.5.x/About.md)
*   [v2.4.x](https://milvus.io/api-reference/go/v2.4.x/About.md)
*   [v2.3.x](https://milvus.io/api-reference/go/v2.3.x/About.md)
*   [v2.2.x](https://milvus.io/api-reference/go/v2.2.x/About.md)

*   
Go 

    *   Collection   
    *   Connections   
    *   
Index 

        *   [CreateIndex()](https://milvus.io/api-reference/go/v2.3.x/Index/CreateIndex().md) 
        *   [DescribeIndex()](https://milvus.io/api-reference/go/v2.3.x/Index/DescribeIndex().md) 
        *   [DropIndex()](https://milvus.io/api-reference/go/v2.3.x/Index/DropIndex().md) 
        *   [GetIndexBuildProgress()](https://milvus.io/api-reference/go/v2.3.x/Index/GetIndexBuildProgress().md) 
        *   [indexLimitations](https://milvus.io/api-reference/go/v2.3.x/Index/indexLimitations.md) 

    *   Partition   

*   [Home](https://milvus.io/)
*   [Docs](https://milvus.io/docs/v2.3.x)
*   [API Reference](https://milvus.io/api-reference/go/v2.3.x/About.md)
*   Go

*   Index

*   indexLimitations

Copy page

# Index Parameter Range

Searching with most indexes that Milvus supported requires specifying construction and search parameters. Listed below are the type and ranges of these parameters.

| Index | Type | Const. Param & Range | Search Param & Range | Note |
| --- | --- | --- | --- | --- |
| Flat | entity.Flat | N/A | N/A | No parameter is required for search with Flat. |
| BinFlat | entity.BinFlat | `nlist`∈[1, 65536] | `nprobe`∈[1, `nlist`] |  |
| IvfFlat | entity.IvfFlat | `nlist`∈[1, 65536] | `nprobe`∈[1, `nlist`] |  |
| BinIvfFlat | entity.BinIvfFlat | `nlist`∈[1, 65536] | `nprobe`∈[1, `nlist`] | BinIvfFlat will be supported in upcoming version of Milvus. |
| IvfSQ8 | entity.IvfSQ8 | `nlist`∈[1, 65536] | `nprobe`∈[1, `nlist`] |  |
| IvfSQ8H | entity.IvfSQ8H | `nlist`∈[1, 65536] | `nprobe`∈[1, `nlist`] |  |
| IvfPQ | entity.IvfPQ | `nlist`∈[1, 65536] `m` dim===0 (mod self) `nbits`∈[1, 16] | `nprobe`∈[1, `nlist`] |  |
| RNSG | entity.NSG | `out_degree`∈[5, 300] `candidate_pool_size`∈[50, 1000] `search_length`∈[10, 300] `knng`∈[5, 300] | `search_length`∈[10, 300] |  |
| HNSW | entity.HNSW | `M`∈[4, 64] `efConstruction`∈[8, 512] | `ef`∈[topK, 32768] |  |
| RHNSWFlat | entity.RHNSWFlat | `M`∈[4, 64] `efConstruction`∈[8, 512] | `ef`∈[topK, 32768] |  |
| RHNSW_PQ | entity.RHNSW_PQ | `M`∈[4, 64] `efConstruction`∈[8, 512] `PQM` dim===0 (mod self) | `ef`∈[topK, 32768] |  |
| RHNSW_SQ | entity.RHNSWSQ | `M`∈[4, 64] `efConstruction`∈[8, 512] | `ef`∈[topK, 32768] |  |
| IvfHNSW | entity.IvfHNSW | `nlist`∈[1, 65536] `M`∈[4, 64] `efConstruction`∈[8, 512] | `nprobe`∈[1, `nlist`] `ef`∈[topK, 32768] |  |
| ANNOY | entity.ANNOY | `n_trees`∈[1, 1024] | `search_k`∈-1 or [topk, n * n_trees] |  |
| NGTPANNG | entity.NGTPANNG | `edge_size`∈[1, 200] `forcedly_pruned_edge_size`∈[selectively_pruned_edge_size + 1, 200] `selectively_pruned_edge_size`∈[1, forcedly_pruned_edge_size -1 ] | `max_search_edges`∈[-1, 200] `epsilon`∈[-1.0, 1.0] | Search parameter epsilon type is float64. |
| NGTONNG | entity.NGTONNG | `edge_size`∈[1, 200] `outgoing_edge_size`∈[1, 200] `incoming_edge_size`∈[1, 200] | `max_search_edges`∈[-1, 200] `epsilon`∈[-1.0, 1.0] | Search parameter epsilon type is float64. |

## Try Managed Milvus for Free

Zilliz Cloud is hassle-free, powered by Milvus and 10x faster.

[Get Started](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_right_card&utm_content=api-reference/go/v2.3.x/Index/indexLimitations.md)

*   [Edit this page](https://github.com/milvus-io/web-content/edit/master/API_Reference/milvus-sdk-go/v2.3.x/Index/indexLimitations.md)
*   [Create an issue](https://github.com/milvus-io/web-content/issues/new/choose)

##### Feedback

Was this page helpful?



Made with Love ![Image 8: Blue Heart Emoji](https://milvus.io/images/blue-heart.webp) by the Devs from [Zilliz](https://zilliz.com/)

### Get Milvus Updates

Subscribe

Follow Us

[](https://github.com/milvus-io/milvus)[](https://twitter.com/milvusio)[](https://milvus.io/discord)[](https://www.linkedin.com/company/the-milvus-project/)[](https://www.youtube.com/channel/UCMCo_F7pKjMHBlfyxwOPw-g)

Ask AI about Milvus


Copyright © Milvus. 2026 All rights reserved.

Resources

*   [Docs](https://milvus.io/docs)
*   [Blog](https://milvus.io/blog)
*   [Managed Milvus](https://cloud.zilliz.com/signup?utm_source=milvusio&utm_medium=referral&utm_campaign=milvus_footer&utm_content=api-reference/go/v2.3.x/Index/indexLimitations.md)
*   [Book a Demo](https://milvus.io/contact)
*   [AI Quick Reference](https://milvus.io/ai-quick-reference)

Tutorials

*   [Bootcamps](https://milvus.io/bootcamp)
*   [Demo](https://milvus.io/milvus-demos)
*   [Video](https://www.youtube.com/c/MilvusVectorDatabase)

Tools

*   [Attu](https://github.com/zilliztech/attu)
*   [Milvus CLI](https://github.com/zilliztech/milvus_cli)
*   [Milvus Sizing Tool](https://milvus.io/tools/sizing)
*   [Milvus Backup Tool](https://github.com/zilliztech/milvus-backup)
*   [Vector Transport Service (VTS)](https://github.com/zilliztech/vts)
*   [Deep Searcher](https://github.com/zilliztech/deep-searcher)
*   [Claude Context](https://github.com/zilliztech/claude-context)

Community

*   [Milvus Office Hours](https://meetings.hubspot.com/chloe-williams1/milvus-office-hour?uuid=4cb203e5-482a-47e0-90a6-7acc511d61f4)
*   [Discord](https://milvus.io/discord)
*   [Github](https://github.com/milvus-io/milvus)

Ask AI![Image 14: Ask AI](https://milvus.io/inkeep/milvus-icon-white.png)

How we use cookies

This website stores cookies on your computer. By continuing to browse or by clicking ‘Accept’, you agree to the storing of cookies on your device to enhance your site experience and for analytical purposes.

Reject Accept