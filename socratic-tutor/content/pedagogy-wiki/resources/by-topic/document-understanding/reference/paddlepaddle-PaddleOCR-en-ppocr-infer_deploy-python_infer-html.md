# Source: https://paddlepaddle.github.io/PaddleOCR/en/ppocr/infer_deploy/python_infer.html
# Title: Python Inference for PP-OCR Model Zoo¶
# Fetched via: search
# Date: 2026-04-09

Paddle provides a variety of deployment schemes to meet the deployment requirements of different scenarios.
Please choose according to the actual situation:
PP-OCR has supported muti deployment schemes.
Click the link to get the specific tutorial.
- Python Inference
- C++ Inference
- Serving (Python/C++)
- Paddle-Lite (ARM CPU/OpenCL ARM GPU)
- Paddle.js
- Jetson Inference
- Paddle2ONNX
If you need the deployment tutorial of academic algorithm models other than PP-OCR, please directly enter the main page of corresponding algorithms, entrance。

```

1. 1 Introduction
2. 2 Core Capabilities 1. 2.1 PP-OCRv5
   2. 2.2 PP-StructureV3
   3. 2.3 PP-ChatOCRv4
3. 3 Codebase Architecture Design 1. 3.1 Overall Architecture
   2. 3.2 Inference Library Design
4. 4 Deployment 1. 4.1 High-Performance Inference
   2. 4.2 Serving
   3. 4.3 On-Device Deployment
   4. 4.4 MCP Server
5. 5 Conclusion
6. A Acknowledgments
7. B Usage of command and API details 1. B.1 Run inference by CLI
   2. B.2 Run inference by Python API
8. C More details on MCP host configuration

001

…

###### Abstract

This technical report introduces PaddleOCR 3.0, an Apache-licensed open-source toolkit for OCR and document parsing. To address the growing demand for document understanding in the era of large language models, PaddleOCR 3.0 presents three major solutions: (1) PP-OCRv5 for multilingual text recognition, (2) PP-StructureV3 for hierarchical document parsing, and (3) PP-ChatOCRv4 for key information extraction.
Compared to mainstream vision-language models (VLMs), these models with fewer than 100 million parameters achieve competitive accuracy and efficiency, rivaling billion-parameter VLMs. In addition to offering a high-quality OCR model library, PaddleOCR 3.0 provides efficient tools for training, inference, and deployment, supports heterogeneous hardware acceleration, and enables developers to easily build intelligent document applications.

…

In this context, we introduce PaddleOCR 3.0, a major release designed to systematically enhance text recognition accuracy and document parsing capabilities, with a particular focus on the complex scenarios encountered in modern AI applications. PaddleOCR 3.0 encompasses several core innovations. First, it presents the high-precision text recognition pipeline PP-OCRv5, which leverages advanced model architectures and training strategies to deliver state-of-the-art accuracy across printed, handwritten, and multilingual documents, while maintaining efficiency suitable for both cloud and edge deployment.

…

## 2 Core Capabilities

PaddleOCR 3.0 comprises three core capabilities: PP-OCRv5, PP-StructureV3 and PP-ChatOCRv4. This section elaborates on the problems addressed by these capabilities, details of the model solution, and their performance metrics.

### 2.1 PP-OCRv5

PP-OCRv5 is a high-precision and lightweight OCR system designed to perform effectively in a wide range of scenarios. It supports a diverse range of scripts within a single model, including Simplified Chinese, Traditional Chinese, Chinese Pinyin, English, and Japanese. To address the diverse hardware environments and varying requirements for inference speed, PP-OCRv5 offers two distinct model variants: a server version and a mobile version.
The server version is specifically optimized for systems equipped with hardware accelerators such as GPUs, thereby enabling accelerated inference and higher throughput. In contrast, the mobile version is tailored for deployment in CPU-only environments, with optimizations targeting resource-constrained devices. Unless otherwise specified, all mentions of PP-OCRv5 in this paper refer by default to the server version. Figure 3 illustrates the framework of PP-OCRv5, which comprises four key components: image preprocessing, text detection, text line orientation classification, and text recognition. The following will introduce these four components.

…

## 3 Codebase Architecture Design

### 3.1 Overall Architecture

The overall architecture of the PaddleOCR 3.0 codebase is illustrated in Figure 10. At its foundation, PaddleOCR 3.0 is built upon the PaddlePaddle framework (Ma et al., 2019), which incorporates a neural network compiler for performance optimization, supplies a highly extensible intermediate representation (IR), and ensures broad hardware compatibility. Building on this foundation, PaddleOCR 3.0 is structured around two core components: a model training toolkit and an inference library. The inference library offers flexible integration paths that naturally extend to deployment. The deployment capabilities will be introduced in Section 4.
The training toolkit provides a comprehensive suite of utilities that support the complete training pipeline for various models, including text detection models, text recognition models, etc. It also facilitates the conversion of trained models from dynamic graph format to static graph format, thereby enhancing their suitability for inference and deployment in production environments. Users can execute Python scripts with a single command to perform tasks such as model training, evaluation, and export. Additionally, various parameters can be configured to meet different requirements, such as specifying the path to a pre-trained model or using a custom dataset directory.
Complementing this, the inference library is designed to be lightweight and highly efficient. It supports loading both officially released inference models and custom models trained by users. The library enables inference across eight end-to-end model pipelines and can be readily integrated into real-world applications. We will elaborate the design of the inference library in the next subsection. The inference library serves as the foundation for downstream deployment capabilities, including high-performance inference across various frameworks, deploying the model pipeline as a service, deploying it to mobile devices, and running it via a Model Context Protocol (MCP) server.

…

- •

  Interface Layer: The library offers both a Python API and a CLI for user interaction. In PaddleOCR 3.0, all OCR tasks are accessed through a consistent and unified Python API. To facilitate a smooth transition for existing users, the API preserves backward compatibility for key methods and parameters. The CLI has been completely redesigned compared to PaddleOCR 2.x, introducing subcommands that clearly distinguish between different tasks and thereby providing a cleaner, more intuitive user experience.
- •

  Wrapper Layer: This layer offers Pythonic wrappers for core PaddleX components, including models and pipelines. These wrappers deliver unified interfaces and flexible configuration management. In addition to maintaining the backward compatibility in the argument-based approach previously preferred in PaddleOCR 2.x, the PaddleX-style configuration file-based approach is also supported, which allows configurations to be stored and reused in a portable and reproducible manner.
- •

  Foundation Layer: At the foundation lies the PaddleX 3.0 toolkit, which forms the core of PaddleOCR 3.0. It offers powerful features for inference optimization and model deployment, which are fully integrated into PaddleOCR 3.0. Transferring the basis from PaddleOCR scripts to PaddleX ensures the separation of roles of the model training toolkit and the inference library, eliminating redundant entry points and clarifying functional boundaries. This decoupling allows each component to evolve independently, reduces user confusion, and lays the foundation for a more robust and maintainable system design.

…

## 4 Deployment

An overview of the deployment capabilities of PaddleOCR 3.0 is depicted in Figure 11. To support a wide range of application scenarios, PaddleOCR 3.0 offers flexible and comprehensive deployment options, including high-performance inference, serving, and on-device deployment. In real-world production environments, OCR-related systems are often subject to constraints beyond recognition accuracy, such as latency, throughput, and hardware compatibility.
PaddleOCR addresses these requirements by providing configurable deployment tools that simplify integration across various platforms. In addition, to facilitate integration with LLM applications, PaddleOCR provides an MCP server, which allows users to leverage high-performance inference pipelines or pipeline servers.

### 4.1 High-Performance Inference

PaddleOCR 3.0 provides the high-performance inference feature that enables users to optimize runtime performance without the need to manually tune low-level configurations. High-performance inference provides notable acceleration for some key models. For instance, on NVIDIA Tesla T4 devices, enabling high-performance inference reduces the single-model inference latency of PP-OCRv5_mobile_rec by 73.1% and that of PP-OCRv5_mobile_det by 40.4%. The key features of PaddleOCR 3.0’s high-performance inference capability include:
- •

  Automatic selection of appropriate inference backends based on the runtime environment and model characteristics, including support for Paddle Inference, OpenVINO (Intel Corporation, 2018), ONNX Runtime (Microsoft Corporation, 2018), and TensorRT (NVIDIA Corporation, 2017).
- •

  Built-in optimization strategies such as multi-threading and FP16 inference to better utilize hardware resources.
- •

  On-demand model conversion from PaddlePaddle static graphs to ONNX format to enable acceleration on compatible inference engines.

Users can easily achieve inference acceleration by enabling the enable_hpi switch, while all underlying optimization details are managed by PaddleOCR. For advanced needs, PaddleOCR also supports fine-grained tuning of high-performance inference configurations in pipelines by passing Python/command line parameters or modifying configuration files.

…

- •

  Basic Serving: A lightweight solution based on FastAPI (Ramírez, 2018) with minimal setup, suitable for rapid validation and scenarios with low concurrency requirements. For this solution, users can run any pipeline as a service with a single command via the CLI. For the client-side code, PaddleOCR 3.0 provides rich calling examples in seven programming languages: Python, C++, Java, Go, C#, Node.js, and PHP. Users can refer to these examples to quickly integrate the service capabilities into their own applications.

…

### 4.4 MCP Server

PaddleOCR 3.0 provides a lightweight MCP server, enabling smooth integration of PaddleOCR’s core capabilities into any MCP-compatible host. Both the OCR and PP-StructureV3 pipelines are currently accessible as tools via the MCP server.

Built on top of the PaddleOCR inference library, the MCP server supports various inference and deployment methods provided by PaddleOCR. At present, it can operate in one of three working modes:
- •

  Local: Runs the PaddleOCR pipeline directly on the local machine using the installed Python library. This mode is suitable for offline usage and situations with strict data privacy requirements. High-performance inference can be activated to accelerate the inference process.
- •

  AI Studio: Utilizes cloud services hosted by the PaddlePaddle AI Studio community (PaddlePaddle Team, 2019). This mode is ideal for quickly trying out features, validating solutions, and for no-code development scenarios.

…

Regardless of the selected working mode, setting up the PaddleOCR MCP server is straightforward for users. Example configuration files are included in the appendix Appendix for reference. Additionally, the PaddleOCR MCP server supports both stdio and Streamable HTTP transport mechanisms, offering flexibility for a wide range of deployment scenarios. With its adaptable architecture and support for multiple deployment modes, the PaddleOCR MCP server can effectively address diverse real-world application needs, delivering robust and scalable solutions for both individual developers and enterprise users.

…

## Appendix B Usage of command and API details

To use PaddleOCR 3.0, you can simply install the paddleocr package from PyPI. PaddleOCR 3.0 provides command-line interface (CLI) and Python API for users to use conveniently.

### B.1 Run inference by CLI

We provide convenient CLI methods for users to quickly experience the capabilities of PP-OCRv5, PP-StructureV3, and PP-ChatOCRv4, as follows:

⬇

1# Run PP-OCRv5 inference

2paddleocr ocr -i test.png \

3 --use_doc_orientation_classify False \

…

12# Get the Qianfan API Key at first, then run PP-ChatOCRv4

13paddleocr pp_chatocrv4_doc -i test.png \

14 -k number \

15 --qianfan_api_key your_api_key \

16 --use_doc_orientation_classify False \

…

### B.2 Run inference by Python API

We also provide a clean interface to facilitate users in using and integrating it into their own projects.

1. PP-OCRv5 Example

⬇

1# Initialize PaddleOCR instance

2from paddleocr import PaddleOCR

3ocr = PaddleOCR(

4 use_doc_orientation_classify=False,

5 use_doc_unwarping=False,
6 use_textline_orientation=False)

7

8# Run OCR inference on a sample image

9result = ocr.predict(input="test.png")

10

11# Visualize the results and save the JSON results

12for res in result:

13 res.print()

14 res.save_to_img("output")

15 res.save_to_json("output")
2. PP-StructureV3 Example

⬇

1# Initialize PPStructureV3 instance

2from paddleocr import PPStructureV3

3

4pipeline = PPStructureV3(

5 use_doc_orientation_classify=False,

6 use_doc_unwarping=False)

7

8# Run PPStructureV3 inference
9output = pipeline.predict(input="test.png")

10

11# Visualize the results and save the JSON results

12for res in output:

13 res.print()

14 res.save_to_json(save_path="output")

15 res.save_to_markdown(save_path="output")

3. PP-ChatOCRv4 Example
⬇

1from paddleocr import PPChatOCRv4Doc

2

3chat_bot_config = {

4 "module_name": "chat_bot",

5 "model_name": "xxx",

6 "base_url": "https://qianfan.baidubce.com/v2",

7 "api_type": "openai",
8 "api_key": "api_key", # your api_key

9}

10

11retriever_config = {

12 "module_name": "retriever",

13 "model_name": "embedding-v1",

14 "base_url": "https://qianfan.baidubce.com/v2",

15 "api_type": "qianfan",
16 "api_key": "api_key", # your api_key

17}

18

19# Initialize PPChatOCRv4Doc instance

20pipeline = PPChatOCRv4Doc(

21 use_doc_orientation_classify=False,

22 use_doc_unwarping=False)

23

24visual_predict_res = pipeline.visual_predict(
25 input="test.png",

26 use_common_ocr=True,

27 use_seal_recognition=True,

28 use_table_recognition=True)

29

30mllm_predict_info = None

31use_mllm = False

32visual_info_list = []

33

34for res in visual_predict_res:

35 visual_info_list.append(res["visual_info"])
36 layout_parsing_result = res["layout_parsing_result"]

37

38vector_info = pipeline.build_vector(

39 visual_info_list,

40 flag_save_bytes_vector=True,

41 retriever_config=retriever_config)

42

43chat_result = pipeline.chat(

44 key_list=["number of people"],

45 visual_info=visual_info_list,
46 vector_info=vector_info,

47 mllm_predict_info=mllm_predict_info,

48 chat_bot_config=chat_bot_config,

49 retriever_config=retriever_config)

50print(chat_result)

The General OCR pipeline is designed to solve text recognition tasks, extracting text information from images and outputting it in text form. This pipeline integrates the end-to-end OCR series systems, PP-OCRv5 and PP-OCRv4, supporting recognition of over 80 languages. Additionally, it includes functions for image orientation correction and distortion correction.
Based on this pipeline, precise text content prediction at the millisecond level on CPUs can be achieved, covering a wide range of applications including general, manufacturing, finance, and transportation sectors. The pipeline also provides flexible deployment options, supporting calls in various programming languages on multiple hardware platforms. Moreover, it offers the capability for custom development, allowing you to train and optimize on your own dataset. The trained models can also be seamlessly integrated.
**The General OCR pipeline includes mandatory text detection and text recognition modules, as well as optional document image orientation classification, text image correction, and text line orientation classification modules.** The document image orientation classification and text image correction modules are integrated as a document preprocessing sub-line into the General OCR pipeline. Each module contains multiple models, and you can choose the model based on the benchmark test data below.

### 1.1 Model benchmark data ¶

**If you prioritize model accuracy, choose a high-accuracy model; if you prioritize inference speed, choose a faster inference model; if you care about model storage size, choose a smaller model.**

> The inference time only includes the model inference time and does not include the time for pre- or post-processing.

**Document Image Orientation Classification Module (Optional):**
|Model|Model Download Link|Top-1 Acc (%)|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Introduction|
|--|--|--|--|--|--|--|
|PP-LCNet_x1_0_doc_ori|Inference Model/Training Model|99.06|2.62 / 0.59|3.24 / 1.19|7|A document image classification model based on PP-LCNet_x1_0, with four categories: 0 degrees, 90 degrees, 180 degrees, and 270 degrees.|

…

|Model|Model Download Link|CER|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Description|
|--|--|--|--|--|--|--|
|UVDoc|Inference Model/Training Model|0.179|19.05 / 19.05|- / 869.82|30.3|High-accuracy text image rectification model|

…

|Model|Model Download Link|Top-1 Acc (%)|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Introduction|
|--|--|--|--|--|--|--|
|PP-LCNet_x0_25_textline_ori|Inference Model/Training Model|98.85|2.16 / 0.41|2.37 / 0.73|0.96|Text line classification model based on PP-LCNet_x0_25, with two classes: 0 degrees and 180 degrees|
|PP-LCNet_x1_0_textline_ori|Inference Model/Training Model|99.42|- / -|2.98 / 2.98|6.5|Text line classification model based on PP-LCNet_x1_0, with two classes: 0 degrees and 180 degrees|

…

|Model|Model Download Link|Detection Hmean (%)|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Introduction|
|--|--|--|--|--|--|--|
|PP-OCRv5_server_det|Inference Model/Training Model|83.8|89.55 / 70.19|383.15 / 383.15|84.3|PP-OCRv5 server-side text detection model with higher accuracy, suitable for deployment on high-performance servers|
|PP-OCRv5_mobile_det|Inference Model/Training Model|79.0|10.67 / 6.36|57.77 / 28.15|4.7|PP-OCRv5 mobile-side text detection model with higher efficiency, suitable for deployment on edge devices|
|PP-OCRv4_server_det|Inference Model/Training Model|69.2|127.82 / 98.87|585.95 / 489.77|109|PP-OCRv4 server-side text detection model with higher accuracy, suitable for deployment on high-performance servers|
|PP-OCRv4_mobile_det|Inference Model/Training Model|63.8|9.87 / 4.17|56.60 / 20.79|4.7|PP-OCRv4 mobile-side text detection model with higher efficiency, suitable for deployment on edge devices|

…

|PP-OCRv3_server_det|Inference Model/Training Model|Accuracy comparable to PP-OCRv4_server_det|119.50 / 75.00|379.35 / 318.35|102.1|PP-OCRv3 server text detection model with higher accuracy, suitable for deployment on high-performance servers|

…

|Model|Model Download Link|Recognition Avg Accuracy (%)|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Introduction|
|--|--|--|--|--|--|--|
|PP-OCRv5_server_rec|Inference Model/Training Model|86.38|8.46 / 2.36|31.21 / 31.21|81|PP-OCRv5_rec is a next-generation text recognition model. This model is dedicated to efficiently and accurately supporting four major languages—Simplified Chinese, Traditional Chinese, English, and Japanese—with a single model. It supports complex text scenarios, including handwritten, vertical text, pinyin, and rare characters. While maintaining recognition accuracy, it also balances inference speed and model robustness, providing efficient and precise technical support for document understanding in various scenarios.|
|PP-OCRv5_mobile_rec|Inference Model/Training Model|81.29|5.43 / 1.46|21.20 / 5.32|16|PP-OCRv5_rec is a next-generation text recognition model. This model is dedicated to efficiently and accurately supporting four major languages—Simplified Chinese, Traditional Chinese, English, and Japanese—with a single model. It supports complex text scenarios, including handwritten, vertical text, pinyin, and rare characters. While maintaining recognition accuracy, it also balances inference speed and model robustness, providing efficient and precise technical support for document understanding in various scenarios.|
|PP-OCRv4_server_rec_doc|Inference Model/Training Model|86.58|8.69 / 2.78|37.93 / 37.93|182|PP-OCRv4_server_rec_doc is trained on a mixed dataset of more Chinese document data and PP-OCR training data based on PP-OCRv4_server_rec. It has added the ability to recognize some traditional Chinese characters, Japanese, and special characters, and can support the recognition of more than 15,000 characters. In addition to improving the text recognition capability related to documents, it also enhances the general text recognition capability.|
|PP-OCRv4_mobile_rec|Inference Model/Training Model|78.74|5.26 / 1.12|17.48 / 3.61|10.5|The lightweight recognition model of PP-OCRv4 has high inference efficiency and can be deployed on various hardware devices, including edge devices.|
|PP-OCRv4_server_rec|Inference Model/Training Model|85.19|8.75 / 2.49|36.93 / 36.93|173|The server-side model of PP-OCRv4 offers high inference accuracy and can be deployed on various types of servers.|
|en_PP-OCRv4_mobile_rec|Inference Model/Training Model|70.39|4.81 / 1.23|17.20 / 4.18|7.5|The ultra-lightweight English recognition model, trained based on the PP-OCRv4 recognition model, supports the recognition of English letters and numbers.|

…

❗ The above list features the **4 core models** that the text recognition module primarily supports. In total, this module supports **18 models**. The complete list of models is as follows:
👉Model List Details * **PP-OCRv5 Multi-Scenario Model** |Model|Model Download Link|Chinese Recognition Avg Accuracy (%)|English Recognition Avg Accuracy (%)|Traditional Chinese Recognition Avg Accuracy (%)|Japanese Recognition Avg Accuracy (%)|GPU Inference Time (ms) [Normal Mode / High-Performance Mode]|CPU Inference Time (ms) [Normal Mode / High-Performance Mode]|Model Storage Size (MB)|Description|

…

This model efficiently and accurately supports four major languages with a single model: Simplified Chinese, Traditional Chinese, English, and Japanese. It recognizes complex text scenarios including handwritten, vertical text, pinyin, and rare characters. While maintaining recognition accuracy, it balances inference speed and model robustness, providing efficient and precise technical support for document understanding in various scenarios.|

…

This model efficiently and accurately supports four major languages with a single model: Simplified Chinese, Traditional Chinese, English, and Japanese. It recognizes complex text scenarios including handwritten, vertical text, pinyin, and rare characters. While maintaining recognition accuracy, it balances inference speed and model robustness, providing efficient and precise technical support for document understanding in various scenarios.|

…

It has added the recognition capabilities for some traditional Chinese characters, Japanese, and special characters. The number of recognizable characters is over 15,000. In addition to the improvement in document-related text recognition, it also enhances the general text recognition capability.|
|PP-OCRv4_mobile_rec|Inference Model/Training Model|78.74|5.26 / 1.12|17.48 / 3.61|10.5|The lightweight recognition model of PP-OCRv4 has high inference efficiency and can be deployed on various hardware devices, including edge devices.|
|PP-OCRv4_server_rec|Inference Model/Training Model|85.19|8.75 / 2.49|36.93 / 36.93|173|The server-side model of PP-OCRv4 offers high inference accuracy and can be deployed on various types of servers.|

…

|Mode|GPU Configuration|CPU Configuration|Acceleration Technology Combination|
|--|--|--|--|
|Normal Mode|FP32 Precision / No TRT Acceleration|FP32 Precision / 8 Threads|PaddleInference|
|High-Performance Mode|Optimal combination of pre-selected precision types and acceleration strategies|FP32 Precision / 8 Threads|Pre-selected optimal backend (Paddle/OpenVINO/TRT, etc.)|

…

|Pipeline configuration|description|
|--|--|
|OCR-default|Default configuration|
|OCR-nopp-mobile|Based on the default configuration, document image preprocessing is disabled and mobile det and rec models are used|
|OCR-nopp-server|Based on the default configuration, document image preprocessing is disabled|
|OCR-nopp-min736-mobile|Based on the default configuration, document image preprocessing is disabled, det model input resizing strategy is set to min+736, and mobile det and rec models are used|
|OCR-nopp-min736-server|Based on the default configuration, document image preprocessing is disabled, and the det model input resizing strategy is set to min+736|

…

|OCR-nopp-max960-server|Based on the default configuration, document image preprocessing is disabled, and the det model input resizing strategy is set to max+960|
|OCR-nopp-min1280-server|Based on the default configuration, document image preprocessing is disabled, and the det model input resizing strategy is set to min+1280|
|OCR-nopp-min1280-mobile|Based on the default configuration, document image preprocessing is disabled, det model input resizing strategy is set to min+1280, and mobile det and rec models are used|

…

If you are satisfied with the performance of the pipeline, you can directly integrate and deploy it. You can choose to download the deployment package from the cloud, or refer to the methods in Section 2.2 Local Experience for local deployment. If you are not satisfied with the effect, you can **fine-tune the models in the pipeline using your private data**.

# Mobile deployment based on Paddle-Lite¶

This tutorial will introduce how to use Paddle-Lite to deploy PaddleOCR ultra-lightweight Chinese and English detection models on mobile phones.

Paddle-Lite is a lightweight inference engine for PaddlePaddle. It provides efficient inference capabilities for mobile phones and IoT, and extensively integrates cross-platform hardware to provide lightweight deployment solutions for end-side deployment issues.

## 1. Preparation¶

### Preparation environment¶

- Computer (for Compiling Paddle Lite)

- Mobile phone (arm7 or arm8)

### 1.1 Prepare the cross-compilation environment¶

The cross-compilation environment is used to compile C++ demos of Paddle Lite and PaddleOCR. Supports multiple development environments.

For the compilation process of different development environments, please refer to the corresponding documents.

### 1.2 Prepare Paddle-Lite library¶

There are two ways to obtain the Paddle-Lite library:



[Recommended] Download directly, the download link of the Paddle-Lite library is as follows:

Platform Paddle-Lite library download link Android arm7 / arm8 IOS arm7 / arm8

Note: 1. The above Paddle-Lite library is compiled from the Paddle-Lite 2.10 branch. For more information about Paddle-Lite 2.10, please refer to link.
**Note: It is recommended to use paddlelite>=2.10 version of the prediction library, other prediction library versions download link**



Compile Paddle-Lite to get the prediction library. The compilation method of Paddle-Lite is as follows:

|1 2 3 4 5||
|--|--|
Note: When compiling Paddle-Lite to obtain the Paddle-Lite library, you need to turn on the two options
`--with_cv=ON --with_extra=ON`,

`--arch` means the

`arm` version, here is designated as armv8,

More compilation commands refer to the introduction link 。

After directly downloading the Paddle-Lite library and decompressing it, you can get the

`inference_lite_lib.android.armv8/` folder, and the Paddle-Lite library obtained by compiling Paddle-Lite is located
`Paddle-Lite/build.lite.android.armv8.gcc/inference_lite_lib.android.armv8/` folder.

The structure of the prediction library is as follows:

|1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22||
|--|--|

## 2 Run¶

### 2.1 Inference Model Optimization¶

Paddle Lite provides a variety of strategies to automatically optimize the original training model, including quantization, sub-graph fusion, hybrid scheduling, Kernel optimization and so on. In order to make the optimization process more convenient and easy to use, Paddle Lite provide opt tools to automatically complete the optimization steps and output a lightweight, optimal executable model.
If you have prepared the model file ending in .nb, you can skip this step.

The following table also provides a series of models that can be deployed on mobile phones to recognize Chinese. You can directly download the optimized model.
|Version|Introduction|Model size|Detection model|Text Direction model|Recognition model|Paddle-Lite branch|
|--|--|--|--|--|--|--|
|PP-OCRv3|extra-lightweight chinese OCR optimized model|16.2M|download link|download link|download link|v2.10|
|PP-OCRv3(slim)|extra-lightweight chinese OCR optimized model|5.9M|download link|download link|download link|v2.10|
|PP-OCRv2|extra-lightweight chinese OCR optimized model|11M|download link|download link|download link|v2.10|
|PP-OCRv2(slim)|extra-lightweight chinese OCR optimized model|4.6M|download link|download link|download link|v2.10|
If you directly use the model in the above table for deployment, you can skip the following steps and directly read Section 2.2.
If the model to be deployed is not in the above table, you need to follow the steps below to obtain the optimized model.

Step 1: Refer to document to install paddlelite, which is used to convert paddle inference model to paddlelite required for running nb model

|`1`||
|--|--|
After installation, the following commands can view the help information
|`1`||
|--|--|
Introduction to paddle_lite_opt parameters:

|Options|Description|
|--|--|
|--model_dir|The path of the PaddlePaddle model to be optimized (non-combined form)|
|--model_file|The network structure file path of the PaddlePaddle model (combined form) to be optimized|
|--param_file|The weight file path of the PaddlePaddle model (combined form) to be optimized|
|--optimize_out_type|Output model type, currently supports two types: protobuf and naive_buffer, among which naive_buffer is a more lightweight serialization/deserialization implementation. If you need to perform model prediction on the mobile side, please set this option to naive_buffer. The default is protobuf|
|--optimize_out|The output path of the optimized model|
|--valid_targets|The executable backend of the model, the default is arm. Currently it supports x86, arm, opencl, npu, xpu, multiple backends can be specified at the same time (separated by spaces), and Model Optimize Tool will automatically select the best method. If you need to support Huawei NPU (DaVinci architecture NPU equipped with Kirin 810/990 Soc), it should be set to npu, arm|
|--record_tailoring_info|When using the function of cutting library files according to the model, set this option to true to record the kernel and OP information contained in the optimized model. The default is false|
`--model_dir` is suitable for the non-combined mode of the model to be optimized, and the inference model of PaddleOCR is the combined mode, that is, the model structure and model parameters are stored in a single file.
Step 2: Use paddle_lite_opt to convert the inference model to the mobile model format.

The following takes the ultra-lightweight Chinese model of PaddleOCR as an example to introduce the use of the compiled opt file to complete the conversion of the inference model to the Paddle-Lite optimized model

|1 2 3 4 5 6 7 8 9 10||
|--|--|
After the conversion is successful, there will be more files ending with

`.nb` in the inference model directory, which is the successfully converted model file.

### 2.2 Run optimized model on Phone¶

Some preparatory work is required first.



Prepare an Android phone with arm8. If the compiled prediction library and opt file are armv7, you need an arm7 phone and modify ARM_ABI = arm7 in the Makefile.



Make sure the phone is connected to the computer, open the USB debugging option of the phone, and select the file transfer mode.
Install the adb tool on the computer.

3.1. Install ADB for MAC:

`1`

`brew cask install android-platform-tools`

3.2. Install ADB for Linux

1 2

`sudo apt update sudo apt install -y wget adb`

3.3. Install ADB for windows
To install on win, you need to go to Google's Android platform to download the adb package for installation:link

Verify whether adb is installed successfully

`1`

`adb devices`

If there is device output, it means the installation is successful。

1 2

`List of devices attached 744be294 device`
Prepare optimized models, prediction library files, test images and dictionary files used.

|1 2 3 4 5 6 7 8 9 10 11 12 13||
|--|--|
Prepare the test image, taking PaddleOCR/doc/imgs/11.jpg as an example, copy the image file to the demo/cxx/ocr/debug/ folder. Prepare the model files optimized by the lite opt tool, ch_PP-OCRv3_det_slim_opt.nb , ch_PP-OCRv3_rec_slim_opt.nb , and place them under the demo/cxx/ocr/debug/ folder.
The structure of the OCR demo is as follows after the above command is executed:

|1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18||
|--|--|
**Note**:

`ppocr_keys_v1.txt`is a Chinese dictionary file. If the nb model is used for English recognition or other language recognition, dictionary file should be replaced with a dictionary of the corresponding language. PaddleOCR provides a variety of dictionaries under ppocr/utils/, including:
|1 2 3 4 5 6||
|--|--|


`config.txt`of the detector and classifier, as shown below:

1 2 3 4 5 6
`max_side_len 960 # Limit the maximum image height and width to 960 det_db_thresh 0.3 # Used to filter the binarized image of DB prediction, setting 0.-0.3 has no obvious effect on the result det_db_box_thresh 0.5 # DDB post-processing
filter box threshold, if there is a missing box detected, it can be reduced as appropriate det_db_unclip_ratio 1.6 # Indicates the compactness of the text box, the smaller the value, the closer the text box to the text use_direction_classify 0 # Whether to use the direction classifier, 0 means not to use, 1 means to use rec_image_height 48 # The height of the input image of the recognition model, the PP-OCRv3 model needs to be set to 48, and the PP-OCRv2 model needs to be set to 32`
Run Model on phone

After the above steps are completed, you can use adb to push the file to the phone to run, the steps are as follows:

|1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20||
|--|--|
If you modify the code, you need to recompile and push to the phone.

The outputs are as follows:

…

A2: Replace the .jpg test image under ./debug with the image you want to test, and run adb push to push new image to the phone.

Q3: How to package it into the mobile APP?

A3: This demo aims to provide the core algorithm part that can run OCR on mobile phones. Further, PaddleOCR/deploy/android_demo is an example of encapsulating this demo into a mobile app for reference.
Q4: When running the demo, an error is reported

`Error: This model is not supported, because kernel for 'io_copy' is not supported by Paddle-Lite.`

A4: The problem is that the installed paddlelite version does not match the downloaded prediction library version. Make sure that the paddleliteopt tool matches your prediction library version, and try to switch to the nb model again.