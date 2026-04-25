# Source: https://discuss.huggingface.co/t/orpo-dpo-dataset-clarification/103637/2
# Title: ORPO/DPO dataset clarification - Hugging Face Forums (lewtun reply)
# Fetched via: jina
# Date: 2026-04-09

Title: ORPO/DPO dataset clarification - 🤗Datasets - Hugging Face Forums



## post by qxakshat on Aug 23, 2024

[![Image 1](https://avatars.discourse-cdn.com/v4/letter/q/e274bd/48.png)](https://discuss.huggingface.co/u/qxakshat)

I am trying to make a new dataset for preference training but finding correct way to implement it. As described here [ORPO Trainer](https://huggingface.co/docs/trl/main/en/orpo_trainer)

 or [DPO Trainer](https://huggingface.co/docs/trl/main/en/dpo_trainer)

 the trainer requires 3 columns “prompt”, “chosen” and “rejected”

 like this

```
orpo_dataset_dict = {
    "prompt": [
        "hello",
        "how are you",...
    ],
    "chosen": [
        "hi nice to meet you",
        "I am fine",...
    ],
    "rejected": [
        "leave me alone",
        "I am not fine",...
    ],
}
```

But while seeing some of the dpo/orpo datasets (ex. mlabonne/orpo-dpo-mix-40k) its formatted in a different way with roles (user, assistant, etc.) like below, see the prompt itself gets **repeated here in chosen and rejected**, where as the official doc doesn’t suggest so.

```
{'source': 'ultrachat',
 'chosen': '<|im_start|>user\nCan you provide examples of how different cultures approach grief and mourning, and how this has evolved over time?<|im_end|>\n<|im_start|>assistant\nOf course, I\'ll do my best to provide you with accurate and helpful information.\n\nGrief and mourning are universal human experiences, and different cultures have developed unique ways of coping with loss and honoring the deceased. These practices have evolved over time, reflecting changes in societal values, beliefs, and traditions. Here are some examples:\n\n1. Ancient Egypt: In ancient Egyptian culture, mourning was a complex and elaborate process that lasted for 70 days. During this time, the family of the deceased would observe a period of mourning, known as "the sorrows of the heart," which involved abstaining from certain foods, wearing plain clothes, and covering their faces with dust and ashes. After 70 days, the family would hold a feast to celebrate the deceased\'s transition to the afterlife.\n2. Hinduism: In Hindu culture, the mourning period typically lasts for 13 days, during which time the family observes rituals and ceremonies to help the deceased\'s soul transition to the afterlife. The family members are expected to follow certain customs, such as wearing simple clothes, avoiding certain foods, and not participating in social events. On the 13th day, a ritual called "Shraddha" is performed, which involves offering food and water to the deceased\'s soul.\n3. Buddhism: In Buddhist culture, mourning is seen as an opportunity for spiritual growth and reflection. The family of the deceased typically observes a period of mourning that lasts for 49 days, during which time they are encouraged to focus on spiritual practices such as meditation, chanting, and offering food and incense to the monks. On the 49th day, a ceremony called "Bardo" is held to help the deceased\'s soul transition to the next life.\n4. Victorian England: During the Victorian era, mourning was a highly ritualized and codified practice that lasted for several years. The family of the deceased would wear black clothing and jewelry, and observe strict social norms, such as avoiding social events and not participating in certain activities. The length and intensity of the mourning period varied depending on the social status of the deceased and the relationship of the mourner to the deceased.\n5. Modern-day Japan: In contemporary Japanese culture, mourning is typically a private and individualized experience. The family of the deceased may observe a period of mourning that lasts for several days or weeks, during which time they may visit the gravesite, offer food and incense, and engage in spiritual practices such as Zen Buddhism. The Japanese also have a tradition of "condolence money," where friends and family members give money to the bereaved family to help offset the costs of the funeral and to show their respects.\n\nThese examples illustrate how different cultures have developed unique ways of coping with loss and honoring the deceased, and how these practices have evolved over time to reflect changes in societal values and beliefs. It\'s important to note that each culture has its own unique traditions and customs surrounding grief and mourning, and it\'s essential to respect and appreciate these differences.<|im_end|>\n',
'rejected': '<|im_start|>user\nCan you provide examples of how different cultures approach grief and mourning, and how this has evolved over time?<|im_end|>\n<|im_start|>assistant\nGrief and mourning practices have varied greatly across cultures and through time. For example, in some cultures mourners will shave their head to signify their grief, while in other cultures people may cut their finger nails as a sign of mourning. In some cultures, the period of mourning is strictly regulated and controlled, while in other cultures, individuals has the freedom to express their grief in whatever way they choose. Over time, some cultural practices have developed to help support the grieving process, such as sending food and other gifts to the mourning person.<|im_end|>\n',
 'prompt': 'Can you provide examples of how different cultures approach grief and mourning, and how this has evolved over time?',
 'question': 'Can you provide examples of how different cultures approach grief and mourning, and how this has evolved over time?'}
```

What is the correct way to create the dataset for orpo or dpo?

[![Image 2](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/lewtun/48/30995_2.png)](https://discuss.huggingface.co/u/lewtun "lewtun")

## post by lewtun on Aug 28, 2024

[![Image 3](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/lewtun/48/30995_2.png)](https://discuss.huggingface.co/u/lewtun)

Hello [@qxakshat](https://discuss.huggingface.co/u/qxakshat), the expected dataset format for the `DPOTrainer` in TRL is indeed as shown in the doc, i.e. a triple of `(prompt, chosen, rejected)`.

However, as you point out, most preference datasets just have a chosen/rejected column. What is done for these cases is to select the first message as the prompt, and the N-1 messages as the chosen/rejected columns. You can see an example in the alignment handbook here: [alignment-handbook/src/alignment/data.py at 27f7dbf00663dab66ad7334afb7a1311fa251f41 · huggingface/alignment-handbook · GitHub](https://github.com/huggingface/alignment-handbook/blob/27f7dbf00663dab66ad7334afb7a1311fa251f41/src/alignment/data.py#L73-L90)

Overall I think we can simplify this further in TRL directly to just pass chosen/rejected columns, but that will require a bit of refactoring.

## post by qxakshat on Aug 29, 2024

[![Image 4](https://avatars.discourse-cdn.com/v4/letter/q/e274bd/48.png)](https://discuss.huggingface.co/u/qxakshat)

Hi [@lewtun](https://discuss.huggingface.co/u/lewtun) thanks for the response, also wanted to ask weather the function you shared is being used in ORPOTrainer as well?

## Closed on Aug 29, 2024


This topic was automatically closed 12 hours after the last reply. New replies are no longer allowed.