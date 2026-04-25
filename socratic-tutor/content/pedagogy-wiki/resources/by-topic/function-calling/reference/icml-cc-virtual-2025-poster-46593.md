# Source: https://icml.cc/virtual/2025/poster/46593
# Title: The Berkeley Function Calling Leaderboard (BFCL) — ICML Poster
# Fetched via: jina
# Date: 2026-04-09

Title: ICML Poster The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models


# ICML Poster The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models
# ICML 2025


## Main Navigation


*   [ICML](https://icml.cc/virtual/2025/poster/46593#)
    *   [Help/FAQ](https://icml.cc/FAQ)

* * *

    *   [Contact ICML](https://icml.cc/Help/Contact)

* * *

    *   [Downloads](https://icml.cc/Downloads)

* * *

    *   [Code of Conduct](https://icml.cc/yearly-document/CodeOfConduct)

* * *

    *   [Create Profile](https://icml.cc/Profile/create)

* * *

    *   [Journal To Conference Track](https://icml.cc/public/JournalToConference)

* * *

    *   [Inclusion](https://icml.cc/public/Inclusion)

* * *


* * *

    *   [Future Meetings](https://icml.cc/Conferences/FutureMeetings)

* * *

    *   [Press](https://icml.cc/Conferences/2026/Press)

* * *

    *   [Careers](https://icml.cc/careers)

*   [My Stuff](https://icml.cc/MyStuff)

[Login](https://icml.cc/accounts/login?nextp=/virtual/2025/poster/44866)

*   [Select Year: (2025)](https://icml.cc/virtual/2025/poster/46593#)
    *   [2026](https://icml.cc/Conferences/2026)

* * *

    *   [2025](https://icml.cc/Conferences/2025)

* * *

    *   [2024](https://icml.cc/Conferences/2024)

* * *

    *   [2023](https://icml.cc/Conferences/2023)

* * *

    *   [2022](https://icml.cc/Conferences/2022)

* * *

    *   [2021](https://icml.cc/Conferences/2021/index.html)

* * *

    *   [2020](https://icml.cc/Conferences/2020/)

* * *

    *   [2019](https://icml.cc/Conferences/2019/)

* * *

    *   [2018](https://icml.cc/Conferences/2018)

* * *

    *   [2017](https://icml.cc/Conferences/2017)

* * *

    *   [2016](https://icml.cc/Conferences/2016)

* * *

    *   [2015](https://icml.cc/Conferences/2015)

* * *

    *   [2014](https://icml.cc/Conferences/2014)

* * *

    *   [2013](https://icml.cc/Conferences/2013)

* * *

    *   [2012](https://icml.cc/Conferences/2012)

* * *

    *   [2011](https://icml.cc/Conferences/2011)

* * *

    *   [2010](https://icml.cc/Conferences/2010)

* * *

    *   [2009](https://icml.cc/Conferences/2009)

* * *

    *   [2008](https://icml.cc/Conferences/2008)

* * *

    *   [2007](https://icml.cc/Conferences/2008)

* * *

    *   [2006](https://icml.cc/Conferences/2007)

* * *

    *   [2005](https://icml.cc/Conferences/2005)

* * *

    *   [2004](https://icml.cc/Conferences/2005)

* * *

    *   [2002](https://icml.cc/Conferences/2002)

* * *

    *   [1996](https://icml.cc/Conferences/1996)

* * *

    *   [IMLS Archives](http://www.machinelearning.org/archive.html)

*   [Getting Started](https://icml.cc/virtual/2025/index.html)
*   [Schedule](https://icml.cc/virtual/2025/calendar)
*   [Tutorials](https://icml.cc/virtual/2025/events/tutorial)
*   [Main Conference](https://icml.cc/virtual/2025/poster/46593#)
    *   [Invited Talks](https://icml.cc/virtual/2025/eventlistwithbios/invited%20talk)

* * *

    *   [Orals](https://icml.cc/virtual/2025/events/oral)

* * *

    *   [Spotlight Posters](https://icml.cc/virtual/2025/events/2025SpotlightPosters)

* * *

    *   [Awards](https://icml.cc/virtual/2025/awards_detail)

* * *

    *   [Test of Time Award](https://icml.cc/virtual/2025/test-of-time-award)

* * *

    *   [Papers](https://icml.cc/virtual/2025/papers.html)

*   [Workshops](https://icml.cc/virtual/2025/events/workshop)
*   [Community](https://icml.cc/virtual/2025/poster/46593#)
    *   [Socials](https://icml.cc/virtual/2025/community?show=socials)

*   [Exhibitors](https://icml.cc/virtual/2025/poster/46593#)
    *   [Exhibitors](https://icml.cc/virtual/2025/sponsor_list)
    *   [Expo](https://icml.cc/virtual/2025/events/expo)

*   [Organizers](https://icml.cc/virtual/2025/organizers)
*   [](https://icml.cc/virtual/2025/search)
    *   [FAQ](https://icml.cc/virtual/2025/faq)

* * *

    *   [RocketChat Help](https://chat.icml.cc/)

* * *

    *   [RocketChat Desktop Client](https://icml.cc/virtual/2025/poster/46593)

Poster

# The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models

 Shishir G. Patil · Huanzhi Mao · Fanjia Yan · Charlie Ji · Vishnu Suresh · Ion Stoica · Joseph E Gonzalez 

2025 Poster

 [[OpenReview](https://openreview.net/forum?id=2GmDdhBdDk "OpenReview")]

### Abstract

Function calling, also called tool use, refers to an LLM's ability to invoke external functions, APIs, or user-defined tools in response to user queries—an essential capability for agentic LLM applications. Despite its prominence, there did not exist a standard benchmark to evaluate function calling abilities, due to two reasons – the challenging nature of evaluating when a function call is valid, and the challenge of acquiring diverse, real-world functions. We present the Berkeley Function Calling Leaderboard (BFCL), a comprehensive benchmark designed to evaluate function calling capabilities in a wide range of real-world settings. The BFCL benchmark evaluates serial and parallel function calls, across various programming languages using a novel Abstract Syntax Tree (AST) evaluation method that can easily scale to thousands of functions. We construct the benchmark using a combination of expert curated, and user-contributed functions and associated prompts. Finally, BFCL benchmark evaluates the ability of models to abstain and reason in stateful multi-step agentic setting. Evaluating a wide range of models, we observe that while state-of-the-art LLMs excel at singleturn calls, memory, dynamic decision-making, and long-horizon reasoning remain open challenges. Since its preview, BFCL has become the defacto standard for evaluating function-calls, and can be accessed at gorilla.cs.berkeley.edu/leaderboard.html.

Show more

### Lay Summary

Imagine a helpful AI that can look up the weather, book a flight, or crunch numbers for you simply by “calling” the right online tool or app—much like a human who opens the correct website or piece of software on command. Today’s large language models (LLMs) are starting to do exactly that, but the community lacked a fair, comprehensive, and real-world evaluation to measure how well they perform these tool-using skills.Our work introduces the Berkeley Function Calling Leaderboard (BFCL), a public “obstacle course” that puts AIs through thousands of real-world tasks. Some tests are short and simple (one-off questions), others mimic back-and-forth conversations, and the most demanding ones ask the AI to juggle memory, reasoning and multiple steps—just as an autonomous assistant would in daily life. To grade the answers quickly and reliably, we created a novel checking method that looks at the structure of each tool call rather than running every tool for real, letting the benchmark scale to thousands of functions.Early results reveal a split personality: top AIs ace the one-shot questions but still stumble when they must remember context, manage long conversations, or decide when not to act. By spotlighting these gaps, the BFCL gives researchers and companies a clear target for the next generation of more capable, trustworthy AI assistants. Anyone can explore the live leaderboard online and watch the field improve in real time.

Show more

### Video

Chat is not available.

Successful Page Load

ICML uses cookies for essential functions only. We do not sell your personal information. [Our Privacy Policy »](https://icml.cc/public/PrivacyPolicy)Accept

###### ![Image 2: ICML logo](https://icml.cc/static/core/img/ICML-logo.svg)

The ICML Logo above may be used on presentations. Right-click and choose download. It is a vector graphic and may be used at any scale.

###### Useful links

[About ICML](https://icml.cc/About)

[ICML Proceedings at PMLR](https://proceedings.mlr.press/)

[Code of Conduct](https://icml.cc/yearly-document/CodeOfConduct)

###### Contact

1269 Law Street, San Diego CA 92109

[Email](https://icml.cc/Help/Contact)

[ICML Proceedings at PMLR](https://proceedings.mlr.press/)