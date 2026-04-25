# Source: https://blog.langchain.dev/is-langgraph-used-in-production/
# Author: LangChain
# Author Slug: langchain
# Title: Is LangGraph Used In Production?
# Fetched via: browser
# Date: 2026-04-10

Leading companies like Uber, LinkedIn, and Replit are choosing LangGraph to build agents that are not only powerful but also reliable. In 2024, the focus shifted towards specialized AI agents designed for specific business needs. But getting AI agents production-ready isn’t as simple as plugging in an LLM to produce intelligent outputs. Companies need solutions that provide reliability, observability, and control. 

This piece explores the key challenges of putting AI agents into production and how leading companies like Uber, LinkedIn, and Replit are overcoming them, with some help from LangGraph. 🪄

Many companies are choosing LangGraph for reliable agents

Companies across a variety of industries are turning to LangGraph to build scalable agent systems. LinkedIn streamlined hiring by building an AI-powered recruiter that automates candidate sourcing, matching, and messaging. Their hierarchical agent system, built on LangGraph, has freed up their human recruiters to focus on high-level strategy – resulting in more efficient hiring.

Another example of operational efficiency — AppFolio created a copilot that’s saved over 10 hours a week for their property managers, as LangGraph helped them cut app latency and 2x the accuracy of their decisions.

For Uber and Replit, LangGraph greatly sped up the development cycle when scaling up complex workflows. Replit’s AI agent acts as a copilot for building software from scratch; with LangGraph under the hood, they’ve architected a multi-agent system with human-in-the-loop capabilities (so users can see their agent actions, from package installations to file creation) - making development more transparent.

Uber integrated LangGraph to streamline large-scale code migrations within their developer platform. They carefully structured a network of specialized agents so that each step of their unit test generation was handled with precision. Similarly, Elastic has used LangGraph to orchestrate their network of AI agents for real-time threat detection – which has helped them respond to security risks much more quickly and effectively.

Why is it so hard to put AI agents into production?

While LLM-powered agents hold immense promise, getting them production-ready is challenging - especially when it comes to ensuring performance quality and reliability. 

Performance quality was the top challenge for respondents in the "State of AI Agents" survey ran by LangChain in the tail end of 2024

From working closely with hundreds of companies, we see the following key hurdles to deploying agents in production: 

Unpredictability of LLMs - Unlike traditional software, AI agents don’t follow a fixed set of rules. Instead, they generate responses dynamically. On top of that, the UX for agents allows for free-form text input, including unpredictable human speech – making it difficult to guarantee accurate and contextually-appropriate responses. 
Complexity of orchestration - Many real-world applications require multiple agents to work together, with each handling different tasks. Coordinating them effectively — including managing task dependencies, error recovery, and communication – adds another layer of difficulty.
Observability and debugging limitations - When an agent makes a bad decision, understanding why can feel like a shot in the dark. Diagnosing failures and maintaining performance require robust tracing and monitoring, which most agent frameworks don’t have built-in.

Given these hurdles, we see most companies choosing a framework to have the right tool set to meet their bar for shipping to production. This is also where LangGraph comes into play. 

What is LangGraph?

LangGraph is a controllable agent framework designed for production use. Unlike other agentic frameworks, LangGraph is:

Low-level and customizable – LangGraph allows you to flexibly design agents for your company’s bespoke needs. LangGraph primitives are fully descriptive and, unlike higher-level abstractions, can scale beyond prototyping. 
Highly reliable – Gain full control over agent actions with moderation checks, human-in-the-loop, and persisted context for long-running workflows — so your agent can stay on course. 
Optimized for observability – While LangGraph doesn’t depend on any other LangChain product, it integrates seamlessly with LangSmith for added visibility into agent interactions, performance monitoring, and debugging.

When we built LangGraph in early 2024, we intentionally gave developers the choice to structure their agents without the limitations of black-box architectures. LangGraph has since become the default framework for many agentic applications in production. We learned from LangChain that while higher level abstractions helped developers get started quickly, it’s the lower level flexibility that can handle varied production queries. LangGraph has a steeper learning curve, but users find they don't scale off of it.

The future of AI agents with LangGraph

As we enter 2025, LangGraph is poised to drive the next wave of AI agent adoption. By building on the lessons learned from these leading companies, we aim to empower more developers to build reliable, production-ready AI agents.

Looking for more insights? Check out the latest stories on how companies are using LangGraph, or explore our latest video tutorial on how to build effective AI agents.

JOIN OUR NEWSLETTER

Updates from the LangChain team and community

Enter your email
Subscribe