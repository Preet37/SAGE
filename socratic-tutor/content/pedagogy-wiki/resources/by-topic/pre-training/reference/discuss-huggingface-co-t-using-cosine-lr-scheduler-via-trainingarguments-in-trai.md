# Source: https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783/8
# Title: Using Cosine LR scheduler via TrainingArguments in Trainer
# Fetched via: jina
# Date: 2026-04-09

Title: Using Cosine LR scheduler via TrainingArguments in Trainer - Beginners - Hugging Face Forums



## post by spranjal25 on Feb 16, 2022

## post by sgugger on Feb 16, 2022

2 months later

## post by ollibolli on Apr 4, 2022

5 months later

## post by Gozdi on Sep 13, 2022

[![Image 1](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/gozdi/48/4221_2.png)](https://discuss.huggingface.co/u/gozdi)

[@sgugger](https://discuss.huggingface.co/u/sgugger) What if I dont want learning rate decaying to 0 but let’s say to 50% of peak lr? Is there any way to do this?

## post by sgugger on Sep 14, 2022

[![Image 2](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/sgugger/48/2291_2.png)](https://discuss.huggingface.co/u/sgugger)

You can pass your own learning rate scheduler to the `Trainer`.

1 year later

## post by berkecr on Sep 29, 2023

[![Image 3](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/berkecr/48/32071_2.png)](https://discuss.huggingface.co/u/berkecr)

4 months later

## post by brando on Jan 23, 2024

[![Image 4](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/brando/48/30114_2.png)](https://discuss.huggingface.co/u/brando)

[@sgugger](https://discuss.huggingface.co/u/sgugger) is this the right way to do it?

```
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments
from transformers.optimization import get_cosine_schedule_with_warmup
from transformers import PagedAdamW_32bit
from datasets import load_dataset

def train_gpt2_model(dataset_path: str, model_name: str = "gpt2", num_train_epochs: int = 3):
    # Load the tokenizer and model
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Load and preprocess the dataset
    dataset = load_dataset("text", data_files=dataset_path)
    tokenized_dataset = dataset.map(lambda e: tokenizer(e['text'], truncation=True, padding='max_length', max_length=512), batched=True)

    # Initialize the optimizer
    optimizer = PagedAdamW_32bit(model.parameters())

    # Training arguments including the learning rate scheduler
    training_args = TrainingArguments(
        output_dir="./gpt2_trained",
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=2,  # Adjust based on your GPU memory
        warmup_steps=500,  # Number of warmup steps
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
    )

    # Create the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        optimizers=(optimizer, None)  # Scheduler is None, will be set later
    )

    # Set the scheduler
    scheduler = get_cosine_schedule_with_warmup(
        optimizer,
        num_warmup_steps=training_args.warmup_steps,
        num_training_steps=trainer.get_train_dataloader().__len__()
    )
    trainer.lr_scheduler = scheduler

    # Train the model
    trainer.train()

    # Save the model
    model.save_pretrained("./gpt2_trained")

if __name__ == "__main__":
    dataset_path = "path/to/your/dataset.json"
    train_gpt2_model(dataset_path)
```

## post by brando on Jan 23, 2024

[![Image 5](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/brando/48/30114_2.png)](https://discuss.huggingface.co/u/brando)

you can set it in the trainer

```
# -- max steps manually decided depending on how many tokens we want to train on
    per_device_train_batch_size = batch_size
    print(f'{per_device_train_batch_size=}')
    print(f'{num_epochs=} {max_steps=}')

    # -- Get Optimizer & Scheduler
    # - Get Optimizer
    if optim == 'paged_adamw_32bit':
        from transformers import PagedAdamW_32bit
        optimizer = PagedAdamW_32bit(model.parameters())
    elif optim == 'adamw_manual':
        optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    else:
        optimizer = AdamW(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    print(f'{optimizer=}')
    # - Get Scheduler
    if lr_scheduler_type == 'cosine_with_warmup_manual':
        lr_scheduler = get_cosine_schedule_with_warmup(
            optimizer,
            num_warmup_steps=int(max_steps*warmup_ratio),
            num_training_steps=max_steps,
        )
    else:
        lr_scheduler = None
    print(f'{lr_scheduler=}')

    # -- Training arguments and trainer instantiation ref: https://huggingface.co/docs/transformers/v4.31.0/en/main_classes/trainer#transformers.TrainingArguments
    output_dir = Path(f'~/data/results_{today}/').expanduser() if not debug else Path(f'~/data/results/').expanduser()
    # output_dir = '.'
    # print(f'{debug=} {output_dir=} \n {report_to=}')
    training_args = TrainingArguments(
        output_dir=output_dir,  # The output directory where the model predictions and checkpoints will be written.
        # output_dir='.',  # The output directory where the model predictions and checkpoints will be written.
        # num_train_epochs = num_train_epochs, 
        max_steps=max_steps,  # TODO: hard to fix, see above
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,  # based on alpaca https://github.com/tatsu-lab/stanford_alpaca, allows to process effective_batch_size = gradient_accumulation_steps * batch_size, num its to accumulate before opt update step
        gradient_checkpointing = gradient_checkpointing,  # TODO depending on hardware set to true?
        # optim=optim,
        # warmup_steps=int(max_steps*warmup_ratio),  # TODO: once real training starts we can select this number for llama v2, what does llama v2 do to make it stable while v1 didn't?
        # warmup_ratio=warmup_ratio,  # copying alpaca for now, number of steps for a linear warmup, TODO once real training starts change? 
        # weight_decay=0.01,  # TODO once real training change?
        weight_decay=weight_decay,  # TODO once real training change?
        learning_rate = learning_rate,  # TODO once real training change? anything larger than -3 I've had terrible experiences with
        max_grad_norm=1.0, # TODO once real training change?
        # lr_scheduler_type=lr_scheduler_type,  # TODO once real training change? using what I've seen most in vision 
        # lr_scheduler_kwargs=lr_scheduler_kwargs,  # ref: https://huggingface.co/docs/transformers/v4.37.0/en/main_classes/optimizer_schedules#transformers.SchedulerType 
        logging_dir=Path('~/data/maf/logs').expanduser(),
        # save_steps=4000,  # alpaca does 2000, other defaults were 500
        save_steps=max_steps//3,  # alpaca does 2000, other defaults were 500
        # save_steps=1,  # alpaca does 2000, other defaults were 500
        # logging_steps=250,
        # logging_steps=50,  
        logging_first_step=True,
        # logging_steps=3,
        logging_steps=1,
        remove_unused_columns=False,  # TODO don't get why https://stackoverflow.com/questions/76879872/how-to-use-huggingface-hf-trainer-train-with-custom-collate-function/76929999#76929999 , https://claude.ai/chat/475a4638-cee3-4ce0-af64-c8b8d1dc0d90
        report_to=report_to,  # change to wandb!
        fp16=False,  # never ever set to True
        bf16=torch.cuda.get_device_capability(torch.cuda.current_device())[0] >= 8,  # if >= 8 ==> brain float 16 available or set to True if you always want fp32
    )
    print(f'{pretrained_model_name_or_path=}\n{optim=}\n{learning_rate=}')

    # TODO: might be nice to figure our how llamav2 counts the number of token's they've trained on
    print(f'{train_dataset=}')
    # print(f'{eval_dataset=}')
    trainer = Trainer(
        model=model,
        args=training_args,  
        train_dataset=train_dataset,
        optimizers=(optimizer, lr_scheduler),
    )

    # - Train
    cuda_visible_devices = os.environ.get('CUDA_VISIBLE_DEVICES')
    if cuda_visible_devices is not None:
        print(f"CUDA_VISIBLE_DEVICES = {cuda_visible_devices}")
    trainer.train()
    trainer.save_model(output_dir=output_dir)  # TODO is this really needed? https://discuss.huggingface.co/t/do-we-need-to-explicity-save-the-model-if-the-save-steps-is-not-a-multiple-of-the-num-steps-with-hf/56745
```

related [How do use lr_scheduler - #12 by brando](https://discuss.huggingface.co/t/how-do-use-lr-scheduler/4046/12)

4 months later

## post by edwarddgao on May 16, 2024

[![Image 6](https://avatars.discourse-cdn.com/v4/letter/e/b782af/48.png)](https://discuss.huggingface.co/u/edwarddgao)

Much easier way:

```
lr_scheduler_type = "cosine_with_restarts",
lr_scheduler_kwargs = { "num_cycles": 5 },
```

## post by ChayanM on May 21, 2024

[![Image 7](https://avatars.discourse-cdn.com/v4/letter/c/e8c25b/48.png)](https://discuss.huggingface.co/u/chayanm)

13 days later

## post by botkop on Jun 3, 2024

[![Image 8](https://sea2.discourse-cdn.com/hellohellohello/user_avatar/discuss.huggingface.co/botkop/48/3143_2.png)](https://discuss.huggingface.co/u/botkop)

is this documented somewhere?