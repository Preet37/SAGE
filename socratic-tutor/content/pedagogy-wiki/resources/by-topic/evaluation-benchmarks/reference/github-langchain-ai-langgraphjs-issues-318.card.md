# Source: https://github.com/langchain-ai/langgraphjs/issues/318
# Author: LangChain
# Author Slug: langchain
# Title: Where to add config to streamEvents? · Issue #318 · langchain-ai/langgraphjs
# Fetched via: browser
# Date: 2026-04-10

langchain-ai
/
langgraphjs
Public
Notifications
Fork 455
 Star 2.8k
Where to add config to streamEvents? #318
New issue
Closed
Description
Guido Rietbroek (guidorietbroek)
opened 

Maybe a stupid question, but I can't find it in the docs.

If I want to add a thread_id to a final response of a graph (specific node), how to add this thread id as config?

let config = {
    configurable: {
      thread_id: "1",
    }

const eventStream = await graph.streamEvents(
  { messages: [["user", "What's the capital of Nepal?"]] },
  { version: "v2" },
  { includeNames: ["Summarizer"] }
);


And why do you need to use version v1 or v2?

Activity
hinthornw commented 
William FH (hinthornw)
 · edited by hinthornw
Edits
Contributor

In the second positional location (where version is passed)

Here's the ref doc for streamEvents. options extends RunnableConfig, which contains the configuration values you're looking for. It also contains info about the differences between the versions.

We version the endpoints explicitly since streamEvents returns all the sub-events. Streaming is critical for any application, and we plan to make some improvements to tracing in the future that might influence some of the characteristics of those events. Things that would influence these characteristics would be scoped to a new version.

justinlevi commented 
Justin Levi Winter (justinlevi)
Contributor

Perhaps somewhat related, but how would I limit only the last node to stream to a response client?

If I have several nodes and each node invokes a chain, currently I'm seeing on_chat_model_stream events for all chains and I only want to forward on chunks from the last generation node.

guidorietbroek commented 
Guido Rietbroek (guidorietbroek)
Author

Thanks William FH (@hinthornw)

Can you just confirm this is how it is supposed to work?

const eventStream = await graph.streamEvents(
  { messages: [["user", "What's the capital of Nepal?"]] },
  { version: "v2", ...config },
  { includeNames: ["Summarizer"] }
);


Justin Levi Winter (@justinlevi) see this js example for your answer: https://langchain-ai.github.io/langgraphjs/how-tos/stream-tokens/#other-graphs

guidorietbroek commented 
Guido Rietbroek (guidorietbroek)
Author

So the confusing was caused by the fact that I get an error when using Claude in my LangGraph in combination with streamEvents. When changing to GPT4o the streaming is working.

This is the error I get:

An error occurred: Error: No parseable tool calls provided to AnthropicToolsOutputParser.

I am using a Zod schema with the structuredoutput:

const securitySchema = z.object({
        securityCheck: z.enum(["safe", "unsafe"])
        .describe("Response if an incoming user input is safe to handle or not. "),
    });

    // const model = new ChatAnthropic({
    //     temperature: 0,
    //     apiKey: process.env.ANTHROPIC_API_KEY,
    //     model: "claude-3-haiku-20240307",
    // })

    const model = new ChatOpenAI({
        temperature: 0,
        apiKey: process.env.OPENAI_API_KEY,
        model: "gpt-4o-2024-05-13",
    })

const structuredModel = model.withStructuredOutput(securitySchema, {name: "securitySchema"});


Is this a bug?

hwchase17 commented 
Harrison Chase (hwchase17)

do you have a langsmith trace to share?

guidorietbroek commented 
Guido Rietbroek (guidorietbroek)
 · edited by guidorietbroek
Edits
Author

Harrison Chase (@hwchase17) Sure!

https://smith.langchain.com/public/96a53a9c-a47a-4f46-8558-e5ec23d31307/r

dqbd commented 
David Duong (dqbd)
Collaborator

Seems to be fixed in latest @langchain/anthropic, closing

David Duong (dqbd)
closed this as completed
Sign up for free
 to join this conversation on GitHub. Already have an account? Sign in to comment
Metadata
Assignees
No one assigned
Labels
No labels
Type
No type
Fields
Give feedback
No fields configured for issues without a type.
Projects
No projects
Milestone
No milestone
Relationships
None yet
Development
Code with agent mode
No branches or pull requests
Participants
+1
Issue actions