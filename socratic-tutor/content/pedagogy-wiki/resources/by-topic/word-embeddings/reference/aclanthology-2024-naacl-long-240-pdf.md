# Source: https://aclanthology.org/2024.naacl-long.240.pdf
# Title: A Systematic Comparison of Contextualized Word Embeddings for Lexical Semantic Change
# Fetched via: jina
# Date: 2026-04-09

Title: 2024.naacl-long.240.pdf



Number of Pages: 21

> Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers) , pages 4262–4282 June 16-21, 2024 ©2024 Association for Computational Linguistics

## A Systematic Comparison of Contextualized Word Embeddings for Lexical Semantic Change 

Francesco Periti 

University of Milan Via Celoria, 18 20133 Milano, Italy 

francesco.periti@unimi.it 

Nina Tahmasebi 

University of Gothenburg Renströmsgatan 6 40530 Göteborg, Sweden 

nina.tahmasebi@gu.se 

Abstract 

Contextualized embeddings are the pre-ferred tool for modeling Lexical Semantic Change (LSC). Current evaluations typically fo-cus on a specific task known as Graded Change Detection (GCD). However, performance com-parison across work are often misleading due to their reliance on diverse settings. In this paper, we evaluate state-of-the-art models and approaches for GCD under equal conditions. We further break the LSC problem into Word-in-Context (WiC) and Word Sense Induction (WSI) tasks, and compare models across these different levels. Our evaluation is performed across different languages on eight available benchmarks for LSC, and shows that (i) APD outperforms other approaches for GCD; (ii) XL-LEXEME outperforms other contextual-ized models for WiC, WSI, and GCD, while being comparable to GPT-4; (iii) there is a clear need for improving the modeling of word mean-ings, as well as focus on how , when , and why 

these meanings change, rather than solely fo-cusing on the extent of semantic change. 

1 Introduction 

Lexical Semantic Change (LSC) is the problem of automatically identifying words that change their meaning over time (Montanelli and Periti, 2023; Tahmasebi et al., 2021; Kutuzov et al., 2018; Tang, 2018). The interest in this problem has been signif-icantly fueled by the advent of word embeddings and modern language models. After more than a decade of ad hoc evaluation, a new evaluation framework was recently introduced, aimed at as-sessing and comparing the performance of different models and approaches (Schlechtweg et al., 2020). This framework was adopted to create benchmarks in different languages. Each benchmark includes a diachronic corpus spanning two time periods, along with a list of target words and tasks aimed at detecting word meaning change over time. The most popular task, known as Graded Change Detection (GCD), consists of ranking a list of target words based on their degree of change. The initial excitement for word embeddings prompted researchers and practitioners to solve the GCD task by using static embedding mod-els (Schlechtweg et al., 2020; Shoemark et al., 2019). However, the shift towards more advanced Transformer architectures has established the use of contextualized embedding models as the pre-ferred tool for addressing GCD (Montanelli and Periti, 2023; Kutuzov et al., 2022b). On one hand, these models distinguish the different meanings of a word by contextualizing each occurrence with a different embedding. On the other hand, the gen-eration and processing of contextualized embed-dings across entire corpora pose scalability chal-lenges, both in terms of time and memory consump-tion (Periti et al., 2022; Montariol et al., 2021). Dif-ferent strategies have been adopted to tackle these challenges, leading to a proliferation of evaluations across diverse settings (e.g., limited samples of benchmarks) and conditions (e.g., pre-trained vs. fine-tuned models). As a result, these evaluations on GCD hinder a fair comparison among the perfor-mance of different models and approaches, thereby deviating from the original goal of the framework. Moreover, while the GCD task is attracting more and more evaluations, it addresses only a partial complexity inherent to the established framework. Notably, the framework includes three distinct as-pects also discussed in Schlechtweg et al. (2024): 

i) semantic proximity judgments of word in-context ,

ii) word sense induction based on proximity judgments, 

iii) quantification of semantic change from in-duced senses. 

4262 As a matter of fact, when contextualized embed-ding models are used to address GCD, cosine simi-larities among word embeddings serve as surrogate for (i) , without evaluation focused on this aspect. Additionally, most approaches to GCD, pass from 

(i) to (iii) , sidestepping the intermediate aspect (ii) .That is, they quantify semantic change as overall proximity variation, without inducing word senses. Consequently, while these approaches can be evalu-ated through GDC, they preclude the interpretation of which meaning(s) have changed. We argue that (i) and (ii) are equally relevant aspects as (iii) , constituting a fundamental aspect of the LSC problem. Their evaluation can pro-vide valuable insights into the current state of LSC modeling, while offering a broader perspective on contextualized embedding models in Natural Lan-guage Processing (NLP). 1

Original contribution of our work 

• We systematically evaluate and compare var-ious models and approaches for GCD under equal settings and conditions. Our evalua-tion for GCD spans eight different languages. Importantly, we perform the first evaluation over Chinese and the second evaluation for Norwegian within the existing literature. Our results show superior performance of the re-cent state-of-the-art model for GCD, namely XL-LEXEME, over various approaches. • We are the first to evaluate contextualized embedding models for (i) and (ii) within the existing literature. Our evaluation of (i) 

and (ii) relies on two well-known tasks in NLP, namely Word-in-Context (WiC), and Word Sense Induction (WSI). Im-portantly, we evaluate various models as com-putational annotators .• We compare GPT-4 to contextualized mod-els through the WiC, WSI, and GCD tasks. Our evaluation reveals that GPT-4 obtains comparable performance to XL-LEXEME. In contrast to the limited accessibility 2 and high associated cost 3 of GPT-4, XL-LEXEME is a considerably smaller, open-source model. Thus, we argue that the use of GPT-4 is not justified for modeling the LSC problem.      

> 1Software is available at https://github.com/ FrancescoPeriti/CSSDetection .
> 2https://platform.openai.com/docs/ guides/rate-limits
> 3https://openai.com/pricing
> Figure 1: DWUG for the German word Eintagsfliege .Nodes represent word usages. Edges represent the relat-edness between usages. Colors indicate clusters (senses) inferred from the full graph (Laicher et al., 2021).

2 Background and related work 

The established LSC framework adheres to the novel annotation paradigm for word senses and en-compasses (i-iii) (Schlechtweg et al., 2021). (i) Hu-man annotators provide semantic proximity judg-ments for pairs of word usages sampled from a diachronic corpus spanning two time periods. (ii) 

Word usages and judgments are represented as nodes and edges in a weighted, diachronic graph, known as Diachronic Word Usage Graph (DWUG). This graph is then clustered with a graph clustering algorithm and the resulting clusters are interpreted as word senses (see Figure 1), thus sidestepping the need for explicit word sense definitions. Finally, 

(iii) given a word, a ground truth score of semantic change is computed by comparing the probability distributions of clusters in different time periods, e.g., a cluster with most of its usages from one time period indicates a substantial semantic change. Originally, the framework was proposed in a shared task at SemEval-2020, including bench-marks for four languages, namely English (EN), German (DE), Swedish (SW), and Latin (LA) (Schlechtweg et al., 2020). Benchmarks for Italian (Basile et al., 2020), Russian (RU) (Kutuzov and Pivovarova, 2021b,c), Spanish (SP) (Zamora-Reina et al., 2022b), Norwegian (NO) (Kutuzov et al., 2022a), and Chinese (ZH) (Chen et al., 2023a, 2022) have recently been introduced. Each benchmark 4 consists of a diachronic corpus and a set of target words over which the human annota-tion was conducted. The evaluation over a bench-mark is typically conducted through the GCD task where the goal is to rank the targets by degree of semantic change across the corpus. The Spearman correlation between predicted and ground truth 

scores is used to evaluate models and approaches.       

> 4See https://github.com/ChangeIsKey/ LSCDBenchmark for acomprehensive overview of available benchmarks

4263 2.1 Approaches to Graded Change Detection 

GCD is typically addressed using two kinds of approaches for modeling word meanings: form-

and sense -based (Montanelli and Periti, 2023; Giu-lianelli et al., 2020). The former capture signals of change by analysing how the dominant meaning, or the degree of polysemy of a word, changes over time (e.g., Giulianelli et al., 2020; Martinc et al., 2020a). The latter cluster word usages according to their meanings and then estimate the semantic change of a word by comparing the cluster distribu-tion of its usages over time (e.g., Periti et al., 2023; Martinc et al., 2020b). Form- and sense-based approaches can be further distinguished into su-pervised , which leverage external knowledge (e.g., dictionaries, Rachinskiy and Arefyev, 2022) or other forms of supervision (e.g., Word-in-Context datasets, Cassotti et al., 2023), and unsupervised ,which rely solely on the knowledge encoded in pre-trained models (e.g., Aida and Bollegala, 2023). 

2.2 Comparison of approaches 

Models and approaches for GCD have been evalu-ated under different settings and conditions. For ex-ample, some studies utilized the entire diachronic corpus to estimate the change of each target (e.g., Periti et al., 2022), while others relied on smaller samples (e.g., Rodina et al., 2021), or solely on the annotated word usages (e.g., Laicher et al., 2021). Also, different versions of the ground truth are used (e.g., Schlechtweg et al., 2022a). In the current literature, some studies fine-tune the mod-els on the corpus (e.g., Rosin et al., 2022), while others directly use pre-trained models (e.g., Kud-isov and Arefyev, 2022). Performance compar-ison are conducted across different models such as BERT (e.g., Laicher et al., 2021), mBERT (e.g., Beck, 2020), and XLM-R (e.g., Giulianelli et al., 2022). However, even when the same model is employed, different layer aggregations are used, such as concatenating the output of the last four en-coder layers (e.g., Kanjirangat et al., 2020), or sum-ming the output of all the encoder layers (e.g., Giu-lianelli et al., 2022). Moreover, sense-based ap-proaches are compared with different clustering algorithms such as Affinity Propagation (e.g., Mart-inc et al., 2020b), A Posteriori affinity Propagation (e.g., Periti et al., 2022), and K-Means (e.g., Mon-tariol et al., 2021). As a results, comparing Spearman correlation across different evaluations is often misleading .

2.3 Current modeling of LSC 

Current modeling of LSC overlooks the procedure 

(i-iii) used to generate the ground truth. Mostly, only (iii) is evaluated by relying on form-based approaches. However, these approaches capture only the degree of semantic change, preventing its interpretation. Sense-based approaches could fill this gap by explaining how and what has changed, but currently suffer from lower performance on 

(iii) and are therefore less pursued. As a results, it is not clear which meanings these models and approaches are capturing. There is thus a need to carefully evaluate their ability in both (i) and (ii) .Thus far, this evaluation is missing. To the best of our knowledge, only Laicher et al. (2021) evalu-ate (ii) through the WSI task. This evaluation needs to be extended beyond a single model, using the same procedure used to generate the ground truth. 

A systematic comparison under equal settings and conditions is necessary to evaluate different models and approaches. Thus, we first evaluate standard form- and sense-based approaches to pro-vide a fair performance comparison on GCD across eight languages. We then assess different models as computational annotators by evaluating them on (i-iii) through WiC, WSI, and GCD. Aligning with Karjus (2023), if computational models per-form close to human-level, their usage would rep-resent an unprecedented opportunity to scale up semantic change studies in the humanities and so-cial sciences. 

3 Evaluation setup 

We consider benchmarks for eight different lan-guages: EN, LA, DE, SV, ES, RU, NO, and ZH (see Table 6). For each benchmark, we evalu-ate four different models: BERT (Devlin et al., 2019), mBERT, XLM-R (Conneau et al., 2020), and XL-LEXEME (Cassotti et al., 2023). BERT is a monolingual model, mBERT, XLM-R, and XL-LEXEME are multilingual models. BERT, mBERT, and XLM-R are pre-trained masked language mod-els. XL-LEXEME is a fine-tuned XLM-R model that leverages the SBERT architecture to solve the WiC task, thus serving as a WiC pre-trained model. Aligning with the unsupervised nature of the LSC framework, we compare pre-trained models without performing additional fine-tuning (see Ta-ble 7). For each model and each target word in a benchmark, we collect contextualized embed-dings for all its word usages in both time periods. 4264 Specifically, we generate the sets of embeddings 

Φ1 = {a1, ..., a n} and Φ2 = {b1, ..., b m} for the word usages associated to time periods t1 and t2,respectively. 

3.1 Standard Graded Change Detection 

We compare the use of different models with four standard approaches to GCD, specifically two form-based and two sense-based. Similar to Laicher et al. (2021), we consider the raw data originally used to derive ground truth scores, instead of considering the associated corpora. This ensures an accurate evaluation under a controlled setting. 

3.2 Computational annotators 

We assess different models as computational anno-tators by using cosine similarities between embed-dings as a surrogate of human judgments. In our evaluation, we consider word usage pairs where human judgments are available, instead of consid-ering all potential usage pairs (as in Section 3.1). Specifically, we adhere to the framework (i-iii) and evaluate different models through the WiC, WSI, and GCD tasks. Inspired by Periti et al. (2024); Laskar et al. (2023); Koco´ n et al. (2023); Karjus (2023), we evaluate GPT-4 and compare its use to contextu-alized models. However, the limited accessibility and high associated cost constraint our extension only to the EN benchmark. 

4 Comparing approaches for GCD 

We evaluate different approaches for GCD using Spearman correlation (Spearman, 1904) between computational predictions and ground truth scores. Specifically, we process the embeddings of each target using the following approaches. 

4.1 Form-based approaches 

In the most recent survey on LSC by Montanelli and Periti (2023), it was observed that cosine dis-tance over word prototype (PRT) and the average pairwise distance (APD) consistently demonstrated superior performance compared to alternative ap-proaches. Thus, we employ these approaches: 

PRT computes the degree of change of a word w

as the cosine distance between the average embed-dings μ1 and μ2 (also know as prototype embed-dings) of w in the time periods t1 and t2 (Martinc et al., 2020a; Kutuzov and Giulianelli, 2020). For-mally, given a word w, we compute its degree of change by computing: PRT (Φ 1, Φ2) = 1 − cosine (μ1, μ 2) (1) The intuition behind PRT is that a prototype em-bedding encodes the dominant meaning of a word, and as such, the semantic change is computed as a shift in the dominant meaning over time. 

APD computes the degree of change of a word w

as the average pairwise distance between the word embeddings in Φ1 and Φ2 (Giulianelli et al., 2020; Kutuzov and Giulianelli, 2020). Formally, given a word w, we compute its degree of change, where d

is cosine distance, as follows: APD (Φ 1, Φ2) = 1

|Φ1|| Φ2| · ∑  

> a∈Φ1, b ∈Φ2

d(a, b )

(2) The intuition behind APD is that different word embeddings encode the polysemy of a word, and as such, the semantic change is computed as a shift in the word’s degree of polysemy. 

4.2 Sense-based approaches 

We choose two state-of-the-art sense-based ap-proaches (Montanelli and Periti, 2023).The first uti-lizes the unsupervised clustering algorithm Affinity Propagation (AP, Frey and Dueck, 2007) combined with the Jensen Shannon divergence (JSD, Lin, 1991). Additionally, we employ the evolutionary extension of Affinity Propagation, called A Posteri-ori affinity Propagation (APP, Castano et al., 2024), combined with the average pairwise distances be-tween sense prototypes (APDP). This approach is called WiDiD (Periti et al., 2022). 

AP+JSD leverages the AP clustering to distin-guish the different contextual usages of a given word w. Specifically, the embeddings Φ1, and Φ2

are collectively clustered to generate clusters com-prising embeddings from both time periods (i.e., 

t1 and t2), or embeddings exclusive from a time period (i.e., t1 or t2). The semantic change of w

is computed as the JSD between the probability distributions p1 and p2 of clusters in time periods 

t1 and t2. These distributions represent the relative number of embeddings from Φ1 and Φ2 grouped in each cluster, respectively (Martinc et al., 2020b,c). Formally, the degree of semantic change is: JSD (p1, p 2) = 12 (KL (p1|| M ) + KL (p2|| M )) 

(3) 4265 where KL stands for Kullback-Leibler divergence and M = (p1+p2)2 . The intuition behind AP+JSD is that different clusters encode nuanced word mean-ings, and as such, the semantic change is com-puted as an overall measure of the differences in the prominence of each sense over time. 

WiDiD leverages the APP clustering to distin-guish the usages of a given word w. Specifically, the embeddings Φ1, and Φ2 are individually clus-tered to generate incremental clusters of embed-dings that evolve with each clustering iteration. The semantic change of w is computed as the av-erage pairwise distances between the sense proto-types Ψ1 and Ψ2 of w in the time periods t1 and 

t2, where Ψ1 and Ψ2 are the set of embeddings ob-tained by averaging the embeddings Φ1 and Φ2 in each cluster, respectively (Periti et al., 2023; Kash-leva et al., 2022). Formally, given a word w, the degree of semantic change is computed as follows: 5

APDP (Φ 1, Φ2) = APD (Ψ 1, Ψ2) (4) The intuition behind WiDiD is similar to AP+JSD. However, while the latter considers change as the difference between the amount of probability for a sense over time, WiDiD is similar to APD in computing the shift in prototypical word meanings. 

4.3 Evaluation results - Table 1 

We present the results of our evaluation in Table 1 for both form- and sense-based approaches. For the sake of comparison, we include state-of-the-art (SOTA) results in Table 5. 6 As a general remark, we note instances where our results surpass SOTA (e.g., XL-LEXEME+APD for EN). We attribute this to the controlled setting established in our ex-periments. We note also instances where our results are lower than SOTA (e.g., BERT+APD for SV). This discrepancy may be influenced by various fac-tors such as different versions of the benchmarks (e.g., 37 vs 46 targets for EN in DWUG version 2.0.1, Schlechtweg et al., 2020). Additionally, vari-ations in text pre-processing can play a beneficial role. For instance, Laicher et al. (2021) demon-strate the effectiveness of lemmatization to mitigate word form biases, while Martinc et al. (2020c) sug-gest that filtering Named Entities can help models  

> 5Following Periti et al. (2023), we use the Canberra dis-tance instead of the cosine distance
> 6Our comparison includes results from different bench-marks using the same approaches. However, some bench-marks might have been assessed using other approaches.

avoid inflating semantic change. Moreover, some studies fine-tune or utilize different embedding lay-ers , whereas we adhere to the standard, generally adopted procedures without fine-tuning, consider-ing embeddings generated from the last (i.e., 12 th )layer of the models. Finally, there are sometimes significantly different results reported by differ-ent studies under similar conditions. For instance, Zhou et al. (2023) achieve a correlation of .706 using pre-trained BERT and APD, whereas others typically report correlations ranging between .400 and .600 (e.g., .489, Keidar et al., 2022; .514, Giu-lianelli et al., 2020; .546, Kutuzov and Giulianelli, 2020; .571, Laicher et al., 2021). This disparity cannot currently be explained. 

Languages. We obtain strong correlations with all benchmarks but LA. Our results show a

weighted average correlation of .751 when em-ploying XL-LEXEME + APD. In this calculation, we assign weights based on the number of targets in each benchmark, considering larger sets more reliable than smaller ones. For LA, it can be ar-gued that the models were not directly tailored or fine-tuned for Latin. However, XL-LEXEME demonstrates optimal performance in GCD in SV and medium performance in SP and NO without specific training on either (Cassotti et al., 2023). This leads us to consider that the quality of the LA benchmark potentially is lower than other bench-marks, as it was developed using a different proce-dure (Schlechtweg et al., 2020). 

Form-based vs Sense-based. We note that form-based approaches significantly outperform sense-based approaches. Our results consistently high-light APD as the most effective approach, regard-less of the skewness in the distribution of judg-ments, as previously argued by Kutuzov and Giu-lianelli (2020). In addition, WiDiD consistently demonstrate superior performance over AP+JSD. This can be attributed to the use of i) an evolution-ary clustering algorithm, which enables to consider the time dimension of text in a dynamic way; or, al-ternatively ii) APD over sense-prototypes, as APD has demonstrated high effectiveness. Our leaderboard is as follows: APD, PRT, Wi-DiD, AP+JSD. Although form-based approaches exhibit superior effectiveness, they fall short in cap-turing word meanings and interpreting detected se-mantic changes. In contrast, although sense-based approaches theoretically facilitate such modeling and interpretation, they obtain poor results in GCD, 4266 EN LA DE SV ES RU NO ZH Avg w                                   

> C1−C2C1−C2C1−C2C1−C2C1−C2C1−C2C2−C3C1−C3C1−C2C2−C3C1−C2Ci−Cj
> form-based  APD BERT mBERT XLM-R XL-LEXEME
> SOTA: sup .
> SOTA: uns.
> .563 .363 .444
> .886 *
> .757 .706
> -.102 .151
> .231
> -.056 .443
> .271 .398 .264
> .839 *
> .877 .731
> .270 .389 .257
> .812 *
> .754 .602
> .335 .341 .386
> .665 *
> n.a. n.a.
> .518 .368 .290
> .796 *
> .799 .372
> .482 .345 .287
> .820 *
> .833 .480
> .416 .386 .318
> .863 *
> .842 .457
> .441 .279 .195
> .659
> .757 .389
> .466 .488 .379
> .640 *
> .757 .387
> .656 .689 .500
> .731 *
> n.a. n.a.
> .449 .371 .316
> .751 *PRT BERT mBERT XLM-R XL-LEXEME
> SOTA: sup .
> SOTA: uns.
> .457 .270 .411
> .676
> .531 .467
> -.380 .424
> .506 *
> n.a. .561
> .422 .436 .369
> .824
> n.a. .755
> .158 .193 .020
> .696
> n.a. .392
> .413 .543 .505
> .632
> n.a. n.a.
> .400 .391 .321
> .704
> n.a. .294
> .374 .356 .443
> .750
> n.a. 313
> .347 .423 .405
> .727
> n.a. 313
> .507 .219 .387
> .764 *
> n.a. .378
> .444 .438 .149
> .519
> n.a. .270
> .712
> .524 .558 .699
> n.a. n.a.
> .406 .395 .381
> .693 sense-based  AP+JSD BERT mBERT XLM-R XL-LEXEME
> SOTA: sup .
> SOTA: uns.
> .289 .181 .278
> .493
> n.a. .436
> -.277
> .398
> .033
> n.a. .481
> .469 .280 .224
> .499
> n.a. .583
> - .090 .023 -.076
> .118
> n.a. .343
> .225 .067 .224
> .392
> n.a. n.a.
> .069 .017 - .068
> .106
> n.a. n.a.
> .279 .086
> .209
> .053
> n.a. n.a.
> .094 - .116
> .130
> .117
> n.a. n.a.
> .314
> .035 - .100 .297
> n.a. n.a.
> .011 - .090 .030
> .381
> n.a. n.a.
> .165 .465 .448
> .308
> n.a. n.a.
> .179 .077 .142
> .223
> WiDiD BERT mBERT XLM-R XL-LEXEME
> SOTA: sup .
> SOTA: uns.
> .385 .323 .564
> .652
> n.a. .651
> -- .039 - .064
> .236
> n.a. -.096
> .355 .312 .499
> .677
> n.a. .527
> .106 .195 .129
> .475
> n.a. .499
> .383 .343 .459
> .522
> n.a. .544
> .135 - .068
> .268
> .178
> n.a. .273
> .102 .160 .216
> .354
> n.a. .393
> .243 .142 .342
> .364
> n.a. .407
> .233 .241 .226
> .561
> n.a. n.a.
> .087 .290 .349
> .457
> n.a. n.a.
> .533 .338 .382
> .563
> n.a. n.a.
> .239 .181 .314
> .422

Table 1: Evaluation of standard approaches to GCD in terms of Spearman correlation. Top score for each approach and benchmark in bold . The top score of each benchmark is marked with an asterisk (*). We include state-of-the-art performance achieved by supervised (sup.) and unsupervised (uns.) approaches in italic . Avg is the weighted average score based on the number of targets in each benchmark. Results not available denoted as n.a. 

raising concerns about their reliability and whether they capture meaningful patterns or produce noisy aggregation. We will investigate this in Section 5. 

Supervised vs Unsupervised. We note that the use of supervision significantly improves the mod-eling of semantic change for both form- and sense-based approaches. While Cassotti et al. (2023) have previously evaluated XL-LEXEME + APD, we extend the evaluation to sense-based approaches, demonstrating that supervision enhances the per-formance of AP+JSD and WiDiD. 

Models. We note that the use of XL-LEXEME significantly improves the modeling of LSC com-pared to standard BERT, mBERT, and XLM-R. However, we observe a pattern in performance, indicating that on average, BERT performs bet-ter than mBERT, which, in turn, performs better than XLM-R for form-based approaches. This sug-gests that the use of XLM-R models is not more effective than BERT models for LSC, confirming the medium-low correlation coefficients obtained by Giulianelli et al. (2022) using XLM-R. 

Layers. As different works employ different em-bedding layers, we repeat our evaluation by con-sidering embeddings generated by each layer of BERT, mBERT, and XLM-R (see Appendix C). Our evaluation aligns with recent findings on other downstream tasks (Ma et al., 2019; Reif et al., 2019; Liang and Shi, 2023) and shows that using early layers consistently results in higher performance. For example, we note a correlation of .747 for ZH by using layer 4, compared to .656 obtained by using the last layer of BERT. On average, and in line with Periti and Dubossarsky (2023), we find that the best results for each language are obtained by leveraging embeddings from layers 8 – 10. Furthermore, since previous studies aggregated outputs from different layers, we also use aggre-gated embeddings extracted from different layers through sum and concatenation (see Appendix C). Specifically, our evaluation covers all possible layer combinations with lengths of 2 (e.g., layers 1 and 2), 3 (e.g., layers 6, 7, and 8), and 4 (e.g., lay-ers 9, 10, 11, 12). We find no improvement in aggregating the output of the last four layers for addressing GCD. By employing alternative layer combinations, we obtain higher correlation com-pared to both the last layer and the last four layers. For instance, for EN, using the sum of layers 2, 4, 5, and 8 for APD+BERT, or the concatenation of layers 4, 5, 6, and 11 for WiDiD+BERT, results in correlation of .692 and .760, respectively; com-pared to .563 (APD) and .385 (WiDiD) by using the last BERT layer. However, no combination consis-tently emerges as the optimal choice across various benchmarks or models. Instead, we observe that using a middle layer, such as layer 8, tends to be advantageous across benchmarks and models com-pared to the last layer or the aggregation of the last 4267 EN DE SV ES RU NO ZH Avg w                                                

> C1−C2C1−C2C1−C2C1−C2C1−C2C2−C3C1−C3C1−C2C2−C3C1−C2Ci−Cj
> WiC
> BERT mBERT XLM-R XL-LEXEME GPT-4.0
> Agreement
> .503 .332 .352
> .626
> .606
> .633
> .350 .344 .289
> .628
> -
> .666
> .221 .284 .255
> .631
> -
> .672
> .319 .289 .288
> .547
> -
> .531
> .314 .280 .212
> .549
> -
> .531
> .344 .273 .250
> .558
> -
> .567
> .350 .293 .251
> .564
> -
> .564
> .429 .283 .317
> .484
> -
> .761
> .406 .333 .261
> .521
> -
> .667
> .516 .413 .392
> .630
> -
> .602
> .358 .301 .272
> .568
> -
> .593
> WSI  BERT mBERT XLM-R XL-LEXEME GPT-4.0 .136 / .700 .067 / .644 .068 / .737 .273 / .834
> .340 /.877
> .047 / .662 .054 / .679 .024 / .725
> .300 /.788
> - / -.023 / .596 .024 / .648 .031 / .680
> .249 /.766
> - / -.189 / .695 .228 / .700 .164 / .755
> .400 /.820
> - / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -- / -.251 / .771 .241 / .759 .179 / .775
> .337 /.806
> - / -.247 / .758 .159 / .753 .183 / .715
> .304 /.808
> - / -.279 / .759 .172 / .713 .279 / .806
> .448 /.836
> - / -.166 / .702 .146 / .696 .133 / .743
> .339 /.810
> - / -
> GCD  BERT mBERT XLM-R XL-LEXEME GPT-4.0 .425 .120 .219 .801
> .818
> .116 .205 .069
> .799
> -.148 .234 .143
> .721
> -.284 .394 .464
> .655
> -.487 .372 .284
> .780
> -.452 .325 .301
> .824
> -.469 .408 .375
> .851
> -.571 .290 .395
> .620
> -.521 .454 .345
> .567
> -
> .808
> .737 .557 .716 -.422 .357 .324
> .754
> -

Table 2: Evaluation of contextualized models as computational annotators : Spearman correlation for WiC and GCD, Adjusted Random Index and Purity (ARI / PUR) for WSI. Top score for each approach and benchmark is highlighted in bold . Avg is a weighted average based on the number of targets in each benchmark test set. For the sake of comparison, we report the Krippendorff’s α score for inter-human annotator agreement in WiC ( italic ). 

four layers (see Figure 2 and 3). 

5 Computational annotation 

We evaluate different models on reproducing hu-man judgments (i) , the inferred word senses (ii) ,and the resulting change scores (iii) .We leverage models as annotators, hence the term computational annotator , using the same procedure employed for benchmark construc-tion (Schlechtweg, 2023; Schlechtweg et al., 2021, 2020; Schlechtweg and Schulte im Walde, 2020; Schlechtweg et al., 2018). However, we cannot evaluate LA as the benchmark was developed dif-ferently nor (ii) for the RU benchmark since no word senses were provided (Kutuzov and Pivo-varova, 2021b,c). 

5.1 (i) - Word-in-Context 

Given a benchmark, a word usage pair is associated with two contexts, c1 and c2, along with the aver-age judgment of multiple annotators (see Exam-ple A). We thus use the cosine similarity between the embeddings of w in the contexts c1 and c2 as computational proximity judgement. Our evaluation is grounded in the Word-in-Context (WiC) task (Loureiro et al., 2022; Ra-ganato et al., 2020; Pilehvar and Camacho-Collados, 2019). In contrast to the original WiC definition, our WiC evaluation aligns with the con-tinuous framework introduced by Armendariz et al. (2020) in the Graded Word Similarity in Context task. Specifically, we evaluate the quality of com-putational predictions by computing the Spearman correlation with human judgments. 

5.2 (ii) - Word Sense Induction 

We first create a DWUG using the computational annotations in Section 5.1. Then, we derive sense clusters through a variation of correlation cluster-ing (Bansal et al., 2004) on the DWUG. Our evaluation is grounded in the Word Sense Induction (WSI) task (Aksenova et al., 2022; Man-andhar et al., 2010; Agirre and Soroa, 2007). We evaluate the quality of clusters from computa-tionally annotated DWUGs against clusters from human-annotated DWUGs. Specifically, we use Adjusted Rand Index (ARI, Hubert and Arabie, 1985) and Purity (PUR, Manning, 2009) as metrics to quantify the cluster agreement. ARI compre-hensively evaluates the similarity among clustering result. However, it may yield low scores when a clustering result contains numerous small, yet coherent clusters. This does not necessarily indi-cate poor clustering quality, especially when the clusters are semantically meaningful. PUR assigns each cluster to the class that is most frequent in the cluster, measuring the accuracy of this assign-ment by counting the relative number of correctly assigned elements. 

5.3 (iii) - Graded Change Detection 

Given a word w, we split its DWUG into two sub-graphs representing nodes from the two time peri-ods (see Figure 1) and quantify the semantic change of w by computing the √JSD between the two time-specific cluster distributions. In contrast, for RU, we adhere to the RuShiftEval procedure and quantify semantic change through the application of the COMPARE metric that directly measures the 4268 mean relatedness of annotated word usage pairs as semantic change scores (Schlechtweg et al., 2018). Our evaluation is based on the GCD task and thus use Spearman correlation as evaluation metric be-tween predicted ranking and ground truth rankings. 

5.4 Evaluation results – Table 2 (i) - Word-in-Context Our evaluation reveals that pre-trained models such as BERT, mBERT, and XLM-R demonstrate a low average correlation with human judgments (.358, .301, .272). In con-trast, XL-LEXEME and GPT-4 emerge as powerful solutions for scaling up and aiding human annota-tions. For EN, they obtain a moderately strong correlation (.626, .606) with human judgments, only marginally lower than the Krippendorf α hu-man agreement (.633). In particular, XL-LEXEME slightly outperforms a considerably larger model like GPT-4 in terms of parameters, at a considerable lower cost. In contrast to previous cross-lingual evaluation (Conneau et al., 2020) and in line with the finding in Table 1, mBERT consistently outper-forms XLM-R. However, our results highlight the advantageous use of monolingual BERT models over the multilingual ones, for assessing (i) - WiC. We consider the WiC evaluation to be the most valuable as it involves a direct comparison between computational predictions and human judgments. 

(ii) - Word Sense Induction Our evaluation indi-cates that moderate performance in (i) -WiC leads to moderately low performance in inferring word sense. We obtain low ARI scores across all models and benchmarks, with XL-LEXEME and GPT-4 exhibiting the highest values. Specifically, GPT-4 outperforms XL-LEXEME (with .340 compared to .273) in ARI for EN. However, we highlight that even such low scores represent a moderately high 

result, given an inter-annotator agreement of .633. XL-LEXEME consistently demonstrates high PUR scores across all benchmarks, while other models yield slightly lower PUR scores, suggest-ing that some word sense patterns are captured when using contextualized models. Previous stud-ies highlight that contextualized models tend to produce a large number of clusters (Martinc et al., 2020b; Periti et al., 2022), thereby influencing PUR scores. Therefore, it is crucial to interpret PUR in conjunction with ARI. 

(iii) - Graded Change Detection As for GCD, we obtain average results for BERT, mBERT, XLM-R, and XL-LEXEME equal to .422, .357, .324, .754, respectively. These results are consistent with those presented in Table 1, when compared to form-based approaches (.316 – .751). We observe that employing more word usage pairs, as in Ta-ble 1, proves beneficial for certain benchmarks in the GCD tasks (e.g., XL-LEXEME+APD for EN and DE). However, we note that these results for 

(ii) - WSI are significantly higher to those obtained by sense-based approaches (.077 – .422). This can likely be attributed the fact that here we are using the same clustering algorithm that was used for ob-taining the ground truth clusters, or to the fact that the clustering algorithm is more able to capture nu-anced word meaning than AP and APP. In contrast, for RU, following the RuShiftEval procedure does not improve the performance and results between Table 1 and 2 are somewhat comparable. 

6 Concluding remarks 

We have performed a first-ever evaluation of mod-els and approaches for modeling LSC under equal settings and conditions, over eight different lan-guages. First, we evaluated different models com-bined with standard approaches to the popular GCD task. In particular, we consider BERT, mBERT, XLM-R, XL-LEXEME as pre-trained models, APD and PRT as form-based approaches, and AP+JSD and WiDiD as sense-based approaches. We find that the XL-LEXEME consistently outper-forms other models across all approaches, and thus should be used as the defacto standard. We also find that form-based approaches significantly out-perform sense-based approaches, with APD as the best approach for GCD. Among the sense-based approaches, we find that evolutionary clustering is advantageous in contrast to static clustering and should be a focus of future work. We addition-ally extended the evaluation to includes the WiC and WSI tasks, both inherently crucial to solve the complex task of LSC. We compare GPT-4 to the previous models and find that GPT-4 and XL-LEXEME both perform close to human-level while the other models obtain only low-moderate per-formance. Due to the costs associated with using GPT-4, it is not affordable to evaluate it on the re-maining languages. Since XL-LEXEME obtains results close those of GPT-4, even beating it for the WiC task, we argue that XL-LEXEME can be used for LSC tasks as a affordable, scalable solution. All in all, considering the current state of the LSC modeling, we argue that only obtaining state-4269 of-the-art performance on GCD does not solve the LSC problem , as there is a clear need to dis-tinguish the different senses of a word and how these evolve over time (Periti et al., 2023, 2022; Castano et al., 2024). GCD maintains relevance for identifying words that have changed across mul-tiple time periods in need of further sense-based 

modeling. GCD also serves to quantify the change on the level of vocabulary. In conclusion, we of-fer a first comparable evaluation of contextualized word embeddings for LSC and establish clear set-tings that should be used for future comparison and evaluation. With this work, we want to raise awareness of the current trend of the community in modeling only the GCD task. Our aim is to shift the focus from merely assessing how much to 

how (de Sá et al., 2024), when , and why , prompting the development of both unsupervised and super-vised approaches for addressing the full spectrum of LSC. 

7 Limitations 

There are limitations we had to consider in the making of this paper. Firstly, we could not evalu-ate GPT-4 across all languages due to both price and API limitations. This means that while the results are comparable with XL-LEXEME for EN, we do not know how GPT-4 will behave for the other languages. Although we are aware of open source solution such as LLaMA, our initial experi-ments, revealed that its performance does not match that of GPT-4. As LLaMA still necessitates expen-sive research infrastructure, we chose to focus only GPT-4. Our decision to use GPT-4 over the cheaper GPT-3 is based on recent studies showing conflict-ing results across different tasks. Notably, Karjus (2023) reported high scores for GPT-4 in the GCD task. However, Periti et al. (2024); Laskar et al. (2023); Koco´ n et al. (2023) reported low scores for the WiC task when employing GPT-3. As a result, we opted for GPT-4 to ensure relevance and accuracy in our evaluations. Since the instruction-tuning datasets of OpenAI models are unknown, the datasets used for eval-uation may or may not be part of the instruction-tuning training data of OpenAI. We also acknowl-edge that OpenAI continues to train and release new models, which could potentially affect the re-producibility of our results, as well as invalidate future evaluations (Balloccu et al., 2024). In this paper, we evaluate different contextual-ized models utilizing the popular Transformers li-brary for deep learning maintained by Hugging Face (Wolf et al., 2020). We specifically excluded the evaluation of a BERT model for Latin, opt-ing instead to focus on mBERT, XLM-R, and XL-LEXEME. At the beginning of our evaluation, we were not aware of any experiments using Latin BERT models to address GCD, nor were we aware of an open BERT version for Latin on the Hugging Face platform. As we have only recently become aware of novel BERT models that are exclusively trained and fine-tuned for Latin (Riemenschneider and Frank, 2023; Lendvai and Wick, 2022), we plan to further test and utilize these models in our future work. To make a fair comparison between different contextualized models, we employed the same procedure across all benchmarks and languages. However, different languages have different struc-tures and hence different requirements. It would be equally fair to have different processing of the different benchmarks (e.g., lemmatization for Ger-man, Laicher et al., 2021). We opted to reduce the number of open variables to be able to make this first evaluation. Future work could optimize each language and then compare model performance. Lastly, the models compared in this study, de-spite sharing similar architectures, tokenize text sequences differently based on their reference vo-cabulary. Consequently, a word may be split into different subtokens by one model and represented as a single token by another. Additionally, when contexts exceed the maximum input size, different models may truncate them at various points. Ad-hering to standard procedures in the field of LSC, we use the average embeddings of sub-words when a word is split into multiple sub-words. However, the impact of different truncation methods was not evaluated. 

Acknowledgments 

This work has in part been funded by the project To-wards Computational Lexical Semantic Change De-tection supported by the Swedish Research Council (2019–2022; contract 2018-01184), and in part by the research program Change is Key! supported by Riksbankens Jubileumsfond (under reference num-ber M21-0021). The computational resources were provided by the National Academic Infrastructure for Supercomputing in Sweden (NAISS), partially funded by the Swedish Research Council through 4270 grant agreement no. 2022-06725. 

References 

Eneko Agirre and Aitor Soroa. 2007. SemEval-2007 Task 02: Evaluating Word Sense Induction and Dis-crimination Systems. In Proceedings of the Fourth International Workshop on Semantic Evaluations (SemEval-2007) , pages 7–12, Prague, Czech Repub-lic. Association for Computational Linguistics. Taichi Aida and Danushka Bollegala. 2023. Swap and Predict – Predicting the Semantic Changes in Words across Corpora by Context Swapping. In Findings of the Association for Computational Linguistics: EMNLP 2023 , pages 7753–7772, Singapore. Associ-ation for Computational Linguistics. Anna Aksenova, Ekaterina Gavrishina, Elisei Rykov, and Andrey Kutuzov. 2022. RuDSI: Graph-based Word Sense Induction Dataset for Russian. In 

Proceedings of TextGraphs-16: Graph-based Meth-ods for Natural Language Processing , pages 77–88, Gyeongju, Republic of Korea. Association for Com-putational Linguistics. Carlos Santos Armendariz, Matthew Purver, Senja Pol-lak, Nikola Ljubeši´ c, Matej Ulˇ car, Ivan Vuli´ c, and Mohammad Taher Pilehvar. 2020. SemEval-2020 Task 3: Graded Word Similarity in Context. In Pro-ceedings of the Fourteenth Workshop on Semantic Evaluation , pages 36–49, Barcelona (online). Inter-national Committee for Computational Linguistics. Simone Balloccu, Patrícia Schmidtová, Mateusz Lango, and Ondrej Dusek. 2024. Leak, Cheat, Repeat: Data Contamination and Evaluation Malpractices in Closed-Source LLMs. In Proceedings of the 18th Conference of the European Chapter of the Associa-tion for Computational Linguistics (Volume 1: Long Papers) , pages 67–93, St. Julian’s, Malta. Associa-tion for Computational Linguistics. Nikhil Bansal, Avrim Blum, and Shuchi Chawla. 2004. Correlation clustering. Machine learning , 56:89– 113. Pierpaolo Basile, Annalina Caputo, Tommaso Caselli, Pierluigi Cassotti, and Rossella Varvara. 2020. DIACR-Ita@ EVALITA2020: Overview of the EVALITA2020 DiachronicLexical Semantics (DIACR-Ita) Task. In Proceedings of the Evalua-tion Campaign of Natural Language Processing and Speech Tools for Italian (EVALITA) , Online. CEUR-WS. Christin Beck. 2020. DiaSense at SemEval-2020 Task 1: Modeling Sense Change via Pre-trained BERT Embeddings. In Proceedings of the Four-teenth Workshop on Semantic Evaluation , pages 50– 58, Barcelona (online). International Committee for Computational Linguistics. Pierluigi Cassotti, Lucia Siciliani, Marco DeGemmis, Giovanni Semeraro, and Pierpaolo Basile. 2023. XL-LEXEME: WiC Pretrained Model for Cross-Lingual LEXical sEMantic changE. In Proceedings of the 61st Annual Meeting of the Association for Compu-tational Linguistics (Volume 2: Short Papers) , pages 1577–1585, Toronto, Canada. Association for Com-putational Linguistics. Silvana Castano, Alfio Ferrara, Stefano Montanelli, and Francesco Periti. 2024. Incremental Affinity Propa-gation based on Cluster Consolidation and Stratifica-tion. Jing Chen, Emmanuele Chersoni, and Chu-ren Huang. 2022. Lexicon of Changes: Towards the Evalua-tion of Diachronic Semantic Shift in Chinese. In 

Proceedings of the 3rd Workshop on Computational Approaches to Historical Language Change , pages 113–118, Dublin, Ireland. Association for Computa-tional Linguistics. Jing Chen, Emmanuele Chersoni, Dominik Schlechtweg, Jelena Prokic, and Chu-Ren Huang. 2023a. ChiWUG: A Graph-based Evaluation Dataset for Chinese Lexical Semantic Change Detection. In 

Proceedings of the 4th Workshop on Computational Approaches to Historical Language Change , pages 93–99, Singapore. Association for Computational Linguistics. Jing Chen, Emmanuele Chersoni, Dominik Schlechtweg, Jelena Prokic, and Chu-Ren Huang. 2023b. ChiWUG: A Graph-based Evaluation Dataset for Chinese Lexical Semantic Change Detection. In 

Proceedings of the 4th Workshop on Computational Approaches to Historical Language Change , pages 93–99, Singapore. Association for Computational Linguistics. Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, Francisco Guzmán, Edouard Grave, Myle Ott, Luke Zettle-moyer, and Veselin Stoyanov. 2020. Unsupervised Cross-lingual Representation Learning at Scale. In 

Proceedings of the 58th Annual Meeting of the Asso-ciation for Computational Linguistics , pages 8440– 8451, Online. Association for Computational Lin-guistics. Jader Martins Camboim de Sá, Marcos Da Silveira, and Cédric Pruski. 2024. Survey in Characterization of Semantic Change. Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Un-derstanding. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Tech-nologies, Volume 1 (Long and Short Papers) , pages 4171–4186, Minneapolis, Minnesota. Association for Computational Linguistics. 4271 Brendan J Frey and Delbert Dueck. 2007. Clustering by Passing Messages Between Data Points. science ,315(5814):972–976. Mario Giulianelli, Marco Del Tredici, and Raquel Fer-nández. 2020. Analysing Lexical Semantic Change with Contextualised Word Representations. In Pro-ceedings of the 58th Annual Meeting of the Asso-ciation for Computational Linguistics , pages 3960– 3973, Online. Association for Computational Lin-guistics. Mario Giulianelli, Andrey Kutuzov, and Lidia Pivo-varova. 2022. Do Not Fire the Linguist: Grammati-cal Profiles Help Language Models Detect Semantic Change. In Proceedings of the 3rd Workshop on Computational Approaches to Historical Language Change , pages 54–67, Dublin, Ireland. Association for Computational Linguistics. Lawrence Hubert and Phipps Arabie. 1985. Comparing Partitions. Journal of classification , 2:193–218. Vani Kanjirangat, Sandra Mitrovic, Alessandro An-tonucci, and Fabio Rinaldi. 2020. SST-BERT at SemEval-2020 Task 1: Semantic Shift Tracing by Clustering in BERT-based Embedding Spaces. In 

Proceedings of the Fourteenth Workshop on Semantic Evaluation , pages 214–221, Barcelona (online). Inter-national Committee for Computational Linguistics. Andres Karjus. 2023. Machine-assisted Mixed Meth-ods: Augmenting Humanities and Social Sciences with Artificial Intelligence. Kseniia Kashleva, Alexander Shein, Elizaveta Tukhtina, and Svetlana Vydrina. 2022. HSE at LSCDiscov-ery in Spanish: Clustering and Profiling for Lexical Semantic Change Discovery. In Proceedings of the 3rd Workshop on Computational Approaches to His-torical Language Change , pages 193–197, Dublin, Ireland. Association for Computational Linguistics. Daphna Keidar, Andreas Opedal, Zhijing Jin, and Mrin-maya Sachan. 2022. Slangvolution: A Causal Anal-ysis of Semantic Change and Frequency Dynamics in Slang. In Proceedings of the 60th Annual Meet-ing of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 1422–1442, Dublin, Ireland. Association for Computational Linguistics. Jan Koco´ n, Igor Cichecki, Oliwier Kaszyca, Mateusz Kochanek, Dominika Szydło, Joanna Baran, Julita Bielaniewicz, Marcin Gruza, Arkadiusz Janz, Kamil Kanclerz, Anna Koco´ n, Bartłomiej Koptyra, Wik-toria Mieleszczenko-Kowszewicz, Piotr Miłkowski, Marcin Oleksy, Maciej Piasecki, Łukasz Radli´ nski, Konrad Wojtasik, Stanisław Wo´ zniak, and Prze-mysław Kazienko. 2023. ChatGPT: Jack of All Trades, Master of None. Information Fusion ,99:101861. Artem Kudisov and Nikolay Arefyev. 2022. BOS at LSCDiscovery: Lexical Substitution for Interpretable Lexical Semantic Change Detection. In Proceedings of the 3rd Workshop on Computational Approaches to Historical Language Change , pages 165–172, Dublin, Ireland. Association for Computational Lin-guistics. Andrey Kutuzov and Mario Giulianelli. 2020. UiO-UvA at SemEval-2020 Task 1: Contextualised Em-beddings for Lexical Semantic Change Detection. In 

Proceedings of the Fourteenth Workshop on Semantic Evaluation , pages 126–134, Barcelona (online). Inter-national Committee for Computational Linguistics. Andrey Kutuzov, Lilja Øvrelid, Terrence Szymanski, and Erik Velldal. 2018. Diachronic Word Embed-dings and Semantic Shifts: a Survey. In Proceedings of the 27th International Conference on Computa-tional Linguistics , pages 1384–1397, Santa Fe, New Mexico, USA. Association for Computational Lin-guistics. Andrey Kutuzov and Lidia Pivovarova. 2021a. RuShiftEval. Andrey Kutuzov and Lidia Pivovarova. 2021b. RuShiftEval: A Shared Task on Semantic Shift Detec-tion for Russian. In Proceedings of the Conference on Computational Linguistics and Intellectual Tech-nologies (Dialogue) , 20, (online). RSUH. Andrey Kutuzov and Lidia Pivovarova. 2021c. Three-part Diachronic Semantic Change Dataset for Rus-sian. In Proceedings of the 2nd International Work-shop on Computational Approaches to Historical Language Change 2021 , pages 7–13, Online. As-sociation for Computational Linguistics. Andrey Kutuzov, Samia Touileb, Petter Mæhlum, Tita Enstad, and Alexandra Wittemann. 2022a. Nor-DiaChange: Diachronic Semantic Change Dataset for Norwegian. In Proceedings of the Thirteenth Lan-guage Resources and Evaluation Conference , pages 2563–2572, Marseille, France. European Language Resources Association. Andrey Kutuzov, Samia Touileb, Petter Mæhlum, Tita Ranveig Enstad, and Alexandra Wittemann. 2021. NorDiaChange. Andrey Kutuzov, Erik Velldal, and Lilja Øvrelid. 2022b. Contextualized Embeddings for Semantic Change Detection: Lessons Learned. In Northern European Journal of Language Technology, Volume 8 , Copen-hagen, Denmark. Northern European Association of Language Technology. Severin Laicher, Sinan Kurtyigit, Dominik Schlechtweg, Jonas Kuhn, and Sabine Schulte im Walde. 2021. Ex-plaining and Improving BERT Performance on Lexi-cal Semantic Change Detection. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Student Research Workshop , pages 192–202, Online. Associ-ation for Computational Linguistics. Md Tahmid Rahman Laskar, M Saiful Bari, Mizanur Rahman, Md Amran Hossen Bhuiyan, Shafiq Joty, and Jimmy Huang. 2023. A Systematic Study and 4272 Comprehensive Evaluation of ChatGPT on Bench-mark Datasets. In Findings of the Association for Computational Linguistics: ACL 2023 , pages 431– 469, Toronto, Canada. Association for Computational Linguistics. Piroska Lendvai and Claudia Wick. 2022. Finetuning Latin BERT for Word Sense Disambiguation on the Thesaurus Linguae Latinae. In Proceedings of the Workshop on Cognitive Aspects of the Lexicon , pages 37–41, Taipei, Taiwan. Association for Computa-tional Linguistics. Cheng Li, Jindong Wang, Yixuan Zhang, Kaijie Zhu, Wenxin Hou, Jianxun Lian, Fang Luo, Qiang Yang, and Xing Xie. 2023. Large Language Models Under-stand and Can be Enhanced by Emotional Stimuli. Meng Liang and Yao Shi. 2023. Named Entity Recogni-tion Method Based on BERT-whitening and Dynamic Fusion Model. In 2023 5th International Conference on Natural Language Processing (ICNLP) , pages 191–197. Jianhua Lin. 1991. Divergence Measures Based on the Shannon Entropy. IEEE Transactions on Information Theory , 37(1):145–151. Daniel Loureiro, Aminette D’Souza, Areej Nasser Muhajab, Isabella A. White, Gabriel Wong, Luis Espinosa-Anke, Leonardo Neves, Francesco Barbi-eri, and Jose Camacho-Collados. 2022. TempoWiC: An Evaluation Benchmark for Detecting Meaning Shift in Social Media. In Proceedings of the 29th International Conference on Computational Linguis-tics , pages 3353–3359, Gyeongju, Republic of Korea. International Committee on Computational Linguis-tics. Xiaofei Ma, Zhiguo Wang, Patrick Ng, Ramesh Nallap-ati, and Bing Xiang. 2019. Universal Text Represen-tation from BERT: An Empirical Study. Suresh Manandhar, Ioannis Klapaftis, Dmitriy Dligach, and Sameer Pradhan. 2010. SemEval-2010 Task 14: Word Sense Induction & Disambiguation. In Pro-ceedings of the 5th International Workshop on Se-mantic Evaluation , pages 63–68, Uppsala, Sweden. Association for Computational Linguistics. Christopher D Manning. 2009. An Introduction to Infor-mation Retrieval . Cambridge university press. Matej Martinc, Petra Kralj Novak, and Senja Pollak. 2020a. Leveraging Contextual Embeddings for De-tecting Diachronic Semantic Shift. In Proceedings of the Twelfth Language Resources and Evaluation Conference , pages 4811–4819, Marseille, France. Eu-ropean Language Resources Association. Matej Martinc, Syrielle Montariol, Elaine Zosa, and Lidia Pivovarova. 2020b. Capturing Evolution in Word Usage: Just Add More Clusters? In Compan-ion Proceedings of the Web Conference 2020 , WWW ’20, page 343–349, Taipei, Taiwan. Association for Computing Machinery. Matej Martinc, Syrielle Montariol, Elaine Zosa, and Lidia Pivovarova. 2020c. Discovery Team at SemEval-2020 Task 1: Context-sensitive Embed-dings Not Always Better than Static for Semantic Change Detection. In Proceedings of the Four-teenth Workshop on Semantic Evaluation , pages 67– 73, Barcelona (online). International Committee for Computational Linguistics. Barbara McGillivray, Dominik Schlechtweg, Haim Du-bossarsky, Nina Tahmasebi, and Simon Hengchen. 2021. DWUG LA: Diachronic Word Usage Graphs for Latin. Stefano Montanelli and Francesco Periti. 2023. A Sur-vey on Contextualised Semantic Shift Detection. Syrielle Montariol, Matej Martinc, and Lidia Pivovarova. 2021. Scalable and Interpretable Semantic Change Detection. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies , pages 4642–4652, Online. Association for Computational Linguistics. Francesco Periti and Haim Dubossarsky. 2023. The Time-Embedding Travelers@WiC-ITA. In Proceed-ings of the Eighth Evaluation Campaign of Natu-ral Language Processing and Speech Tools for Ital-ian. Final Workshop (EVALITA 2023) , Parma, Italy. CEUR.org. Francesco Periti, Haim Dubossarsky, and Nina Tah-masebi. 2024. (Chat)GPT v BERT Dawn of Justice for Semantic Change Detection. In Findings of the Association for Computational Linguistics: EACL 2024 , pages 420–436, St. Julian’s, Malta. Associa-tion for Computational Linguistics. Francesco Periti, Alfio Ferrara, Stefano Montanelli, and Martin Ruskov. 2022. What is Done is Done: an In-cremental Approach to Semantic Shift Detection. In 

Proceedings of the 3rd Workshop on Computational Approaches to Historical Language Change , pages 33–43, Dublin, Ireland. Association for Computa-tional Linguistics. Francesco Periti, Sergio Picascia, Stefano Montanelli, Alfio Ferrara, and Nina Tahmasebi. 2023. Study-ing Word Meaning Evolution through Incremental Semantic Shift Detection: A Case Study of Italian Parliamentary Speeches. Mohammad Taher Pilehvar and Jose Camacho-Collados. 2019. WiC: the Word-in-Context Dataset for Eval-uating Context-Sensitive Meaning Representations. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computa-tional Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers) , pages 1267–1273, Minneapolis, Minnesota. Association for Computa-tional Linguistics. Martin Pömsl and Roman Lyapin. 2020. CIRCE at SemEval-2020 Task 1: Ensembling Context-Free and 4273 Context-Dependent Word Representations. In Pro-ceedings of the Fourteenth Workshop on Semantic Evaluation , pages 180–186, Barcelona (online). Inter-national Committee for Computational Linguistics. Maxim Rachinskiy and Nikolay Arefyev. 2022. Gloss-Reader at LSCDiscovery: Train to Select a Proper Gloss in English – Discover Lexical Semantic Change in Spanish. In Proceedings of the 3rd Work-shop on Computational Approaches to Historical Language Change , pages 198–203, Dublin, Ireland. Association for Computational Linguistics. Alessandro Raganato, Tommaso Pasini, Jose Camacho-Collados, and Mohammad Taher Pilehvar. 2020. XL-WiC: A Multilingual Benchmark for Evaluating Se-mantic Contextualization. In Proceedings of the 2020 Conference on Empirical Methods in Natural Lan-guage Processing (EMNLP) , pages 7193–7206, On-line. Association for Computational Linguistics. Emily Reif, Ann Yuan, Martin Wattenberg, Fernanda B Viegas, Andy Coenen, Adam Pearce, and Been Kim. 2019. Visualizing and Measuring the Geometry of BERT. In Advances in Neural Information Process-ing Systems , volume 32. Curran Associates, Inc. Frederick Riemenschneider and Anette Frank. 2023. Ex-ploring Large Language Models for Classical Philol-ogy. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Vol-ume 1: Long Papers) , pages 15181–15199, Toronto, Canada. Association for Computational Linguistics. Julia Rodina, Yuliya Trofimova, Andrey Kutuzov, and Ekaterina Artemova. 2021. ELMo and BERT in Semantic Change Detection for Russian. In Analysis of Images, Social Networks and Texts , pages 175–186, Cham. Springer International Publishing. Guy D. Rosin, Ido Guy, and Kira Radinsky. 2022. Time Masking for Temporal Language Models. In Pro-ceedings of the Fifteenth ACM International Confer-ence on Web Search and Data Mining , WSDM ’22, page 833–841, Virtual Event, AZ, USA. Association for Computing Machinery. Dominik Schlechtweg. 2023. Human and Computa-tional Measurement of Lexical Semantic Change .Ph.D. thesis, University of Stuttgart. Dominik Schlechtweg, Haim Dubossarsky, Simon Hengchen, Barbara McGillivray, and Nina Tah-masebi. 2022a. DWUG EN: Diachronic Word Usage Graphs for English. Dominik Schlechtweg, Barbara McGillivray, Simon Hengchen, Haim Dubossarsky, and Nina Tahmasebi. 2020. SemEval-2020 Task 1: Unsupervised Lexical Semantic Change Detection. In Proceedings of the Fourteenth Workshop on Semantic Evaluation , pages 1–23, Barcelona (online). International Committee for Computational Linguistics. Dominik Schlechtweg, Barbara McGillivray, Simon Hengchen, Haim Dubossarsky, and Nina Tahmasebi. 2022b. DWUG DE: Diachronic Word Usage Graphs for German. Dominik Schlechtweg and Sabine Schulte im Walde. 2020. Simulating Lexical Semantic Change from Sense-Annotated Data. In Proceedings of the 13th International Conference on the Evolution of Lan-guage (EvoLang13) , Brussels, Belgium. Dominik Schlechtweg, Sabine Schulte im Walde, and Stefanie Eckmann. 2018. Diachronic Usage Relat-edness (DURel): A Framework for the Annotation of Lexical Semantic Change. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Hu-man Language Technologies, Volume 2 (Short Pa-pers) , pages 169–174, New Orleans, Louisiana. As-sociation for Computational Linguistics. Dominik Schlechtweg, Nina Tahmasebi, Simon Hengchen, Haim Dubossarsky, and Barbara McGillivray. 2021. DWUG: A large Resource of Diachronic Word Usage Graphs in Four Languages. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing , pages 7079–7091, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics. Dominik Schlechtweg, Shafqat Mumtaz Virk, and Niko-lay Arefyev. 2024. The lscd benchmark: a testbed for diachronic word meaning tasks. Dominik Schlechtweg, Shafqat Mumtaz Virk, Pauline Sander, Emma Sköldberg, Lukas Theuer Linke, Tuo Zhang, Nina Tahmasebi, Jonas Kuhn, and Sabine Schulte im Walde. 2023. The DURel Annota-tion Tool: Human and Computational Measurement of Semantic Proximity, Sense Clusters and Semantic Change. Philippa Shoemark, Farhana Ferdousi Liza, Dong Nguyen, Scott Hale, and Barbara McGillivray. 2019. Room to Glo: A Systematic Comparison of Semantic Change Detection Approaches with Word Embed-dings. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natu-ral Language Processing (EMNLP-IJCNLP) , pages 66–76, Hong Kong, China. Association for Computa-tional Linguistics. Charles Spearman. 1904. The Proof and Measurement of Association Between Two Things. American Jour-nal of Psychology , 15:88–103. Nina Tahmasebi, Lars Borin, and Adam Jatowt. 2021. 

Survey of Computational Approaches to Lexical Se-mantic Change Detection , pages 1–91. Language Science Press, Berlin. Nina Tahmasebi, Simon Hengchen, Dominik Schlechtweg, Barbara McGillivray, and Haim Dubossarsky. 2022. DWUG SV: Diachronic Word Usage Graphs for Swedish. 4274 Xuri Tang. 2018. A State-of-the-art of Semantic Change Computation. Natural Language Engineer-ing , 24(5):649–676. Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pier-ric Cistac, Tim Rault, Remi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen, Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame, Quentin Lhoest, and Alexander Rush. 2020. Transformers: State-of-the-Art Natural Language Processing. In 

Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations , pages 38–45, Online. Association for Computational Linguistics. Frank D. Zamora-Reina, Felipe Bravo-Marquez, and Dominik Schlechtweg. 2022a. Dwug es: Diachronic word usage graphs for spanish. Frank D. Zamora-Reina, Felipe Bravo-Marquez, and Dominik Schlechtweg. 2022b. LSCDiscovery: A Shared Task on Semantic Change Discovery and De-tection in Spanish. In Proceedings of the 3rd Work-shop on Computational Approaches to Historical Language Change , pages 149–164, Dublin, Ireland. Association for Computational Linguistics. Jinan Zhou and Jiaxin Li. 2020. TemporalTeller at SemEval-2020 Task 1: Unsupervised Lexical Seman-tic Change Detection with Temporal Referencing. In 

Proceedings of the Fourteenth Workshop on Semantic Evaluation , pages 222–231, Barcelona (online). Inter-national Committee for Computational Linguistics. Wei Zhou, Nina Tahmasebi, and Haim Dubossarsky. 2023. The Finer They Get: Combining Fine-Tuned Models For Better Semantic Change Detection. In 

Proceedings of the 24th Nordic Conference on Com-putational Linguistics (NoDaLiDa) , pages 518–528, Tórshavn, Faroe Islands. University of Tartu Library. 4275 Appendix A Semantic proximity 

As an example, consider the following word usage pair ⟨w, c 1, c 2⟩ extracted by the English benchmark for the word w =plane .• c1: But we are most familiar with the exhibi-tions of gravity in bodies descending inclined 

planes , as in the avalanche and the cataract. • c2: Over the next several years, he said, the Coast Guard will get 60 more people, two new 270-foot vessels and al twin-engine planes .Following the DURel relatedness scale (see Ta-ble 3), the pair is annotated with an average judg-ment of 1 by human annotators. 

x

4: Identical 3: Closely related 2: Distantly related 1: Unrelated       

> Table 3: The DURel relatedness scale used in Schlechtweg et al. (2023); Schlechtweg (2023); Schlechtweg et al. (2021, 2020); Schlechtweg and Schulte im Walde (2020); Schlechtweg et al. (2018)

B State-of-the-art for Graded Change Detection 

In Table 5, we report the current top scores for GCD in the state-of-the-art with a reference to the paper from where the result is taken. Notably, we report results for different benchmarks using four different approaches evaluated in this paper. How-ever, some benchmarks might have been assessed using other approaches that are excluded from this table. 

C Graded Change Detection across layers 

In Table 4, we report correlation scores for GCD across benchmarks. Specifically, we report results for BERT, mBERT, and XLM-R (separated by slash, i.e. “/”) by utilizing all layers of the models (1-12), individually .In Figure 2 and 3, we report correlation scores distribution for GCD obtained by using all possible layer combinations of length 2 (e.g., Layer 1 and 2), length 3 (e.g., Layer 10, 11, 12), and length 4 (e.g., Layer 1, 10, 11, 12) for BERT, mBERT, and XLM-R. For the sake of comparison, we report in Table 8 the overall top score for GCD obtained using BERT, mBERT, and XLM-R. Specifically, we present re-sults for the optimal combination and the outcome obtained by summing the last four layers, separated by a slash. Additionally, we include the standard result obtained using the last layer individually. 

D Benchmarks 

In Table 6, we report the benchmarks used in this work. Specifically, for each benchmark, we report time periods, diachronic corpus composition, num-ber of targets, and benchmark versions. 

E BERT, mBERT, XLM-R, XL-LEXEME 

In Table 7, we report the BERT, mBERT, XLM-R, and XL-LEXEME models employed in our evaluation. All the models are base versions with 12 encoder layers and can be accessed on 

huggingface.co .

F BERT, mBERT, XLM-R, XL-LEXEME 

In Table 7, we report the BERT, mBERT, XLM-R, and XL-LEXEME models employed in our evaluation. All the models are base versions with 12 encoder layers and can be accessed on 

huggingface.co .4276 G GPT-4 evaluation 

We evaluate GPT-4 as computational annotator by relying on computational proximity judgments gathered through the following method. 

Model initialization. We initialized the model with the following prompt (guideline):                       

> Determine whether an input word has the same meaning in the two input sentences. Answer with ’Same’, ’Related’, ’Linked’, or ’Distinct’. This is very important to my career.

Notably, we combine and refine two differ-ent prompts used in previous works. We drew inspiration from the prompt utilized by Karjus (2023) to assess GPT-4 in addressing the Graded Change Detection task. Additionally, we drew inspiration from the prompt utilized by Li et al. (2023), called EmotionPrompt , which combines the original prompt with emotional stimuli to enhance the performance of Large Language Models. 

Model template. For each word usage pair, we used the following prompt:                               

> Determine whether [Target word] has the same meaning in the following sentences. Do they refer to roughly the Same, different but closely Related, distant/figuratively Linked or unrelated Distinct word meanings?
> Sentence 1: [Context 1]
> Sentence 2: [Context 2]

Notably, drawing inspiration from the Ope-nAI documentation 7 and the prompts utilized in previous work for the Word-in-Context task (Ko-co´ n et al., 2023; Laskar et al., 2023), we structured our prompt in a format that facilitates parsing and comprehension. For each usage pair ⟨w, c 1, c 2⟩ of a word w, we substitute [Target word] with the actual target w and [Context 1] and [Context 2] with c1 and c2, respectively. We prompt GPT-4 without providing any mes-sage history. This means that, for each usage pair 

⟨w, c 1, c 2⟩, we re-initialize the model with the ini-tial prompt (guideline) and subsequently prompt 

> 7platform.openai.com/docs/guides/ prompt-engineering

the model to gather a semantic proximity judgment for the pair ⟨w, c 1, c 2⟩. This approach ensures that the model relies solely on its pre-trained knowl-edge, preventing potential biases stemming from previously prompted pairs. 4277 EN LA DE SV ES RU NO ZH Avg w

C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C2 − C3 C1 − C3 C1 − C2 C2 − C3 C1 − C2 Ci − Cj

> form-based

APD 12345678910 11 12 .358 / .278 / .064 .464 / .346 / .229 .574 / .389 / .314 .628 / .410 / .400 

.684 / .412 / .452 .667 / .395 / .438 .614 / .419 / .395 .642 / .408 / .426 .600 / .406 / .460 .530 / .348 / .511 .554 / .305 / .548 

.563 / .363 / .444 - / .153 / .073 - / .119 / .006 - / .047 / -.025 - / .022 / -.010 - / -.028 / .043 - / -.005 / .061 - / -.009 / .073 - / .023 / .043 - / .044 / -.047 - / .008 / -.082 - / .023 / -.069 - / .102 / .151 

.144 / .218 / .270 .155 / .208 / .319 .164 / .232 / .301 .176 / .241 / .326 .237 / .344 / .414 .309 / .397 / .471 .335 / .434 / .471 .389 / .481 / .474 

.427 / .423 / .479 

.354 / .333 / .433 .275 / .315 / .409 .271 / .398 / .264 .213 / .132 / .134 .255 / .129 / .234 .295 / .189 / .289 .307 / .254 / .286 

.305 / .321 / .351 .242 / .352 / .424 .237 / .404 / .441 .248 / .455 / .456 .250 / .463 / .468 .275 / .414 / .497 .267 / .309 / .500 

.270 / .389 / .257 .167 / .104 / .003 .255 / .164 / .076 .307 / .212 / .139 .394 / .276 / .184 .450 / .345 / .279 .468 / .361 / .277 

.479 / .364 / .280 .438 / .430 / .297 .399 / .413 / .352 .282 / .331 / .407 .257 / .265 / .444 

.335 / .341 / .386 .335 / .204 / .258 .374 / .198 / .245 .427 / .215 / .238 .492 / .257 / .287 .519 / .295 / .374 .516 / .338 / .438 .549 / .402 / .439 .566 / .427 / .430 .539 / .382 / .401 .515 / .362 / .369 .439 / .333 / .361 .518 / .368 / .290 .281 / .204 / .308 .309 / .188 / .283 .370 / .218 / .292 .427 / .247 / .346 .465 / .275 / .453 .463 / .305 / .503 .495 / .379 / .473 

.495 / .400 / .466 .479 / .364 / .419 .461 / .313 / .405 .393 / .256 / .394 .482 / .345 / .287 .261 / .214 / .253 .303 / .218 / .236 .360 / .242 / .241 .431 / .280 / .288 .456 / .318 / .373 .467 / .347 / .432 

.523 / .429 / .430 .531 / .451 / .427 

.534 / .405 / .404 .523 / .379 / .402 .461 / .330 / .401 .476 / .386 / .318 .160 / .143 / .145 .199 / .155 / .153 .290 / .170 / .171 .364 / .168 / .143 .396 / .192 / .165 .400 / .180 / .172 .429 / .262 / .191 .416 / .291 / .197 .429 / .257 / .190 .418 / .226 / .191 .378 / .196 / .215 .441 / .279 / .195 .234 / .219 / .203 .288 / .213 / .235 .371 / .223 / .243 .463 / .322 / .264 .497 / .364 / .330 .532 / .374 / .367 

.547 / .437 / .375 .529 / .499 / .373 .525 / .462 / .394 .531 / .425 / .411 .530 / .403 / .432 

.466 / .488 / .379 .340 / -.100 / -.222 .540 / .263 / .338 .594 / .464 / .540 

.747 / .613 / .615 .720 / .662 / .600 .667 / .661 / .629 .645 / .725 / .618 .654 / .715 / .638 .667 / .670 / .646 

.625 / .656 / .613 .604 / .628 / .601 .656 / .689 / .500 .255 / .171 / .166 .312 / .198 / .216 .371 / .232 / .244 .438 / .275 / .284 .471 / .315 / .36 .473 / .338 / .398 

.494 / .390 / .393 

.497 / .421 / .396 .486 / .391 / .388 .450 / .346 / .387 .405 / .303 / .392 .449 / .371 / .316 PRT 12345678910 11 12 .295 / .195 / .221 .409 / .271 / .382 .436 / .295 / .453 .467 / .290 / .487 .494 / .315 / .476 .516 / .353 / .447 .529 / .383 / .462 .539 / .383 / .464 

.549 / .358 / .437 .511 / .355 / .481 .452 / .342 / .501 

.457 / .270 / .411 - / .289 / .303 - / .286 / .263 - / .277 / .271 - / .255 / .297 - / .232 / .322 - / .257 / .350 - / .304 / .349 - / .292 / .359 - / .311 / .319 - / .280 / .329 - / .298 / .308 - / .380 / .424 

.133 / .162 / .122 .217 / .198 / .125 .267 / .230 / .141 .297 / .285 / .204 .343 / .384 / .294 .379 / .421 / .357 .400 / .437 / .385 .398 / .468 / .402 .390 / .469 / .477 .380 / .454 / .486 .412 / .430 / .507 .422 / .436 / .369 .215 / .001 / .045 .274 / .006 / .066 

.301 / .012 / .078 .280 / .017 / .087 .233 / .060 / .129 .206 / .082 / .171 .178 / .008 / .184 .197 / .081 / .196 .201 / .096 / .247 .193 / .133 / .223 .169 / .076 / .245 

.158 / .193 / .020 .303 / .295 / .190 .407 / .397 / .328 .438 / .424 / .364 .455 / .446 / .388 .455 / .495 / .439 .451 / .524 / .449 .466 / .498 / .453 .453 / .514 / .463 

.476 / .501 / .503 .417 / .482 / .538 .422 / .489 / .540 

.413 / .543 / .505 .263 / .271 / .220 .304 / .279 / .216 .338 / .311 / .203 .398 / .329 / .246 .399 / .364 / .323 .391 / .359 / .365 

.411 / .379 / .358 .404 / .393 / .375 .375 / .353 / .382 .349 / .376 / .409 .319 / .344 / .412 

.400 / .391 / .321 .206 / .149 / .305 .261 / .139 / .352 .305 / .191 / .405 .346 / .235 / .433 .395 / .327 / .509 .390 / .374 / .519 

.426 / .447 / .510 .410 / .421 / .531 

.402 / .404 / .471 .379 / .382 / .447 .317 / .335 / .439 .374 / .356 / .443 .159 / .169 / .144 .196 / .161 / .153 .251 / .195 / .162 .306 / .250 / .234 .331 / .313 / .323 .331 / .365 / .384 

.380 / .413 / .384 

.380 / .411 / .396 .353 / .384 / .401 .335 / .366 / .431 .303 / .321 / .438 

.347 / .423 / .405 .032 / -.005 / .028 .122 / -.020 / .092 .250 / .042 / .111 .378 / .019 / .102 .440 / .096 / .137 .449 / .104 / .181 

.511 / .161 / .192 .449 / .227 / .292 .481 / .243 / .351 .482 / .212 / .373 .448 / .197 / .360 .507 / .219 / .387 

.161 / .168 / .039 .349 / .215 / -.020 .365 / .294 / .005 .408 / .303 / .075 .466 / .367 / .189 .471 / .330 / .232 .501 / .371 / .236 .493 / .389 / .246 

.485 / .380 / .239 .481 / .398 / .263 

.503 / .365 / .214 .444 / .438 / .149 .383 / .017 / -.139 .582 / .192 / .140 .676 / .397 / .424 .691 / .525 / .544 .651 / .551 / .531 .637 / .556 / .475 .641 / .613 / .549 .664 / .619 / .575 .671 / .606 / .646 

.626 / .583 / .619 .602 / .550 / .620 

.712 / .524 / .558 .220 / .178 / .165 .302 / .209 / .216 .348 / .253 / .253 .389 / .283 / .296 .408 / .337 / .357 .408 / .362 / .383 

.433 / .389 / .390 .426 / .400 / .409 .422 / .385 / .418 .396 / .378 / .431 .371 / .350 / .432 

.406 / .395 / .381 

> sense-based

AP 12345678910 11 12 .129 / .220 / .032 .288 / .079 / -.128 .267 / .161 / .016 .353 / .330 / .087 

.432 / .221 / .322 .431 / .208 / .330 .144 / .362 / .321 .228 / .418 / .175 .424 / .357 / .311 .233 / .317 / .289 .148 / .338 / .374 

.289 / .181 / .278 - / -.011 / .409 

- / .008 / .215 - / -.012 / .218 - / -.106 / .253 - / -.024 / .281 - / -.000 / .286 - / -.044 / .233 - / -.101 / .260 - / .120 / .153 - / .124 / .381 - / .132 / .266 - / .277 / .398 -.108 / -.087 / -.040 .113 / -.131 / -.017 .007 / -.043 / .120 -.041 / .088 / .054 .143 / .235 / .196 .243 / .372 / .280 .284 / .443 / .387 .417 / .353 / .393 .339 / .322 / .361 .393 / .328 / .334 .465 / .275 / .435 .469 / .280 / .224 -.121 / -.021 / -.244 -.138 / -.141 / -.244 -.201 / -.117 / -.177 -.213 / -.131 / -.172 -.015 / -.083 / -.125 -.129 / -.040 / -.070 -.070 / -.031 / -.155 

.124 / .114 / -.082 .054 / .010 / -.195 -.023 / .061 / -.210 -.057 / .175 / .133 

-.090 / .023 / -.076 .168 / .233 / .172 .104 / .109 / .140 .161 / .142 / .063 .263 / .195 / .266 

.247 / .319 / .162 .363 / .251 / .002 

.406 / .301 / .216 .384 / .401 / .031 .270 / .296 / .157 .294 / .201 / .151 .351 / .310 / .039 .225 / .067 / .224 .050 / -.001 / -.154 -.127 / -.154 / -.036 -.006 / .007 / -.019 .093 / -.159 / -.042 .072 / -.085 / -.035 -.049 / -.111 / -.094 .082 / -.069 / .067 

.058 / -.014 / -.073 .038 / .013 / -.081 

.126 / .108 / .044 -.004 / .034 / -.069 .069 / .017 / -.068 .132 / .108 / .060 .038 / .110 / .073 -.002 / .058 / .129 .045 / .096 / .104 .169 / .014 / .140 .173 / .093 / .176 .288 / .235 / .084 .128 / .230 / .211 .072 / .149 / .232 .116 / .169 / .240 .068 / .141 / .279 .279 / .086 / .209 .098 / -.143 / .023 .096 / -.109 / -.025 .027 / -.130 / -.020 .168 / -.076 / .050 .081 / -.019 / .025 .091 / .035 / .291 

.190 / .158 / .131 .088 / .137 / .228 .098 / .055 / .011 .187 / .082 / .194 .157 / .113 / .262 

.094 / -.116 / .130 -.104 / -.237 / -.019 .031 / -.230 / -.025 -.118 / .016 / -.060 -.281 / -.123 / -.016 -.318 / -.027 / .033 -.192 / -.076 / .031 -.257 / -.114 / -.051 -.165 / -.114 / -.109 -.016 / .005 / .045 

.151 / -.127 / -.041 .021 / -.232 / -.211 

.314 / .035 / -.100 -.048 / .021 / -.239 -.039 / .104 / .028 -.051 / -.011 / .124 .257 / -.282 / .020 .323 / .143 / .149 

.440 / .206 / .131 .115 / .140 / -.130 -.029 / .469 / .256 

.092 / .198 / .031 .168 / .271 / .101 .090 / .146 / .062 .011 / -.090 / .030 .118 / -.179 / .110 .301 / -.058 / -.048 .189 / .221 / -.143 .360 / .322 / -.047 .251 / .689 / .343 

.458 / .342 / .280 .292 / .226 / .344 .113 / .231 / .045 .423 / .404 / .245 .430 / .291 / .436 .322 / .223 / .243 .165 / .465 / .448 

.060 / .011 / .012 .052 / -.030 / .006 .033 / .021 / .028 .113 / .014 / .064 .140 / .097 / .112 .166 / .099 / .132 .183 / .153 / .131 .148 / .192 / .117 .157 / .158 / .104 

.197 / .158 / .169 

.151 / .151 / .158 .179 / .077 / .142 WiDiD 12345678910 11 12 .253 / .301 / .278 .434 / .261 / .065 .423 / .268 / .147 

.611 / .228 / .448 .527 / .078 / .393 .458 / .250 / .625 

.305 / .328 / .475 .449 / .312 / .411 .544 / .509 / .567 .396 / .301 / .587 .299 / .218 / .627 

.385 / .323 / .564 - / .028 / -.048 - / .018 / -.130 - / .026 / .019 - / .030 / .108 - / -.020 / -.037 - / -.030 / -.050 - / .139 / .106 - / .091 / .038 - / -.066 / .104 - / -.024 / .187 

- / -.064 / -.111 - / -.039 / -.064 .147 / .204 / .219 .106 / .143 / .292 .115 / .120 / .474 .126 / .067 / .424 .190 / .173 / .509 

.293 / .294 / .433 .235 / .253 / .514 .344 / .341 / .565 .353 / .299 / .573 .315 / .407 / .477 .258 / .381 / .486 

.355 / .312 / .499 .120 / .052 / -.062 -.041 / .015 / -.118 .198 / .029 / .106 .176 / -.130 / .312 .151 / -.074 / .300 .211 / .148 / .335 

.295 / .198 / .414 

.071 / .354 / .321 .184 / .319 / .203 .145 / .233 / .148 .172 / .128 / .343 .106 / .195 / .129 .132 / .051 / -.015 .103 / .105 / .110 .228 / .108 / .118 .292 / .175 / .221 .356 / .295 / .310 .382 / .387 / .346 .382 / .318 / .324 .340 / .371 / .395 .324 / .450 / .372 .306 / .388 / .471 .424 / .432 / .464 .383 / .343 / .459 .159 / .047 / .125 .209 / -.046 / .274 

.251 / -.073 / .345 

.091 / -.039 / .332 -.034 / .023 / .259 .094 / .063 / .184 .017 / .032 / .292 .000 / -.008 / .105 -.002 / .075 / .108 .011 / .087 / .270 .134 / .152 / .220 .135 / -.068 / .268 .108 / .073 / .197 .076 / .180 / .060 .091 / .113 / .184 .010 / .041 / .307 .071 / .076 / .314 .141 / .066 / .210 .203 / .285 / .152 .284 / .260 / .243 .083 / .076 / .171 

.302 / .090 / .308 .234 / .120 / .334 

.102 / .160 / .216 .090 / -.036 / .051 .212 / -.038 / -.008 .233 / .077 / .153 .157 / -.053 / .059 .205 / .137 / .202 .182 / .288 / .264 .216 / .188 / .458 

.025 / .203 / .267 .205 / .205 / .388 .060 / .172 / .328 .185 / .087 / .312 

.243 / .142 / .342 .356 / .150 / .090 .285 / -.030 / .085 .229 / -.102 / .074 .242 / .038 / .002 

.297 / .100 / .023 .261 / -.080 / .215 .244 / .119 / .247 .221 / .226 / .262 .183 / .063 / .174 .155 / .179 / .234 .218 / .195 / .345 

.233 / .241 / .226 .120 / .127 / .154 .161 / .103 / .214 .239 / .064 / .204 .340 / .152 / .062 .380 / .156 / .316 .428 / .295 / .102 .397 / .195 / -.034 .449 / .428 / .155 .390 / .118 / .149 

.488 / .175 / .275 .296 / .291 / .438 

.087 / .290 / .349 .122 / .026 / .160 .371 / -.013 / .063 .256 / .114 / .349 .388 / .279 / .417 

.524 / .193 / .217 .446 / .271 / .335 .338 / .298 / .293 .475 / .325 / .286 .404 / .347 / .328 .428 / .355 / .383 

.539 / .277 / .372 .533 / .338 / .382 .146 / .074 / .103 .175 / .060 / .094 .216 / .065 / .203 .200 / .054 / .244 .218 / .112 / .265 .252 / .185 / .269 .237 / .211 / .304 .224 / .242 / .271 .222 / .212 / .280 .224 / .204 / .339 

.260 / .199 / .345 

.239 / .181 / .314 

Table 4: Comprehensive evaluation of standard approaches to GCD by using the layers 1-12 of BERT / mBERT / XLM-R . Top score for each approach, model, and benchmark in bold . Avg is the weighted average score based on the number of targets in each benchmark. 4278 EN LA DE SV ES RU NO ZH 

C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C2 − C3 C1 − C3 C1 − C2 C2 − C3 C1 − C2

> form-based
> APD

XL-L. : .757 Cassotti et al. BERT: .706 Zhou et al. XL-L. : -.056 Cassotti et al. mBERT: .443 Pömsl and Lyapin XL-L. : .877 Cassotti et al. BERT: .731 Laicher et al. XL-L. .754 Cassotti et al. BERT: .602 Laicher et al. n.a. n.a. XL-L. : .799 Cassotti et al. XLM-R: .372 Giulianelli et al. XL-L. : .833 Cassotti et al. XLM-R: .480 Giulianelli et al. XL-L. : .842 Cassotti et al. XLM-R: .457 Giulianelli et al. XL-L. : .757 Cassotti et al. XLM-R: .389 Giulianelli et al. XL-L. : .757 Cassotti et al. XLM-R: .387 Giulianelli et al. n.a. n.a. PRT  BERT: .531 Zhou et al. BERT: .467 Rosin et al. n.a. mBERT: .561 Kutuzov and Giulianelli n.a. BERT: .755 Laicher et al. n.a. BERT: .392 Zhou and Li n.a. n.a. n.a. XLM-R: .294 Giulianelli et al. n.a. XLM-R: .313 Giulianelli et al. n.a. XLM-R: .313 Giulianelli et al. n.a. XLM-R: .378 Giulianelli et al. n.a. XLM-R: .270 Giulianelli et al. n.a. n.a. 

> sense-based
> AP+JSD

n.a. BERT: .436 Martinc et al. n.a. mBERT: .481 Martinc et al. n.a. BERT: .583 Montariol et al. n.a. BERT: .343 Martinc et al. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. n.a. 

> WiDiD

n.a. BERT: .651 Periti et al. n.a. XLM-R: - .096 Periti et al. n.a. XLM-R: .527 Periti et al. n.a. XLM-R: .499 Periti et al. n.a. BERT: .544 Periti et al. n.a. mBERT: .273 Periti et al. n.a. mBERT: .393 Periti et al. n.a. mBERT: .407 Periti et al. n.a. n.a. n.a. n.a. n.a. n.a. 

Table 5: State-of-the-art performance for GCD : Top Spearman correlations obtained across benchmarks by form-and sense-based approaches. For each approach, we report correlation for both supervised (above the line) and 

unsupervised (below the line) settings. 

EN LA DE SV ES RU NO ZH 

C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C2 − C3 C1 − C3 C1 − C2 C2 − C3 C1 − C2

Time periods 

C1: 1810 – 1860 

C2: 1960 – 2010 

C1: 200 – 0 

C2: 0 – 2000 

C1: 1800 – 1899 

C2: 1946 – 1990 

C1: 1790 – 1830 

C2: 1895 – 1903 

C1: 1810 – 1906 

C2: 1994 – 2020 

C1: 1700 – 1916 

C2: 1918 – 1990 

C2: 1918 – 1990 

C3: 1992 –2016 

C1: 1700 – 1916 

C3: 1992 –2016 

C1: 1929 –1965 

C2: 1970 – 2013 

C1: 1980 – 1990 

C2: 2012 – 2019 

C1: 1954 – 1978 

C2: 1979 – 2003 Diachronic Corpus 

C1: CCOHA 

C2: CCOHA 

C1: LatinISE 

C2: LatinISE 

C1: DTA 

C2: BZ+ND 

C1: Kubhist 

C2: Kubhist 

C1: PG 

C2: TED2013, NC MultiUN Europarl 

C1: RNC 

C2: RNC 

C3: RNC 

C1: RNC 

C2: RNC 

C3: RNC 

C1: RNC 

C2: RNC 

C3: RNC 

C1: NBdigital 

C2: NBdigital 

C1: NBdigital 

C2: NAK 

C1: People’s Daily 

C2: People’s Daily # targets 46 40 50 44 100 111 111 111 40 40 40 Benchmark version version 2.0.1 Schlechtweg et al. version 1 McGillivray et al. version 2.3.0 Schlechtweg et al. version 2.0.1 Tahmasebi et al. version 4.0.0 Zamora-Reina et al. version 1 Kutuzov and Pivovarova version 1 Kutuzov et al. version 1 Chen et al. 

Table 6: LSC benchmark for Graded Change Detection . Overview of time periods, diachronic corpus composi-tion, number of targets, and benchmark versions used in this study. 

BERT mBERT XLM-R XL-LEXEME English bert-base-uncased bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Latin - bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

German bert-base-german-cased bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Swedish af-ai-center/bert-base-swedish-uncased bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Spanish dccuchile/bert-base-spanish-wwm-uncased bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Russian DeepPavlov/rubert-base-cased bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Norwegian NbAiLab/nb-bert-base bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Chinese bert-base-chinese bert-base-multilingual-cased xlm-roberta-base pierluigic/xl-lexeme 

Table 7: BERT, mBERT, XLM-R, and XL-LEXEME models employed in our evaluation. All models are available at huggingface.co .4279 Figure 2: Score distribution for GCD obtained by using all possible layer combinations of length 2 (e.g., Layer 1 and 2), length 3 (e.g., Layer 10, 11, 12), and length 4 (e.g., Layer 1, 10, 11, 12) for BERT, mBERT, and XLM-R. The y-axis represents the Spearman correlation. We highlight the performance for GCD obtained using Layer 8, Layer 12, and the sum of the last 4 layers (i.e., ⊕ 9-12). 4280 Figure 3: Score distribution for GCD obtained by using all possible layer combinations of length 2 (e.g., Layer 1 and 2), length 3 (e.g., Layer 10, 11, 12), and length 4 (e.g., Layer 1, 10, 11, 12) for BERT, mBERT, and XLM-R. The y-axis represents the Spearman correlation. We highlight the performance for GCD obtained using Layer 8, Layer 12, and the sum of the last 4 layers (i.e., ⊕ 9-12). 4281 ]

EN LA DE SV ES RU NO ZH 

C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C1 − C2 C2 − C3 C1 − C3 C1 − C2 C2 − C3 C1 − C2

> form-based

APD BERT mBERT XLM-R 

.692 / .566 (.563) 

.466 / .365 (.363) 

.579 / .518 (.444) 

/.136 / .034 (.102) 

.080 / -.072 (.151) 

.412 / .349 (.271) 

.468 / .370 (.398) 

.496 / .438 (.264) 

.325 / .272 (.270) 

.486 / .398 (.389) 

.496 / .496 (.257) 

.488 / .310 (.335) 

.423 / .351 (.341) 

.443 / .398 (.386) 

.573 / .537 (.518) 

.419 / .365 (.368) 

.441 / .368 (.290) 

.506 / .477 (.482) 

.393 / .324 (.345) 

.491 / .404 (.287) 

.546 / .522 (.476) 

.443 / .386 (.386) 

.432 / .397 (.318) 

.463 / .457 (.441) 

.320 / .248 (.279) 

.215 / .180 (.195) 

.556 / .521 (.466) 

.496 / .429 (.488) 

.421 / .418 (.379) 

.760 / .658 (.656) 

.739 / .674 (.689) 

.675 / .627 (.500) 

PRT BERT mBERT XLM-R 

.550 / .520 (.457) 

.382 / .339 (.270) 

.513 / .476 (.411) 

/.352 / .305 (.380) 

.365 / .312 (.424) 

.421 / .397 (.422) 

.467 / .454 (.436) 

.497 / .486 (.369) 

.293 / .170 (.158) 

.132 / .105 (.193) 

.253 / .236 (.020) 

.478 / .441 (.413) 

.555 / .514 (.543) 

.538 / .522 (.505) 

.425 / .368 (.400) 

.411 / .373 (.391) 

.409 / .402 (.320) 

.418 / .374 (.374) 

.442 / .386 (.356) 

.530 / .453 (.443) 

.383 / .346 (.347) 

.434 / .367 (.423) 

.449 / .435 (.405) 

.538 / .513 (.507) 

.256 / .228 (.219) 

.384 / .384 (.387) 

.513 / .481 (.444) 

.432 / .405 (.438) 

.270 / .220 (.149) 

.706 / .649 (.712 )

.648 / .588 (.524) 

.642 / .627 (.558) 

> sense-based

AP BERT mBERT XLM-R .464 / .245 (.289) 

.501 / .313 (.181) 

.473 / .340 (.278) 

/.326 / .179 (.277) 

.482 / .398 (.398) 

.520 / .435 (.469) 

.428 / .329 (.280) 

.502 / .370 (.224) 

.201 / -.061 (-.090) 

.193 / .090 (.023) 

.235 / .022 (-.076) 

.499 / .295 (.225) 

.484 / .259 (.067) 

.307 / .170 (.224) 

.292 / .149 (.069) 

.209 / .123 (.017) 

.162 / .012 (-.068) 

.418 / .216 (.279) 

.316 / .175 (.086) 

.378 / .247 (.209) 

.386 / .207 (.094) 

.247 / .058 (-.116) 

.358 / .224 (.130) 

.329 / .028 (.314) 

.194 / -.105 (.035) 

.322 / .132 (-.100) 

.466 / .227 (.011) 

.539 / .275 (-.090) 

.465 / .035 (.030) 

.671 / .587 (.165) 

.645 / .256 (465) 

.583 / .135 (.448) 

WiDiD BERT mBERT XLM-R .635 / .441 (.385) 

.600 / .317 (.323) 

.760 / .663 (.564) 

/.252 / .055 (-.039) 

.347 / -.077 (-.064) 

.465 / .322 (.355) 

.610 / .422 (.312) 

.721 / .557 (.499) 

.432 / .177 (.106) 

.521 / .413 (.195) 

.503 / .220 (.129) 

.466 / .361 (.383) 

.575 / .272 (.343) 

.526 / .437 (.459) 

.388 / .136 (.135) 

.255 / .215 (-.068) 

.426 / .223 (.268) 

.410 / .190 (.102) 

.373 / .056 (.160) 

.460 / .352 (.216) 

.408 / .280 (.243) 

.327 / .252 (.142) 

.485 / .304 (.342) 

.531 / .160 (.233) 

.500 / .459 (.241) 

.505 / .399 (.226) 

.578 / .336 (.087) 

.467 / .292 (.290) 

.440 / .336 (.349) 

.701 / .537 (.533) 

.620 / .513 (.338) 

.637 / .349 (.382) 

Table 8: Top score for GCD obtained using BERT, mBERT, and XLM-R. We present results for the optimal combination and the outcome obtained by summing the last four layers, separated by a slash (i.e., best results / sum of last four layers). Additionally, for comparison purposes, we include the result obtained using the last layer individually 

(enclosed in brackets). . Top scores for approach and benchmark are highlighted in bold .4282