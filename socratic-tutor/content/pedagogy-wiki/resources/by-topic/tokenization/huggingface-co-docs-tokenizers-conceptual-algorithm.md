# Source: https://huggingface.co/docs/tokenizers/conceptual/algorithm
# Author: Hugging Face
# Author Slug: hugging-face
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 2092
Tokenization is a fundamental concept in natural language processing (NLP), especially when dealing with language models.
In this article, we'll explore what a tokenizer does, how it works, and how we can leverage it using Hugging Face's `transformers` library [https://huggingface.co/docs/transformers/index] for a variety of applications.
### What is a Tokenizer?
At its core, a tokenizer breaks down raw text into smaller units called tokens.
These tokens can represent words, subwords, or characters, depending on the type of tokenizer being used.
The goal of tokenization is to convert human-readable text into a form that is more interpretable by machine learning models.
Tokenization is critical because most models don’t understand text directly.
Instead, they need numbers to make predictions, which is where the tokenizer comes in.
It takes in text, processes it, and outputs a mathematical representation that the model can work with.
In this post, we'll walk through how tokenization works using a pre-trained model from Hugging Face, explore the different methods available in the `transformers` library, and look at how tokenization influences downstream tasks such as sentiment analysis.
...
First, let's import the necessary libraries from the `transformers` package and load a pre-trained model.
We'll use the "DistilBERT" model fine-tuned for sentiment analysis.
```
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
# Load the pre-trained model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
# Create the classifier pipeline
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
```
### Tokenizing Text
With the model and tokenizer set up, we can start tokenizing a simple sentence.
Here's an example sentence:
```
sentence = "I love you!
I love you!
I love you!"
```
…
#### 1.
Tokenizer Output: Input IDs and Attention Mask
When you call the tokenizer directly, it processes the text and outputs several key components:
- **`input_ids`**: A list of integer IDs representing the tokens.
Each token corresponds to an entry in the model's vocabulary.
- **`attention_mask`**: A list of ones and zeros indicating which tokens should be attended to by the model.
This is especially useful when dealing with padding.
```
res = tokenizer(sentence)
print(res)
```
…
```
{
'input_ids': [101, 1045, 2293, 2017, 999, 1045, 2293, 2017, 999, 1045, 2293, 2017, 999, 102],
'attention_mask': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}
```
- **`input_ids`**: The integers represent the tokens.
For example, `1045` corresponds to "I", `2293` to "love", and `999` to "!".
- **`attention_mask`**: The ones indicate that all tokens should be attended to.
If there were padding tokens, you would see zeros in this list, indicating they should be ignored.
#### 2.
Tokenization
If you're curious about how the tokenizer splits the sentence into individual tokens, you can use the `tokenize()` method.
This will give you a list of tokens without the underlying IDs:
```
tokens = tokenizer.tokenize(sentence)
print(tokens)
```
…
```
['i', 'love', 'you', '!', 'i', 'love', 'you', '!', 'i', 'love', 'you', '!']
```
Notice that tokenization involves breaking down the sentence into smaller meaningful units.
The tokenizer also converts all characters to lowercase, as we are using the `distilbert-base-uncased` model, which is case-insensitive.
#### 3.
Converting Tokens to IDs
Once we have the tokens, the next step is to convert them into their corresponding integer IDs using the `convert_tokens_to_ids()` method:
```
ids = tokenizer.convert_tokens_to_ids(tokens)
print(ids)
```
…
Each token has a unique integer ID that represents it in the model's vocabulary.
These IDs are the actual input that the model uses for processing.
#### 4. Decoding the IDs Back to Text
Finally, you can decode the token IDs back into a human-readable string using the `decode()` method:
…
Notice that the decoded string is very close to the original input, except for the removal of capitalization, which was standard behavior for the "uncased" model.
...
- **101**: Marks the beginning of the sentence.
- **102**: Marks the end of the sentence.
...
As mentioned earlier, the `attention_mask` helps the model distinguish between real tokens and padding tokens.
In this case, the `attention_mask` is a list of ones, indicating that all tokens should be attended to.
If there were padding tokens, you would see zeros in the mask to instruct the model to ignore them.
### Tokenizer Summary
To summarize, tokenization is a crucial step in converting text into a form that machine learning models can process.
Hugging Face’s tokenizer handles various tasks such as:
- Converting text into tokens.
- Mapping tokens to unique integer IDs.
- Generating attention masks for models to know which tokens are important.
### Conclusion
Understanding how a tokenizer works is key to leveraging pre-trained models effectively.
By breaking down text into smaller tokens, we enable the model to process the input in a structured, efficient manner.
Whether you're using a model for sentiment analysis, text generation, or any other NLP task, the tokenizer is an essential tool in the pipeline.

Hugging Face Comprehensive Guide
...
At its core, Hugging Face serves as an open-source platform for Natural LanguageProcessing (NLP) and machine learning research, providing developers, researchers, anddata scientists with accessible tools to build, share, and deploy AI models[2].
The platformhas become instrumental in democratizing AI technology, making cutting-edge machinelearning capabilities available to everyone from students to enterprises.
...
4. Tokenizers LibraryThe Tokenizers library provides high-speed tokenization supporting multiple algorithmsfor converting raw text into tokens suitable for model input.
Tokenization Algorithms:Byte-Pair Encoding (BPE) – Used by GPT models: Iteratively merges most frequent character pairs Reduces vocabulary size while maintaining information Example: "natural language" → ["natural", "_language"]WordPiece – Used by BERT:
Performance Characteristics:The Tokenizers library achieves exceptional speed through Rust implementation: Tokenizes ~1 million tokens per second Provides 100x speedup compared to pure Python implementations Critical for production deployment of high-throughput NLP systems
Use Cases: • Creative writing assistance and content generation • Chatbot response generation • Code completion tools • Data augmentation for training datasetsSummarization condenses lengthy documents into concise summaries while preservingkey information.
Key Capabilities: • Support for 100+ language combinations • Handles idioms and cultural expressions better than rule-based systems • Continuous improvement through community contributions • Custom domain adaptation through fine-tuningCode Example:from transformers import MarianMTModel, MarianTokenizer
Translate textsrc_text = "Hello, how are you today?"translated = [Link](**tokenizer(src_text, return_tensors="pt"))print(tokenizer.batch_decode(translated))Business Applications: Global content localization Real-time conversation translation Document translation at scale Multilingual customer support automation
...
Prepare inputinputs = tokenizer("Hello world!", return_tensors="pt")
Get predictionsoutputs = model(**inputs)logits = [Link]Low-Level Configuration (For Advanced Users):from transformers import BertConfig, BertModelCustom configurationconfig = BertConfig(vocab_size=30522,hidden_size=768,num_hidden_layers=12,num_attention_heads=12,intermediate_size=3072)
Load datasetdataset = load_dataset("ag_news")
Tokenizetokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")def tokenize_function(examples):return tokenizer(examples["text"], padding="max_length", truncation=True)tokenized_datasets = [Link](tokenize_function, batched=True)
trainer = Trainer(model=model,args=training_args,train_dataset=tokenized_datasets["train"],eval_dataset=tokenized_datasets["test"],)[Link]()
Real-World Example:A company with 5,000 customer support tickets (classified by issue type) can: 1.

## Huggingface tutorial Series : tokenizer
This article was compiled after listening to the tokenizer part of the Huggingface tutorial series..
Summary of the tokenizers
## What is tokenizer
A tokenizer is a program that splits a sentence into sub-words or word units and converts them into input ids through a look-up table.
In the Huggingface tutorial, we learn tokenizers used specifically for transformers-based models.
## word-based tokenizer
Several tokenizers tokenize word-level units.
It is a tokenizer that tokenizes based on space.
When splitting based on space, it becomes as follows.
You can also create rules that tokenize based on punctuation.
We will convert this to input_ids in the look-up-tabl
Let’s look at the problems of word-based.
...
Popular libraries of these rule-based tokenizers are spaCy and Moses.
A popular model is Transformer XL.The vocabulary size for this model is a whopping 267,735.
Usually, big-size vocabulary increases time complexity and memory usage because it causes the size of the embedding layer to grow.
Usually, monolingual models have a vocabulary size of less than 50000.
## Character-level
It is a tokenizer that tokenizes character by character.
The advantage is that the vocabulary size is small.
### small size vocabulary
Out-of-vocabulary issues are relatively rare.
...
Subword is a tokenizing method that considers both advantages and disadvantages.
Meaningful words should not be split, and rare words should be split into semantic units.
For example, the word dog is a frequently used word, so it should not be split, and dogs would have to be split into dog and s.
In the subword method, when tokenizing the word tokenization, it will be tokenized with token and ization.
In other words, ***the subword method helps to separate tokens related to syntactic (grammar) and tokens related to semantic (semantic).* **
***The Subword tokenizer identifies whether a word is a start token or an end token.* ** For example, Bert uses ## to distinguish between start and end tokens in words.
Different tokenizers use different prefixes.
Besides Bert, some PLMs use various subword tokenizers.
Subword tokenizer reduces the size of vocab and specifies which word token it is by using prefix and suffix.
…
1. I am using dictionary tokenization as a rule-based tokenizer such as word-based, sentence-based.
Then, count the number (frequency) of each word.
2. A basic vocabulary with a sign (letter?) from these words.
3. Two symbols (2-gram) were selected and selected the most.
(This is called a merge rule)
4. The desired number of horses (normal size) can be combined.
That is, the desired vocabulary size(number of merges) and base-vocab size become hyperparameters.
Let’s take an example.
```
("hug", 10), ("pug", 5), ("pun", 12), ("bun", 4), ("hugs", 5)
...
After pre-tokenization, the words are separated like this.
...
The next two symbols with the highest frequency becomes “u” + “n” (16 times).
Therefore, “un” is added to the vocabulary.Finally , the vocabs become `["b", "g", "h", "n", "p", "s", "u", "ug", "un", "hug"]` .
So, for example, “bug” can be tokenized as “b” and “ug”, but in the case of “mug”, it will be tokenized as “UNK” and “ug”.
GPT uses the 478 base vocab size and 40,000 merge rules .
These values are set as hyperparameters to have a total of 40478 vocabs.
...
However, in GPT2, to have a better base vocab, bytes are used as the base vocab, and the size of the base vocab is 256.
However, the base characters are included in the base vocab.
According to the literature description, GPT2 can tokenize all text without symbols by applying a special rule to punctuation marks.
GPT2 has a vocab size of 50257, which consists of 256 as the base vocab size, 1 as a special end token, and 50000 learned merge rules.

`//! Represents a tokenization pipeline.
//!
//! A [`Tokenizer`](struct.Tokenizer.html) is composed of some of the following parts.
//! - [`Normalizer`](trait.Normalizer.html): Takes care of the text normalization (like unicode normalization).
//! - [`PreTokenizer`](trait.PreTokenizer.html): Takes care of the pre tokenization (ie.
How to split tokens and pre-process
//! them.
//! - [`Model`](trait.Model.html): A model encapsulates the tokenization algorithm (like BPE, Word base, character
//! based, ...).
//! - [`PostProcessor`](trait.PostProcessor.html): Takes care of the processing after tokenization (like truncating, padding,
//! ...).
use ahash::AHashMap;
use std::{
fs::{read_to_string, File},
io::{prelude::*, BufReader},
ops::{Deref, DerefMut},
path::{Path, PathBuf},
};

use serde::de::DeserializeOwned;
use serde::{Deserialize, Serialize};

use crate::utils::iter::ResultShunt;
use crate::utils::parallelism::*;
use crate::utils::progress::{ProgressBar, ProgressStyle};

…

pub use crate::utils::padding::{pad_encodings, PaddingDirection, PaddingParams, PaddingStrategy};
pub use crate::utils::truncation::{
truncate_encodings, TruncationDirection, TruncationParams, TruncationStrategy,
};
pub use added_vocabulary::*;
pub use encoding::*;
pub use normalizer::{NormalizedString, OffsetReferential, SplitDelimiterBehavior};
pub use pre_tokenizer::*;
pub type Error = Box<dyn std::error::Error + Send + Sync>;
pub type Result<T> = std::result::Result<T, Error>;
pub type Offsets = (usize, usize);

/// Takes care of pre-processing strings.
pub trait Normalizer {
fn normalize(&self, normalized: &mut NormalizedString) -> Result<()>;
}
/// The `PreTokenizer` is in charge of doing the pre-segmentation step. It splits the given string
/// in multiple substrings, keeping track of the offsets of said substrings from the
/// `NormalizedString`. In some occasions, the `PreTokenizer` might need to modify the given
/// `NormalizedString` to ensure we can entirely keep track of the offsets and the mapping with
/// the original string.
pub trait PreTokenizer {
fn pre_tokenize(&self, pretokenized: &mut PreTokenizedString) -> Result<()>;
}
/// Represents a model used during Tokenization (like BPE or Word or Unigram).
pub trait Model {
type Trainer: Trainer + Sync;
/// Tokenize the given sequence into multiple underlying `Token`. The `offsets` on the `Token`
/// are expected to be relative to the given sequence.
fn tokenize(&self, sequence: &str) -> Result<Vec<Token>>;
/// Find the ID associated to a string token
fn token_to_id(&self, token: &str) -> Option<u32>;
/// Find the string token associated to an ID
fn id_to_token(&self, id: u32) -> Option<String>;
/// Retrieve the entire vocabulary mapping (token -> ID)
fn get_vocab(&self) -> HashMap<String, u32>;
/// Retrieve the size of the vocabulary
fn get_vocab_size(&self) -> usize;
/// Save the current `Model` in the given folder, u