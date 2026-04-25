# Source: https://radimrehurek.com/gensim/models/word2vec.html
# Title: models.word2vec – Word2vec embeddings — gensim
# Fetched via: trafilatura
# Date: 2026-04-09

models.word2vec
– Word2vec embeddings[¶](#module-gensim.models.word2vec)
Introduction[¶](#introduction)
This module implements the word2vec family of algorithms, using highly optimized C routines, data streaming and Pythonic interfaces.
The word2vec algorithms include skip-gram and CBOW models, using either
hierarchical softmax or negative sampling: [Tomas Mikolov et al: Efficient Estimation of Word Representations
in Vector Space](https://arxiv.org/pdf/1301.3781.pdf), [Tomas Mikolov et al: Distributed Representations of Words
and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546).
Other embeddings[¶](#other-embeddings)
There are more ways to train word vectors in Gensim than just Word2Vec.
See also [ Doc2Vec](doc2vec.html#gensim.models.doc2vec.Doc2Vec),
[.](fasttext.html#gensim.models.fasttext.FastText)
FastText
The training algorithms were originally ported from the C package [https://code.google.com/p/word2vec/](https://code.google.com/p/word2vec/)
and extended with additional functionality and
[optimizations](https://rare-technologies.com/parallelizing-word2vec-in-python/) over the years.
For a tutorial on Gensim word2vec, with an interactive web app trained on GoogleNews,
visit [https://rare-technologies.com/word2vec-tutorial/](https://rare-technologies.com/word2vec-tutorial/).
Usage examples[¶](#usage-examples)
Initialize a model with e.g.:
>>> from gensim.test.utils import common_texts
>>> from gensim.models import Word2Vec
>>>
>>> model = Word2Vec(sentences=common_texts, vector_size=100, window=5, min_count=1, workers=4)
>>> model.save("word2vec.model")
The training is streamed, so ``sentences`` can be an iterable, reading input data from the disk or network on-the-fly, without loading your entire corpus into RAM.
Note the sentences
iterable must be restartable (not just a generator), to allow the algorithm
to stream over your dataset multiple times. For some examples of streamed iterables,
see [ BrownCorpus](#gensim.models.word2vec.BrownCorpus),
[or](#gensim.models.word2vec.Text8Corpus)
Text8Corpus
[.](#gensim.models.word2vec.LineSentence)
LineSentence
If you save the model you can continue training it later:
>>> model = Word2Vec.load("word2vec.model")
>>> model.train([["hello", "world"]], total_examples=1, epochs=1)
(0, 2)
The trained word vectors are stored in a [ KeyedVectors](keyedvectors.html#gensim.models.keyedvectors.KeyedVectors) instance, as model.wv:
>>> vector = model.wv['computer'] # get numpy vector of a word
>>> sims = model.wv.most_similar('computer', topn=10) # get other similar words
The reason for separating the trained vectors into KeyedVectors is that if you don’t need the full model state any more (don’t need to continue training), its state can be discarded, keeping just the vectors and their keys proper.
This results in a much smaller and faster object that can be mmapped for lightning fast loading and sharing the vectors in RAM between processes:
>>> from gensim.models import KeyedVectors
>>>
>>> # Store just the words + their trained embeddings.
>>> word_vectors = model.wv
>>> word_vectors.save("word2vec.wordvectors")
>>>
>>> # Load back with memory-mapping = read-only, shared across processes.
>>> wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')
>>>
>>> vector = wv['computer'] # Get numpy vector of a word
Gensim can also load word vectors in the “word2vec C format”, as a
[ KeyedVectors](keyedvectors.html#gensim.models.keyedvectors.KeyedVectors) instance:
>>> from gensim.test.utils import datapath
>>>
>>> # Load a word2vec model stored in the C *text* format.
>>> wv_from_text = KeyedVectors.load_word2vec_format(datapath('word2vec_pre_kv_c'), binary=False)
>>> # Load a word2vec model stored in the C *binary* format.
>>> wv_from_bin = KeyedVectors.load_word2vec_format(datapath("euclidean_vectors.bin"), binary=True)
It is impossible to continue training the vectors loaded from the C format because the hidden weights,
vocabulary frequencies and the binary tree are missing. To continue training, you’ll need the
full [ Word2Vec](#gensim.models.word2vec.Word2Vec) object state, as stored by
[, not just the](#gensim.models.word2vec.Word2Vec.save)
save()
[.](keyedvectors.html#gensim.models.keyedvectors.KeyedVectors)
KeyedVectors
You can perform various NLP tasks with a trained model. Some of the operations
are already built-in - see [ gensim.models.keyedvectors](keyedvectors.html#module-gensim.models.keyedvectors).
If you’re finished training a model (i.e. no more updates, only querying),
you can switch to the [ KeyedVectors](keyedvectors.html#gensim.models.keyedvectors.KeyedVectors) instance:
>>> word_vectors = model.wv
>>> del model
to trim unneeded model state = use much less RAM and allow fast loading and memory sharing (mmap).
Embeddings with multiword ngrams[¶](#embeddings-with-multiword-ngrams)
There is a [ gensim.models.phrases](phrases.html#module-gensim.models.phrases) module which lets you automatically
detect phrases longer than one word, using collocation statistics.
Using phrases, you can learn a word2vec model where “words” are actually multiword expressions,
such as new_york_times or financial_crisis:
>>> from gensim.models import Phrases
>>>
>>> # Train a bigram detector.
>>> bigram_transformer = Phrases(common_texts)
>>>
>>> # Apply the trained MWE detector to a corpus, using the result to train a Word2vec model.
>>> model = Word2Vec(bigram_transformer[common_texts], min_count=1)
Pretrained models[¶](#pretrained-models)
Gensim comes with several already pre-trained models, in the
[Gensim-data repository](https://github.com/RaRe-Technologies/gensim-data):
>>> import gensim.downloader
>>> # Show all available models in gensim-data
>>> print(list(gensim.downloader.info()['models'].keys()))
['fasttext-wiki-news-subwords-300',
'conceptnet-numberbatch-17-06-300',
'word2vec-ruscorpora-300',
'word2vec-google-news-300',
'glove-wiki-gigaword-50',
'glove-wiki-gigaword-100',
'glove-wiki-gigaword-200',
'glove-wiki-gigaword-300',
'glove-twitter-25',
'glove-twitter-50',
'glove-twitter-100',
'glove-twitter-200',
'__testing_word2vec-matrix-synopsis']
>>>
>>> # Download the "glove-twitter-25" embeddings
>>> glove_vectors = gensim.downloader.load('glove-twitter-25')
>>>
>>> # Use the downloaded vectors as usual:
>>> glove_vectors.most_similar('twitter')
[('facebook', 0.948005199432373),
('tweet', 0.9403423070907593),
('fb', 0.9342358708381653),
('instagram', 0.9104824066162109),
('chat', 0.8964964747428894),
('hashtag', 0.8885937333106995),
('tweets', 0.8878158330917358),
('tl', 0.8778461217880249),
('link', 0.8778210878372192),
('internet', 0.8753897547721863)]
-
class gensim.models.word2vec.BrownCorpus(dirname)
[¶](#gensim.models.word2vec.BrownCorpus) Bases:
object
Iterate over sentences from the
[Brown corpus](https://en.wikipedia.org/wiki/Brown_Corpus)(part of[NLTK data](https://www.nltk.org/data.html)).
-
class gensim.models.word2vec.Heapitem(count, index, left, right)
[¶](#gensim.models.word2vec.Heapitem) Bases:
Heapitem
Create new instance of Heapitem(count, index, left, right)
-
count
[¶](#gensim.models.word2vec.Heapitem.count) Alias for field number 0
-
index
[¶](#gensim.models.word2vec.Heapitem.index) Alias for field number 1
-
left
[¶](#gensim.models.word2vec.Heapitem.left) Alias for field number 2
-
right
[¶](#gensim.models.word2vec.Heapitem.right) Alias for field number 3
-
count
-
class gensim.models.word2vec.LineSentence(source, max_sentence_length=10000, limit=None)
[¶](#gensim.models.word2vec.LineSentence) Bases:
object
Iterate over a file that contains sentences: one line = one sentence. Words must be already preprocessed and separated by whitespace.
- Parameters
source (string or a file-like object) – Path to the file on disk, or an already-open file object (must support seek(0)).
limit (int or None) – Clip the file to the first limit lines. Do no clipping if limit is None (the default).
Examples
>>> from gensim.test.utils import datapath >>> sentences = LineSentence(datapath('lee_background.cor')) >>> for sentence in sentences: ... pass
-
class gensim.models.word2vec.PathLineSentences(source, max_sentence_length=10000, limit=None)
[¶](#gensim.models.word2vec.PathLineSentences) Bases:
object
Like
, but process all files in a directory in alphabetical order by filename.LineSentence
The directory must only contain files that can be read by
: .bz2, .gz, and text files. Any file not ending with .bz2 or .gz is assumed to be a text file.gensim.models.word2vec.LineSentence
The format of files (either text, or compressed text files) in the path is one sentence = one line, with words already preprocessed and separated by whitespace.
Warning
Does not recurse into subdirectories.
- Parameters
source (str) – Path to the directory.
limit (int or None) – Read only the first limit lines from each file. Read all if limit is None (the default).
-
class gensim.models.word2vec.Text8Corpus(fname, max_sentence_length=10000)
[¶](#gensim.models.word2vec.Text8Corpus) Bases:
object
Iterate over sentences from the “text8” corpus, unzipped from
[https://mattmahoney.net/dc/text8.zip](https://mattmahoney.net/dc/text8.zip).
-
class gensim.models.word2vec.Word2Vec(sentences=None, corpus_file=None, vector_size=100, alpha=0.025, window=5, min_count=5, max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5, ns_exponent=0.75, cbow_mean=1, hashfxn=<built-in function hash>, epochs=5, null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000, compute_loss=False, callbacks=(), comment=None, max_final_vocab=None, shrink_windows=True)
[¶](#gensim.models.word2vec.Word2Vec) Bases:
SaveLoad
Train, use and evaluate neural networks described in
[https://code.google.com/p/word2vec/](https://code.google.com/p/word2vec/).Once you’re finished training a model (=no more updates, only querying) store and use only the
instance inKeyedVectors
self.wv
to reduce memory.The full model can be stored/loaded via its
andsave()
methods.load()
The trained word vectors can also be stored/loaded from a format compatible with the original word2vec implementation via self.wv.save_word2vec_format and
.gensim.models.keyedvectors.KeyedVectors.load_word2vec_format()
- Parameters
sentences (iterable of iterables, optional) – The sentences iterable can be simply a list of lists of tokens, but for larger corpora, consider an iterable that streams the sentences directly from disk/network. See
,BrownCorpus
orText8Corpus
inLineSentence
module for such examples. See also theword2vec
[tutorial on data streaming in Python](https://rare-technologies.com/data-streaming-in-python-generators-iterators-iterables/). If you don’t supply sentences, the model is left uninitialized – use if you plan to initialize it in some other way.corpus_file (str, optional) – Path to a corpus file in
format. You may use this argument instead of sentences to get performance boost. Only one of sentences or corpus_file arguments need to be passed (or none of them, in that case, the model is left uninitialized).LineSentence
vector_size (int, optional) – Dimensionality of the word vectors.
window (int, optional) – Maximum distance between the current and predicted word within a sentence.
min_count (int, optional) – Ignores all words with total frequency lower than this.
workers (int, optional) – Use these many worker threads to train the model (=faster training with multicore machines).
sg ({0, 1}, optional) – Training algorithm: 1 for skip-gram; otherwise CBOW.
hs ({0, 1}, optional) – If 1, hierarchical softmax will be used for model training. If 0, hierarchical softmax will not be used for model training.
negative (int, optional) – If > 0, negative sampling will be used, the int for negative specifies how many “noise words” should be drawn (usually between 5-20). If 0, negative sampling will not be used.
ns_exponent (float, optional) – The exponent used to shape the negative sampling distribution. A value of 1.0 samples exactly in proportion to the frequencies, 0.0 samples all words equally, while a negative value samples low-frequency words more than high-frequency words. The popular default value of 0.75 was chosen by the original Word2Vec paper. More recently, in
[https://arxiv.org/abs/1804.04212](https://arxiv.org/abs/1804.04212), Caselles-Dupré, Lesaint, & Royo-Letelier suggest that other values may perform better for recommendation applications.cbow_mean ({0, 1}, optional) – If 0, use the sum of the context word vectors. If 1, use the mean, only applies when cbow is used.
alpha (float, optional) – The initial learning rate.
min_alpha (float, optional) – Learning rate will linearly drop to min_alpha as training progresses.
seed (int, optional) – Seed for the random number generator. Initial vectors for each word are seeded with a hash of the concatenation of word + str(seed). Note that for a fully deterministically-reproducible run, you must also limit the model to a single worker thread (workers=1), to eliminate ordering jitter from OS thread scheduling. (In Python 3, reproducibility between interpreter launches also requires use of the PYTHONHASHSEED environment variable to control hash randomization).
max_vocab_size (int, optional) – Limits the RAM during vocabulary building; if there are more unique words than this, then prune the infrequent ones. Every 10 million word types need about 1GB of RAM. Set to None for no limit.
max_final_vocab (int, optional) – Limits the vocab to a target vocab size by automatically picking a matching min_count. If the specified min_count is more than the calculated min_count, the specified min_count will be used. Set to None if not required.
sample (float, optional) – The threshold for configuring which higher-frequency words are randomly downsampled, useful range is (0, 1e-5).
hashfxn (function, optional) – Hash function to use to randomly initialize weights, for increased training reproducibility.
epochs (int, optional) – Number of iterations (epochs) over the corpus. (Formerly: iter)
trim_rule (function, optional) –
Vocabulary trimming rule, specifies whether certain words should remain in the vocabulary, be trimmed away, or handled using the default (discard if word count < min_count). Can be None (min_count will be used, look to
), or a callable that accepts parameters (word, count, min_count) and returns eitherkeep_vocab_item()
gensim.utils.RULE_DISCARD
,gensim.utils.RULE_KEEP
orgensim.utils.RULE_DEFAULT
. The rule, if given, is only used to prune vocabulary during build_vocab() and is not stored as part of the model.- The input parameters are of the following types:
word (str) - the word we are examining
count (int) - the word’s frequency count in the corpus
min_count (int) - the minimum count threshold.
sorted_vocab ({0, 1}, optional) – If 1, sort the vocabulary by descending frequency before assigning word indexes. See
.sort_by_descending_frequency()
batch_words (int, optional) – Target size (in words) for batches of examples passed to worker threads (and thus cython routines).(Larger batches will be passed if individual texts are longer than 10000 words, but the standard cython code truncates to that maximum.)
compute_loss (bool, optional) – If True, computes and stores loss value which can be retrieved using
.get_latest_training_loss()
callbacks (iterable of
, optional) – Sequence of callbacks to be executed at specific stages during training.CallbackAny2Vec
shrink_windows (bool, optional) – New in 4.1. Experimental. If True, the effective window size is uniformly sampled from [1, window] for each target word during training, to match the original word2vec algorithm’s approximate weighting of context words by distance. Otherwise, the effective window size is always fixed to window words to either side.
Examples
Initialize and train a
modelWord2Vec
>>> from gensim.models import Word2Vec >>> sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]] >>> model = Word2Vec(sentences, min_count=1)
-
wv
[¶](#gensim.models.word2vec.Word2Vec.wv) This object essentially contains the mapping between words and embeddings. After training, it can be used directly to query those embeddings in various ways. See the module level docstring for examples.
- Type
-
add_lifecycle_event(event_name, log_level=20, **event)
[¶](#gensim.models.word2vec.Word2Vec.add_lifecycle_event) Append an event into the lifecycle_events attribute of this object, and also optionally log the event at log_level.
Events are important moments during the object’s life, such as “model created”, “model saved”, “model loaded”, etc.
The lifecycle_events attribute is persisted across object’s
andsave()
operations. It has no impact on the use of the model, but is useful during debugging and support.load()
Set self.lifecycle_events = None to disable this behaviour. Calls to add_lifecycle_event() will not record events into self.lifecycle_events then.
- Parameters
event_name (str) – Name of the event. Can be any label, e.g. “created”, “stored” etc.
event (dict) –
Key-value mapping to append to self.lifecycle_events. Should be JSON-serializable, so keep it simple. Can be empty.
This method will automatically add the following key-values to event, so you don’t have to specify them:
datetime: the current date & time
gensim: the current Gensim version
python: the current Python version
platform: the current platform
event: the name of this event
log_level (int) – Also log the complete event dict, at the specified log level. Set to False to not log at all.
-
add_null_word()
[¶](#gensim.models.word2vec.Word2Vec.add_null_word)
-
build_vocab(corpus_iterable=None, corpus_file=None, update=False, progress_per=10000, keep_raw_vocab=False, trim_rule=None, **kwargs)
[¶](#gensim.models.word2vec.Word2Vec.build_vocab) Build vocabulary from a sequence of sentences (can be a once-only generator stream).
- Parameters
corpus_iterable (iterable of list of str) – Can be simply a list of lists of tokens, but for larger corpora, consider an iterable that streams the sentences directly from disk/network. See
,BrownCorpus
orText8Corpus
module for such examples.LineSentence
corpus_file (str, optional) – Path to a corpus file in
format. You may use this argument instead of sentences to get performance boost. Only one of sentences or corpus_file arguments need to be passed (not both of them).LineSentence
update (bool) – If true, the new words in sentences will be added to model’s vocab.
progress_per (int, optional) – Indicates how many words to process before showing/updating the progress.
keep_raw_vocab (bool, optional) – If False, the raw vocabulary will be deleted after the scaling is done to free up RAM.
trim_rule (function, optional) –
Vocabulary trimming rule, specifies whether certain words should remain in the vocabulary, be trimmed away, or handled using the default (discard if word count < min_count). Can be None (min_count will be used, look to
), or a callable that accepts parameters (word, count, min_count) and returns eitherkeep_vocab_item()
gensim.utils.RULE_DISCARD
,gensim.utils.RULE_KEEP
orgensim.utils.RULE_DEFAULT
. The rule, if given, is only used to prune vocabulary during current method call and is not stored as part of the model.- The input parameters are of the following types:
word (str) - the word we are examining
count (int) - the word’s frequency count in the corpus
min_count (int) - the minimum count threshold.
**kwargs (object) – Keyword arguments propagated to self.prepare_vocab.
-
build_vocab_from_freq(word_freq, keep_raw_vocab=False, corpus_count=None, trim_rule=None, update=False)
[¶](#gensim.models.word2vec.Word2Vec.build_vocab_from_freq) Build vocabulary from a dictionary of word frequencies.
- Parameters
word_freq (dict of (str, int)) – A mapping from a word in the vocabulary to its frequency count.
keep_raw_vocab (bool, optional) – If False, delete the raw vocabulary after the scaling is done to free up RAM.
corpus_count (int, optional) – Even if no corpus is provided, this argument can set corpus_count explicitly.
trim_rule (function, optional) –
Vocabulary trimming rule, specifies whether certain words should remain in the vocabulary, be trimmed away, or handled using the default (discard if word count < min_count). Can be None (min_count will be used, look to
), or a callable that accepts parameters (word, count, min_count) and returns eitherkeep_vocab_item()
gensim.utils.RULE_DISCARD
,gensim.utils.RULE_KEEP
orgensim.utils.RULE_DEFAULT
. The rule, if given, is only used to prune vocabulary during current method call and is not stored as part of the model.- The input parameters are of the following types:
word (str) - the word we are examining
count (int) - the word’s frequency count in the corpus
min_count (int) - the minimum count threshold.
update (bool, optional) – If true, the new provided words in word_freq dict will be added to model’s vocab.
-
create_binary_tree()
[¶](#gensim.models.word2vec.Word2Vec.create_binary_tree) Create a
[binary Huffman tree](https://en.wikipedia.org/wiki/Huffman_coding)using stored vocabulary word counts. Frequent words will have shorter binary codes. Called internally frombuild_vocab()
.
-
estimate_memory(vocab_size=None, report=None)
[¶](#gensim.models.word2vec.Word2Vec.estimate_memory) Estimate required memory for a model using current settings and provided vocabulary size.
- Parameters
vocab_size (int, optional) – Number of unique tokens in the vocabulary
report (dict of (str, int), optional) – A dictionary from string representations of the model’s memory consuming members to their size in bytes.
- Returns
A dictionary from string representations of the model’s memory consuming members to their size in bytes.
- Return type
dict of (str, int)
-
get_latest_training_loss()
[¶](#gensim.models.word2vec.Word2Vec.get_latest_training_loss) Get current value of the training loss.
- Returns
Current training loss.
- Return type
float
-
init_sims(replace=False)
[¶](#gensim.models.word2vec.Word2Vec.init_sims) Precompute L2-normalized vectors. Obsoleted.
If you need a single unit-normalized vector for some key, call
instead:get_vector()
word2vec_model.wv.get_vector(key, norm=True)
.To refresh norms after you performed some atypical out-of-band vector tampering, call :meth:`~gensim.models.keyedvectors.KeyedVectors.fill_norms() instead.
- Parameters
replace (bool) – If True, forget the original trained vectors and only keep the normalized ones. You lose information if you do this.
-
init_weights()
[¶](#gensim.models.word2vec.Word2Vec.init_weights) Reset all projection weights to an initial (untrained) state, but keep the existing vocabulary.
-
classmethod load(*args, rethrow=False, **kwargs)
[¶](#gensim.models.word2vec.Word2Vec.load) Load a previously saved
model.Word2Vec
See also
save()
Save model.
- Parameters
fname (str) – Path to the saved file.
- Returns
Loaded model.
- Return type
-
make_cum_table(domain=2147483647)
[¶](#gensim.models.word2vec.Word2Vec.make_cum_table) Create a cumulative-distribution table using stored vocabulary word counts for drawing random words in the negative-sampling training routines.
To draw a word index, choose a random integer up to the maximum value in the table (cum_table[-1]), then finding that integer’s sorted insertion point (as if by bisect_left or ndarray.searchsorted()). That insertion point is the drawn index, coming up in proportion equal to the increment at that slot.
-
predict_output_word(context_words_list, topn=10)
[¶](#gensim.models.word2vec.Word2Vec.predict_output_word) Get the probability distribution of the center word given context words.
Note this performs a CBOW-style propagation, even in SG models, and doesn’t quite weight the surrounding words the same as in training – so it’s just one crude way of using a trained model as a predictor.
- Parameters
context_words_list (list of (str and/or int)) – List of context words, which may be words themselves (str) or their index in self.wv.vectors (int).
topn (int, optional) – Return topn words and their probabilities.
- Returns
topn length list of tuples of (word, probability).
- Return type
list of (str, float)
-
prepare_vocab(update=False, keep_raw_vocab=False, trim_rule=None, min_count=None, sample=None, dry_run=False)
[¶](#gensim.models.word2vec.Word2Vec.prepare_vocab) Apply vocabulary settings for min_count (discarding less-frequent words) and sample (controlling the downsampling of more-frequent words).
Calling with dry_run=True will only simulate the provided settings and report the size of the retained vocabulary, effective corpus length, and estimated memory requirements. Results are both printed via logging and returned as a dict.
Delete the raw vocabulary after the scaling is done to free up RAM, unless keep_raw_vocab is set.
-
prepare_weights(update=False)
[¶](#gensim.models.word2vec.Word2Vec.prepare_weights) Build tables and model weights based on final vocabulary settings.
-
reset_from(other_model)
[¶](#gensim.models.word2vec.Word2Vec.reset_from) Borrow shareable pre-built structures from other_model and reset hidden layer weights.
- Structures copied are:
Vocabulary
Index to word mapping
Cumulative frequency table (used for negative sampling)
Cached corpus length
Useful when testing multiple models on the same corpus in parallel. However, as the models then share all vocabulary-related structures other than vectors, neither should then expand their vocabulary (which could leave the other in an inconsistent, broken state). And, any changes to any per-word ‘vecattr’ will affect both models.
- Parameters
other_model (
) – Another model to copy the internal structures from.Word2Vec
-
save(*args, **kwargs)
[¶](#gensim.models.word2vec.Word2Vec.save) Save the model. This saved model can be loaded again using
, which supports online training and getting vectors for vocabulary words.load()
- Parameters
fname (str) – Path to the file.
-
scan_vocab(corpus_iterable=None, corpus_file=None, progress_per=10000, workers=None, trim_rule=None)
[¶](#gensim.models.word2vec.Word2Vec.scan_vocab)
-
score(sentences, total_sentences=1000000, chunksize=100, queue_factor=2, report_delay=1)
[¶](#gensim.models.word2vec.Word2Vec.score) Score the log probability for a sequence of sentences. This does not change the fitted model in any way (see
for that).train()
Gensim has currently only implemented score for the hierarchical softmax scheme, so you need to have run word2vec with hs=1 and negative=0 for this to work.
Note that you should specify total_sentences; you’ll run into problems if you ask to score more than this number of sentences but it is inefficient to set the value too high.
See the
[article by Matt Taddy: “Document Classification by Inversion of Distributed Language Representations”](https://arxiv.org/pdf/1504.07295.pdf)and the[gensim demo](https://github.com/piskvorky/gensim/blob/develop/docs/notebooks/deepir.ipynb)for examples of how to use such scores in document classification.- Parameters
sentences (iterable of list of str) – The sentences iterable can be simply a list of lists of tokens, but for larger corpora, consider an iterable that streams the sentences directly from disk/network. See
,BrownCorpus
orText8Corpus
inLineSentence
module for such examples.word2vec
total_sentences (int, optional) – Count of sentences.
chunksize (int, optional) – Chunksize of jobs
queue_factor (int, optional) – Multiplier for size of queue (number of workers * queue_factor).
report_delay (float, optional) – Seconds to wait before reporting progress.
-
seeded_vector(seed_string, vector_size)
[¶](#gensim.models.word2vec.Word2Vec.seeded_vector)
-
train(corpus_iterable=None, corpus_file=None, total_examples=None, total_words=None, epochs=None, start_alpha=None, end_alpha=None, word_count=0, queue_factor=2, report_delay=1.0, compute_loss=False, callbacks=(), **kwargs)
[¶](#gensim.models.word2vec.Word2Vec.train) Update the model’s neural weights from a sequence of sentences.
Notes
To support linear learning-rate decay from (initial) alpha to min_alpha, and accurate progress-percentage logging, either total_examples (count of sentences) or total_words (count of raw words in sentences) MUST be provided. If sentences is the same corpus that was provided to
earlier, you can simply use total_examples=self.corpus_count.build_vocab()
Warning
To avoid common mistakes around the model’s ability to do multiple training passes itself, an explicit epochs argument MUST be provided. In the common and recommended case where
is only called once, you can set epochs=self.epochs.train()
- Parameters
corpus_iterable (iterable of list of str) –
The
corpus_iterable
can be simply a list of lists of tokens, but for larger corpora, consider an iterable that streams the sentences directly from disk/network, to limit RAM usage. See,BrownCorpus
orText8Corpus
inLineSentence
module for such examples. See also theword2vec
[tutorial on data streaming in Python](https://rare-technologies.com/data-streaming-in-python-generators-iterators-iterables/).corpus_file (str, optional) – Path to a corpus file in
format. You may use this argument instead of sentences to get performance boost. Only one of sentences or corpus_file arguments need to be passed (not both of them).LineSentence
total_examples (int) – Count of sentences.
total_words (int) – Count of raw words in sentences.
epochs (int) – Number of iterations (epochs) over the corpus.
start_alpha (float, optional) – Initial learning rate. If supplied, replaces the starting alpha from the constructor, for this one call to`train()`. Use only if making multiple calls to train(), when you want to manage the alpha learning-rate yourself (not recommended).
end_alpha (float, optional) – Final learning rate. Drops linearly from start_alpha. If supplied, this replaces the final min_alpha from the constructor, for this one call to train(). Use only if making multiple calls to train(), when you want to manage the alpha learning-rate yourself (not recommended).
word_count (int, optional) – Count of words already trained. Set this to 0 for the usual case of training on all words in sentences.
queue_factor (int, optional) – Multiplier for size of queue (number of workers * queue_factor).
report_delay (float, optional) – Seconds to wait before reporting progress.
compute_loss (bool, optional) – If True, computes and stores loss value which can be retrieved using
.get_latest_training_loss()
callbacks (iterable of
, optional) – Sequence of callbacks to be executed at specific stages during training.CallbackAny2Vec
Examples
>>> from gensim.models import Word2Vec >>> sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]] >>> >>> model = Word2Vec(min_count=1) >>> model.build_vocab(sentences) # prepare the model vocabulary >>> model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs) # train word vectors (1, 30)
-
update_weights()
[¶](#gensim.models.word2vec.Word2Vec.update_weights) Copy all the existing weights, and reset the weights for the newly added vocabulary.
-
class gensim.models.word2vec.Word2VecTrainables
[¶](#gensim.models.word2vec.Word2VecTrainables) Bases:
SaveLoad
Obsolete class retained for now as load-compatibility state capture.
-
add_lifecycle_event(event_name, log_level=20, **event)
[¶](#gensim.models.word2vec.Word2VecTrainables.add_lifecycle_event) Append an event into the lifecycle_events attribute of this object, and also optionally log the event at log_level.
Events are important moments during the object’s life, such as “model created”, “model saved”, “model loaded”, etc.
The lifecycle_events attribute is persisted across object’s
andsave()
operations. It has no impact on the use of the model, but is useful during debugging and support.load()
Set self.lifecycle_events = None to disable this behaviour. Calls to add_lifecycle_event() will not record events into self.lifecycle_events then.
- Parameters
event_name (str) – Name of the event. Can be any label, e.g. “created”, “stored” etc.
event (dict) –
Key-value mapping to append to self.lifecycle_events. Should be JSON-serializable, so keep it simple. Can be empty.
This method will automatically add the following key-values to event, so you don’t have to specify them:
datetime: the current date & time
gensim: the current Gensim version
python: the current Python version
platform: the current platform
event: the name of this event
log_level (int) – Also log the complete event dict, at the specified log level. Set to False to not log at all.
-
classmethod load(fname, mmap=None)
[¶](#gensim.models.word2vec.Word2VecTrainables.load) Load an object previously saved using
from a file.save()
- Parameters
fname (str) – Path to file that contains needed object.
mmap (str, optional) – Memory-map option. If the object was saved with large arrays stored separately, you can load these arrays via mmap (shared memory) using mmap=’r’. If the file being loaded is compressed (either ‘.gz’ or ‘.bz2’), then `mmap=None must be set.
See also
save()
Save object to file.
- Returns
Object loaded from fname.
- Return type
object
- Raises
AttributeError – When called on an object instance instead of class (this is a class method).
-
save(fname_or_handle, separately=None, sep_limit=10485760, ignore=frozenset({}), pickle_protocol=4)
[¶](#gensim.models.word2vec.Word2VecTrainables.save) Save the object to a file.
- Parameters
fname_or_handle (str or file-like) – Path to output file or already opened file-like object. If the object is a file handle, no special array handling will be performed, all attributes will be saved to the same file.
separately (list of str or None, optional) –
If None, automatically detect large numpy/scipy.sparse arrays in the object being stored, and store them into separate files. This prevent memory errors for large objects, and also allows
[memory-mapping](https://en.wikipedia.org/wiki/Mmap)the large arrays for efficient loading and sharing the large arrays in RAM between multiple processes.If list of str: store these attributes into separate files. The automated size check is not performed in this case.
sep_limit (int, optional) – Don’t store arrays smaller than this separately. In bytes.
ignore (frozenset of str, optional) – Attributes that shouldn’t be stored at all.
pickle_protocol (int, optional) – Protocol number for pickle.
See also
load()
Load object from file.
-
add_lifecycle_event(event_name, log_level=20, **event)
-
class gensim.models.word2vec.Word2VecVocab
[¶](#gensim.models.word2vec.Word2VecVocab) Bases:
SaveLoad
Obsolete class retained for now as load-compatibility state capture.
-
add_lifecycle_event(event_name, log_level=20, **event)
[¶](#gensim.models.word2vec.Word2VecVocab.add_lifecycle_event) Append an event into the lifecycle_events attribute of this object, and also optionally log the event at log_level.
Events are important moments during the object’s life, such as “model created”, “model saved”, “model loaded”, etc.
The lifecycle_events attribute is persisted across object’s
andsave()
operations. It has no impact on the use of the model, but is useful during debugging and support.load()
Set self.lifecycle_events = None to disable this behaviour. Calls to add_lifecycle_event() will not record events into self.lifecycle_events then.
- Parameters
event_name (str) – Name of the event. Can be any label, e.g. “created”, “stored” etc.
event (dict) –
Key-value mapping to append to self.lifecycle_events. Should be JSON-serializable, so keep it simple. Can be empty.
This method will automatically add the following key-values to event, so you don’t have to specify them:
datetime: the current date & time
gensim: the current Gensim version
python: the current Python version
platform: the current platform
event: the name of this event
log_level (int) – Also log the complete event dict, at the specified log level. Set to False to not log at all.
-
classmethod load(fname, mmap=None)
[¶](#gensim.models.word2vec.Word2VecVocab.load) Load an object previously saved using
from a file.save()
- Parameters
fname (str) – Path to file that contains needed object.
mmap (str, optional) – Memory-map option. If the object was saved with large arrays stored separately, you can load these arrays via mmap (shared memory) using mmap=’r’. If the file being loaded is compressed (either ‘.gz’ or ‘.bz2’), then `mmap=None must be set.
See also
save()
Save object to file.
- Returns
Object loaded from fname.
- Return type
object
- Raises
AttributeError – When called on an object instance instead of class (this is a class method).
-
save(fname_or_handle, separately=None, sep_limit=10485760, ignore=frozenset({}), pickle_protocol=4)
[¶](#gensim.models.word2vec.Word2VecVocab.save) Save the object to a file.
- Parameters
fname_or_handle (str or file-like) – Path to output file or already opened file-like object. If the object is a file handle, no special array handling will be performed, all attributes will be saved to the same file.
separately (list of str or None, optional) –
If None, automatically detect large numpy/scipy.sparse arrays in the object being stored, and store them into separate files. This prevent memory errors for large objects, and also allows
[memory-mapping](https://en.wikipedia.org/wiki/Mmap)the large arrays for efficient loading and sharing the large arrays in RAM between multiple processes.If list of str: store these attributes into separate files. The automated size check is not performed in this case.
sep_limit (int, optional) – Don’t store arrays smaller than this separately. In bytes.
ignore (frozenset of str, optional) – Attributes that shouldn’t be stored at all.
pickle_protocol (int, optional) – Protocol number for pickle.
See also
load()
Load object from file.
-
add_lifecycle_event(event_name, log_level=20, **event)