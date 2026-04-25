"""
Seed the SAGE database with courses, lessons, concept maps, and a demo user.
Run: python seed.py
"""
import asyncio
import json
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from passlib.context import CryptContext

DATABASE_URL = "sqlite+aiosqlite:///./sage.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed():
    from app.database import create_tables
    await create_tables()

    async with AsyncSessionLocal() as db:
        await _seed_courses(db)
        await _seed_demo_user(db)
    print("✓ Database seeded successfully")


async def _seed_demo_user(db: AsyncSession):
    from app.models.user import User
    result = await db.execute(select(User).where(User.email == "demo@sage.ai"))
    if result.scalar_one_or_none():
        return

    user = User(
        email="demo@sage.ai",
        username="demo",
        display_name="Demo Student",
        hashed_password=pwd_context.hash("demo1234"),
    )
    db.add(user)
    await db.commit()
    print("  ✓ Demo user: demo@sage.ai / demo1234")


async def _seed_courses(db: AsyncSession):
    from app.models.lesson import Course, Lesson, LessonChunk
    from app.models.concept import ConceptNode, ConceptEdge

    # ── Course 1: ML/AI Foundations ──────────────────────────────
    result = await db.execute(select(Course).where(Course.slug == "ml-ai-foundations"))
    if not result.scalar_one_or_none():
        course = Course(
            slug="ml-ai-foundations",
            title="ML/AI Foundations",
            description="From linear algebra to transformers — the mathematical and intuitive foundations of modern AI.",
            level="intermediate",
            tags=["machine-learning", "deep-learning", "transformers", "python"],
        )
        db.add(course)
        await db.flush()

        lessons_data = [
            {
                "slug": "neural-networks-basics",
                "title": "Neural Networks: The Basics",
                "order": 1,
                "summary": "Understand how neural networks compute, learn weights via backpropagation, and why depth matters.",
                "key_concepts": ["perceptron", "activation functions", "forward pass", "backpropagation", "gradient descent"],
                "estimated_minutes": 25,
                "content_md": """# Neural Networks: The Basics

## What is a Neural Network?
A neural network is a computational graph where information flows through layers of interconnected nodes (neurons). Each connection has a **weight** — a number that determines how much influence one neuron has on the next.

## The Perceptron
The simplest neural network unit:
```
output = activation(w₁x₁ + w₂x₂ + ... + wₙxₙ + bias)
```
Where `x` are inputs, `w` are weights, and `activation` introduces non-linearity.

## Activation Functions
- **ReLU**: f(x) = max(0, x) — most common in hidden layers
- **Sigmoid**: f(x) = 1/(1+e⁻ˣ) — squashes to [0,1], used for binary classification
- **Softmax**: converts logits to probability distribution

## Forward Pass
Information flows input → hidden layers → output. Each layer applies: `output = activation(W·x + b)`

## Backpropagation
The chain rule applied to compute gradients:
1. Compute loss (how wrong the network is)
2. Compute ∂loss/∂weight for each weight
3. Update: weight = weight - learning_rate × gradient

## Gradient Descent
We minimize loss by following the gradient downhill:
- **SGD**: update on each sample
- **Mini-batch**: update on small batches (most common)
- **Adam**: adaptive learning rates per parameter

## Why Depth?
Deeper networks learn hierarchical representations:
- Layer 1: edges and textures
- Layer 2: shapes and patterns
- Layer 3+: complex concepts

Universal approximation theorem: a 2-layer network can approximate any continuous function, but depth makes this practical.
""",
            },
            {
                "slug": "attention-transformers",
                "title": "Attention & Transformers",
                "order": 2,
                "summary": "How self-attention allows transformers to process sequences in parallel and why they dominate modern AI.",
                "key_concepts": ["self-attention", "multi-head attention", "positional encoding", "transformer architecture", "scaled dot-product"],
                "estimated_minutes": 30,
                "content_md": """# Attention & Transformers

## The Problem with RNNs
RNNs process sequences step by step — slow to train, poor at long-range dependencies. Attention solves this by allowing every position to directly attend to every other position.

## Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(QKᵀ / √d_k) · V
```
- **Q** (Query): what am I looking for?
- **K** (Key): what do I have to offer?
- **V** (Value): what do I actually contain?

The dot product QKᵀ computes similarity. Scaling by √d_k prevents vanishing gradients.

## Multi-Head Attention
Run attention h times with different learned projections:
```
MultiHead(Q,K,V) = Concat(head₁,...,headₕ) Wᵒ
```
Each head learns to attend to different aspects.

## Positional Encoding
Transformers process all positions in parallel — they need explicit position info:
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

## Transformer Architecture
Encoder:
- Multi-head self-attention
- Feed-forward network
- LayerNorm + residual connections

Decoder:
- Masked self-attention (can't look ahead)
- Cross-attention to encoder outputs
- Feed-forward + residuals

## Why Transformers Won
1. Parallelizable — GPUs love it
2. Long-range dependencies — O(1) path between any two positions
3. Scalable — performance improves predictably with scale (scaling laws)
""",
            },
            {
                "slug": "fine-tuning-lora",
                "title": "Fine-Tuning & LoRA",
                "order": 3,
                "summary": "Adapt large pretrained models to specific tasks efficiently using parameter-efficient fine-tuning methods.",
                "key_concepts": ["transfer learning", "full fine-tuning", "LoRA", "rank decomposition", "PEFT", "QLoRA"],
                "estimated_minutes": 25,
                "content_md": """# Fine-Tuning & LoRA

## Transfer Learning
Pretrained models capture general knowledge. Fine-tuning adapts them to specific tasks by training on task-specific data — cheaper than training from scratch.

## Full Fine-Tuning
Update all parameters. Effective but expensive:
- GPT-3 (175B params) needs ~350GB GPU RAM
- Risk of catastrophic forgetting

## Parameter-Efficient Fine-Tuning (PEFT)
Only update a small number of parameters while keeping the base model frozen.

## LoRA: Low-Rank Adaptation
Key insight: weight updates during fine-tuning have low intrinsic rank.

Instead of updating W (d×d), learn two small matrices A (d×r) and B (r×d):
```
W' = W + BA  where r << d
```

For d=4096, r=8: from 16M params to 65K — 250× compression!

During training: only A and B are updated. W is frozen.
At inference: merge W' = W + BA (no latency overhead).

## Why It Works
The update ΔW = BA lives in a low-rank subspace. Researchers found this subspace captures the task-relevant information efficiently.

## QLoRA
Quantize the base model to 4-bit, run LoRA adapters in 16-bit:
- Can fine-tune 65B model on a single 48GB GPU
- Tiny quality degradation from quantization

## Practical Tips
- r=8 to r=64 for most tasks
- Target attention matrices (Q, K, V) and FFN layers
- α (scaling factor) typically equals r
""",
            },
        ]

        for ld in lessons_data:
            lesson = Lesson(
                course_id=course.id,
                slug=ld["slug"],
                title=ld["title"],
                order=ld["order"],
                summary=ld["summary"],
                key_concepts=ld["key_concepts"],
                content_md=ld["content_md"],
                estimated_minutes=ld["estimated_minutes"],
            )
            db.add(lesson)
            await db.flush()

            # chunk and store the lesson content
            from app.core.retrieval import chunk_text
            chunks = chunk_text(ld["content_md"], chunk_size=200, overlap=40)
            for idx, chunk_text_val in enumerate(chunks):
                chunk = LessonChunk(
                    lesson_id=lesson.id,
                    chunk_index=idx,
                    text=chunk_text_val,
                )
                db.add(chunk)

        # Concept nodes for ML course
        concepts = [
            ("Perceptron", "The fundamental neural network unit", "concept"),
            ("Activation Functions", "Non-linear transformations applied to layer outputs", "concept"),
            ("Backpropagation", "Algorithm to compute gradients through the network", "skill"),
            ("Gradient Descent", "Optimization algorithm to minimize loss", "skill"),
            ("Self-Attention", "Mechanism allowing each position to attend to all others", "concept"),
            ("Transformer", "Architecture based on self-attention mechanisms", "concept"),
            ("LoRA", "Low-rank adaptation for efficient fine-tuning", "skill"),
            ("Transfer Learning", "Reusing pretrained models for new tasks", "concept"),
            ("Loss Function", "Measures how wrong the model's predictions are", "concept"),
            ("Embeddings", "Dense vector representations of tokens or concepts", "concept"),
        ]

        concept_nodes = []
        for i, (label, desc, ntype) in enumerate(concepts):
            node = ConceptNode(
                course_id=course.id,
                label=label,
                description=desc,
                node_type=ntype,
                x_pos=float(i % 4 * 200),
                y_pos=float(i // 4 * 150),
            )
            db.add(node)
            concept_nodes.append(node)

        await db.flush()

        edges = [
            (0, 2, "requires"),  # Perceptron → Backprop
            (0, 1, "requires"),  # Perceptron → Activation
            (2, 3, "requires"),  # Backprop → Gradient Descent
            (4, 5, "extends"),   # Self-Attention → Transformer
            (3, 5, "relates"),   # Gradient Descent → Transformer
            (5, 6, "requires"),  # Transformer → LoRA
            (7, 6, "requires"),  # Transfer Learning → LoRA
            (8, 3, "requires"),  # Loss → Gradient Descent
            (9, 4, "requires"),  # Embeddings → Self-Attention
        ]

        for src, tgt, etype in edges:
            edge = ConceptEdge(
                source_id=concept_nodes[src].id,
                target_id=concept_nodes[tgt].id,
                edge_type=etype,
            )
            db.add(edge)

        await db.commit()
        print("  ✓ ML/AI Foundations course seeded")

    # ── Course 2: Agentic AI ──────────────────────────────────────
    result = await db.execute(select(Course).where(Course.slug == "agentic-ai"))
    if not result.scalar_one_or_none():
        course2 = Course(
            slug="agentic-ai",
            title="Intro to Agentic AI",
            description="Build autonomous AI agents that reason, plan, use tools, and coordinate to solve complex problems.",
            level="advanced",
            tags=["agents", "llm", "tool-use", "multi-agent", "fetch-ai"],
        )
        db.add(course2)
        await db.flush()

        lesson2 = Lesson(
            course_id=course2.id,
            slug="agent-fundamentals",
            title="Agent Fundamentals",
            order=1,
            summary="What makes an AI system an agent? Perception, reasoning, action, and the agent loop.",
            key_concepts=["agent loop", "tool use", "planning", "memory", "multi-agent coordination"],
            estimated_minutes=30,
            content_md="""# Agent Fundamentals

## What is an AI Agent?
An agent perceives its environment, reasons about it, and takes actions to achieve goals. Unlike a chatbot that responds and forgets, an agent maintains state and pursues objectives over multiple steps.

## The Agent Loop
```
while not done:
    observation = perceive(environment)
    thought = reason(observation, memory, goal)
    action = plan(thought)
    result = execute(action)
    memory.update(result)
```

## Key Components
- **Perception**: reading inputs (text, images, tool outputs, sensors)
- **Reasoning**: LLM-powered thinking (chain-of-thought, ReAct, tree-of-thought)
- **Memory**: working (context window), episodic (logs), semantic (vector DB)
- **Action**: tool calls, code execution, API calls, agent spawning

## Tool Use
Modern LLMs can call functions/tools. The model decides WHEN and HOW to call them:
```json
{"tool": "search_web", "args": {"query": "current SpaceX launch"}}
```

## Planning Strategies
- **ReAct**: Reason → Act → Observe → Repeat
- **Chain-of-Thought**: Break complex reasoning into steps
- **Tree-of-Thought**: Explore multiple reasoning branches

## Multi-Agent Systems
Complex tasks can be decomposed across specialized agents:
- **Orchestrator**: coordinates, delegates
- **Specialist agents**: domain expertise
- **Communication**: shared state, message passing

## Fetch.ai & Agentverse
Fetch.ai enables autonomous agents to discover each other on a decentralized network. Agents register on Agentverse and can be discovered via ASI:One.
""",
        )
        db.add(lesson2)
        await db.commit()
        print("  ✓ Agentic AI course seeded")


if __name__ == "__main__":
    asyncio.run(seed())
