# Source: https://storage.googleapis.com/sdc-prod/v1/safety-report/Waymo-Public-Road-Safety-Performance-Data.pdf
# Title: Waymo Public Road Safety Performance Data
# Fetched via: search
# Date: 2026-04-09

Abstract:Waymo's mission to reduce traffic injuries and fatalities and improve mobility for all has led us to expand deployment of automated vehicles on public roads without a human driver behind the wheel.
As part of this process, Waymo is committed to providing the public with informative and relevant data regarding the demonstrated safety of Waymo's automated driving system, which we call the Waymo Driver.
The data presented in this paper represents more than 6.1 million miles of automated driving in the Phoenix, Arizona metropolitan area, including operations with a trained operator behind the steering wheel from calendar year 2019 and 65,000 miles of driverless operation without a human behind the steering wheel from 2019 and the first nine months of 2020.
The paper includes every collision and minor contact experienced during these operations as well as every predicted contact identified using Waymo's counterfactual, what if, simulation of events had the vehicle's trained operator not disengaged automated driving.
There were 47 contact events that occurred over this time period, consisting of 18 actual and 29 simulated contact events, none of which would be expected to result in severe or life threatening injuries.
This paper presents the collision typology and severity for each actual and simulated event, along with diagrams depicting each of the most significant events.
Nearly all the events involved one or more road rule violations or other errors by a human driver or road user, including all eight of the most severe events, which we define as involving actual or expected airbag deployment in any involved vehicle.
When compared to national collision statistics, the Waymo Driver completely avoided certain collision modes that human driven vehicles are frequently involved in, including road departure and collisions with fixed objects.

## Abstract
Waymo’s mission to reduce traffic injuries and fatalities and improve mobility for all has led us to expand deployment of automated vehicles on public roads without a human driver behind the wheel.
As part of this process, Waymo is committed to providing the public with informative and relevant data regarding the demonstrated safety of Waymo’s automated driving system, which we call the Waymo Driver.
The data presented in this paper represents more than 6.1 million miles of automated driving in the Phoenix, Arizona metropolitan area, including operations with a trained operator behind the steering wheel from calendar year 2019 and 65,000 miles of driverless operation without a human behind the steering wheel from 2019 and the first nine months of 2020.
The paper includes every collision and minor contact experienced during these operations as well as every predicted contact identified using Waymo’s counterfactual, what if, simulation of events had the vehicle’s trained operator not disengaged automated driving.
There were 47 contact events that occurred over this time period, consisting of 18 actual and 29 simulated contact events, none of which would be expected to result in severe or life threatening injuries.
This paper presents the collision typology and severity for each actual and simulated event, along with diagrams depicting each of the most significant events.
Nearly all the events involved one or more road rule violations or other errors by a human driver or road user, including all eight of the most severe events, which we define as involving actual or expected airbag deployment in any involved vehicle.
When compared to national collision statistics, the Waymo Driver completely avoided certain collision modes that human driven vehicles are frequently involved in, including road departure and collisions with fixed objects.

Waymo's safety goal is to reduce traffic injuries and fatalities by driving safely and responsibly. Achieving this goal requires not only superior safety performance by the Waymo Driver, but also public acceptance of automated vehicles ("AVs"). The purpose of this paper is to make available relevant data to promote awareness and discussions that ultimately foster greater public confidence in AVs. [1] , which is an overview of safety readiness methodologies showing how Waymo follows rigorous engineering development and test practices, applying industry standards where appropriate, and developing new methods where those currently available are insufficient.
Our extensive experience has taught us that no single safety methodology is sufficient for AVs; instead, multiple methodologies working in concert are needed. These safety methodologies are supported at Waymo by three basic types of testing: simulation, closed-course, and real-world (public road) testing. While each of these forms of testing is a necessary part of Waymo's validation process, public road testing yields some of the most direct measures of the AV's performance within a given operational design domain (ODD).

…

Waymo analyzes each disengagement to identify potential collisions, near-misses, and other metrics. If the simulation outcome reveals an opportunity to improve the behavior of the ADS, then the simulation is used to develop and test changes to software algorithms. The disengagement event is also added to a library of scenarios, so that future software can be tested against the scenario. At an aggregate level, Waymo uses results from counterfactual disengagement simulations to produce metrics relevant to the AV's on-road performance.

…

The aim of this paper is to share information about driving events that is informative about the safety performance of the Waymo Driver. This paper provides information about collisions and other, more minor, contacts experienced during Waymo's public road operations. This paper includes safety data in the form of event counts and event descriptions from over 6.1 million miles of driving conducted in the Waymo Driver's driverless ODD.

…

### 2.3 Data from Counterfactual ("What If") Simulation

This section discusses the simulation and analysis processes used to determine which instances of operator disengagements would likely have resulted in contact with other road users had the vehicle continued in its automated operations. This involves simulation first of the AV, then if needed, of the behavior of other agents.

## Simulation of the AV motion post-disengagement
After a vehicle operator disengages, the manually-controlled trajectory of the Waymo vehicle will likely differ from the one the AV would have followed had the disengagement not occurred. The first step in post-disengage simulation is therefore to simulate the AV's counterfactual post-disengage motion. This is performed by providing a simulation running Waymo self-driving software with the AV's pre-disengage position, attitude, velocity, and acceleration along with the AV's recorded sensor observations and simulating the response of the software and resulting motion of the Waymo vehicle.

…

Post-disengage simulation reveals that the AV's software would have slowed significantly for the pedestrian before later proceeding. The vehicle following behind the AV did not slow during the actual event, because the AV operator's rapid disengagement made slowing unnecessary. Therefore, the initial post-disengage simulation might show that the vehicle behind the AV overlaps with the AV's simulated position at some points in time.

…

Waymo considers a broad spectrum of potential human driving performance in developing and evaluating the AV, but for transparency and simplicity, the results reported in this paper are based on deterministic models that generate a single response to a given input. Other methods can be used to capture a range of possible human responses, such as probabilistic counterfactual outcomes, but they are more complex.
Waymo's proprietary human collsion avoidance behavior models are based on existing road user behavior modelling frameworks [7,8] and calibrated using naturalistic human collision and near-collision data. The agent's collision avoidance actions are modeled as occurring in response to deviations between the agent's initial expectations and how the situation actually played out (i.e., violations of the agent's expectations [7]).

…

In the prior example of the AV slowing for a pedestrian near a crosswalk, a human collision avoidance behavior model would be used to determine the simulated behavior of the vehicle behind the AV. The AV's motion as it slows defines the stimulus to the following driver's collision avoidance model. The output of the model is a simulated braking and/or swerving response by the following driver after the modeled response time.

## Contact analysis of simulated collisions

…

In the rare cases where contact is inferred, the event is analyzed to determine the event severity of the resulting contact. This determination categorizes collisions based on likelihood of injury and is based on the collision object (e.g., other vehicles, static objects, or vulnerable road users such as pedestrians or cyclists), impact velocity, and impact geometry. Waymo's methods for determining event severity category are developed using national crash databases and are periodically refined to reflect updated data.

…

The Waymo-involved events are tallied in columns categorized by estimated event severity using the ISO 26262 [10] severity classes: S0, S1, S2, and S3, ranging from no injury expected (S0) to possible critical injuries expected (S3). This scale is based on likelihood of AIS injury level [11] (e.g. S1 signifies at least 10% probability of AIS-1 level or higher level injury), which Waymo has estimated for both actual and simulated collisions using the change in velocity and principle direction of force estimated for each involved vehicle.
In order to provide more information about event severity within the S1 designation, S1 severity events have been separated into two columns in Table 1 based on whether each event is of sufficient severity to result in actual or simulated airbag deployment for any involved vehicle. Of the eight airbag-deployment-level S1 events, 4 five are simulated events with expected airbag deployment, two were actual events involving deployment of only another vehicle's frontal airbags, and one actual event involved deployment of another vehicle's frontal airbags and the Waymo vehicle's side airbags. There were no 5 actual or predicted S2 or S3 events.
The rightmost two columns of Table 1 include human collision statistics in the form of the percent contributions from each Manner of Collision to the total counts of collisions and fatal collisions. These values have been calculated using NHTSA's Crash Report Sampling System (CRSS) (police-reported collisions) and FARS [9] (fatal collisions only) data for collisions in urban land zones occurring on ≤ 45 mph roadways , which approximates Waymo's ODD.

…

In total, the Waymo vehicle was involved in 20 events involving contact with another object and experienced 27 disengagements that resulted in contact in post-disengagement simulation, for a total of 47 events (actual and simulated). In two of the actual events (which occurred after disengagement), post-disengage simulation revealed that the event would have been moderately more severe had the trained operator not disengaged. Therefore, these two events are treated in this paper according to their more severe simulated outcomes, yielding a total of 18 actual outcomes and 29 simulated outcomes.

…

The first two of these groups of single-vehicle collisions combine to contribute approximately 60% to all human-driven fatal collisions on ≤ 45 mph urban roadways, both nationally and within Maricopa County, Arizona, where Waymo's ODD is located.

…

In each instance, the Waymo Driver decelerated and stopped, and a pedestrian or cyclist made contact with the right side of the stationary Waymo vehicle while the pedestrian or cyclist was traveling at low speeds. These three events are illustrated below and none of these actual or simulated events can reasonably be considered injurious.

To summarize the single-vehicle event outcomes, the Waymo Driver was involved in one actual and two simulated non-injurious events where a pedestrian or cyclist struck a stationary Waymo vehicle at low speeds.

…

There were two such collisions involving the Waymo Driver, one actual and one simulated (both S0 severity). In both scenarios, the Waymo vehicle was stopped or traveling forward at low speed and the other vehicle was reversing at a speed of less than 3 mph at the moment of contact to the side of the Waymo vehicle.

### 3.3 Multiple Vehicle Events: Same Direction Sideswipe

Same direction sideswipe collisions are a more common vehicle collision mode, and are typically low in severity. These events are typically experienced during lane changing or merging maneuvers. The Waymo Driver was involved in ten simulated same direction sideswipe collisions. The events in this category have been assigned to the subcategories in rows 8 and 9 of Table 1.

## Other vehicle changing lanes, Waymo vehicle straight
The collisions in this subcategory involved seven simulated collisions and one actual collision. In each of these, the Waymo vehicle was stopped or traveling straight in a designated lane at or below the speed limit. The other vehicle changed lanes into the area occupied by the Waymo vehicle, which resulted in simulated or actual sideswipe collisions.

8

Reversing collisions can include "Rear-to-rear", "Rear-to-side", and "Other" in NHTSA databases' definition of Manner of Collision.

## Other vehicle straight, Waymo vehicle changing lanes

…

The data includes one event in this category, which occurred when the Waymo vehicle was traveling straight in a designated lane while self-driving with a trained operator late at night. This event involved another vehicle traveling the wrong direction in the Waymo vehicle's lane of travel (see Figure 2 below, Event A ). In simulation, the Waymo Driver detected the wrong way vehicle, initiated full braking, and was simulated to come to a complete stop in its lane prior to impact. The simulated collision assumes that the wrong way vehicle would have continued on the same path as observed in the actual event.
The absence of simulated collision avoidance movement by the other vehicle reflects our assumption based on driving behavior and circumstances that the other driver was significantly impaired or fatigued. The resulting simulated collision shows the other vehicle traveling 29 mph when it strikes the stationary Waymo vehicle (S1 severity with expected airbag deployment).

### 3.5 Multiple Vehicle Events: Rear End

…

This grouping consists of eight actual collisions (including two of S1 severity) from the subcategories in rows 12-14 of Table 1. In these collisions, the Waymo vehicle had been traveling straight and was stopped for a traffic control device (six cases) or gradually decelerating (two cases) due to traffic controls or traffic conditions. Most (six cases) of these collisions had relative contact speeds less than 6 mph. Figure 3 (Event B) depicts the one collision within this grouping that involved actual or expected airbag deployment (S1 and resulting in airbag deployment of the striking vehicle).

…

Two actual collisions involved the Waymo vehicle being struck on the rear bumper while traveling straight at a constant speed at or below the speed limit. In one collision, the Waymo Driver had slowed to a constant speed in the course of traveling over a speed bump. In the other collision (Figure 4, Event C), the Waymo vehicle, traveling straight at the speed limit, was struck by a vehicle traveling 23 mph over the posted speed limit. Both collisions were of S1 severity, with airbag deployment occurring in the striking vehicle in the latter collision within this grouping.

## Rear end struck event group in right turning maneuvers

…

The remaining rear end struck collision involved a deceleration to a near stop by the Waymo Driver while making a left turn in an intersection with a following vehicle that was traveling at a speed and following distance that did not allow for the following driver to successfully respond to the Waymo Driver's braking. The simulated collision impact was estimated to be 16 mph, and this event is categorized as S1 severity.

## Rear end striking event
The single simulated event (row 17 in Table 1) in this grouping involved a vehicle that swerved into the lane in front of the Waymo and braked hard immediately after cutting in despite lack of any obstruction ahead (consistent with antagonistic motive). The Waymo Driver was simulated to have achieved full braking in response to the other vehicle's braking, but was simulated to contact the lead vehicle with a relative impact speed of 1 mph (S0 severity).

…

This grouping consists of the events in rows 19 to 23 of Table 1. The collisions in this grouping (ten simulated, one actual) involve the Waymo vehicle traveling straight in a designated lane at or below the speed limit. In all scenarios, the turning/crossing other vehicle either disregarded traffic controls or otherwise did not properly yield right-of-way.

…

The Waymo Driver's simulated response in Event F resulted in a 23 mph simulated speed reduction prior to impact and also involved initiation of an evasive swerve. In Event G, there was insufficient time for a significant reduction in speed prior to simulated collision. In sum, the collisions in this angled event grouping (ten simulated, one actual) were characterized by the other vehicle failing to yield right-of-way to the Waymo vehicle, and they involved the Waymo vehicle traveling straight with the right-of-way, with a speed at or below the speed limit.

## Angled event group with Waymo vehicle crossing another vehicle's path
The collisions in this grouping (row 24 of Table 1) involve four simulated collisions, where the Waymo Driver was making a right turn from a rightmost lane that was either splitting to an additional lane, or had been the result of two lanes merging to one. In each event, a passenger vehicle attempted to pass the Waymo vehicle on the right while the Waymo Driver was slowing to make the right turn with the right turn signal activated. In each case, the Waymo vehicle's trained operator disengaged, while in simulation the Waymo Driver turned, resulting in simulated collision.

…

To summarize the findings from the data above: • Over 6.1 million miles of automated driving, including 65,000 miles of driverless operation without a human behind the wheel, there were 47 collision or other contact events (18 actual and 29 simulated, one during driverless operation). • Of the sixteen rear end events , eight events involved the Waymo being struck while stopped or gradually decelerating for traffic controls or traffic ahead.
Two events involved the Waymo being struck while traveling at a constant speed. Another group of five rear end struck events were characterized by inadequate response by other vehicles to the Waymo vehicle's slowing behavior when turning. The single event where the Waymo was the striking vehicle involved a passing vehicle that swerved into the lane in front of the Waymo vehicle and braked hard despite lack of any obstruction ahead (consistent with antagonistic motive).

…

• All of the three single vehicle events were non-injurious (S0 severity) events which involved the Waymo vehicle being struck by a pedestrian or cyclist while stationary. • Two reversing events (S0 severity) involved other vehicles reversing at < 3 mph into the side of a Waymo vehicle, while the Waymo vehicle was either stopped or traveling forward below the speed limit. • One head-on (S1 severity) event occurred with another vehicle traveling the wrong direction at night in the Waymo vehicle's lane of travel, after the Waymo Driver had stopped in reaction to the oncoming vehicle.

…

This illustrates a key challenge faced by AVs operating in a predominantly human traffic system and underscores the importance of driving in a way that is interpretable and predictable by other road users.

The primary purpose of Waymo's public road operations is to continue refining and improving AV operations in their intended environment. Unlike human drivers, who primarily improve through individual experience, the learnings from an event experienced by a single AV can be used to permanently improve the safety performance of an entire fleet of AVs. As a result, AV performance can continually improve, while aggregate human driving performance is essentially stagnant.

…

The mix of events in Section 3 highlights certain performance characteristics of the Waymo Driver. The Waymo Driver experienced zero actual or simulated events in the "road departure, fixed object, rollover" single-vehicle collision typology (Row 1 in Table 1, 27% of all US roadway fatalities), reflecting the system's ability to navigate the ODD in a highly reliable manner.

…

For a given metric, the larger the difference in performance, the fewer miles that are required to establish statistical confidence in a hypothesis of non-inferiority or superiority. The 6.1 million miles in self-driving with trained operators mode underlying the data in Section 3 provide sufficient statistical signal to detect moderate-to-large differences in S0 and S1 event frequencies, and Waymo makes use of these event rates for tracking longer-term improvements to the Waymo Driver.
Higher-severity collision risk 6.1 million miles does not provide statistical power to draw meaningful conclusions about the frequencies of events of severity S2 or S3. At this mileage scale, the statistical noise is extremely large and zero or low event counts only provide performance bounds, which necessitates the consideration of other metrics to fully assess the safety of the Waymo Driver.
As a consequence, Waymo uses other methods to evaluate the higher-severity performance, including both simulation-based and closed-course scenario-based collision-avoidance testing [1], In addition, low-severity data, when evaluated in the context of each event's collision geometry, may be informative of high-severity risk. While this and other complementary methods are beyond the scope of this paper, they enable the empirical driving data discussed in this paper to provide utility for better understanding high-severity collision risk.

## Comparison benchmarks
Human driver collision rates have been widely discussed as providing a benchmark for AVs [12,13]. However, ample care must be taken when choosing the benchmarks for comparison. The data in this paper includes all events involving actual or simulated contact between the AV and another object. By including low-speed events involving non-police-reportable contact (e.g. a less than 2 mph vehicle-to-vehicle contact or a pedestrian walking into the side of a stationary vehicle), the scope of events is considerably greater than the scope of police-reported or insurance-reported collisions commonly used to generate performance baselines.

…

Although Waymo has found the collision frequencies observed in this data to compare favorably to analogous frequencies observed in naturalistic driving studies [15], such comparisons are very challenging to perform validly. This is not only due to statistical variability but, more importantly, due to systematic uncertainties arising from the ODD-specificity of our data (e.g., road speed distribution and traffic density), inherent limitations of simulation, and assumptions in human response models.

…

Taken together, these 47 lower severity (S0 and S1) events (18 actual and 29 simulated, one during driverless operation) show significant contribution from other agents, namely human-related deviations from traffic rules and safe driving performance. Nearly all the actual and simulated events involved one or more road rule violations or other incautious behavior by another agent, including all eight of the most severe events involving actual or expected airbag deployment.

…

Due to the typology of those collisions initiated by other actors as well as the Waymo Driver's proficiency in avoiding certain collision modes, the data presented shows a significant shift in the relative distributions of collision types as compared to national crash statistics for human drivers. For example, the Waymo Driver experienced zero actual or simulated collision-relevant contacts in the NHTSA "road departure, fixed object, rollover" single-vehicle collision typology (27% of all US roadway fatalities).

…

Data from more than 6.1 million miles of driving (representing over 500 years of driving for the average U.S. licensed driver) provides sufficient statistical signal to detect moderate-to-large differences in S0 and S1 event frequencies. However, as discussed in Waymo's Safety Methodologies and Safety Readiness Determinations 1 our assessment of AV safety uses multiple complementary methodologies, including simulation and closed course testing, which allows for comprehensive testing, including rare scenarios beyond those encountered in this dataset.

## Making roads safer

The trust and safety of the communities where we operate is paramount to us. That’s why we’re voluntarily sharing our safety data.

**The data to date indicate the Waymo Driver is already making roads safer in the places where we currently operate.** Specifically, the data below demonstrate that the Waymo Driver is better than humans at avoiding crashes that result in injuries — both of any severity and specifically serious ones — as well as those that lead to airbag deployments.
This hub compares the Waymo Driver’s Rider-Only (RO) crash rates to human crash benchmarks for surface streets. It leverages best practices in safety impact analysis and builds upon dozens of Waymo’s safety publications, providing an unprecedented level of transparency within the autonomous driving industry. By sharing our data and methodologies, we also invite you to join us as we push for advancements in measuring safety impact.

…

### Waymo Driver compared to human benchmarks

This table shows how many fewer RO crashes Waymo had (regardless of who was at fault) compared to human drivers with the average benchmark crash rate if they were to drive the same distance in the areas we operate. Results have been rounded to the nearest whole number.

Compared to an average human driver over the same distance in our operating cities, the Waymo Driver had
Overall crash reduction

92% Fewer serious injury or worse crashes (35 fewer)

83% Fewer airbag deployment in any vehicle crashes (230 fewer)

82% Fewer injury-causing crashes (544 fewer)

Crash reductions involving injuries to Vulnerable Road Users

92% Fewer pedestrian crashes with injuries (62 fewer)

…

### Waymo Driver compared to human benchmarks

Airbag deployments, any injury

The graphs below show how many fewer incidents (crashes) per million miles (IPMM) Waymo had compared to human drivers with the benchmark crash rate. The error bars represent 95% confidence intervals for the IPMM estimate.

The reductions are shown for all locations combined and separately for individual cities.

…

### Waymo Driver compared to human benchmarks

Percent difference in crash rate

The graphs below show the percent difference between the Waymo and human benchmark crash rates by location, with 95% confidence intervals. A negative number means the Waymo Driver reduced crashes compared to the human driver. Confidence intervals that do not cross 0% mean the percent difference is statistically significant.

…

This graph shows the percentage of SGO-reported crashes where the maximum Delta-V (from either the Waymo vehicle or other vehicle) was less than 1 mph—meaning the collision resulted in a <1mph change in velocity. A Delta-V less than 1 mph usually results in only minor damage (dents and scratches). This graph includes vehicle-to-vehicle and single vehicle crashes, but not crashes with pedestrians, cyclists, and motorcyclists.
Delta-V is estimated using an impulse-momentum crash model with inputs measured by the Waymo vehicle’s sensor system. Note: Comparable human benchmarks for <1mph Delta-V are currently not possible to estimate with high certainty.

% of SGO Collisions with less than 1mph change in velocity (Delta-V <1mph)

…

### Waymo Driver compared to human benchmarks by crash type

These graphs show how many fewer RO (rider-only) crashes Waymo had (regardless of who was at fault) compared to human drivers with the average benchmark crash rate if they were to drive the same distance in the areas we operate. Crashes were classified into one of 11 crash types, and are representative of all locations. Data are available by individual cities in the download section.

…

> The true safety impact of ADS technologies can only be understood through careful, scientific comparisons. This tool is an important step toward achieving transparency, consistency, and accuracy in estimating ADS safety benefits.
> Orsolya Hegedus, Head Automotive & Mobility Solutions, Swiss Re
> In our research, we have been fortunate to see up-close how strong Waymo’s performance data has been.

…

## Methodology
- ### Methodology
 - #### Comparing autonomous vehicle and human performance
 **Despite the public availability of crash data for both human-driven and autonomous vehicles, drawing meaningful comparisons between the two is challenging.** To ensure a fair comparison, there’s a number of factors that should be taken into consideration. Here are some of the most important: - AV and human data have different definitions of a crash. AV operators like Waymo must report any physical contact that results or allegedly results in any property damage, injury, or fatality, while most human crash data require at least enough damage for the police to file a collision report.

…

- It’s important to look at rates of events (incidents per mile) instead of absolute counts. Waymo is growing its operations in the cities we operate in. With more driving miles come more absolute collisions. It’s critical to consider the total miles driven to accurately calculate incident rates. If you do not consider the miles driven, it may appear like incidents are increasing while in reality the rate of incidents could be going down.
- All streets within a city are not equally challenging. Waymo’s operations have expanded over time, and, because Waymo operates as a ride-hailing service, the driving mix largely reflects user demand. The results on this data hub show human benchmarks reported in Scanlon et al. (2024) and extended upon in Kusano et al. (2025) that are adjusted to account for differences in driving mix using a method described by Chen et al. (2024). See the “Human Benchmarks” section below for more details.

…

OutcomeDescriptionWaymo Data*Human BenchmarkAny-injury-reportedA crash where any road user is injured as a result of the crashAny SGO reported crash with the field “Highest Injury Severity Alleged” is “Minor”, “Moderate”, or “Serious”, or “Fatality”). “Unknown” reported severity where the SGO narrative mentions injuries of unknown severity are also included.Police-reported crashed vehicle rate where at least one road user had a reported injury.

…

 - #### Human benchmarks

 The human benchmark data are the same as reported in Scanlon et al. (2024), and extended upon in Kusano et al. (2025). These benchmarks are derived from state police reported crash records and Vehicle Miles Traveled (VMT) data in the areas Waymo currently operates RO services at large scale (Phoenix, San Francisco, Los Angeles, and Austin).
The human benchmarks were made in a way that only included the crashes and VMT corresponding to passenger vehicles traveling on the types of roadways Waymo operates on (excluding freeways). The any-injury-reported benchmark also used a 32% underreporting correction (based on NHTSA’s Blincoe et al., 2023 study to adjust for crashes not reported by humans. The serious injury or worse (referred to as “suspected serious injury+” in the papers) and airbag deployment human benchmarks rates used the observed crashes without an underreporting correction.
All streets within a city are not equally challenging. If Waymo drives more frequently in more challenging parts of the city that have higher crash rates, it may affect crash rates compared to quieter areas. The benchmarks reported by Scanlon et al. are at a city level, not for specific streets or areas. The human benchmarks shown on this data hub were adjusted using a method described by Chen et al. (2024) that models the effect of spatial distribution on crash risk.
The methodology adjusts the city-level benchmarks to account for the unique driving distribution of the Waymo driving. The result of the reweighting method is human benchmarks that are more representative of the areas of the city Waymo drives in the most, which improves data alignment between the Waymo and human crash data. Achieving the best possible data alignment, given the limitations of the available data, are part of the newly published Retrospective Automated Vehicle Evaluation (RAVE) best practices (Scanlon et al., 2024b).

…

 - #### Confidence intervals and data limitations

 Confidence intervals for Incidents Per Million Miles (IPMM) crash rates were computed using a Poisson Exact method. The confidence intervals for the percent reduction used a Clopper-Pearson binomial described in Nelson (1970). Both confidence intervals were assessed at a 95% confidence level. These confidence intervals use the same methods as described in Kusano et al. (2023).

…

Although, it is likely there is more underreporting in human crash data compared to AV crash data. The any-injury-reported benchmark does use an underreporting correction from Blincoe et al. (2023) based on multiple analyses of national crash police-report and insurance data and a national phone survey. It is not straightforward to compute confidence intervals on the any-injury-reported underreporting estimate because it is derived from multiple sources. There is also evidence that underreporting may differ between localities, meaning a national estimate may not fully represent underreporting in the cities Waymo operates in.

…

## Frequently Asked Questions
- ### 1. Are the results trustworthy?
 - #### 1.1. Are the safety impact results a fair apples-to-apples comparison of Waymo and human driving?
 - ##### 1.1.1. How is the safety impact research designed and carried out?

 Although comparing crash rates boils down to 4 simple counts – crashes and miles for Automated Driving System (ADS) and a benchmark – there are many decisions about the study design and data sources used that can affect the outcome. Safety impact research has been a well-used tool in the vehicle safety research literature, dating back to safety advances like electronic stability control and automated emergency braking. ADS which are responsible for the entire dynamic driving task present some unique challenges, and as a result the

…

 - ##### 1.1.3. Do the Waymo and human data measure the same outcomes?

 Aligning the Automated Driving System (ADS) and human crash data is one of the most important dimensions of doing a fair apples-to-apples comparison, and an important step to aligning data is coming up with a consistent definition for a “crash.” Waymo’s Safety Impact research uses past safety evaluation research as a starting point to pick crash outcomes that can be best identified in both ADS and human data sources.

…

Chen et al. (2025) found that time of day affects crash rates (crash rates late at night are generally higher than during the day). The bottleneck for accounting for more factors when aligning the benchmark and Waymo data is often a lack of data for the human driving exposure. For example, the VMT data used to do the dynamic benchmark is provided as an annual average, so it can’t be used to adjust for time of day.

…

 - ##### 1.1.5. Why does the comparison use all human drivers from the area Waymo operates in the benchmark?

 The results on the safety impact data hub compare Waymo’s crash performance to the current human driving fleet from the areas where Waymo operates using best practices to align the Waymo and human crash data. This comparison answers the research question, “what is the effect of Waymo’s driving on the status quo.” This type of research question is the most basic question researchers ask when a new vehicle technology is being developed and deployed (for example, automated emergency braking, electronic stability control). This type of status quo comparison demonstrates the potential of a vehicle technology to improve traffic safety.

…

prior researchandour prospective safety determination methodologiesexamining our collision avoidance performance, we readily compare the Waymo Driver’s performance against a “non-impaired with eyes on the conflict (NIEON)” driver. There are methodological challenges with creating a comparable crash rate version of this benchmark, because the exact amount of VMT for a “NIEON” like driver is not readily available to quantify benchmarks, primarily due to the fact that human drivers are not always in a NIEON state when driving.

…

statistical power. The question being answered by the Safety Impact Data Hub is are the Waymo and benchmark crash rates different? The input to this calculation is the number of crashes and the number of miles driven by Waymo and the benchmark populations and is modeled using a Poisson distribution, the most common distribution for handling count data.

…

Now consider another experiment with Waymo data. Consider the figure below that keeps the number of Waymo airbag deployment in any vehicle crashes (34) and VMT (71.1 million miles) constant while assuming different orders of magnitude of miles driven in the human benchmark population (benchmark rate of 1.649 incidents per million miles with 17.8 billion miles traveled).
The point estimate is that Waymo has 71% fewer of these crashes than the benchmark. The confidence intervals (also sometimes called error bars) show uncertainty for this reduction at a 95% confidence level (95% confidence is the standard in most statistical testing). If the error bars do not cross 0%, that means that from a statistical standpoint we are 95% confident the result is not due to chance, which we also refer to as statistical significance.
This “simulation” shows the effect on statistical significance when varying the VMT of the benchmark population. This comparison would be statistically significant even if the benchmark population had fewer miles driven than the Waymo population (10 million miles). Furthermore, as long as the human benchmark has more than 100 million miles, there is almost no discernable difference in the confidence intervals of the comparison.
This means that comparisons in large US cities (based on billions of miles) are no different from a statistical perspective than a comparison to the entire US annual driving (trillions of miles). Like the school test example, Waymo has driven enough miles (tens to hundred of millions of miles) and the reductions are large enough (70%-90% reductions) that statistical significance can be achieved.

…

- Scanlon, J. M., Kusano, K. D., Fraade-Blanar, L. A., McMurry, T. L., Chen, Y. H., & Victor, T. (2024). Benchmarks for Retrospective Automated Driving System Crash Rate Analysis Using Police-Reported Crash Data. Traffic Injury Prevention, 25(sup1), S51-S65.

Waymo Rider-Only Automated Driving
System at One Million Miles
Trent Victor, Kristofer Kusano, Tilia Gode, Ruoshu Chen, Matthew Schwall
Waymo, LLC
Abstract
This paper examines the safety performance of the Waymo Driver™, Waymo’s Automated
Driving System (ADS). It analyzes one million miles of driving on public roads in parts of

…

at least one vehicle was towed. There were an additional 18 minor-contact events that were too
minor to meet the tow-away and police-report criteria for CISS, where nine of these 20 contact
events had no damage. Neither the CISS-comparable- nor the minor-contact events were
intersection related or involved VRUs (Vulnerable Road Users), and every vehicle-to-vehicle
event involved one or more road rule violations and/or dangerous behaviors on the part of the
other vehicle’s operator. 55% of all contact events occurred with a stationary Waymo vehicle,
and 40% were parking related, with some overlaps between the two categories. These results,
in combination with previous reported data and past studies performed by Waymo on fatalities
reconstruction and on collision-avoidance testing, support the assertion that the Waymo Driver
is successful at reducing injuries and fatalities today. To establish a valid comparative
assessment of the Waymo Driver, it is most efficient to apply the same requirements to ADS and
Human comparison, only counting events that are likely included in human-reported crash data
benchmark, for example, only CISS-compatible collisions. Confidence in conclusions about the
safety of the Waymo Driver will increase continuously as both credibility of available data and
the validity of predictions improves over time.
Introduction
This paper builds on previous work (Schwall et al., 2020; Scanlon et al., 2020, 2021; Kusano et

…

the severity of that harm), Waymo’s safety philosophy is to reduce traffic injuries and fatalities,
that is, to achieve what we call a Positive Safety Impact (PSI)2.
As detailed in Webb et al. (2020), Waymo’s process for making safety readiness determinations
entails an ordered examination of the relevant metrics and outputs from a number of safety

…

prospective safety impact estimation methods are used3. These include re-simulating a certain
software version and system configuration against historical logs and predicting potential
collisions on public road driving with counterfactual simulations (Schwall et al., 2020). For
analysis of reconstructions of fatalities, counterfactual simulations have also been used

…

2010). The first way is to reduce the severity of the harmful events (shown as (a) in Figure 1). In
(a), the total frequency of events is not changed, but the crash severity is reduced. The second
way to reduce risk is to reduce the overall frequency of harmful events, while the relative
distribution of crash severity is held constant (shown as (b) in Figure 1). An effective ADS does
both (a) and (b) simultaneously, resulting in a distribution that moves both downward and to the
left.
Figure 1. Illustration of reduction in injury risk through reduction in severity and frequency of
harmful events.
Evaluation of collision severity
Injury risk in automotive collisions can be evaluated using dose-response models that link the
dose (e.g., the impact severity measured by change in velocity during the crash) to the
Copyright © 2023 Waymo LLC
3

…

al., 2021).
Evaluation of collision frequency
The concept of determining the frequency of collisions, either in the overall count of collisions, or
a rate of collisions per mile driven or hour operated, is an easy-to-understand concept. An
occurrence rate (e.g., number of crashes per mile) based on ADS’ on-road driving performance

…

benchmark is needed.
Calibration of human benchmark data to ADS data is essential to enable proper comparison and
has many challenges including these key issues:
●
Representative high-severity collisions. Benchmark data must have enough exposure
(mileage) to contain a representative sample for rare collisions (serious injuries and
fatalities, unusual conflict types). Nationally representative collision databases, such as
Copyright © 2023 Waymo LLC
4

…

mileage to contain high severity collisions (serious injuries and fatalities) (Blanco, et al.,
2016).
●
Correction of under reporting of collisions. The benchmark and ADS data must be
calibrated to correct for collision identification and under reporting issues. For example,
24.3% of injury collisions and 59.7% of property-damage-only collisions are not reported

…

benchmark data must be matched on ODD. This leads to a situation termed the ODD
dilemma, the tradeoff between using large, robust datasets (e.g., nationally
representative databases) and small, ODD-specific datasets (Scanlon et al., 2021). Note
that ODD matching differences between ADS and Naturalistic Driving Studies (NDS)
datasets also exist. Similarly, misinterpretations can occur when assessing traffic risks
simply as a ratio of total fatalities to total travel distances (Redelmeier, 2014) as this may
obscure important factors such as regional variations.
●
Vehicle characteristics like type, age, size and fitment of advanced driver assistance

…

miles of rider-only (RO) operations of the Waymo Driver, an ADS, and (b) explore what
conclusions can be made from this observed real-world safety performance in terms of the
frequency and severity of these contact events. In the methods section, we will describe how we
operationalized the definitions of the contact events reported in this study, how we estimated
injury risk for these contact events, and which human crash datasets we will use to compare to
these ADS contact events. In the results section we will provide descriptions (dates, conflict
types, collision partners, vehicle damage, and narrative description) of the identified contact
events. Finally, we end this paper with discussion and conclusions.

…

collisions with no contribution compared to collisions with significant contribution. It is also an
important lens through which Waymo can prioritize engineering efforts to where improvements
are most likely to be impactful for further enhancing the safety of autonomous driving
technology. In reviewing events from the perspective of contribution, it is significant that every
vehicle-to-vehicle contact event in the first one million miles involved one or more road rule
violations or dangerous behaviors on the part of the operator of the other vehicle.
Copyright © 2023 Waymo LLC
10

…

behind. In these struck from behind contact events, the Waymo equipped vehicle was either
stationary or moving slowly at the time of impact. In all struck cases, the Waymo equipped
vehicle was yielding to a traffic light or other stopped vehicles. In 3 out of the 5 struck from
behind cases, the Waymo Vehicle was stopped or moving forward preparing to turn right on a
red traffic light. In 1 of the 5 struck-from-behind contacts the Waymo Vehicle was stopped
yielding to traffic as it prepared to merge onto another roadway. In 1 of the 5 struck-from-behind
contacts, the Waymo vehicle was coming to a gradual stop (no more than 0.2 g deceleration) to
yield to traffic stopped at a red traffic light. There was 1 front to rear conflict where the Waymo
equipped vehicle struck the rear of another vehicle after it changed lanes into the Waymo
vehicle’s lane and applied the brakes (see narrative description for event 7 in Table 1).
Contact with Objects in the Roadway
Five (5) of the 20 contact events were single vehicle incidents where the Waymo vehicle
contacted an object that was in the roadway. In these contact events, the Waymo vehicle did not
leave the roadway. At the time of impact, the Waymo equipped vehicle was traveling between 8
and 13 mph and the objects were either stationary or traveling at less than 3 mph. The objects

…

over the lane line while traveling at speed.
Comparison with nationally representative collision databases
As detailed in Table 1 above, the vast majority of the contact events are of minor severity, where
nine of the 20 events resulted in no damage. To provide further context for the types and
severities of the Waymo contact events, we computed the risk of potential occupants involved in

…

and Waymo events, the cumulative distributions of the Waymo events are to the left of the CISS
distribution, suggesting the Waymo events have a severity distribution with more probability
density shifted towards lower p(MAIS2+). There were observed Waymo contact events in the
Backing, Front-to-Rear, Opposite Direction Lateral Incursion, and Single Vehicle conflict groups.
There was only 1 opposite direction lateral incursion Waymo contact event with p(MAIS2+) =
0%, which is represented as a single point at 100% cumulative percent.
The shapes of the cumulative distributions in Figure 3 confirm that most of the Waymo contact
events do not meet the reporting requirements for CISS, described below. Events number 1 and

…

substantially lower than the police-reported data in backing, opposite direction lateral incursion,
single vehicle collisions, and front-to-rear collisions with maximum p(MAIS2+) risk in Waymo
“not CISS comparable” contact events lower than the minimum reconstructed CISS collisions.
Although weighted two-sample Kolmogorov-Smirnov (KS) tests show significance when

…

that were too minor to meet the criteria for inclusion in CISS. Most contact events resulted in
little damage, with nine of the 20 events resulting in no damage. 55% of the contact events
occurred with a stationary Waymo vehicle, and 40% were parking-related, with some overlaps
between the two categories. Every vehicle-to-vehicle contact event involved one or more road

…

that despite a simpler driving environment, human drivers experience an increased rate of
injurious collisions at night due to a higher prevalence at night of alcohol, fatigue, and speeding
– risk factors that the Waymo Driver does not engage in at any hour. Another potential
explanation is that human drivers also experience more contact events during the daytime than

…

police-reported data in backing, opposite direction lateral incursion, and single vehicle collisions.
The severity for front-to-rear Waymo contact events, when combining both the
CISS-comparable and minor contact events, was significantly lower than the police-reported
data. This is an expected result because CISS is designed to under-report low-severity events,

…

For example, the most frequent collision mode reported from the Waymo contact events was
another party backing into the Waymo vehicle in a parking lot or while the Waymo vehicle was
parked on the roadside (8 out of 20 contact events). Given the relatively low speeds that are
likely when vehicles are starting from standstill, a high severity outcome is unlikely. In contrast,