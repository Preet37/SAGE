# Card: ROS 2 QoS Policies + Standard Profiles (Iron)
**Source:** https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** ROS 2 QoS policy definitions + predefined QoS profiles (defaults for pub/sub, services, sensor data, parameters) and compatibility rules.

## Key Content
- **QoS = profile of policies** applied per publisher/subscription/service client/server; **incompatible QoS can prevent any message delivery**.
- **Core QoS policies (definitions):**
  - **History:** *Keep last* (store up to **N** samples) vs *Keep all* (store all, limited by middleware resources).
  - **Depth:** queue size **N**, **only honored if History=Keep last**.
  - **Reliability:** *Best effort* (may drop) vs *Reliable* (guaranteed delivery; may retry).
  - **Durability:** *Transient local* (publisher persists samples for late joiners) vs *Volatile* (no persistence).
  - **Deadline:** expected max time between publishes.
  - **Lifespan:** max time from publish to receive before message is **stale**; expired messages **silently dropped**.
  - **Liveliness:** *Automatic* vs *Manual by topic* (publisher must assert alive via API).
  - **Lease duration:** max time allowed without liveliness assertion before considered lost.
- **Default pub/sub profile (ROS 1–like):** History=Keep last, **Depth=10**, Reliability=Reliable, Durability=Volatile, Liveliness=System default; Deadline/Lifespan/Lease duration = Default (unspecified).
- **Services profile rationale:** **Reliable + Volatile** (avoid restarted servers receiving **outdated requests**; client protected from multiple responses, server not protected from side-effects).
- **Sensor data profile rationale:** prioritize timeliness over completeness → **Best effort** + **smaller queue** (than default).
- **Parameters profile:** like services but **much larger depth** to avoid losing requests when client can’t reach server.
- **Compatibility model (Request vs Offered):** subscriber requests “minimum acceptable”; publisher offers “maximum provided”; connect only if **every policy** requested is **not more stringent** than offered.
  - **Reliability compatibility (Pub→Sub):** BE→BE Yes; BE→Reliable **No**; Reliable→BE Yes; Reliable→Reliable Yes.
  - **Durability compatibility:** Volatile→Transient local **No**; Transient local→Transient local Yes (**new+old**); Transient local→Volatile Yes (**new only**). **Latched behavior requires both sides Transient local.**
  - **Deadline/Lease duration:** Default→x **No**; x→Default Yes; x→y compatible iff **y ≥ x**.
  - **Liveliness:** Automatic→Manual **No**; Manual→Automatic Yes.
- **QoS events:** offered/requested deadline missed, liveliness lost/changed, offered/requested incompatible QoS; plus **matched events** on connect/disconnect.

## When to surface
Use when students ask how to choose ROS 2 QoS for sensors vs services/parameters, why messages aren’t arriving (QoS incompatibility), or how reliability/durability/deadline/liveliness settings affect real-time robot perception-action loops.