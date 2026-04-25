# Source: https://platform.openai.com/docs
# Fetched via: headless browser (Playwright)
# Downloaded: 2026-04-09
# Words: 261
# Author: OpenAI
# Author Slug: openai
API Platform
Developer quickstart

Make your first API request in minutes. Learn the basics of the OpenAI platform.

Get started
javascript
1
2
3
4
5
6
7
8
9

import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
  model: "gpt-5.4",
  input: "Write a short bedtime story about a unicorn.",
});

console.log(response.output_text);
Models
Start with gpt-5.4 for complex reasoning and coding, or choose gpt-5.4-mini and gpt-5.4-nano for lower-latency, lower-cost workloads.
View all
GPT-5.4
New
Best intelligence at scale for agentic, coding, and professional workflows
GPT-5.4 mini
New
Our strongest mini model yet for coding, computer use, and subagents
GPT-5.4 nano
New
Our cheapest GPT-5.4-class model for simple high-volume tasks
Start building
Read and generate text
Use the API to prompt a model and generate text
Use a model's vision capabilities
Allow models to see and analyze images in your application
Generate images as output
Create images with GPT Image 1
Build apps with audio
Analyze, transcribe, and generate audio with API endpoints
Build agentic applications
Use the API to build agents that use tools and computers
Achieve complex tasks with reasoning
Use reasoning models to carry out complex tasks
Get structured data from models
Use Structured Outputs to get model responses that adhere to a JSON schema
Tailor to your use case
Adjust our models to perform specifically for your use case with fine-tuning, evals, and distillation
Help center
Frequently asked account and billing questions
Developer forum
Discuss topics with other developers
Cookbook
Open-source collection of examples and guides
Status
Check the status of OpenAI services