TUTOR_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": (
                "Semantic web search powered by Perplexity. Returns 3 rich results (up to 5K chars each). "
                "Write queries as natural questions, NOT keyword strings — e.g. 'What rank values did Hu et al. "
                "test in the LoRA ablation study and what were the results?' is far better than "
                "'LoRA rank 1 2 4 8 ablation Hu 2021'. One good query usually suffices; avoid "
                "re-searching the same topic. Each call adds ~3s latency."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_lesson_context",
            "description": (
                "Retrieve the full content, concepts, and curated resources for a lesson. "
                "Use the lesson slug from the curriculum index to look up any lesson. "
                "Use this when the learner asks about topics covered in other lessons."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_slug": {
                        "type": "string",
                        "description": "The slug of the lesson (e.g. 'attention-mechanism')",
                    },
                    "lesson_id": {
                        "type": "string",
                        "description": "The ID of the lesson (alternative to slug)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_lesson_transcript",
            "description": (
                "Retrieve the full video transcript for the current or another lesson. "
                "Use this when the learner asks about specific parts of the video, "
                "wants more detail on what the instructor said, or references a timestamp."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_slug": {
                        "type": "string",
                        "description": "The slug of the lesson (from curriculum index)",
                    },
                    "lesson_id": {
                        "type": "string",
                        "description": "The ID of the lesson (alternative to slug)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_lesson_reference_kb",
            "description": (
                "Retrieve the pre-searched reference knowledge base for a lesson. "
                "Contains verified facts, paper results, benchmarks, and implementation "
                "details gathered from authoritative sources. Use this to ground specific "
                "claims in verified information. Provide a lesson slug from the curriculum map."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_slug": {
                        "type": "string",
                        "description": "The slug of the lesson (e.g. 'attention-mechanism')",
                    },
                    "lesson_id": {
                        "type": "string",
                        "description": "The ID of the lesson (alternative to slug)",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_curated_resources",
            "description": (
                "Get curated teaching resources (videos, blogs, papers) for specific "
                "concepts from the pedagogy wiki. Returns structured resource entries "
                "with educator names, titles, URLs, YouTube IDs, and pedagogical "
                "justifications. Use proactively when a well-timed video clip or blog "
                "post would deepen the learner's understanding — for example, before "
                "diving into math, after introducing a concept, or when a visual "
                "explanation would help. Output resources using <resource> tags."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concepts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Concepts to find curated resources for "
                            "(e.g. ['self-attention', 'transformer architecture'])"
                        ),
                    },
                },
                "required": ["concepts"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_relevant_images",
            "description": (
                "Get curated educational images (diagrams, visualizations, charts) "
                "for specific concepts from the pedagogy wiki. Returns image paths, "
                "captions, and guidance on when to show each image. Use this when "
                "a visual diagram would help the student understand — e.g. attention "
                "weight heatmaps, architecture diagrams, encoder-decoder flow charts, "
                "or training curves. Output results using <image> tags."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "concepts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "Concepts to find images for "
                            "(e.g. ['bahdanau attention', 'alignment scores'])"
                        ),
                    },
                },
                "required": ["concepts"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_progress",
            "description": (
                "Get the learner's progress including which lessons they have completed. "
                "Use this to personalize responses based on what the learner already knows."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "lesson_id": {
                        "type": "string",
                        "description": "The current lesson ID to check progress context for",
                    }
                },
                "required": ["lesson_id"],
            },
        },
    },
]
