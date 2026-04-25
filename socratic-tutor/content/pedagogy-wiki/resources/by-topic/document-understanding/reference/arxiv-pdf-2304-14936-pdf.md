# Source: https://arxiv.org/pdf/2304.14936.pdf
# Author: Seif Laatiri et al.
# Title: arXiv:2304.14936 (KIE benchmark generalization / train-test similarity analysis)
# Fetched via: jina
# Date: 2026-04-09

Title: 2304.14936v1.pdf



Number of Pages: 15

# Information Redundancy and Biases in Public Document Information Extraction Benchmarks 

Seif Laatiri, Pirashanth Ratnamogan, Jo¨ el Tang, Laurent Lam, William Vanhuffel, Fabien Caspani 

BNP Paribas (seifedinne.laatiri;pirashanth.ratnamogan;joel.tang;laurent.lam)@bnpparibas.com (william.vanhuffel;fabien.caspani)@bnpparibas.com 

Abstract. Advances in the Visually-rich Document Understanding (VrDU) field and particularly the Key-Information Extraction (KIE) task are marked with the emergence of efficient Transformer-based approaches such as the LayoutLM models. Despite the good performance of KIE models when fine-tuned on public benchmarks, they still struggle to gen-eralize on complex real-life use-cases lacking sufficient document annota-tions. Our research highlighted that KIE standard benchmarks such as SROIE and FUNSD contain significant similarity between training and testing documents and can be adjusted to better evaluate the general-ization of models. In this work, we designed experiments to quantify the information re-dundancy in public benchmarks, revealing a 75% template replication in SROIE’s official test set and 16% in FUNSD’s. We also proposed re-sampling strategies to provide benchmarks more representative of the generalization ability of models. We showed that models not suited for document analysis struggle on the adjusted splits dropping on average 10,5% F1 score on SROIE and 3.5% on FUNSD compared to multi-modal models dropping only 7,5% F1 on SROIE and 0.5% F1 on FUNSD. 

Keywords: Visually-rich Document Understanding · Key Information Extraction · Named Entity Recognition · Generalization Assessment. 

# 1 Introduction 

Visually-rich Document Understanding (VrDU) is a field that has seen progress lately following the recent breakthroughs in Natural Language Processing and Computer Vision. This field aims to transform documents into structured data by simultaneously leveraging their textual, positional and visual attributes. Since scanned documents are often noisy, recent works addressed VrDU as a two com-ponent stream: first extracting the text with optical character recognition and then performing analysis using OCR text, document’s layout and visual at-tributes. Real life business documents can belong to multiple categories such as fi-nancial reports, employee contracts, forms, emails, letters, receipts, resumes and  

> arXiv:2304.14936v1 [cs.CL] 28 Apr 2023 2S. Laatiri et al.

others. Thus it is challenging to create general pipelines capable of handling all types of documents. State-of-the-art models focus on document-level pre-training objectives then fine-tuning on downstream tasks. These models show promising results on public information extraction benchmarks such as FUNSD [11], SROIE [10], CORD [21], Kleister NDA [28]. However, on real world com-plex use cases it is difficult to replicate the same performances due to a lack of annotated samples and diversity in their templates. In this paper, we show that common benchmarks can be managed to better evaluate the generalization ability of information extraction models and thus become more viable tools for model selection for real-world business use cases. To this end, we focus on SROIE [10] and FUNSD [11] and explore their potential to challenge the generalization power of a given model. We design experiments to measure document similarities in the official training and testing splits of these benchmarks and propose resampling strategies to render these benchmarks a better evaluation of models’ performance on unseen documents. We then investigate the impact of these resampling strategies on state-of-the-art VrDU models. 

# 2 Background 

2.1 Related work Dataset biases and model generalization in NLP The study of dataset biases and model generalization is an important area of research that has already been conducted on several NLP tasks. In the Named Entity Recognition task, several studies have highlighted the fact that the common datasets CONLL 2003 [25] and OntoNotes 5 [34] are strongly biased by an unrealistic lexical overlap between mentions in training and test sets [3,29]. In the co-reference task, the same lexical overlap with respect to co-reference mentions was observed in CONLL 2012 [22] and led to an overestimation of the performance of deep learning models compared to classical methods for real world applications [20]. The Natural Language Inference (NLI) task also suffers from a dataset with bias. Indeed, MultiNLI has been reported to suffer from both lexical overlap and hypothesis-only bias: the fact that hypothesis sentences contain words associated with a target label [6]. Deep Learning models are extremely sensitive to these biases. However in real world, models should be able to generalize to new out of domain data. Multiple studies experimented models memorization capability [2] and models robustness in order to perform on out of domain data in multiple tasks: translation [19], co-reference [30] or named entity recognition [29]. To the best of our knowledge, our work is the first one assessing and analyzing biases in the context of information extraction from documents. 

Information extraction models When performing visual analysis on docu-ments, early work handled separately the different modalities. Preliminary work Information redundancy in public KIE benchmarks 3

[7,26] focused on extracting tabular data from documents by combining heuris-tic rules and convolutional networks to detect and recognize tabular data. Later work [27] used visual features for document layout detection by incorporating contextual information in Faster R-CNNs [24]. Follow up research [16,38] com-bined textual and visual information by introducing a graph convolution based model for key information extraction. This approach exhibited good results how-ever, models are only using supervised data which is limited. In addition, these pre-training methods do not inherently combine textual and visual attributes as they are merged during fine-tuning instead. Following the rise of Transformers, more Transformer based models were adapted for VrDU with novel pre-training objectives. LayoutLM [36] uses 2D positional embeddings in order to integrate layout information with word em-beddings and is pretrained on layout understanding tasks. LayoutLMv2 [35] adds token-level visual features extracted with Convolution Neural Networks and models interactions among text, layout and image. Later work aimed to match the reconstruction pre-training objectives of masked text with a similar objective for reconstructing visual attributes such as LayoutLMv3 [9] which pro-posed to predict masked image areas through a set of image tokens similarly to visual Transformers [5,13]. Other recent approaches [12,15] experimented with an OCR-free setup by leveraging an encoder-decoder visual transformer. 

2.2 Datasets 

Multiple datasets exist to benchmark a variety of document understanding tasks. For instance RVL-CDIP [8] is an image-centric dataset for document image classification, FUNSD [11], CORD [21], SROIE [10] and Kleister-NDA [28] are datasets for key information extraction respectively from forms, receipts and contracts whilst DocVQA [18] is a benchmark for visual question answering. In this work, we focus on the task of information extraction while investi-gating template similarities in the current documents distribution within the datasets. Documents having the same template are documents sharing the same layout that can be read in the same way. We decided to primarily work with SROIE and FUNSD as they are common benchmarks displaying two different types of documents. In more details, the SROIE dataset for Scanned Receipt OCR and Information Extraction was presented in the 2019 edition of the IC-DAR conference. It represents processes of recognizing text from scanned restau-rant receipts and extracting key entities from them. The dataset contains 1000 annotated scanned restaurant receipts split into train/test splits with the ratio 650/350. Three tasks were set up for the competition: Scanned Receipt Text Lo-calisation, Scanned Receipt Optical Character Recognition and Key Information Extraction from Scanned Receipts. Second, FUNSD is a dataset for Form Understanding in Noisy Scanned Doc-uments that have been a constant benchmark in recent document information extraction work. It contains noisy scanned forms and aims at extracting and structuring their textual contents. The dataset provides annotations for text recognition, entity linking and semantic entity labeling. In this work, FUNSD 4 S. Laatiri et al. 

refers to the revised version of the dataset released by the authors [31] containing the same documents with cleaned annotations. 

2.3 Problem statement 

We formalize key information extraction as a token classification task on the tokenized text extracted from the document. Let us denote by T = t0<i ≤n the sequence of text tokens ti extracted from a document D. Let I be the image of the document D and m the number of entity types (since we perform Inside-Outside-Beginning tagging [23] similarly to named entity recognition tasks, the number of entity classes is 2 m + 1). We aim to build a classifier F such that for every token ti in the sequence: 

F(ti|T, I) = c (1) with c ∈ { 1, . . . , 2m + 1 } the target IOB class of token ti.In IOB tagging, an entity spans over multiple adjacent tokens ( ti)istart ≤i≤iend 

and is only correctly predicted if all of its tokens are correctly predicted, that is F(tistart |T, I) = B − entity and F(ti|T, I) = I − entity f or i ∈ { istart +1, . . . , i end }

# 3 Approach 

3.1 Motivation 

Recent document analysis models such as LayoutLM models [36,35,9], Doc-Former [1], Lilt [32] and others used the datasets mentioned above to evaluate their models and benchmark them against other state-of-the-art works. However, these evaluation metrics are usually difficult to replicate on real-life business use-cases, particularly those obtained on SROIE and FUNSD. This discrepancy is, in part, due to the complexity of business use-cases and their lack of good-quality annotated data. However we also suspect that the current train and test splitting distribution of these datasets does not optimally evaluate the ability of models to generalize on unseen documents. Even though it is a common practice in machine learning to keep similar distributions for both training and testing data, this practice is not optimal when benchmarking and comparing models that will later be finetuned on small datasets or inferred on out-of-domain data. By containing similar documents in both training and testing data, these datasets allow models to memorize predictions during training and simply infer them on test documents without evaluating their ability to understand and analyze new templates of documents. In real business use-cases, this is particularly harming long-term performances, as domain shift often occurs after a certain period of time, when new unseen templates are used. Information redundancy in public KIE benchmarks 5

3.2 Resampling datasets 

For each studied dataset, the current training and testing documents are thor-oughly observed and analysed for homogeneous samples. We customize for every dataset a method to group similar documents and re-sample the training and testing splits to minimize template similarity and redundancy. We remind that the term template in this context refers to the disposition and layout of a doc-ument. 

SROIE: Information extraction in this dataset is performed by extracting se-mantic entities from business receipts such as business’ name, address, the or-der’s date and total price. As shown in Figure 2, receipts from the same business have a similar disposition, they contain the same business’ name and address as well as the same template. The current official data split of SROIE does not account for this factor as same business receipts can be present in both train and test documents. We group same businesses and re-sample train-test splits while assuring that every group is present in only a single split. The sizes of groups of samples sharing the same template varies from 1 to 76 receipts and their distribution is described in Figure 1 in a logarithmic scale.        

> 020 40 60 80
> 10 0
> 10 1
> 10 2
> 301
> 6
> 3
> 2
> 33
> 11
> 3
> 1
> Group size
> Occurrences
> Fig. 1. SROIE: distribution of similarity groups, each group containing receipts of the same template

FUNSD: By investigating FUNSD, we observed that multiple forms of the same template were present in the dataset while being filled with different infor-mation, for instance a standard hospital application filled by different patients. 6 S. Laatiri et al. ‘ 

> Fig. 2. SROIE: Receipts from two different business (a) and (b)

Having the exact same form template in both training and testing is a clear in-dicator of information redundancy as illustrated in the template comparison in Figure 4. Based on the fact that same template forms share similar slot names (questions ), we introduced a similarity metric on forms using the overlap of their question annotations. Based on this assumption, we propose the following overlap score for two forms: 

Overlap (docA, docB ) = Count (QuestionsA ∩ QuestionsB )

M ax (len (QuestionsA ), len (QuestionsB )) where QuestionsA and QuestionsB are respectively the question annotations sets of document A and document B. We have manually defined a set of template groups as ground truths and then evaluated different grouping similarity thresholds, eventually keeping a thresh-hold of 0.7. This metric was next used to group forms of same templates. The sizes of groups in this case was far lower than that of SROIE groups as the biggest group of forms sharing the same template was limited to 4 forms. From 50 forms in the testing set, we found 8 (16%) that shared the same template with at least one training form. We resample the train and test splits accord-ingly, ensuring that no forms with the same template are present in both splits. The resampled splits can be found in https://github.com/Seif-Lat 

3.3 Models 

In the context of information extraction from documents seen as a token classi-fication task, three approaches exist in the literature: Information redundancy in public KIE benchmarks 71 2 3 450 100 130 21 8 1Group size Occurrences  

> Fig. 3. FUNSD: distribution of similarity groups, each group containing forms of the same template

– Standard NLP models using textual information, 

– Layout Aware models using both text and layout information, 

– Multi-modal approaches using text, layout and visual representations of to-kens. In the context of our study, it is important to challenge the common evidence obtained using official datasets: multi-modal approaches are more effective than other approaches. We studied the fine-tuning of the following pretrained models: 

BERT [4] is a bidirectional Transformer-based language model pretrained on a large corpus with Mask Language Modeling (MLM) and Next Sentence Predic-tion (NSP) tasks. 

RoBERTa [17] differs from BERT during pretraining with the use of a signifi-cantly larger dataset, a larger batch size and dynamic masking in the MLM task while dropping the NSP pretraining objective. 

AlBERT [14] is a scalable version of BERT that uses two methods to reduce the model memory footprint: sharing some of the model layers, and a factorized embedding parameterization. 

Lilt [33] is an approach decoupling layout and text representation in order to have the model using more layout information and being more language in-dependent. It uses independent layout and text pretraining but also proposes 8 S. Laatiri et al. ‘

Fig. 4. FUNSD: Forms from two different templates (a) and (b) Information redundancy in public KIE benchmarks 9‘ 

> Fig. 5. Overview of document understanding models

a bi-direction attention complementation mechanism in order to combine two flows: one for layout the other one for the text. 

LayoutLM [36] introduced a multimodal pretraining approach combining text and layout features for document image understanding and information extrac-tion tasks. It leverages both text and layout features and incorporates them into a single framework. 

LayoutLMv2 [35] LayoutLMv2 is one of the first Transformers to use image feature during the pretraining process. They propose to use the output of a CNN architecture to create image token embeddings which gives useful information about the document layout. 

LayoutXLM [37] LayoutXLM has the same architecture as LayoutLMv2 but is pretrained on a multi-lingual dataset. 

LayoutLMv3 [9] LayoutLMv3 uses a multi modal Transformer architecture and introduces an image reconstruction pretraining objective similar to text reconstruction in the masked language modeling objective. 10 S. Laatiri et al. 

# 4 Experiments 

4.1 Experimental setup 

We use the same configuration when fine-tuning all the models. We use a batch size of 2 and an Adam optimizer with an initial learning rate of 2 ∗ 10 −5. We decrease the learning rate by half every 10 epochs without improvement in the validation F1 score. We stop the fine-tuning when the learning rate goes below 10 −7. We finally recover the model with the best validation F1. For each experiment, the test set is defined initially, either the official testing set on the original datasets or our extracted testing set on the resampled datasets. We then generate four different splits from the remaining data as training and validation data with 80-20 ratio, we train and test each model on the four splits and present the average performance in the sections below. We perform this cross validation for a more robust model comparison as we have observed a shift of performance in consecutive trainings of the same model. 

4.2 Results on original datasets 

We train a group of models leveraging different modalities on receipt under-standing and form understanding using the official splits of SROIE and FUNSD. Results are presented in table 1. On form understanding (FUNSD), models us-ing only the textual information of documents (BERT, AlBERT, RoBERTa) perform marginally worse than multi-modal models as their F1 scores are on av-erage 20 points less. RoBERTa has the highest F1 (80.64) score among textual models and is 5 points behind the closest multi-modal model being LayoutXLM with 85.57 F1. Among multi-modal models, LayoutLMv2 and LayoutLMv3 have better scores than LayoutLM and LiLT since they also leverage visual attributes of forms. LayoutLMv3 has the highest F1 score of 88.81 thanks to its efficient multi-modal pre-training. On receipt understanding (SROIE) multi-modal approaches also have higher metrics than textual models, however the discrepancy between them is much lower as the F1 increase between each multi-modal and the average score of all textual models varies from 2 to 4 and is considerably lower than what we observed on FUNSD. On this task LayoutLMv2 achieves the highest score amongst all models, reaching 96.14 F1. These results validate the importance of positional and visual attributes in information extraction tasks on visually rich documents. 

4.3 Results on resampled datasets 

After having resampled the splits of both FUNSD and SROIE, we train the same group of models and present results in table 2. On form understanding, textual models are outperformed by multi-modal models and show a more important decrease in performance compared to results on the original split with an average drop of 3.5 F1 score compared to only 0.5 in multi-modal models. Information redundancy in public KIE benchmarks 11 

SROIE FUNSD Model Params F1 Precision Recall F1 Precision Recall 

BERT base 110M 92.47 92.36 92.68 61.03 60.29 61.90 AlBERT base 12M 92.28 92.28 92.28 57.39 56.08 58.99 RoBERTa base 125M 93.90 93.23 94.61 80.64 81.36 79.96 LayoutLM base 112M 94.57 93.93 95.22 86.07 86.24 85.63 LiLT base 131M 95.41 95.23 95.60 87.41 87.41 87.41 LayoutLMv2 base 200M 96.14 96.39 95.94 88.14 88.31 88.08 LayoutXLM base 369M 94.75 94.57 94.94 85.57 85.87 85.46 LayoutLMv3 base 126M 95.11 94.87 95.70 88.81 89.32 88.46 

BERT large 351M 93.72 93.47 94.02 61.03 60.29 61.90 AlBERT large 18M 88.96 87.86 90.20 58.81 57.46 60.39 RoBERTa large 355M 94.99 94.91 95.09 82.43 82.99 81.78 LayoutLM large 340M 94.70 94.31 95.10 84.29 84.60 84.10 LayoutLMv2 large 426M 96.55 96.69 96.42 88.79 89.06 88.75 LayoutLMv3 large 365M 95.87 95.71 96.03 89.84 89.97 89.56 

Table 1. Performance of state-of-the-art information extraction models on SROIE and FUNSD official testing sets. 

SROIE FUNSD Model Params F1 Precision Recall F1 Precision Recall 

BERT base 110M 81.00 77.04 86.21 55.25 54.97 55.86 AlBERT base 12M 79.86 77.48 82.97 53.66 52.63 54.99 RoBERTa base 125M 86.05 84.15 88.20 78.71 79.16 78.59 LayoutLM base 112M 84.80 82.18 88.02 85.88 85.85 86.11 LiLT base 131M 89.38 86.94 92.11 84.76 85.12 84.91 LayoutLMv2 base 200M 87.92 86.67 89.34 88.61 88.65 88.94 LayoutXLM base 369M 87.99 86.24 90.14 85.51 85.98 86.25 LayoutLMv3 base 126M 87.86 87.29 88.71 89.07 89.26 89.16 

BERT large 351M 81.15 77.53 85.84 55.90 55.46 56.59 AlBERT large 18M 82.82 81.16 84.76 54.93 52.73 57.77 RoBERTa large 355M 87.86 86.16 89.84 80.28 80.16 80.66 LayoutLM large 340M 84.78 82.62 87.91 85.95 85.75 86.34 LayoutLMv2 large 426M 87.98 86.71 89.98 90.14 90.19 90.31 

LayoutLMv3 large 356M 88.47 87.00 90.13 89.86 89.72 90.31 

Table 2. Performance of state-of-the-art information extraction models on SROIE and FUNSD resampled testing sets. 12 S. Laatiri et al. 

On receipt understanding, F1 scores drastically drop compared to results on the original split in table 1, BERT, AlBERT and RoBERTa drop on average 10.5 F1 points whereas multi-modal models drop only 7.5 F1 points on average. Scores on the adjusted splits show a higher discrepancy between the models and are more consistent with the modalities leveraged by each model and the efficiency of their pretraining. For instance LiLT marginally outperforms LayoutLM as its pretraining allows it to better leverage the positional information of documents. The adjusted split also makes the information extraction task more challenging as the average F1 score drops from 94.34 to 85.60 and the highest reached F1 drops from 96.55 to 89.38. These results show that the original splits of both SROIE and FUNSD con-tained data leaks that allowed models to infer on testing data without neces-sarily learning how to understand new templates. The adjusted splits evaluate more properly the generalization ability of models and their capacity to transfer knowledge to unseen templates. 

# 5 Conclusion 

In this paper, we showed that SROIE and FUNSD were featuring information redundancies between their training and testing sets. Having trained multiple state-of-the-art models on VrDU tasks, we showed that this information redun-dancy artificially increases the models performances. In particular, we observe that SROIE is still a challenging benchmark as the average F1 score drops from 96.38 on the official splits to 88.78 on the adjusted splits, proving that it remains a viable benchmark for upcoming works when it is sampled more carefully. These findings demonstrate that generating Independent and Identically Dis-tributed splits for evaluation datasets as is traditionally done is not an optimal approach, as it introduces a high memorization bias especially with large neural networks. The 0% overlap approach presented in this work is an example of an alternate strategy specific to evaluating models’ generalization on unseen tem-plates and is closer to real-world use-cases than traditional splits. Other criteria can also be explored for this same purpose such as a date based resampling. 

# References    

> 1. Appalaraju, S., Jasani, B., Kota, B.U., Xie, Y., Manmatha, R.: Docformer: End-to-end transformer for document understanding. CoRR abs/2106.11539 (2021),
> https://arxiv.org/abs/2106.11539
> 2. Arpit, D., Jastrzebski, S., Ballas, N., Krueger, D., Bengio, E., Kanwal, M.S., Ma-haraj, T., Fischer, A., Courville, A., Bengio, Y., et al.: A closer look at memo-rization in deep networks. In: International conference on machine learning. pp. 233–242. PMLR (2017) 3. Augenstein, I., Derczynski, L., Bontcheva, K.: Generalisation in named entity recognition: A quantitative analysis. Computer Speech & Language 44 , 61–83 (2017)

Information redundancy in public KIE benchmarks 13 4. Devlin, J., Chang, M.W., Lee, K., Toutanova, K.: Bert: Pre-training of deep bidirec-tional transformers for language understanding Proceedings of the 2019 Con-ference of the North American Chapter of the Association for Com-putational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) (2019), https://aclanthology.org/N19-1423.pdf 

5. Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., Dehghani, M., Minderer, M., Heigold, G., Gelly, S., Uszkoreit, J., Houlsby, N.: An image is worth 16x16 words: Transformers for image recognition at scale (2020), 

https://arxiv.org/abs/2010.11929 

6. Gururangan, S., Swayamdipta, S., Levy, O., Schwartz, R., Bowman, S., Smith, N.A.: Annotation artifacts in natural language inference data. In: Proceedings of the 2018 Conference of the North American Chapter of the Association for Com-putational Linguistics: Human Language Technologies, Volume 2 (Short Papers). pp. 107–112. Association for Computational Linguistics, New Orleans, Louisiana (Jun 2018). https://doi.org/10.18653/v1/N18-2017, https://aclanthology.org/ N18-2017 

7. Hao, L., Gao, L., Yi, X., Tang, Z.: A table detection method for pdf documents based on convolutional neural networks. In: 2016 12th IAPR Workshop on Document Analysis Systems (DAS). pp. 287–292 (2016). https://doi.org/10.1109/DAS.2016.23 8. Harley, A.W., Ufkes, A., Derpanis, K.G.: Evaluation of deep convolutional nets for document image classification and retrieval. CoRR abs/1502.07058 (2015), 

http://arxiv.org/abs/1502.07058 

9. Huang, Y., Lv, T., Cui, L., Lu, Y., Wei, F.: Layoutlmv3: Pre-training for document ai with unified text and image masking. In: Proceedings of the 30th ACM International Conference on Multimedia. p. 4083–4091. MM ’22, Association for Computing Machinery, New York, NY, USA (2022). https://doi.org/10.1145/3503161.3548112, https://doi.org/10.1145/3503161. 3548112 

10. Huang, Z., Chen, K., He, J., Bai, X., Karatzas, D., Lu, S., Jawahar, C.: Icdar2019 competition on scanned receipt ocr and information extraction pp. 1516–1520 (2019), https://arxiv.org/pdf/2103.10213.pdf 

11. Jaume, G., Kemal Ekenel, H., Thiran, J.P.: Funsd: A dataset for form under-standing in noisy scanned documents. In: 2019 International Conference on Doc-ument Analysis and Recognition Workshops (ICDARW). vol. 2, pp. 1–6 (2019). https://doi.org/10.1109/ICDARW.2019.10029 12. Kim, G., Hong, T., Yim, M., Nam, J., Park, J., Yim, J., Hwang, W., Yun, S., Han, D., Park, S.: Ocr-free document understanding transformer (2022) 13. Kim, W., Son, B., Kim, I.: Vilt: Vision-and-language transformer without convo-lution or region supervision (2021), https://arxiv.org/abs/2102.03334 

14. Lan, Z., Chen, M., Goodman, S., Gimpel, K., Sharma, P., Soricut, R.: Albert: A lite bert for self-supervised learning of language representations. arXiv preprint arXiv:1909.11942 (2019) 15. Lee, K., Joshi, M., Turc, I., Hu, H., Liu, F., Eisenschlos, J., Khandelwal, U., Shaw, P., Chang, M.W., Toutanova, K.: Pix2struct: Screenshot parsing as pretraining for visual language understanding (2022) 16. Liu, X., Gao, F., Zhang, Q., Zhao, H.: Graph convolution for multimodal informa-tion extraction from visually rich documents. In: NAACL (2019) 17. Liu, Y., Ott, M., Goyal, N., Du, J., Joshi, M., Chen, D., Levy, O., Lewis, M., Zettlemoyer, L., Stoyanov, V.: Roberta: A robustly optimized bert pretraining 14 S. Laatiri et al. approach (2019). https://doi.org/10.48550/ARXIV.1907.11692, https://arxiv. org/abs/1907.11692 

18. Mathew, M., Karatzas, D., Manmatha, R., Jawahar, C.V.: Docvqa: A dataset for VQA on document images. CoRR abs/2007.00398 (2020), https://arxiv.org/ abs/2007.00398 

19. Mghabbar, I., Ratnamogan, P.: Building a multi-domain neural machine transla-tion model using knowledge distillation. In: Giacomo, G.D., Catal´ a, A., Dilkina, B., Milano, M., Barro, S., Bugar´ ın, A., Lang, J. (eds.) ECAI 2020 - 24th Euro-pean Conference on Artificial Intelligence, 29 August-8 September 2020, Santiago de Compostela, Spain, August 29 - September 8, 2020 - Including 10th Conference on Prestigious Applications of Artificial Intelligence (PAIS 2020). Frontiers in Ar-tificial Intelligence and Applications, vol. 325, pp. 2116–2123. IOS Press (2020). https://doi.org/10.3233/FAIA200335, https://doi.org/10.3233/FAIA200335 

20. Moosavi, N.S., Strube, M.: Using linguistic features to improve the generalization capability of neural coreference resolvers. arXiv preprint arXiv:1708.00160 (2017) 21. Park, S., Shin, S., Lee, B., Lee, J., Surh, J., Seo, M., Lee, H.: Cord: A consolidated receipt dataset for post-ocr parsing (2019) 22. Pradhan, S., Moschitti, A., Xue, N., Uryupina, O., Zhang, Y.: Conll-2012 shared task: Modeling multilingual unrestricted coreference in ontonotes. In: Joint Con-ference on EMNLP and CoNLL-Shared Task. pp. 1–40 (2012) 23. Ramshaw, L., Marcus, M.: Text chunking using transformation-based learning. In: Third Workshop on Very Large Corpora (1995), https://aclanthology.org/ W95-0107 

24. Ren, S., He, K., Girshick, R., Sun, J.: Faster r-cnn: Towards real-time object detection with region proposal networks. In: Cortes, C., Lawrence, N., Lee, D., Sugiyama, M., Garnett, R. (eds.) Advances in Neural Information Processing Sys-tems. vol. 28. Curran Associates, Inc. (2015), https://proceedings.neurips.cc/ paper/2015/file/14bfa6bb14875e45bba028a21ed38046-Paper.pdf 

25. Sang, E.F., De Meulder, F.: Introduction to the conll-2003 shared task: Language-independent named entity recognition. arXiv preprint cs/0306050 (2003) 26. Schreiber, S., Agne, S., Wolf, I., Dengel, A., Ahmed, S.: Deepdesrt: Deep learning for detection and structure recognition of tables in document images. In: 2017 14th IAPR International Conference on Document Analysis and Recognition (ICDAR). vol. 01, pp. 1162–1167 (2017). https://doi.org/10.1109/ICDAR.2017.192 27. Soto, C., Yoo, S.: Visual detection with context for document layout analysis. In: Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Pro-cessing (EMNLP-IJCNLP). pp. 3464–3470. Association for Computational Lin-guistics, Hong Kong, China (Nov 2019). https://doi.org/10.18653/v1/D19-1348, 

https://aclanthology.org/D19-1348 

28. Stanislawek, T., Gralinski, F., Wr´ oblewska, A., Lipinski, D., Kaliska, A., Rosalska, P., Topolski, B., Biecek, P.: Kleister: Key information extraction datasets involving long documents with complex layouts. CoRR abs/2105.05796 (2021), https: //arxiv.org/abs/2105.05796 

29. Taill´ e, B., Guigue, V., Gallinari, P.: Contextualized embeddings in named-entity recognition: An empirical study on generalization. In: European Conference on Information Retrieval. pp. 383–391. Springer (2020) 30. Toshniwal, S., Xia, P., Wiseman, S., Livescu, K., Gimpel, K.: On generaliza-tion in coreference resolution. In: Proceedings of the Fourth Workshop on Com-putational Models of Reference, Anaphora and Coreference. pp. 111–120. Asso-ciation for Computational Linguistics, Punta Cana, Dominican Republic (Nov Information redundancy in public KIE benchmarks 15 2021). https://doi.org/10.18653/v1/2021.crac-1.12, https://aclanthology.org/ 2021.crac-1.12 

31. Vu, H.M., Nguyen, D.T.: Revising FUNSD dataset for key-value detection in doc-ument images. CoRR abs/2010.05322 (2020), https://arxiv.org/abs/2010. 05322 

32. Wang, J., Jin, L., Ding, K.: Lilt: A simple yet effective language-independent layout transformer for structured document understanding (2022). https://doi.org/10.48550/ARXIV.2202.13669, https://arxiv.org/abs/2202. 13669 

33. Wang, J., Jin, L., Ding, K.: Lilt: A simple yet effective language-independent layout transformer for structured document understanding. arXiv preprint arXiv:2202.13669 (2022) 34. Weischedel, R., Palmer, M., Marcus, M., Hovy, E., Pradhan, S., Ramshaw, L., Xue, N., Taylor, A., Kaufman, J., Franchini, M., et al.: Ontonotes release 5.0 ldc2013t19. Linguistic Data Consortium, Philadelphia, PA 23 (2013) 35. Xu, Y., Xu, Y., Lv, T., Cui, L., Wei, F., Wang, G., Lu, Y., Florencio, D., Zhang, C., Che, W., Zhang, M., Zhou, L.: LayoutLMv2: Multi-modal pre-training for visually-rich document understanding. In: Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Vol-ume 1: Long Papers). pp. 2579–2591. Association for Computational Linguis-tics, Online (Aug 2021). https://doi.org/10.18653/v1/2021.acl-long.201, https: //aclanthology.org/2021.acl-long.201 

36. Xu, Y., Li, M., Cui, L., Huang, S., Wei, F., Zhou, M.: Layoutlm: Pre-training of text and layout for document image understanding. In: Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Min-ing. p. 1192–1200. KDD ’20, Association for Computing Machinery, New York, NY, USA (2020). https://doi.org/10.1145/3394486.3403172, https://doi.org/ 10.1145/3394486.3403172 

37. Xu, Y., Lv, T., Cui, L., Wang, G., Lu, Y., Florencio, D., Zhang, C., Wei, F.: Layoutxlm: Multimodal pre-training for multilingual visually-rich document un-derstanding. arXiv preprint arXiv:2104.08836 (2021) 38. Yu, W., Lu, N., Qi, X., Gong, P., Xiao, R.: Pick: Processing key information extraction from documents using improved graph learning-convolutional networks (2020), https://arxiv.org/abs/2004.07464