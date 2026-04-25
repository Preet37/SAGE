# Card: OTel Tracing SDK essentials (sampling + processors/exporters)
**Source:** https://opentelemetry.io/docs/specs/otel/trace/sdk/  
**Role:** reference_doc | **Need:** COMPARISON_DATA  
**Anchor:** Canonical SDK semantics for span recording vs sampling, parent-based sampling, span processors/exporters, defaults.

## Key Content
- **Two gating signals for data flow**
  - `Span.IsRecording` (bool): if `false`, span discards attributes/events/status; **SpanProcessors MUST receive only spans with `IsRecording=true`**.
  - `SpanContext.TraceFlags.Sampled` (bool): propagated to children; indicates span will be exported; **SpanExporters MUST receive spans only when `Sampled=true`**.
  - **Forbidden combo:** `Sampled=true` & `IsRecording=false` **MUST NOT be allowed** (would create trace gaps).
- **Recording/Sampled reaction table**
  - `IsRecording=true, Sampled=true` → Processor: yes; Exporter: yes  
  - `IsRecording=true, Sampled=false` → Processor: yes; Exporter: no  
  - `IsRecording=false, Sampled=false` → Processor: no; Exporter: no
- **SDK span creation procedure (ordered)**
  1) Use parent trace ID if valid else generate new trace ID (**before** sampling).  
  2) Call `Sampler.ShouldSample(...)`.  
  3) Generate new span ID **regardless** of sampling decision.  
  4) Create recording/non-recording span per decision (`DROP`, `RECORD_ONLY`, `RECORD_AND_SAMPLE`).
- **Sampler API**
  - `ShouldSample(parentContext, traceId, name, kind, attributes, links) -> SamplingResult`
  - Decisions: `DROP` (IsRecording=false), `RECORD_ONLY` (IsRecording=true, Sampled=false), `RECORD_AND_SAMPLE` (IsRecording=true, Sampled=true).
- **Built-in sampler defaults**
  - **Default sampler:** `ParentBased(root=AlwaysOn)`.
  - `ParentBased` routing (defaults): remote/local parent sampled→`AlwaysOn`; not sampled→`AlwaysOff`.
- **BatchSpanProcessor defaults**
  - `maxQueueSize=2048`, `scheduledDelayMillis=5000`, `exportTimeoutMillis=30000`, `maxExportBatchSize=512` (≤ queue).
- **Span limits defaults**
  - `EventCountLimit=128`, `LinkCountLimit=128`, `AttributePerEventCountLimit=128`, `AttributePerLinkCountLimit=128`.

## When to surface
Use when students ask how OTel decides what gets recorded vs exported, how parent-based sampling works, or how processors/exporters and batching defaults affect observability pipelines (e.g., comparing LangSmith traces to OTel spans).