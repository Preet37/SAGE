# Card: Omniverse end-to-end Gaussian Splatting pipeline (tools + workflow map)
**Source:** https://www.youtube.com/watch?v=KZqv3Z5rRg8  
**Role:** explainer | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end Omniverse pipeline walkthrough (capture/ingest → train splats → visualize/stream in Omniverse), including practical integration steps and tooling choices.

## Key Content
- **Use case framing:** Gaussian Splatting positioned as a method for **real-time 3D reconstruction** supporting **spatial intelligence** applications such as **geospatial digital twins** and **media & entertainment** workflows.
- **Pipeline components called out (library/tooling index):**
  - **NVIDIA Omniverse workflows** for:  
    1) **city-scale capture**,  
    2) **virtual production environments**,  
    3) **dynamic scene rendering**.
  - **Key spatial intelligence libraries mentioned for integration:**
    - **Omniverse NuRec**
    - **3DGRUT**
    - **PPISP**
- **Data/scene representation anchor:** Integration is described as **USD-based Omniverse pipelines** (OpenUSD as the scene interchange/assembly layer for bringing reconstructed content into Omniverse for visualization/rendering/streaming).
- **Practical integration emphasis:** The session is explicitly about “**building pipelines**” (not just theory): how Gaussian Splatting fits into Omniverse workflows from reconstruction outputs into **Omniverse visualization and rendering** contexts.

## When to surface
Use this card when a student asks how to structure an **end-to-end Gaussian Splatting production pipeline** inside **NVIDIA Omniverse/OpenUSD**, or which **Omniverse libraries** (NuRec, 3DGRUT, PPISP) are referenced for spatial intelligence/digital twin workflows.