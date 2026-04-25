# Source: https://www.bioinf.jku.at/publications/older/2604.pdf
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 3205
# Author: Hochreiter and Schmidhuber
# Author Slug: sepp-hochreiter
on the analysis of transcriptional regulation
using epigenomic and transcriptomic data
A dissertation submitted towards the degree
Doctor of Natural Science
of the Faculty of Mathematics and Computer Science
of Saarland University
by
Florian Schmidt
Saarbrücken, April 2019

…

Abstract
The integrative analysis of epigenomics and transcriptomics data is an active re-
search field in Bioinformatics. New methods are required to interpret and process
large omics data sets, as generated within consortia such as the International Human
Epigenomics Consortium. In this thesis, we present several approaches illustrating
how combined epigenomics and transcriptomics datasets, e.g.
for differential or
time series analysis, can be used to derive new biological insights on transcriptional
regulation. In this work we focus on regulatory proteins called transcription factors
(TFs), which are essential for orchestrating cellular processes.
In our novel approaches, we combine epigenomics data, such as DNaseI-seq, pre-
dicted TF binding scores and gene-expression measurements in interpretable ma-
chine learning models.
In joint work with our collaborators within and outside
IHEC, we have shown that our methods lead to biological meaningful results, which
could be validated with wet-lab experiments.
Aside from providing the community with new tools to perform integrative anal-
ysis of epigenomics and transcriptomics data, we have studied the characteristics
of chromatin accessibility data and its relation to gene-expression in detail to bet-
ter understand the implications of both computational processing and of different
experimental methods on data interpretation.
Overall, we provide easy to use tools to enable researchers to benefit from the era
of Biological Data Science.
vii

…

faktoren konzentriert. Dies sind Proteine, die essentiell für die Steuerung regula-
torischer Prozesse in der Zelle sind. In unseren neuen Methoden kombinieren wir
epigenetische Daten, zum Beispiel DNaseI-seq oder ATAC-seq Daten, vorhergesagte
Transkriptionsfaktorbindestellen und Genexpressionsdaten in interpretierbaren Mod-

…

Contents
1
Introduction
1
2
Background
7
2.1
Biological Background . . . . . . . . . . . . . . . . . . . . . . . . . .
7
2.1.1
DNA, RNA, Proteins and the definition of genes
. . . . . . .
7
2.1.2
The genetic code and DNA sequence alterations . . . . . . . .
11
2.1.3
The central dogma of molecular biology
. . . . . . . . . . . .
12
2.1.4

…

14
2.1.6
An introduction to DNA sequencing . . . . . . . . . . . . . .
15
2.1.7
Experimental methods to measure gene-expression . . . . . .
17
2.1.8
Chromatin organization . . . . . . . . . . . . . . . . . . . . .
19
2.1.9
Epigenetic modifications . . . . . . . . . . . . . . . . . . . . .
22
2.1.10 Experimental Methods used to characterize the chromatin ac-
cessibility landscape of a cell
. . . . . . . . . . . . . . . . . .

…

31
2.1.13 Enhancers and repressors
. . . . . . . . . . . . . . . . . . . .
34
2.1.14 CRISPR/Cas9 and viability screens
. . . . . . . . . . . . . .
35
2.1.15 Looking beyond transcriptional regulation through TFs
. . .
36
2.2
Mathematical and Computational Background . . . . . . . . . . . . .
38
2.2.1
Regression . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

…

52
2.2.8
An introduction to minimum description length . . . . . . . .
54
2.3
International efforts to characterize the (epi)genome of primary cells
and cell types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
3
Inferring key TFs from epigenetics and gene-expression data
57
3.1
Predicting TF binding in silico
. . . . . . . . . . . . . . . . . . . . .
57
xi

…

60
3.1.3
Transcription Factor Affinity Prediction (TRAP) . . . . . . .
60
3.1.4
Differences between TF ChIP-seq data and predicted TFBS .
62
3.1.5
Other computational approaches utilising PWMs . . . . . . .
63
3.1.6
Epigenetic priors to compute TFBS predictions . . . . . . . .
67
3.1.7
Protein Interaction Quantification (PIQ) . . . . . . . . . . . .
68
3.2
TEPIC for fast and accurate TFBS prediction . . . . . . . . . . . . .

…

70
3.3
Aggregating genome-wide TFBS to the gene level with TEPIC
. . .
73
3.3.1
Common strategies to aggregate TFBS predictions to the
gene-level . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
73
3.3.2
Computation of TF-gene scores in TEPIC . . . . . . . . . . .
74
3.4
Gene-expression modelling using TF-gene scores . . . . . . . . . . . .
77
3.4.1
Statistical model . . . . . . . . . . . . . . . . . . . . . . . . .
78
3.4.2
Model performance and evaluation . . . . . . . . . . . . . . .
79
3.4.3
Robustness of TF-gene scores derived from ChIP-seq and pre-
dicted TFBS in gene-expression models
. . . . . . . . . . . .
90
3.4.4
Linear models suggest expressed and known transcriptional
regulators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 101
3.4.5
Integration of conformation capture data into TF-gene scores 104
3.5
INVOKE - A pipeline for integrative analysis of TFBS prediction
and gene-expression data . . . . . . . . . . . . . . . . . . . . . . . . . 115
3.5.1
Motivation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . 115

…

4.2.2
A differential TF-gene score . . . . . . . . . . . . . . . . . . . 122
4.2.3
Logistic regression to classify genes as up- or down-regulated
123
4.2.4
Availability and Usability of DYNAMITE . . . . . . . . . . . 124
xii
Contents
4.2.5
Required input . . . . . . . . . . . . . . . . . . . . . . . . . . 124
4.2.6
Output and model interpretation . . . . . . . . . . . . . . . . 125

…

Contributions of all researchers involved in the described project
. . 130
5
EPIC-DREM - Identification of key regulators from time-series
data
133
5.1
Project description . . . . . . . . . . . . . . . . . . . . . . . . . . . . 133
5.1.1
Motivation and research objectives . . . . . . . . . . . . . . . 133
5.1.2
Generated data and used methods
. . . . . . . . . . . . . . . 133
5.1.3

…

Conclusions made for mesenchymal differentiation
. . . . . . 152
5.7
Interactive visualization of dynamic regulatory networks (iDREM)
. 152
5.8
Contributions of all researchers involved in the described project
. . 153
6
Same same but different - Diversity of chromatin accessibility
assays
155
6.1
Motivation and research objectives . . . . . . . . . . . . . . . . . . . 155
6.2
Generated data and experimental setup
. . . . . . . . . . . . . . . . 155

…

6.5
Clustering of NDRs is linked to functional associations . . . . . . . . 160
6.6
Unique accessible regions contribute information to gene-expression
prediction models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 160
xiii
Contents
6.6.1
Feature definition . . . . . . . . . . . . . . . . . . . . . . . . . 161
6.6.2
Linear regression . . . . . . . . . . . . . . . . . . . . . . . . . 162
6.6.3
The union of all NDRs achieves the best model performance . 162
6.7
Shape, sequence and methylation characteristics at the active sites
of the participating enzymes . . . . . . . . . . . . . . . . . . . . . . . 163

…

6.7.3
DNA methylation . . . . . . . . . . . . . . . . . . . . . . . . . 165
6.8
A logistic regression classifier to classify assay specific NDRs . . . . . 165
6.9
General conclusions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 167

…

7.4.2
GTEx and TCGA data
. . . . . . . . . . . . . . . . . . . . . 174
7.5
Cell Ontology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 175
7.6
An ontology score to assess sample similarities . . . . . . . . . . . . . 175
7.6.1
Calculating expected sample similarities from the Cell Ontology175
7.6.2
Using PCA to obtain a sample similarity matrix with respect
to gene-expression data

…

7.7
Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 178
7.7.1
The ontology score leverages information captured in the Cell
Ontology
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 178

…

7.8
Conclusions and Impact of this work . . . . . . . . . . . . . . . . . . 186
7.9
Contributions of all researchers involved in the described project
. . 186
8
Suggesting regulatory sites on the gene-level
189

…

. . . . . . . . . . . . . 204
8.9.1
Data and processing . . . . . . . . . . . . . . . . . . . . . . . 204
8.9.2
Performance of gene-specific expression models
. . . . . . . . 205

…

8.11 Future work and applications of STITCHIT . . . . . . . . . . . . . . 219
8.12 Contributions of all researchers involved in the described project
. . 219
9
Summary, Discussion and Outlook
221
9.1
Software created in the scope of this thesis . . . . . . . . . . . . . . . 221

…

Experimental processing of DEEP DNaseI-seq data . . . . . . 237
B.1.2
Computational processing of DEEP and ENCODE DNaseI-
seq data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 237
B.1.3
Experimental and computational processing of DEEP RNA-
seq data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 238
B.1.4
Experimental and computational processing of DEEP NOMe-

…

B.1.6
ENCODE TF ChIP-seq data
. . . . . . . . . . . . . . . . . . 240
B.1.7
Runtime and TF ChIP-seq comparison . . . . . . . . . . . . . 240
B.1.8
Data used in gene-expression models . . . . . . . . . . . . . . 243
B.1.9
Overview of TF-gene score matrices used to assess the stabil-
ity of TF-gene scores . . . . . . . . . . . . . . . . . . . . . . . 243

…

Contents
B.1.12 Gold standard set used for primary human hepatocytes
. . . 247
B.1.13 Data used for Hi-C models
. . . . . . . . . . . . . . . . . . . 247
B.2
Appendix Chapter 4 . . . . . . . . . . . . . . . . . . . . . . . . . . . 251

…

B.3.2
TF ChIP-seq data used for the TF affinity binarization ex-
periments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256
B.3.3
Identification of super-enhancers from H3K27ac data . . . . . 256

…

DNaseI-seq and ATAC-seq . . . . . . . . . . . . . . . . . . . . 260
B.4.4
Finding open chromatin regions with NOMe data . . . . . . . 260
B.4.5
Processing of RNA-seq data . . . . . . . . . . . . . . . . . . . 260
B.4.6
Access to the HepG2 data sets used in this study . . . . . . . 260
B.4.7
Motif, shape and methylation analysis on additional data sets 260
B.5
Appendix Chapter 7 . . . . . . . . . . . . . . . . . . . . . . . . . . . 265
B.5.1
IHEC data IDs and CL mapping . . . . . . . . . . . . . . . . 265
B.5.2
Quantification of IHEC RNA-seq data . . . . . . . . . . . . . 265
B.5.3

…

Data used within the project
. . . . . . . . . . . . . . . . . . 270
B.6.2
Details on executing the tested methods . . . . . . . . . . . . 275
B.6.3
Details on various STITCHIT validation experiments . . . . . 276

…

1
Introduction
The human body is composed of approximately 37.2 trillion cells [B+13a]. There
are about 200 different cell types [A+05] that is cells with different purpose and
morphology. Despite this diversity, almost all cells do share the same DNA sequence.
This raises the question how cellular diversity is orchestrated and maintained on

lie inside functional element 
 
 
Abstract:  
Identification and prioritization of function-associated variants become an increasing demand as 
next-generation sequencing data rapidly grows and accumulated. Current computational 
methods are developed to predict deleterious and disease-associated variants, not designed to 
predict specific molecular phenotypes of these variants (i.e., their effects on gene expression
regulation). High throughput reporter assays, like massively parallel reporter assay (MPRA) are 
successful in identifying functional elements in the whole genome. These MPRA datasets can 
be integrated with other next generation sequencing (NGS) data like ChIP-Seq to learn a 
knowledge model and predict molecular effect of variants. However, due to the heterogeneity of
data sources and unbalanced data availability, most of TFs have ChIP-Seq experiments in only 
one or few cell lines, which make it difficult to build a model to estimate the molecular effect of 
variants within a functional element by considering these cell-line specific features. 
 
In this paper, we proposed GRAM, a generalized model to study the biological significance of
molecular effect in a cell-specific manner. We defined TF binding waiting-time features (TFT), 
which can reflect not only cell-type specific but loci specific information and is also easily 
calculated from RNA-Seq data. We first found that TF binding features are the most predictive 
features, evolutionary conservation doesn’t show indispensable contribution to molecular effect
employing comprehensive feature selection framework. Using in vitro SELEX TF binding 
features along can achieve similar prediction power as using the TF binding features from ChIP-
Seq. We then integrate with in-vitro TF binding features instead of those inferred from spotty 
covered ChIP-Seq data, and TFT features extracted from RNA-Seq to generalize our model to
all other cell lines. In the multi-phase classification model, the AUROC reaches 0.728 and 
outperforms all the state-of-the-art tools. Finally, GRAM has been assessed in MCF7 and K562 
cell lines, resulting in high predictive performance. 
Introduction  
Next-generation sequencing technologies enable high-throughput whole genome sequencing
and exomes sequencing[1]. Many disease-associated mutations[2] the vast majority of common 
single nucleotide variants have been identified in the human population  [3, 4]. Genome-wide 
association studies(GWAS) have characterized many disease-associated variants, but these 
variants mostly lie outside protein-coding regions, [5], emphasizing the importance of the
understanding of regulatory elements in the human genome. This also drives an urgent need to 
develop high-throughput methods to sift through this deluge of sequence data to quickly 
determine the functional relevance of each noncoding variant[6]. 
 
It has been shown that only a fraction of noncoding variants is functional, and among the 
functional variants, the majority show only modest effects[7]. Therefore, highly quantitative

…

high throughput microarray and NGS methods, massively parallel reporter assay (MPRA) has 
extended the scales to the genome-wide level [9-14]. Recent, In Ryan’s cell paper, they have 
demonstrated the capability of MPRA to identify the causal variants that directly modulate gene 
expression. This study reports 842 variants (emVARs) showing significantly different expression
modulation effect and also provides a high-quality data source has been providing for 
computational modeling [15, 16]. 
 
There is also an increasing need for computational methods to effectively predict the molecular 
effect of variants and provide a better understanding of the underlying biology of these results. A 
host of approaches have been developed to address the problem of variant prioritization from

…

identify the variants on evolutionary fitness. Some tools, like Funseq2, may not belong to one 
particular category because of the integration of a comprehensive data context and 
unsu