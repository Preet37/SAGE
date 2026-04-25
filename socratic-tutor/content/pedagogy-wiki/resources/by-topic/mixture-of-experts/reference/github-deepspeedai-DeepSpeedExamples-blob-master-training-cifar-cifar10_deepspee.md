# Source: https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py
# Title: DeepSpeedExamples: cifar10_deepspeed.py (includes MoE layer specification and runnable training scaffold)
# Fetched via: jina
# Date: 2026-04-09

Title: DeepSpeedExamples/training/cifar/cifar10_deepspeed.py at master · deepspeedai/DeepSpeedExamples


# DeepSpeedExamples/training/cifar/cifar10_deepspeed.py at master · deepspeedai/DeepSpeedExamples · GitHub


Toggle navigation

[](https://github.com/)

[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fdeepspeedai%2FDeepSpeedExamples%2Fblob%2Fmaster%2Ftraining%2Fcifar%2Fcifar10_deepspeed.py)

Appearance settings

*   
Platform

    *   
AI CODE CREATION
        *   [GitHub Copilot Write better code with AI](https://github.com/features/copilot)
        *   [GitHub Spark Build and deploy intelligent apps](https://github.com/features/spark)
        *   [GitHub Models Manage and compare prompts](https://github.com/features/models)
        *   [MCP Registry New Integrate external tools](https://github.com/mcp)

    *   
DEVELOPER WORKFLOWS
        *   [Actions Automate any workflow](https://github.com/features/actions)
        *   [Codespaces Instant dev environments](https://github.com/features/codespaces)
        *   [Issues Plan and track work](https://github.com/features/issues)
        *   [Code Review Manage code changes](https://github.com/features/code-review)

    *   
APPLICATION SECURITY
        *   [GitHub Advanced Security Find and fix vulnerabilities](https://github.com/security/advanced-security)
        *   [Code security Secure your code as you build](https://github.com/security/advanced-security/code-security)
        *   [Secret protection Stop leaks before they start](https://github.com/security/advanced-security/secret-protection)

    *   
EXPLORE
        *   [Why GitHub](https://github.com/why-github)
        *   [Documentation](https://docs.github.com/)
        *   [Blog](https://github.blog/)
        *   [Changelog](https://github.blog/changelog)
        *   [Marketplace](https://github.com/marketplace)

[View all features](https://github.com/features)

*   
Solutions

    *   
BY COMPANY SIZE
        *   [Enterprises](https://github.com/enterprise)
        *   [Small and medium teams](https://github.com/team)
        *   [Startups](https://github.com/enterprise/startups)
        *   [Nonprofits](https://github.com/solutions/industry/nonprofits)

    *   
BY USE CASE
        *   [App Modernization](https://github.com/solutions/use-case/app-modernization)
        *   [DevSecOps](https://github.com/solutions/use-case/devsecops)
        *   [DevOps](https://github.com/solutions/use-case/devops)
        *   [CI/CD](https://github.com/solutions/use-case/ci-cd)
        *   [View all use cases](https://github.com/solutions/use-case)

    *   
BY INDUSTRY
        *   [Healthcare](https://github.com/solutions/industry/healthcare)
        *   [Financial services](https://github.com/solutions/industry/financial-services)
        *   [Manufacturing](https://github.com/solutions/industry/manufacturing)
        *   [Government](https://github.com/solutions/industry/government)
        *   [View all industries](https://github.com/solutions/industry)

[View all solutions](https://github.com/solutions)

*   
Resources

    *   
EXPLORE BY TOPIC
        *   [AI](https://github.com/resources/articles?topic=ai)
        *   [Software Development](https://github.com/resources/articles?topic=software-development)
        *   [DevOps](https://github.com/resources/articles?topic=devops)
        *   [Security](https://github.com/resources/articles?topic=security)
        *   [View all topics](https://github.com/resources/articles)

    *   
EXPLORE BY TYPE
        *   [Customer stories](https://github.com/customer-stories)
        *   [Events & webinars](https://github.com/resources/events)
        *   [Ebooks & reports](https://github.com/resources/whitepapers)
        *   [Business insights](https://github.com/solutions/executive-insights)
        *   [GitHub Skills](https://skills.github.com/)

    *   
SUPPORT & SERVICES
        *   [Documentation](https://docs.github.com/)
        *   [Customer support](https://support.github.com/)
        *   [Community forum](https://github.com/orgs/community/discussions)
        *   [Trust center](https://github.com/trust-center)
        *   [Partners](https://github.com/partners)

[View all resources](https://github.com/resources)

*   
Open Source

    *   
COMMUNITY
        *   [GitHub Sponsors Fund open source developers](https://github.com/sponsors)

    *   
PROGRAMS
        *   [Security Lab](https://securitylab.github.com/)
        *   [Maintainer Community](https://maintainers.github.com/)
        *   [Accelerator](https://github.com/accelerator)
        *   [GitHub Stars](https://stars.github.com/)
        *   [Archive Program](https://archiveprogram.github.com/)

    *   
REPOSITORIES
        *   [Topics](https://github.com/topics)
        *   [Trending](https://github.com/trending)
        *   [Collections](https://github.com/collections)

*   
Enterprise

    *   
ENTERPRISE SOLUTIONS
        *   [Enterprise platform AI-powered developer platform](https://github.com/enterprise)

    *   
AVAILABLE ADD-ONS
        *   [GitHub Advanced Security Enterprise-grade security features](https://github.com/security/advanced-security)
        *   [Copilot for Business Enterprise-grade AI features](https://github.com/features/copilot/copilot-business)
        *   [Premium Support Enterprise-grade 24/7 support](https://github.com/premium-support)

*   [Pricing](https://github.com/pricing)

Search or jump to...

# Search code, repositories, users, issues, pull requests...


Clear

[Search syntax tips](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax)

# Provide feedback

We read every piece of feedback, and take your input very seriously.


 Cancel  Submit feedback 

# Saved searches

## Use saved searches to filter your results more quickly

Name 

Query 

To see all available qualifiers, see our [documentation](https://docs.github.com/search-github/github-code-search/understanding-github-code-search-syntax).

 Cancel  Create saved search 

[Sign in](https://github.com/login?return_to=https%3A%2F%2Fgithub.com%2Fdeepspeedai%2FDeepSpeedExamples%2Fblob%2Fmaster%2Ftraining%2Fcifar%2Fcifar10_deepspeed.py)

[Sign up](https://github.com/signup?ref_cta=Sign+up&ref_loc=header+logged+out&ref_page=%2F%3Cuser-name%3E%2F%3Crepo-name%3E%2Fblob%2Fshow&source=header-repo&source_repo=deepspeedai%2FDeepSpeedExamples)

Appearance settings

Resetting focus

You signed in with another tab or window. [Reload](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py) to refresh your session.You signed out in another tab or window. [Reload](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py) to refresh your session.You switched accounts on another tab or window. [Reload](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/training/cifar/cifar10_deepspeed.py) to refresh your session.Dismiss alert


[deepspeedai](https://github.com/deepspeedai)/**[DeepSpeedExamples](https://github.com/deepspeedai/DeepSpeedExamples)**Public

*   [Notifications](https://github.com/login?return_to=%2Fdeepspeedai%2FDeepSpeedExamples)You must be signed in to change notification settings
*   [Fork 1.1k](https://github.com/login?return_to=%2Fdeepspeedai%2FDeepSpeedExamples)
*   [Star 6.8k](https://github.com/login?return_to=%2Fdeepspeedai%2FDeepSpeedExamples) 

*   [Code](https://github.com/deepspeedai/DeepSpeedExamples)
*   [Issues 300](https://github.com/deepspeedai/DeepSpeedExamples/issues)
*   [Pull requests 25](https://github.com/deepspeedai/DeepSpeedExamples/pulls)
*   [Actions](https://github.com/deepspeedai/DeepSpeedExamples/actions)
*   [Projects](https://github.com/deepspeedai/DeepSpeedExamples/projects)
*   [Security and quality 0](https://github.com/deepspeedai/DeepSpeedExamples/security)
*   [Insights](https://github.com/deepspeedai/DeepSpeedExamples/pulse)

Additional navigation options

*   [Code](https://github.com/deepspeedai/DeepSpeedExamples)
*   [Issues](https://github.com/deepspeedai/DeepSpeedExamples/issues)
*   [Pull requests](https://github.com/deepspeedai/DeepSpeedExamples/pulls)
*   [Actions](https://github.com/deepspeedai/DeepSpeedExamples/actions)
*   [Projects](https://github.com/deepspeedai/DeepSpeedExamples/projects)
*   [Security and quality](https://github.com/deepspeedai/DeepSpeedExamples/security)
*   [Insights](https://github.com/deepspeedai/DeepSpeedExamples/pulse)

[](https://github.com/deepspeedai/DeepSpeedExamples)

## Collapse file tree

## Files

master

Search this repository(forward slash)forward slash/

*         .github  
*         applications  
*         benchmarks  
*         compression  
*         deepnvme  
*         evaluation  
*         inference  
*         scripts  
*         training  
    *          BingBertGlue  
    *          BingBertSquad  
    *          DeepSpeed-Domino  
    *          DeepSpeed-SuperOffload  
    *          DeepSpeed-ZenFlow  
    *          HelloDeepSpeed  
    *          MoQ  
    *          autotuning  
    *          bf16_master_weight  
    *          bing_bert  
    *          cifar  
        *         LICENSE  
        *         NOTICE.txt  
        *         README.md  
        *         cifar10_deepspeed.py  
        *         cifar10_tutorial.py  
        *         requirements.txt  
        *         run_ds.sh  
        *         run_ds_moe.sh  
        *         run_ds_prmoe.sh  

    *          data_efficiency  
    *          gan  
    *          imagenet  
    *          megatron  
    *          offload_states  
    *          pipeline_parallelism  
    *          stable_diffusion  
    *          tensor_parallel  

*       .gitignore  
*       .gitmodules  
*       .pre-commit-config.yaml  
*       CODEOWNERS  
*       CODE_OF_CONDUCT.md  
*       LICENSE  
*       README.md  
*       SECURITY.md  

## Breadcrumbs

1.   [DeepSpeedExamples](https://github.com/deepspeedai/DeepSpeedExamples/tree/master)
2.   /[training](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training)
3.   /[cifar](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/cifar)

/
# cifar10_deepspeed.py

Copy path

Blame More file actions

Blame More file actions

## Latest commit


[Update references to torchvision (](https://github.com/deepspeedai/DeepSpeedExamples/commit/b965b9cd827f096a24e382dcd3b4cd810c9595da)[#949](https://github.com/deepspeedai/DeepSpeedExamples/pull/949)[)](https://github.com/deepspeedai/DeepSpeedExamples/commit/b965b9cd827f096a24e382dcd3b4cd810c9595da)

Jan 21, 2025

[b965b9c](https://github.com/deepspeedai/DeepSpeedExamples/commit/b965b9cd827f096a24e382dcd3b4cd810c9595da)·Jan 21, 2025

## History

[History](https://github.com/deepspeedai/DeepSpeedExamples/commits/master/training/cifar/cifar10_deepspeed.py)

Open commit details

[](https://github.com/deepspeedai/DeepSpeedExamples/commits/master/training/cifar/cifar10_deepspeed.py)History

executable file

·

402 lines (353 loc) · 13.2 KB

 · [](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/CODEOWNERS#L1)

## Breadcrumbs

1.   [DeepSpeedExamples](https://github.com/deepspeedai/DeepSpeedExamples/tree/master)
2.   /[training](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training)
3.   /[cifar](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/cifar)

/
# cifar10_deepspeed.py

Top

## File metadata and controls

*   Code 
*   Blame 

executable file

·

402 lines (353 loc) · 13.2 KB

 · [](https://github.com/deepspeedai/DeepSpeedExamples/blob/master/CODEOWNERS#L1)

[Raw](https://github.com/deepspeedai/DeepSpeedExamples/raw/refs/heads/master/training/cifar/cifar10_deepspeed.py)

Copy raw file

Download raw file

You must be signed in to make or propose changes

More edit options

Open symbols panel

Edit and raw actions

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

329

330

331

332

333

334

335

336

337

338

339

340

341

342

343

344

345

346

347

348

349

350

351

352

353

354

355

356

357

358

359

360

361

362

363

364

365

366

367

368

369

370

371

372

373

374

375

376

377

378

379

380

381

382

383

384

385

386

387

388

389

390

391

392

393

394

395

396

397

398

399

400

401

402

import argparse

import os

import deepspeed

import torch

import torch.nn as nn

import torch.nn.functional as F

import torchvision

from torchvision import transforms

from deepspeed.accelerator import get_accelerator

from deepspeed.moe.utils import split_params_into_different_moe_groups_for_optimizer

def add_argument():

parser=argparse.ArgumentParser(description="CIFAR")

# For train.

parser.add_argument(

"-e",

"--epochs",

default=30,

type=int,

help="number of total epochs (default: 30)",

 )

parser.add_argument(

"--local_rank",

type=int,

default=-1,

help="local rank passed from distributed launcher",

 )

parser.add_argument(

"--log-interval",

type=int,

default=2000,

help="output logging information at a given interval",

 )

# For mixed precision training.

parser.add_argument(

"--dtype",

default="fp16",

type=str,

choices=["bf16", "fp16", "fp32"],

help="Datatype used for training",

 )

# For ZeRO Optimization.

parser.add_argument(

"--stage",

default=0,

type=int,

choices=[0, 1, 2, 3],

help="Datatype used for training",

 )

# For MoE (Mixture of Experts).

parser.add_argument(

"--moe",

default=False,

action="store_true",

help="use deepspeed mixture of experts (moe)",

 )

parser.add_argument(

"--ep-world-size", default=1, type=int, help="(moe) expert parallel world size"

 )

parser.add_argument(

"--num-experts",

type=int,

nargs="+",

default=[

1,

 ],

help="number of experts list, MoE related.",

 )

parser.add_argument(

"--mlp-type",

type=str,

default="standard",

help="Only applicable when num-experts > 1, accepts [standard, residual]",

 )

parser.add_argument(

"--top-k", default=1, type=int, help="(moe) gating top 1 and 2 supported"

 )

parser.add_argument(

"--min-capacity",

default=0,

type=int,

help="(moe) minimum capacity of an expert regardless of the capacity_factor",

 )

parser.add_argument(

"--noisy-gate-policy",

default=None,

type=str,

help="(moe) noisy gating (only supported with top-1). Valid values are None, RSample, and Jitter",

 )

parser.add_argument(

"--moe-param-group",

default=False,

action="store_true",

help="(moe) create separate moe param groups, required when using ZeRO w. MoE",

 )

# Include DeepSpeed configuration arguments.

parser=deepspeed.add_config_arguments(parser)

args=parser.parse_args()

return args

def create_moe_param_groups(model):

"""Create separate parameter groups for each expert."""

parameters= {"params": [p for p in model.parameters()], "name": "parameters"}

return split_params_into_different_moe_groups_for_optimizer(parameters)

def get_ds_config(args):

"""Get the DeepSpeed configuration dictionary."""

ds_config= {

"train_batch_size": 16,

"steps_per_print": 2000,

"optimizer": {

"type": "Adam",

"params": {

"lr": 0.001,

"betas": [0.8, 0.999],

"eps": 1e-8,

"weight_decay": 3e-7,

 },

 },

"scheduler": {

"type": "WarmupLR",

"params": {

"warmup_min_lr": 0,

"warmup_max_lr": 0.001,

"warmup_num_steps": 1000,

 },

 },

"gradient_clipping": 1.0,

"prescale_gradients": False,

"bf16": {"enabled": args.dtype=="bf16"},

"fp16": {

"enabled": args.dtype=="fp16",

"fp16_master_weights_and_grads": False,

"loss_scale": 0,

"loss_scale_window": 500,

"hysteresis": 2,

"min_loss_scale": 1,

"initial_scale_power": 15,

 },

"wall_clock_breakdown": False,

"zero_optimization": {

"stage": args.stage,

"allgather_partitions": True,

"reduce_scatter": True,

"allgather_bucket_size": 50000000,

"reduce_bucket_size": 50000000,

"overlap_comm": True,

"contiguous_gradients": True,

"cpu_offload": False,

 },

 }

return ds_config

if args.moe_param_group:

parameters=create_moe_param_groups(net)

# Initialize DeepSpeed to use the following features.

# 1) Distributed model.

# 2) Distributed data loader.

# 3) DeepSpeed optimizer.

ds_config=get_ds_config(args)

model_engine, optimizer, trainloader,  __ =deepspeed.initialize(

args=args,

model=net,

model_parameters=parameters,

training_data=trainset,

config=ds_config,

 )

# Get the local device name (str) and local rank (int).

local_device=get_accelerator().device_name(model_engine.local_rank)

local_rank=model_engine.local_rank

# For float32, target_dtype will be None so no datatype conversion needed.

target_dtype=None

if model_engine.bfloat16_enabled():

target_dtype=torch.bfloat16

elif model_engine.fp16_enabled():

target_dtype=torch.half

# Define the Classification Cross-Entropy loss function.

criterion=nn.CrossEntropyLoss()

########################################################################

# Step 3. Train the network.

#

# This is when things start to get interesting.

# We simply have to loop over our data iterator, and feed the inputs to the

# network and optimize. (DeepSpeed handles the distributed details for us!)

########################################################################

for epoch in range(args.epochs): # loop over the dataset multiple times

running_loss=0.0

for i, data in enumerate(trainloader):

# Get the inputs. ``data`` is a list of [inputs, labels].

inputs, labels=data[0].to(local_device), data[1].to(local_device)

# Try to convert to target_dtype if needed.

if target_dtype!=None:

inputs=inputs.to(target_dtype)

outputs=model_engine(inputs)

loss=criterion(outputs, labels)

model_engine.backward(loss)

model_engine.step()

# Print statistics

running_loss+=loss.item()

if local_rank==0 and i%args.log_interval== (

args.log_interval-1

 ): # Print every log_interval mini-batches.

print(

f"[{epoch+1 : d}, {i+1 : 5d}] loss: {running_loss/args.log_interval : .3f}"

 )

running_loss=0.0

print("Finished Training")

########################################################################

# Step 4. Test the network on the test data.

########################################################################

test(model_engine, testset, local_device, target_dtype)

if __name__ =="__main__":

args=add_argument()

main(args)

## Footer

[](https://github.com/) © 2026 GitHub,Inc. 

### Footer navigation

*   [Terms](https://docs.github.com/site-policy/github-terms/github-terms-of-service)
*   [Security](https://github.com/security)
*   [Status](https://www.githubstatus.com/)
*   [Community](https://github.community/)
*   [Docs](https://docs.github.com/)
*    Manage cookies 
*    Do not share my personal information 

 You can’t perform that action at this time.