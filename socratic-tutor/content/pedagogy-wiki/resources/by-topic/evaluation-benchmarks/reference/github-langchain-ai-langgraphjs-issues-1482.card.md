# Source: https://github.com/langchain-ai/langgraphjs/issues/1482
# Author: LangChain
# Author Slug: langchain
# Title: recursionLimit not honoured when sent via useStream · Issue #1482 · langchain-ai/langgraphjs
# Fetched via: trafilatura
# Date: 2026-04-10

Checked other resources
Example Code
const submitOptions = {
// Enable all stream modes including custom events
streamMode: ['values', 'updates', 'events', 'custom'] as Array<'values' | 'updates' | 'events' | 'custom'>,
streamSubgraphs: true,
recursionLimit: 50,
streamResumable: true
};
const submitPayload = {
messages: [{
type: "human",
content: input.trim()
}],
project_id: projectId || `project-${Date.now()}`, // Use provided projectId or generate a new one
user_id: user?.uid || '' // Add Firebase user ID
};
thread.submit(submitPayload, submitOptions);
Error Message and Stack Trace (if applicable)
The recursionLimit being sent from thread.submit in useStream is not being honoured and default of 25 is being used always.
Description
We have my langgraph agents in python and trying to integrate them in my nextjs app. We are using the useStream hook for streaming and state management on client side.
System Info
├── @emnapi/core@1.4.3 extraneous
├── @emnapi/runtime@1.4.3 extraneous
├── @emnapi/wasi-threads@1.0.2 extraneous
├── @eslint/eslintrc@3.3.1
├── @google/genai@1.5.1
├── @headlessui/react@2.2.4
├── @hello-pangea/dnd@18.0.1
├── @heroicons/react@2.2.0
├── @hookform/resolvers@5.1.1
├── @langchain/anthropic@0.3.23
├── @langchain/core@0.3.60
├── @langchain/langgraph-checkpoint-sqlite@0.1.5
├── @langchain/langgraph-sdk@0.0.104
├── @langchain/langgraph@0.3.4
├── @prisma/client@6.10.1
├── @radix-ui/react-label@2.1.7
├── @radix-ui/react-select@2.2.5
├── @radix-ui/react-separator@1.1.7
├── @radix-ui/react-slot@1.2.3
├── @radix-ui/react-switch@1.2.5
├── @rushstack/eslint-config@4.3.0
├── @stagewise/toolbar-next@0.1.2
├── @stagewise/toolbar@0.5.0
├── @tailwindcss/postcss@4.1.10
├── @types/js-cookie@3.0.6
├── @types/next-auth@3.13.0
├── @types/node@20.19.1
├── @types/react-beautiful-dnd@13.1.8
├── @types/react-dom@19.1.6
├── @types/react@19.1.8
├── @types/uuid@10.0.0
├── @vercel/otel@1.13.0
├── ai@4.3.16
├── character-entities@2.0.2
├── class-variance-authority@0.7.1
├── clsx@2.1.1
├── date-fns@4.1.0
├── dotenv-cli@8.0.0
├── dotenv@16.5.0
├── eslint-config-next@15.3.2
├── eslint@8.57.1
├── firebase-admin@12.7.0
├── firebase@11.9.1
├── framer-motion@12.18.1
├── handlebars@4.7.8
├── js-cookie@3.0.5
├── langchain@0.3.29
├── langsmith@0.3.33
├── lucide-react@0.507.0
├── next-auth@4.24.11
├── next@15.3.2
├── prettier@3.5.3
├── prisma@6.10.1
├── puppeteer-core@24.12.1
├── react-dom@19.1.0
├── react-hook-form@7.58.1
├── react-markdown@10.1.0
├── react@19.1.0
├── server-only@0.0.1
├── sonner@2.0.5
├── swr@2.3.4
├── tailwind-merge@3.3.1
├── tailwindcss-animate@1.0.7
├── tailwindcss@4.1.10
├── ts-node@10.9.2
├── tw-animate-css@1.3.4
├── typescript@5.8.3
├── uuid@11.1.0
└── zod@3.25.67
Checked other resources
Example Code
const submitOptions = {
// Enable all stream modes including custom events
streamMode: ['values', 'updates', 'events', 'custom'] as Array<'values' | 'updates' | 'events' | 'custom'>,
streamSubgraphs: true,
recursionLimit: 50,
streamResumable: true
};
Error Message and Stack Trace (if applicable)
The recursionLimit being sent from thread.submit in useStream is not being honoured and default of 25 is being used always.
Description
We have my langgraph agents in python and trying to integrate them in my nextjs app. We are using the useStream hook for streaming and state management on client side.
System Info
├── @emnapi/core@1.4.3 extraneous
├── @emnapi/runtime@1.4.3 extraneous
├── @emnapi/wasi-threads@1.0.2 extraneous
├── @eslint/eslintrc@3.3.1
├── @google/genai@1.5.1
├── @headlessui/react@2.2.4
├── @hello-pangea/dnd@18.0.1
├── @heroicons/react@2.2.0
├── @hookform/resolvers@5.1.1
├── @langchain/anthropic@0.3.23
├── @langchain/core@0.3.60
├── @langchain/langgraph-checkpoint-sqlite@0.1.5
├── @langchain/langgraph-sdk@0.0.104
├── @langchain/langgraph@0.3.4
├── @prisma/client@6.10.1
├── @radix-ui/react-label@2.1.7
├── @radix-ui/react-select@2.2.5
├── @radix-ui/react-separator@1.1.7
├── @radix-ui/react-slot@1.2.3
├── @radix-ui/react-switch@1.2.5
├── @rushstack/eslint-config@4.3.0
├── @stagewise/toolbar-next@0.1.2
├── @stagewise/toolbar@0.5.0
├── @tailwindcss/postcss@4.1.10
├── @types/js-cookie@3.0.6
├── @types/next-auth@3.13.0
├── @types/node@20.19.1
├── @types/react-beautiful-dnd@13.1.8
├── @types/react-dom@19.1.6
├── @types/react@19.1.8
├── @types/uuid@10.0.0
├── @vercel/otel@1.13.0
├── ai@4.3.16
├── character-entities@2.0.2
├── class-variance-authority@0.7.1
├── clsx@2.1.1
├── date-fns@4.1.0
├── dotenv-cli@8.0.0
├── dotenv@16.5.0
├── eslint-config-next@15.3.2
├── eslint@8.57.1
├── firebase-admin@12.7.0
├── firebase@11.9.1
├── framer-motion@12.18.1
├── handlebars@4.7.8
├── js-cookie@3.0.5
├── langchain@0.3.29
├── langsmith@0.3.33
├── lucide-react@0.507.0
├── next-auth@4.24.11
├── next@15.3.2
├── prettier@3.5.3
├── prisma@6.10.1
├── puppeteer-core@24.12.1
├── react-dom@19.1.0
├── react-hook-form@7.58.1
├── react-markdown@10.1.0
├── react@19.1.0
├── server-only@0.0.1
├── sonner@2.0.5
├── swr@2.3.4
├── tailwind-merge@3.3.1
├── tailwindcss-animate@1.0.7
├── tailwindcss@4.1.10
├── ts-node@10.9.2
├── tw-animate-css@1.3.4
├── typescript@5.8.3
├── uuid@11.1.0
└── zod@3.25.67