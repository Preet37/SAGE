# Source: https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html
# Title: Generate Synthetic Data — Omniverse Workflows (Defect Detection)
# Fetched via: jina
# Date: 2026-04-09

Title: Viewport Widgets


# Workflows Overview — Omniverse Workflows



✎️ Help us improve. Take the [Omniverse Documentation Annual User Survey](https://nvidiamr.co1.qualtrics.com/jfe/form/SV_agfVIXDT0wg6J6u). Survey ends soon!


Search Ctrl+K

*   [twitter](https://twitter.com/nvidiaomniverse)
*   [youtube](https://www.youtube.com/channel/UCSKUoczbGAcMld7HjpCR8OA)
*   [instagram](https://www.instagram.com/nvidiaomniverse)
*   [www](https://www.nvidia.com/en-us/omniverse/)
*   [linkedin](https://www.linkedin.com/showcase/nvidia-omniverse)
*   [twitch](https://www.twitch.tv/nvidiaomniverse)

Search Ctrl+K


*   [twitter](https://twitter.com/nvidiaomniverse)
*   [youtube](https://www.youtube.com/channel/UCSKUoczbGAcMld7HjpCR8OA)
*   [instagram](https://www.instagram.com/nvidiaomniverse)
*   [www](https://www.nvidia.com/en-us/omniverse/)
*   [linkedin](https://www.linkedin.com/showcase/nvidia-omniverse)
*   [twitch](https://www.twitch.tv/nvidiaomniverse)

Table of Contents

Workflows

*   [Workflows Overview](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html#)
*   [Extension Workflows](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions.html)

    *   [Make an Extension To Spawn Primitives](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/spawn_primitives.html)
    *   [Create a CSV Reader](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/csv_reader.html)
    *   [Display Object Info](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/object_info.html)
    *   [How to make an Object Info Widget Extension](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/widget_info.html)
    *   [Reusable Light Panel](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/light_manipulator.html)
    *   [Slider Manipulator](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/slider_manipulator.html)
    *   [Viewport Reticle](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/viewport_reticle.html)
    *   [UI Window](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/ui_window_tutorial.html)
    *   [Navigating Extensions from Other Developers](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/julia_modeler.html)
    *   [Gradient Style Window](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions/ui_gradient_tutorial.html)

*   [Simulation](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/simulation.html)

    *   [Fluid Dynamics](https://docs.omniverse.nvidia.com/workflows/extensions/latest/ext_fluid-dynamics.html "(in Omniverse Extensions)")

*   [Variant Workflows](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/variant-workflows.html)
*   [Digital Human Real-Time Rendering Setup](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/rtx_rt-dh-setup.html)
*   [Data Driven Product Configurators](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/product-configurator.html)

    *   [Data Structure Tutorials](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/product-configurator/tutorials/data-structure-tutorials.html)

Omniverse Common

*   [Formats](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/formats.html)
*   [Technical Requirements](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/technical-requirements.html)
*   [Omniverse Glossary of Terms](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/glossary-of-terms.html)
*   [Feedback and Forums](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/feedback.html)
*   [Omniverse Licenses](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/legal.html)

    *   [Omniverse License](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/NVIDIA_Omniverse_License_Agreement.html)
    *   [Licensing Disclaimer](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/licensing-notices-disclaimers.html)
    *   [Other Licenses](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/licenses.html)
    *   [Redistributable Omniverse Software](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/redistributable-ov-software.html)

*   [Data Collection & Usage](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/common/data-collection.html)

[Is this page helpful?](https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5)

# Workflows Overview[#](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/generate_data.html#workflows-overview "Link to this heading")

Workflows are step-by-step instructions which allow users to utilize the NVIDIA Omniverse™ platform in the context of broader and more robust projects. They may weave in and out of a variety of applications and even utilize tools outside the Omniverse Platform. The number of possible workflows is virtually unlimited, and this section will explain some of the more common and useful pipelines identified by our engineering team. From planning, design, and development, Omniverse Workflows will get you from point A to point B.

* * *

[next Extension Workflows](https://docs.omniverse.nvidia.com/workflows/latest/defect-detection/extensions.html "next page")


[Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) | [Your Privacy Choices](https://www.nvidia.com/en-us/about-nvidia/privacy-center/) | [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) | [Accessibility](https://www.nvidia.com/en-us/about-nvidia/accessibility/) | [Corporate Policies](https://www.nvidia.com/en-us/about-nvidia/company-policies/) | [Product Security](https://www.nvidia.com/en-us/product-security/) | [Contact](https://www.nvidia.com/en-us/contact/)

Copyright © 2023-2026, NVIDIA Corporation.

Last updated on Apr 09, 2026.

NVIDIA uses cookies to improve your experience on our web site. We and our third-party partners also use cookies and other tools to collect and record information you provide as well as information about your interactions with our websites for performance improvement, analytics, and to assist in marketing efforts. By continuing to use this site or by clicking one of the buttons below, you agree to the use of cookies and other tools as described in our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) and [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) (subject to your settings) and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information on our privacy practices.

We have detected the Global Privacy Control (GPC) signal and have opted you out of all optional cookies on this site for this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. To opt out of non-cookie personal information "sales" / "sharing" for targeted advertising purposes, please visit the [NVIDIA Preference Center](https://www.nvidia.com/en-us/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information on our privacy practices.

We have detected the Global Privacy Control Signal (GPC) and have opted you out of all optional cookies on this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. We have also opted you out of "sharing"/"sales" of personal information outside of cookies. You can manage these settings in the NVIDIA [NVIDIA Preference Center](https://www.nvidia.com/en-us/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

We have detected the Global Privacy Control Signal (GPC) and have opted you out of all optional cookies on this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. We have also opted you out of "sharing"/"sales" of personal information outside of cookies which overrides at least one of your previous settings. You can manage them in the [NVIDIA Preference Center](https://www.nvidia.com/en-us/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

Manage Settings

Turn Off Optional Cookies Agree


Cookie Settings

We and our third-party partners (including social media, advertising, and analytics partners) use cookies and other tracking technologies to collect, store, monitor, and process certain information about you when you visit our website. The information collected might relate to you, your preferences, or your device. We use that information to make the site work, analyze performance and traffic on our website, provide a more personalized web experience, and assist in our marketing efforts.

Under certain privacy laws, you have the right to direct us not to "sell" or "share" your personal information for targeted advertising. To opt-out of the "sale" and "sharing" of personal information through cookies, you must opt-out of optional cookies using the toggles below. To opt out of the "sale" and "sharing" of data collected by other means (e.g., online forms) you must also update your data sharing preferences through the [NVIDIA Preference Center](https://www.nvidia.com/en-us/about-nvidia/privacy-center/).

Click on the different category headings below to find out more and change the settings according to your preference. You cannot opt out of Required Cookies as they are deployed to ensure the proper functioning of our website (such as prompting the cookie banner and remembering your settings, etc.). By clicking "Save and Accept" or "Decline All" at the bottom, you consent to the use of cookies and other tools as described in our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) in accordance with your settings and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). For more information about our privacy practices, please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/).

Required Cookies

Always Active

These cookies enable core functionality such as security, network management, and accessibility. These cookies are required for the site to function and cannot be turned off.

Cookies Details

Performance Cookies


These cookies are used to provide quantitative measures of our website visitors, such as the number of times you visit, time on page, your mouse movements, scrolling, clicks and keystroke activity on the websites; other browsing, search, or product research behavior; and what brought you to our site. These cookies may store a unique ID so that our system will remember you when you return. Information collected with these cookies is used to measure and find ways to improve website performance.

Cookies Details

Personalization Cookies


These cookies collect data about how you have interacted with our website to help us improve your web experience, such as which pages you have visited. These cookies may store a unique ID so that our system will remember you when you return. They may be set by us or by third party providers whose services we have added to our pages. These cookies enable us to provide enhanced website functionality and personalization as well as make the marketing messages we send to you more relevant to your interests. If you do not allow these cookies, then some or all of these services may not function properly.

Cookies Details

Advertising Cookies


These cookies record your visit to our websites, the pages you have visited and the links you have followed to influence the advertisements that you see on other websites. These cookies and the information they collect may be managed by other companies, including our advertising partners, and may be used to build a profile of your interests and show you relevant advertising on other sites. We and our advertising partners will use this information to make our websites and the advertising displayed on it, more relevant to your interests.

Cookies Details

Cookie List

Clear

*   - [x] checkbox label label 

Apply Cancel

Consent Leg.Interest




Decline All Save and Accept