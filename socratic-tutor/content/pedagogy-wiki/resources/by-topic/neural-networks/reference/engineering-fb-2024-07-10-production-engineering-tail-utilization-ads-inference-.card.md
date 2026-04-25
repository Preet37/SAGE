# Card: Tail-utilization optimizations for ads model inference (Meta)
**Source:** https://engineering.fb.com/2024/07/10/production-engineering/tail-utilization-ads-inference-meta/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production metrics: timeout failures ↓ ~2/3, same resources → ~35% more work, p99 latency ↓ ~1/2 via tail-utilization optimizations.

## Key Content
- **Definition (tail utilization):** utilization level of the **top 5% of servers** when ranked by utilization (i.e., 95th-percentile server utilization across fleet).
- **Empirical results (fleet-level):**
  - **Timeout error rate reduced by ~two-thirds**.
  - **Compute footprint delivered ~35% more work** with **no additional resources** (absorbed up to **35% load increase**).
  - **p99 latency cut by ~half**.
- **System context/workflow:**
  - Client request → ads core services → **model inference service**; one client request often triggers **multiple model inferences** (experiments/page type/ad attributes).
  - Service is **sharded**: each **model = shard**; multiple models can be hosted on one job host.
  - Uses **ServiceRouter** (service discovery + load balancing) and **Shard Manager** (shard scaling + placement across heterogeneous hardware).
- **Load balancing approaches:**
  - **Routing LB:** balance across replicas of a model (ServiceRouter).
  - **Placement LB:** move replicas across hosts to tighten utilization distribution (Shard Manager tuning: **load bands, thresholds, balancing frequency**).
- **Key procedures/algorithms & rationale:**
  - **Power of Two Choices** randomized LB using **polling** for fresh load (extra hop negligible for inference requests **>10s of ms**); avoids stale-load randomness from load-header.
  - **Per-model load counter** (instead of host-level outstanding requests) to align assumptions of **ReplicaEstimator + Shard Manager** (replicas should see similar load); tightened replica load distribution.
  - Preferred load counter: **“Outstanding examples CPU”** = estimated total CPU time of active requests, **normalized by #cores**.
  - **Memory bandwidth-aware placement:** memory latency rises **exponentially at ~65–70% utilization** → CPU “spikes” were stalls; treat memory bandwidth as a placement resource.
  - **Snapshot transition budget:** only transition to new model snapshot when utilization below threshold; trade-off: snapshot staleness vs failures; **fast scale-down old snapshots** to reduce staleness overhead.
  - **Cross-tier balancing:** route by **compute capacity** (not host count) + feedback controller to adjust traffic % across hardware tiers/pools.
  - **Predictive replica estimation:** forecast resource usage up to **2 hours ahead** to reduce peak-period failures vs reactive scaling.

## When to surface
Use when students ask how large-scale ML inference systems reduce tail latency/timeouts, improve utilization, or why load-balancing/placement metrics (per-model counters, memory bandwidth, p99) matter in production serving.