# Source: https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/
# Title: Settings
# Fetched via: search
# Date: 2026-04-09

## Key Insights

AI pair-programming tools such as GitHub Copilot have a big impact on developer productivity. This holds for developers of all skill levels, with junior developers seeing the largest gains.

The reported benefits of receiving AI suggestions while coding span the full range of typically investigated aspects of productivity, such as task time, product quality, cognitive load, enjoyment, and learning.
Perceived productivity gains are reflected in objective measurements of developer activity.

While suggestion correctness is important, the driving factor for these improvements appears to be not correctness as such, but whether the suggestions are useful as a starting point for further development.

Potential benefits of generating large sections of code automatically are huge, but evaluating these systems is challenging. Offline evaluation, where the system is shown a partial snippet of code and then asked to complete it, is difficult not least because for longer completions there are many acceptable alternatives and no straightforward mechanism for labeling them automatically.

…

and today neural synthesis tools such as GitHub Copilot, CodeWhisperer, and TabNine suggest code snippets within an IDE with the explicitly stated intention to increase a user’s productivity. Developer productivity has many aspects, and a recent study has shown that tools like these are helpful in ways that are only partially reflected by measures such as completion times for standardized tasks. , a Alternatively, we can leverage the developers themselves as expert assessors of their own productivity. This meshes well with current thinking in software engineering research suggesting measuring productivity on multiple dimensions and using self-reported data. Thus we focus on studying *perceived* productivity.
Here, we investigate whether usage measurements of developer interactions with GitHub Copilot can predict perceived productivity as reported by developers. We analyze survey responses from developers using GitHub Copilot and match their responses to measurements collected from the IDE. We consider acceptance counts and more detailed measures of contribution, such as the amount of code contributed by GitHub Copilot and persistence of accepted completions in the code.
**We find that acceptance rate of shown suggestions is a better predictor of perceived productivity than the alternative measures**. We also find that acceptance rate varies significantly over our developer population as well as over time, and present a deeper dive into some of these variations.

Our results support the principle that acceptance rate can be used for coarse-grained monitoring of the performance of a neural code synthesis system. This ratio of shown suggestions being accepted correlates better than more detailed measures of contribution. However, other approaches remain necessary for fine-grained investigation due to the many human factors involved.

…

For context, in our study GitHub Copilot has an acceptance rate of and a mean DCPU in excess of 312 (See Figure 1). b These differences are presumably due to differences in the kinds of completion offered, or perhaps to user-interface choices. We discuss later how developer objectives, choice of programming language, and even time of day seem to affect our data. Such discrepancies highlight the difficulty in using acceptance rate to understand the value of a system.

…

Measuring developer productivity through activity counts over time (a typical definition of productivity borrowed from economics) disregards the complexity of software development as they account for only a subset of developer outputs. A more holistic picture is formed by measuring

*perceived* productivity through self-reported data across various dimensions and supplementing it with automatically measured data. We used the SPACE framework to design a survey that captures self-reported productivity and paired the self-reported data with usage telemetry.

…

## Data and Methodology

### Usage measurements.

GitHub Copilot provides code completions using OpenAI language models. It runs within the IDE and at appropriate points sends a completion request to a cloud-hosted instance of the neural model. GitHub Copilot can generate completions at arbitrary points in code rather than, for example, only being triggered when a developer types a period for invoking a method on an object. A variety of rules determine when to request a completion, when to abandon requests if the developer has moved on before the model is ready with a completion, and how much of the response from the model to surface as a completion.
As stated in our terms of usage,

c the GitHub Copilot IDE extension records the events shown in Table 1 for all users. We make usage measurements for each developer by counting those events.

**Developer usage events collected by GitHub Copilot.**
|`opportunity`|A heuristic-based determination by the IDE and the plug-in that a completion might be appropriate at this point in the code (for example, the cursor is not in the middle of a word)|
|--|--|
|`shown`|Completion shown to the developer|
|`accepted`|Completion accepted by the developer for inclusion in the source file|
|`accepted_char`|The number of characters in an accepted completion|
|`mostly_unchanged_X`|Completion persisting in source code with limited modifications (Levenshtein distance less than 33%) after X seconds, where we consider durations of 30, 120, 300, and 600 seconds|
|`unchanged_X`|Completion persisting in source code unmodified after X seconds.|
|(active) `hour`|An hour during which the developer was using their IDE with the plug-in active|
Our measures of persistence go further than existing work, which stops at acceptance. The intuition here is that a completion which is accepted into the source file but then subsequently turns out to be incorrect can be considered to have wasted developer time both in reviewing it and then having to go back and delete it. We also record
*mostly* unchanged completions: A large completion requiring a few edits might still be a positive contribution. It is not clear how long after acceptance one should confirm persistence, so we consider a range of options.

The events pertaining to completions form a funnel which we show quantitatively in Table 1. We include a summary of all data in Appendix A.
d ( *All appendices for this article can be found online at* *https://dl.acm.org/doi/10.1145/3633453*).

We normalize these measures against each other and write

`X_per_Y` to indicate we have normalized metric

`X` by metric

`Y`. For example:
`accepted_per_hour` is calculated as the total number of

`accepted` events divided by the total number of (active)

`hour` events.

Table 2 defines the core set of metrics which we feel have a natural interpretation in this context. We note that there are other alternatives and we incorporate these in our discussion where relevant.

…

|Natural name|Explanation|
|--|--|
|Shown rate|Ratio of completion opportunities that resulted in a completion being shown to the user|
|Acceptance rate|Ratio of shown completions accepted by the user|
|Persistence rate|Ratio of accepted completions unchanged after 30, 120, 300, and 600 seconds|
|Fuzzy persistence rate|Ratio of accepted completions mostly unchanged after 30, 120, 300, and 600 seconds|
|Efficiency|Ratio of completion opportunities that resulted in a completion accepted and unchanged after 30, 120, 300, and 600 seconds|
|Contribution speed|Number of characters in accepted completions per distinct, active hour|
|Acceptance frequency|Number of accepted completions per distinct, active hour|
|Persistence frequency|Number of unchanged completions per distinct, active hour|
|Total volume|Total number of completions shown to the user|
|Loquaciousness|Number of shown completions per distinct, active hour|
|Eagerness|Number of shown completions per opportunity|

### Productivity survey.

To understand users’ experience with GitHub Copilot, we emailed a link to an online survey to users. These were participants of the unpaid technical preview using GitHub Copilot with their everyday programming tasks. The only selection criterion was having previously opted in to receive communications. A vast majority of survey users (more than 80%) filled out the survey within the first two days, on or before February 12, 2022.
We therefore focus on data from the four-week period leading up to this point (“the study period”). We received a total of 2,047 responses we could match to usage data from the study period, the earliest on Feb. 10, 2022 and the latest on Mar. 6, 2022.

…

defines 5 dimensions of productivity: **S**atisfaction and well-being, **P**erformance, **A**ctivity, **C**ommunication and collaboration, and **E**fficiency and flow. We use four of these (S,P,C,E) since self reporting on (A) is generally considered inferior to direct measurement.
We included 11 statements covering these four dimensions in addition to a single statement: “I am more productive when using GitHub Copilot.” For each self-reported productivity measure, we encoded its five ordinal response values to numeric labels (1 = Strongly Disagree, , 5 = Strongly Agree). We include the full list of questions and their coding to the SPACE framework in Appendix C. For more information on the SPACE framework and how the empirical software engineering community has been discussing developer productivity, please see the following section.
Early in our analysis, we found that the usage metrics we describe in the Usage Measurements section corresponded similarly to each of the measured dimensions of productivity, and in turn these dimensions were highly correlated to each other (Figure 3). We therefore added an aggregate productivity score calculated as the mean of all 12 individual measures (excluding skipped questions). This serves as a rough proxy for the much more complex concept of productivity, facilitating recognition of overall trends, which may be less discernible on individual variables due to higher statistical variation.

…

**S (Satisfaction and well being)**: This dimension is meant to reflect developers’ fulfillment with the work they do and the tools they use, as well as how healthy and happy they are with the work they do. This dimension reflects some of the easy-to-overlook trade-offs involved when looking exclusively at velocity acceleration (for example, when we target faster turnaround of code reviews without considering workload impact or burnout for developers).
**P (Performance)**: This dimension aims to quantify outcomes rather than output. Example metrics that capture performance relate to quality and reliability, as well as further-removed metrics such as customer adoption or satisfaction. **A (Activity)**: This is the count of outputs—for example, the number of pull requests closed by a developer.
As a result this is a dimension that is best quantified via system data. Given the variety of developers’ activities as part of their work, it is important that the activity dimension accounts for more than coding activity—for instance, writing documentation, creating design specs, and so on. **C (Communication and collaboration)**: This dimension aims to capture that modern software development happens in teams and is, therefore, impacted by the discoverability of documentation or the speed of answering questions, or the onboarding time and process of new team members.
**E (Efficiency and flow)**: This dimension reflects the ability to complete work or make progress with little interruption or delay. It is important to note that delays and interruptions can be caused either by systems or humans, and it is best to monitor both self-reported and observed measurements—for example, use self-reports of the ability to do uninterrupted work, as well as measure wait time in engineering systems).

## What Drives Perceived Productivity?

To examine the relationship between objective measurements of user behavior and self-reported perceptions of productivity, we used our set of core usage measurements (Table 2). We then calculated Pearson’s R correlation coefficient and the corresponding p-value of the F-statistic between each pair of usage measurement and perceived productivity metric. We also computed a PLS regression from all usage measurements jointly.
We summarize these results in Figure 3, showing the correlation coefficients between all measures and survey questions. The full table of all results is included in Appendix B, available online.

**We find acceptance rate (**accepted_per_shown **) most positively predicts users’ perception of productivity, although, given the confounding and human factors, there is still notable unexplained variance.**

…

Looking at the more detailed metrics around persistence, we see that it is generally better over shorter time periods than over longer periods. This is intuitive in the sense that shorter periods move the measure closer to acceptance rate. We also expect that at some point after accepting the completion it becomes simply part of the code and so any changes (or not) after that point will not be attributed to GitHub Copilot. All persistence measures were less well correlated than acceptance rate.
To assess the different metrics in a single model, we ran a regression using projection on latent structures (PLS). The choice of PLS, which captures the common variation of these variables as is linearly connected to the aggregate productivity,

is due to the high collinearity of the single metrics. The first component, to which every metric under consideration contributes positively, explains of the variance. The second component captures the acceptance rate/change rate dichotomy; it explains a further . Both draw most strongly from acceptance rate.

…

|productivity measure|coeff|
|--|--|
|proficiency|`better_code`|
|proficiency|`stay_in_flow`|
|proficiency|`focus_satisfying`|
|proficiency|`less_effort_repetitive`|
|proficiency|`repetitive_faster`|
|years|`better_code`|
|years|`less_frustrated`|
|years|`repetitive_faster`|
|years|`unfamiliar_progress`|
(*: p < 0.05, **: p < 0.01, ***: p < 0.001.)

…

**Figure 4. Different metrics clustering in latent structures predicting perceived productivity. We color the following groups: flawless suggestions (counting the number of unchanged suggestions), persistence rate (ratio of accepted suggestions that are unchanged), and fuzzy persistence rate (accepted suggestions that are mostly unchanged).**

**Figure 5. Linear regressions between acceptance rate and aggregate productivity by subgroup defined through years of professional experience or programming language use. Dashed lines denote averages. The x-axis is clipped at (0, 0.5), and 95% of respondents fall into that range.**

…

## Conclusions

When we set out to connect the productivity benefit of GitHub Copilot to usage measurements from developer activity, we collected measurements about acceptance of completions in line with prior work, but also developed persistence metrics, which arguably capture sustained and direct impact on the resulting code. We were surprised to find acceptance rate (number of acceptances normalized by the number of shown completions) to be better correlated with reported productivity than our measures of persistence.

Everyday, we use tools and form habits to achieve more with less.
Software development produces such a high number of tools and technologies to make work efficient, to the point of inducing decision fatigue.
When we first launched a technical preview of GitHub Copilot in 2021, our hypothesis was that it would improve developer productivity and, in fact, early users shared reports that it did.
In the months following its release, we wanted to better understand and measure its effects with quantitative and qualitative research.
To do that, we first had to grapple with the question: what does it mean to be productive?
...
For example:
...
Because AI-assisted development is a relatively new field, as researchers we have little prior research to draw upon.
We wanted to measure GitHub Copilot’s effects, but what are they?
After early observations and interviews with users, we surveyed more than 2,000 developers to learn at scale about their experience using GitHub Copilot.
We designed our research approach with three points in mind:
- **Look at productivity holistically.** At GitHub we like to think broadly and sustainably about developer productivity and the many factors that influence it.
We used the SPACE productivity framework to pick which aspects to investigate.
- **Include developers’ first-hand perspective.** We conducted multiple rounds of research including qualitative (perceptual) and quantitative (observed) data to assemble the full picture.
We wanted to verify: (a) Do users’ actual experiences confirm what we infer from telemetry?
(b) Does our qualitative feedback generalize to our large user base?
…
### Finding 1: Developer productivity goes beyond speed
Through a large-scale survey, we wanted to see if developers using GitHub Copilot see benefits in other areas beyond speeding up tasks.
Here’s what stood out:
- **Improving developer satisfaction.** Between 60–75% of users reported they feel more fulfilled with their job, feel less frustrated when coding, and are able to focus on more satisfying work when using GitHub Copilot.
That’s a win for developers feeling good about what they do!
- **Conserving mental energy.** Developers reported that GitHub Copilot helped them stay in the flow (73%) and preserve mental effort during repetitive tasks (87%).
That’s developer happiness right there, since we know from previous research that context switches and interruptions can ruin a developer’s day, and that certain types of work are draining [8, 9].
#### Table: Survey responses measuring dimensions of developer productivity when using GitHub Copilot
*All questions were modeled off of the SPACE framework.*
Developers see GitHub Copilot as a productivity aid, but there’s more to it than that.
One user described the overall experience:
The takeaway from our qualitative investigation was that **letting GitHub Copilot shoulder the boring and repetitive work of development reduced cognitive load**.
This makes room for developers to enjoy the more meaningful work that requires complex, critical thinking and problem solving, leading to greater happiness and satisfaction.
### Finding 2: … but speed is important, too
In the survey, we saw that developers reported they complete tasks faster when using GitHub Copilot, especially repetitive ones.
That was an expected finding (GitHub Copilot writes faster than a human, after all), but >90% agreement was still a pleasant surprise.
Developers overwhelmingly perceive that GitHub Copilot is helping them complete tasks faster—can we observe and measure that effect in practice?
For that we conducted a controlled experiment.
#### Figure: Summary of the experiment process and results
We recruited 95 professional developers, split them randomly into two groups, and timed how long it took them to write an HTTP server in JavaScript.
One group used GitHub Copilot to complete the task, and the other one didn’t.
We tried to control as many factors as we could–all developers were already familiar with JavaScript, we gave everyone the same instructions, and we leveraged GitHub Classroom to automatically score submissions for correctness and completeness with a test suite.
We’re sharing a behind-the-scenes blog post soon about how we set up our experiment!
In the experiment, we measured—on average—how successful each group was in completing the task and how long each group took to finish.
- The group that used GitHub Copilot had a **higher rate of completing the task** (78%, compared to 70% in the group without Copilot).
- The striking difference was that **developers who used GitHub Copilot completed the task significantly faster–55% faster than the developers who didn’t use GitHub Copilot**.
Specifically, the developers using GitHub Copilot took on average 1 hour and 11 minutes to complete the task, while the developers who didn’t use GitHub Copilot took on average 2 hours and 41 minutes.
These results are statistically significant (*P=.0017*) and the 95% confidence interval for the percentage speed gain is [21%, 89%].
…
## What do these findings mean for developers?
We’re here to support developers while they build software—that includes working more efficiently and finding more satisfaction in their work.
In our research, we saw that **GitHub Copilot supports faster completion times, conserves developers’ mental energy, helps them focus on more satisfying work, and ultimately find more fun in the coding they do.**
…
With the advent of GitHub Copilot, we’re not alone in exploring the impact of AI-powered code completion tools!
In the realm of productivity, we recently saw an evaluation with 24 students, and Google’s internal assessment of ML-enhanced code completion.
More broadly, the research community is trying to understand GitHub Copilot’s implications in a number of contexts: education, security, labor market, as well as developer practices and behaviors.

to a developer in their integrated development 
environment (IDE) have become the most frequently 
used kind of programmer assistance.1 When 
generating whole snippets of code, they typically use 
a large language model (LLM) to predict what the user 
might type next (the completion) from the context of 
what they are working on at the moment (the prompt).2
This system allows for completions at any position in 
Measuring 
GitHub 
Copilot’s 
Impact on 
Productivity
DOI:10.1145/3633453
Case study asks Copilot users about its impact 
on their productivity, and seeks to find their 
perceptions mirrored in user data.

…

productivity, such as task time, product 
quality, cognitive load, enjoyment, and 
learning.
 
˽ Perceived productivity gains are reflected 
in objective measurements of developer 
activity.
 
˽ While suggestion correctness is 
important, the driving factor for these 
improvements appears to be not 
correctness as such, but whether the 
suggestions are useful as a starting point 
for further development.
54    COMMUNICATIONS OF THE ACM  |  MARCH 2024  |  VOL. 67  |  NO. 3
research

…

cent study has shown that tools like 
these are helpful in ways that are only 
partially reflected by measures such 
as completion times for standardized 
tasks.23,a Alternatively, we can leverage 
the developers themselves as expert 
assessors of their own productivity. 
This meshes well with current think­
ing in software engineering research
suggesting 
measuring 
productiv­
ity on multiple dimensions and using 
self-reported data.6 Thus, we focus on 
studying perceived productivity.
Here, we investigate whether usage 
measurements of developer interac­
tions with GitHub Copilot can predict 
perceived productivity as reported 
by developers. We analyze ​

…

25%
50%
75%
100%
Average number of events per survey user active hour
50
170
mostly unchanged
Completion
unchanged
40
30
20
24
6.6
completion
opportunity
completion
shown
completion
accepted
after 30
seconds
after 2

…

from the IDE. We consider acceptance 
counts and more detailed measures 
of contribution, such as the amount 
of code contributed by GitHub Copilot 
and persistence of accepted comple­
tions in the code. We find that accep­
tance rate of shown suggestions is a 
better predictor of perceived produc­
tivity than the alternative measures.

…

for which the correct method call was in 
the top five suggestions. This metric fell 
from ​
90%​
 in offline evaluation to ​
70%​
 
when used online.21
Due to the diversity of potential 
solutions to a multi-line completion 
task, researchers have used software 
testing to evaluate the behavior of

…

ture is formed by measuring perceived 
productivity 
through 
self-reported 
data across various dimensions6 and 
supplementing it with automatically 
measured data.4 We used the SPACE 
framework6 to design a survey that 
captures 
self-reported 
productivity 
and paired the self-reported data with
usage telemetry.
To the best of our knowledge, this 
is the first study of code suggestion 
tools establishing a clear link between 
usage measurements and developer 
productivity or happiness. A previ­
ous study comparing GitHub Copilot 
against IntelliCode with 25 partici­
pants found no significant correlation 
between task completion times and
survey responses.22
Data and Methodology
Usage measurements. GitHub Copilot 
provides code completions using Ope­
nAI language models. It runs within 
the IDE and at appropriate points 
sends a completion request to a cloud-
hosted instance of the neural model. 
GitHub Copilot can generate comple­

…

completion, and how much of the re­
sponse from the model to surface as a 
completion.
As stated in our terms of usage,b the 
GitHub Copilot IDE extension records 
the events shown in Table 1 for all us­
ers. We make usage measurements 
for each developer by counting those 
events.

…

quantitatively in Table 1. We include 
a summary of all data in Appendix 
A.c (All appendices for this article can 
be found online at https://dl.acm.org/
doi/10.1145/3633453).
We normalize these measures 
against each other and write X _

…

research
Table 2. The core set of measurements considered in this article.
Natural name
Explanation
Shown rate
Ratio of completion opportunities that resulted in a completion being 
shown to the user
Acceptance rate
Ratio of shown completions accepted by the user
Persistence rate
Ratio of accepted completions unchanged after 30, 120, 300, and 600
seconds
Fuzzy persistence rate
Ratio of accepted completions mostly unchanged after 30, 120, 300, 
and 600 seconds
Efficiency
Ratio of completion opportunities that resulted in a completion 
accepted and unchanged after 30, 120, 300, and 600 seconds
Contribution speed
Number of characters in accepted completions per distinct, active hour
Acceptance frequency
Number of accepted completions per distinct, active hour
Persistence frequency
Number of unchanged completions per distinct, active hour
Total volume
Total number of completions shown to the user
Loquaciousness
Number of shown completions per distinct, active hour
Eagerness
Number of shown completions per opportunity
Table 1. Developer usage events collected by GitHub Copilot.
Opportunity
A heuristic-based determination by the IDE and the plug-in that a completion 
might be appropriate at this point in the code (for example, the cursor is not in 
the middle of a word)
Shown
Completion shown to the developer
Accepted
Completion accepted by the developer for inclusion in the source file
Accepted char
The number of characters in an accepted completion
Mostly 
unchanged X
Completion persisting in source code with limited modifications (Levenshtein 
distance less than 33%) after X seconds, where we consider a duration of 30,
120, 300, and 600 seconds
Unchanged X
Completion persisting in source code unmodified after X seconds.
(Active) hour
An hour during which the developer was using their IDE with the plug-in active
when using GitHub Copilot.” For each 
self-reported productivity measure, 
we encoded its five ordinal response

…

munity has been discussing developer 
productivity, please see the following 
section.
Early in our analysis, we found that 
the usage metrics we describe in the 
Usage Measurements section corre­
sponded similarly to each of the mea­
sured dimensions of productivity, and 
in turn these dimensions were highly 
correlated to each other (Figure 3). We
therefore added an aggregate produc­
tivity score calculated as the mean of 
all 12 individual measures (excluding 
skipped questions). This serves as a 
rough proxy for the much more com­
plex concept of productivity, facili­
tating recognition of overall trends, 
which may be less discernible on indi­

…

tivity, which reflects their engineering 
goals—for example, Google uses the 
QUANTS framework, with five compo­
nents of productivity.27 In this article, 
we use the SPACE framework,6 which 
builds on synthesis of extensive and 
diverse literature by expert research­
ers and practitioners in the area of de­

…

in our discussion where relevant.
Productivity survey. To understand 
users’ experience with GitHub Co­
pilot, we emailed a link to an online 
survey to ​
17, 420​
 users. These were 
participants of the unpaid technical 
preview using GitHub Copilot with 
their everyday programming tasks.

…

research
documentation or the speed of an­
swering questions, or the onboard­
ing time and processing of new team 
members.
 
˲ E (Efficiency and flow): This di­
mension reflects the ability to com­
plete work or make progress with little 
interruption or delay. It is important 
to note that delays and interruptions
can be caused either by systems or hu­
mans, and it is best to monitor both 
self-reported and observed measure­
ments—for example, use self-reports 
of the ability to do uninterrupted work, 
as well as measure wait time in engi­
neering systems).
 
˲ A (Activity): This is the count of

…

output. Example metrics that capture 
performance relate to quality and re­
liability, as well as further-removed 
metrics such as customer adoption or 
satisfaction.
Figure 3. Correlation between metrics. Metrics are ordered by similarity based on distance in the correlation matrix, except for manu­
ally fixing the aggregate productivity and acceptance rate at the end for visibility.

…

unchanged_300_per_accepted
learn_from
less_time_searching
unfamiliar_progress
repetitive_faster
less_effort_repetitive
better_code
less_frustrated
focus_satisfying
more_fulfilled
stay_in_flow
tasks_faster
aggregate_productivity
mostly_unchanged_300_per_accepted

…

stay_in_flow
tasks_faster
aggregate_productivity
mostly_unchanged_300_per_accepted
mostly_unchanged_30_per_accepted
mostly_unchanged_600_per_accepted
unchanged_120_per_accepted
shown_per_active_hour
accepted_char_per_active_hour
accepted_per_active_hour

…

Proficiency
Less effort repetitive
0.072**
Proficiency
Repetitive faster
0.055***
Years
Better code
−0.087*
Years
Less frustrated
−0.103**
Years
Repetitive faster
−0.054*
Years
Unfamiliar progress
0.081*

…

code, so any changes (or not) after that 
point will not be attributed to GitHub 
Copilot. All persistence measures 
were less well correlated than accep­
tance rate.
To assess the different metrics in 
a single model, we ran a regression 
using projection on latent structures 
(PLS). The choice of PLS, which cap­
tures the common variation of these 
variables as is linearly connected to 
the aggregate productivity,28 is due to 
the high collinearity of the single met­
rics. The first component, to which 
every metric under consideration con­
tributes positively, explains ​
43 . 2%​
 of 
the variance. The second component

…

of usage measurement and perceived 
productivity metric. We also computed 
a PLS regression from all usage mea­
surements jointly.
We summarize these results in 
Figure 3, showing the correlation co­
efficients between all measures and 
survey questions. The full table of 
all results is included in Appendix B,

…

are productive and how they measure 
productivity, developers do not cite 
lines of code or function points per 
sprint, but rather completing tasks, 
being free of interruptions, usefulness 
of their work, success of the feature 
they worked on, and more.
 
˲ To sum up, after many studies

…

ficiency positively predicts developers 
agreeing that Copilot helps them stay 
in the flow, focus on more satisfying 
work, spend less effort on repetitive 
tasks, and perform repetitive tasks 
faster. Years of experience negatively 
predicts developers feeling less frus­
trated in coding sessions and per­
forming repetitive tasks faster while

…

21 . 2%​
.
Conclusions
When we set out to connect the pro­
ductivity benefit of GitHub Copilot to 
usage measurements from developer 
activity, we collected measurements 
about acceptance of completions in 
line with prior work, but also devel­
oped persistence metrics, which ar­
guably capture sustained and direct 
impact on the resulting code. We 
were surprised to find acceptance rate 
(number of acceptances normalized 
by the number of shown completions) 
to be better correlated with reported 
productivity than our measures of 
persistence.
In hindsight, this makes sense. 
Coding is not typing, and GitHub Co­

1. 1 Introduction
2. 2 Background: Zoominfo
3. 3 Productivity Refresher
4. 4 Projected Benefits of GitHub Copilot 1. 4.1 Augmenting Day-to-day Software Development
2. 4.2 Overall Productivity Gains
…
###### Abstract
This paper presents a comprehensive evaluation of GitHub Copilot’s
deployment and impact on developer productivity at Zoominfo, a leading
Go-To-Market (GTM) Intelligence Platform.
We describe our systematic
four-phase approach to evaluating and deploying GitHub Copilot across
our engineering organization, involving over 400 developers.
…
This paper addresses this gap by presenting a detailed case study of
GitHub Copilot’s production deployment at Zoominfo, a leading
Go-To-Market (GTM) Intelligence Platform, where it is used by over 400
developers who are geographically dispersed, with diverse technical
disciplines, and programming languages.
Our study aims to answer five
key questions in a medium-scale enterprise setting:
…
### 4.1 Augmenting Day-to-day Software Development
- •
Automated Code Generation: GitHub Copilot can generate code
snippets and even complete functions based on the contextual
information provided.
It can suggest logic for the developers while
they’re coding, which can be a significant time-saver, especially
when dealing with routine or repetitive code patterns.
- •
Code Review Assistance: Copilot can also serve as a
pseudo-code-reviewer.
It learns from billions of lines of code,
meaning it can help spot potential bugs, suggest improvements, and
ensure that the code aligns with best practices.
- •
Documentation and Commenting: The AI can provide useful comments
and assist with documentation.
It can explain complex code snippets,
making it easier for other team members to understand the codebase,
hence promoting collaboration.
…
### 4.2 Overall Productivity Gains
- •
Time Efficiency: With automated code generation and intelligent
suggestions, developers can save significant time.
This time can be
used for more critical tasks, such as designing software
architecture or addressing complex problems.
- •
Quality Improvement: By acting as a pseudo-code-reviewer, GitHub
Copilot can help improve the quality of the code, reducing the
likelihood of bugs and rework.
- •
Onboarding and Training: For new hires or junior developers,
GitHub Copilot can act as a learning tool, helping them quickly
understand the codebase, best practices, and contributing
effectively.
- •
Accelerated Development Cycles: By reducing the time spent on
routine tasks, improving code quality, and facilitating faster
onboarding, GitHub Copilot can significantly accelerate our
development cycles.
…
### 5.1 Phase 1: Initial Assessment Phase
We conducted an initial qualitative assessment with five engineers
from July 10th, 2023 to July 17th, 2023 to evaluate GitHub Copilot’s
potential impact on development workflows.
This preliminary evaluation
focused on identifying key benefits and potential challenges within
our existing software development lifecycle.
The preliminary feedback was overwhelmingly positive, with key metrics
including:
- •
Overall experience rating: 8.8 out of 10;
- •
Productivity improvement rating: 8.6 out of 10; and
- •
Code standards alignment: All five participants reported good to
excellent alignment with existing coding standards.
Qualitative feedback highlighted several key observations:
- •
Strong adaptation to existing codebase patterns and conventions;
- •
No reported negative impact on code quality;
- •
Minimal integration challenges with existing development
processes; and
- •
Particularly effective for unit test generation and boilerplate code.
Notable concerns included the following:
- •
Need for modification of suggested code (reported by 3 out of 5
  participants);
- •
Limited visibility across multiple projects; and
- •
Potential over-reliance on automated suggestions.
…
The survey addressed three key dimensions:
1. 1.
   Overall experience and productivity impact,
2. 2.
   Code quality and standards alignment, and
3. 3.
   Security considerations.
The overall experience was positive with the following ratings:
- •
Mean satisfaction rating: 8.0 out of 10, and
- •
Mean productivity improvement rating: 7.6 out of 10.
…
Despite these high scores, developers emphasized the need for rigorous
reviews of AI-generated code to mitigate security and quality risks.
Overall, our analysis revealed strong participant satisfaction with
GitHub Copilot’s core capabilities.
Unit test generation and
boilerplate code creation showed the highest utility, while code
documentation and pattern recognition demonstrated moderate to high
effectiveness.
Variable naming features showed modest utility.
Implementation challenges primarily involved technical integration and
context management across codebases.
Despite these initial adoption
hurdles, the trial demonstrated strong positive outcomes, particularly
in security awareness and code quality maintenance, with most of
participants reporting improved productivity.
This structured trial phase was instrumental in preparing ZoomInfo for
the full rollout of GitHub Copilot, ensuring alignment with
organizational objectives and addressing key developer concerns.
…
- •
90% respondents stated that GitHub Copilot reduces the amount of time it
takes to complete their tasks with a median reduction of 20%.
- •
63% respondents stated using GitHub Copilot allowed them to complete more
tasks per sprint.
- •
77% respondents stated that the quality of their work was improved
when using GitHub Copilot.

1. 1 Introduction
2. 2 Background 1. 2.1 Developer productivity
   2. 2.2 GenAI’s effect on productivity
3. 3 Method
4. 4 Results 1. 4.1 Developer Activity: Copilot Users vs. Non-users
   2. 4.2 Perceived Productivity vs. Measured Output among Copilot users

…

###### Abstract

This study investigates the real-world impact of the generative AI (GenAI) tool GitHub Copilot on developer activity and perceived productivity. We conducted a mixed-methods case study in NAV IT, a large public sector agile organization. We analyzed 26,317 unique non-merge commits from 703 of NAV IT’s GitHub repositories over a two-year period, focusing on commit-based activity metrics from 25 Copilot users and 14 non-users.
The analysis was complemented by survey responses on their roles and perceived productivity, as well as 13 interviews. Our analysis of activity metrics revealed that individuals who used Copilot were consistently more active than non-users, even prior to Copilot’s introduction. We did not find any statistically significant changes in commit-based activity for Copilot users after they adopted the tool, although minor increases were observed.

…

The emergence of GenAI tools such as GitHub Copilot and ChatGPT has further complicated the picture. Developers now spend less time typing code and more time reviewing AI-generated code suggestions [31]. This shift renders many traditional productivity metrics even less meaningful. Furthermore, GenAI tools often lack the domain-specific knowledge required to address context-sensitive challenges, meaning that developers still rely on human collaboration for effective problem-solving when developing large systems [31].

…

We investigate changes in productivity, using a mix of usage data and developers’ own reflections by combining survey responses, interview insights, and analysis of GitHub activity over a two-year period. We make our analysis scripts publicly available, offering a reusable foundation for future research on developer activity using GitHub data (see Appendix A).

…

Those with access to GitHub Copilot completed the task 55.8% faster than the control group. Notably, the productivity gains were larger for less experienced developers. Similarly, [6] studied the impact of Copilot in real workplace settings across three companies, including Microsoft and Accenture. They used metrics such as pull requests, commits, and builds as proxies for completed tasks, and compared developers who were randomly assigned Copilot to a control group.
The results showed a 26.08% increase in completed tasks for the Copilot group, with the greatest gains seen among less experienced developers. Although the authors describe their study as a controlled field experiment, it differs from lab-based experiments because it takes place in real work settings, making the results more relevant to everyday software development.

…

In contrast, developers who were not encouraged reported only 3.9% in time savings and 38% tool usage. Despite these small gains, the study found no significant effects on broader economic outcomes, such as total hours worked or wage increases. In short, controlled task studies report larger productivity effects than field studies and workplace surveys [17, 6, 10].

…

We adopted a case study approach to understand how Copilot influenced development work in practice. Our study combines quantitative and qualitative data, including survey responses, interview insights, and analysis of the developers’ activity on GitHub.

In November and December 2023, we conducted 13 interviews with developers, each lasting between 30 and 60 minutes, with an average duration of 47 minutes. The interviews were transcribed using an AI tool, but we manually reviewed and corrected the transcriptions for accuracy and clarity while listening to the recordings. The transcripts were analyzed thematically, using a combination of open coding, memoing, and comparison.
The survey was distributed between March and April 2024. As part of the survey, respondents who stated having adopted GitHub Copilot were given the following question: Since getting access to GitHub Copilot, have you noticed a change in the following: Your own productivity (from “Major decrease” (-2) to “Major increase” (+2)), which we have used in this case study.

…

The dataset was therefore trimmed at the 95th percentile, calculated individually for each commit activity metric. Low activity users: Users with fewer than one commit per week on average were excluded from the study, as they were not considered representative of professional developers.

The cleaned dataset consisted of 26,317 commits from 703 repositories spread across 39 developers: 25 Copilot users and 14 non-users. We include the roles of these participants as stated in their survey responses; see Figure 1.
Individual commit data can vary significantly in both size and frequency. To better investigate the overall trends for a broad concept like productivity, we aggregated the data into weekly chunks. This ensures that a range of contribution styles would be considered as ”productive”, both small but frequent contributions, and few but large contributions. For weeks with no commits, we manually imputed the value ”0”. The final dataset consisted of N=4095 weekly observations, based on 105
weeks of activity data for each of the 39 developers.

…

Non-users, by contrast, showed a small decline in both additions ( 70) and deletions ( 30) in the same period (thus a roughly flat net change). These shifts were relatively small.

This suggests that Copilot might have enabled users to slightly increase their net code contribution by adding slightly more and deleting slightly less, while maintaining their average commit frequency. Interviewee I13, a Copilot user, described this effect as generating more initial code that could be refined later: “Just getting code generated as a starting point to build on is incredibly good” (I13).
It is important to note that we found no evidence of any negative impact on code quality metrics from Copilot adoption. The structural metrics (e.g., function complexity, average module size) remained virtually unchanged and showed no significant differences between users and non-users. In other words, the Copilot group’s code was not measurably “worse” (or better) in complexity or size due to using the AI assistant. Interview insights support this: none of the developers felt Copilot degraded the quality of their code – if anything, the concerns were about hidden mistakes or subtle bugs, not systematic complexity.

…

Most points in Figure 4 cluster around “No change” to “Slight Increase” in perceived productivity, spanning a range of actual commit changes (some users actually committed less on average but still felt a bit more productive, and vice versa). Quantitatively, across all six activity metrics we examined, the correlations with perceived productivity were not found to be significant.

…

Interestingly, the one activity metric that showed a negligible correlation with perceived productivity was net lines of code (\DeltaDiff, \rho\approx 0.09, where \DeltaDiff is average weekly net diff after adoption minus average weekly net diff before adoption). This indicates that increases in code output volume had essentially no relationship with the feeling of being more productive.
Meanwhile, a few who reported “major increase” in productivity did not stand out in code metrics; their boost may have come from qualitative improvements like less context-switching or more mental energy for challenging parts of the work. One senior developer reflected on this, saying that Copilot did not make hard problems go away, but it did save him time on template code and searching for syntax, which made his day “flow” better (I12).

…

For Copilot users, our findings suggest a relatively small increase in average weekly activity; however, there is no statistically significant difference after adopting Copilot, which differs from prior studies [17, 20, 1, 6]. For example, [17] found that participants with access to GitHub Copilot completed standardized programming tasks 55.8% faster. Similarly, [20] studied the development of a small business application and reported a 70.66% productivity gain, primarily due to ChatGPT’s ability to generate structural code.

…

This broader understanding of productivity may help explain why none of the Copilot users in our sample reported a decrease in productivity. All participants indicated either “No change” or more (slight/major increase) on the Likert scale, even though many showed a decline in average weekly activity levels during the two-year analysis period (see Figure 4).

…

In our study, several Copilot users reported increased productivity despite lower activity levels (see Figure 4), possibly because they spent more time evaluating generated code, as also observed by [31]. This suggests that the tool may reduce cognitive load, streamline routine tasks, and improve developer experience—benefits not easily captured by traditional metrics like commits or lines of code. As developers in our study explained, the flow became better even though the output did not increase.

…

### 5.1 Implication for Practice

In our case, the developers maintained their higher output advantage post-Copilot introduction. This has an implication for evaluating AI tools: if one naively compared Copilot users vs. non-users after rollout, one might wrongly conclude Copilot “caused” more output, whereas our longitudinal view shows how this gap pre-existed GitHub Copilot (Copilot users were already committing more). This quantitative finding aligns with the skepticism voiced by some of the interviewees that simple metrics could be misleading.

…

## 6 Conclusion and Future Work

Our longitudinal study of GitHub Copilot adoption reveals a nuanced impact on developer productivity. In contrast to controlled experiments isolating Copilot’s effects, our real-world data showed no dramatic change in commit-based output after Copilot’s introduction. Notably, those who chose to use Copilot were already among the more active developers beforehand.