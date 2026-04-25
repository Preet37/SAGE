# Source: https://aclanthology.org/2025.coling-main.393v1.pdf
# Title: DAEA: Enhancing Entity Alignment in Real-World Knowledge Graphs
# Fetched via: jina
# Date: 2026-04-09

Title: DAEA: Enhancing Entity Alignment in Real-World Knowledge Graphs Through Multi-Source Domain Adaptation



Number of Pages: 12

> Proceedings of the 31st International Conference on Computational Linguistics , pages 5890–5901 January 19–24, 2025. ©2025 Association for Computational Linguistics

5890 DAEA: Enhancing Entity Alignment in Real-World Knowledge Graphs Through Multi-Source Domain Adaptation 

Linyan Yang 1,2 , Shiqiao Zhou 2*, Jingwei Cheng 1,3 , Fu Zhang 1,3 ,Jizheng Wan 2, Shou Wang 2, Mark Lee 2

> 1

School of Computer Science and Engineering, Northeastern University, China 

> 2

School of Computer Science, University of Birmingham, UK 

> 3

Key Laboratory of Intelligent Computing in Medical Image of Ministry of Education, Northeastern University, China 

> yanglinyanly@163.com, sxz363@student.bham.ac.uk, {chengjingwei, zhangfu}@mail.neu.edu.cn, {j.wan.1, s.wang.2, m.g.lee}@bham.ac.uk

Abstract 

Entity Alignment (EA) is a critical task in Knowledge Graph (KG) integration, aimed at identifying and matching equivalent enti-ties that represent the same real-world ob-jects. While EA methods based on knowl-edge representation learning have shown strong performance on synthetic benchmark datasets such as DBP15K, their effectiveness signifi-cantly decline in real-world scenarios which often involve data that is highly heterogeneous, incomplete, and domain-specific, as seen in datasets like DOREMUS and AGROLD. Ad-dressing this challenge, we propose DAEA, a novel EA approach with Domain Adaptation that leverages the data characteristics of syn-thetic benchmarks for improved performance in real-world datasets. DAEA introduces a multi-source KGs selection mechanism and a specialized domain adaptive entity alignment loss function to bridge the gap between real-world data and optimal benchmark data, mit-igating the challenges posed by aligning en-tities across highly heterogeneous KGs. Ex-perimental results demonstrate that DAEA out-performs state-of-the-art models on real-world datasets, achieving a 29.94% improvement in Hits@1 on DOREMUS and a 5.64% improve-ment on AGROLD. Code is available at https: //github.com/yangxiaoxiaoly/DAEA .

1 Introduction 

Knowledge Graphs (KGs) have recently been de-veloped and utilized across various domains. How-ever, since most KGs are created independently by different organizations and individuals, they often exhibit significant heterogeneity. Knowledge fu-sion seeks to address this by aligning and merging heterogeneous and redundant information within KGs to achieve a globally unified representation of 

> *Corresponding Author
> 1https://www.wikidata.org/wiki/Wikidata:Main_Page
> 2https://www.dbpedia.org/

knowledge (Dong et al., 2014). Entity Alignment (EA) plays a crucial role in this fusion process, with its primary objective being to identify equivalent entities across different KGs. In recent years, methods based on knowledge representation learning have become increasingly popular for tackling the entity alignment challenge. These methods work by projecting entities into a low-dimensional vector space, where the similarity between entities is determined based on their em-beddings. MTransE (Chen et al., 2017), BootEA (Sun et al., 2018), JAPE (Sun et al., 2017), and TransEdge (Sun et al., 2019) utilize TransE (Bor-des et al., 2013) to learn entity and relation em-beddings. GNN-based EA methods (Wang et al., 2018; Xu et al., 2019; Wu et al., 2019a) generate en-tity embeddings by aggregation information from their neighbourhoods via GNNs (Kipf and Welling, 2017). These methods are based on the premise that similar neighborhood structures exist in different KGs, implying isomorphism, which may not hold true due to the heterogeneity of KGs (Sun et al., 2020). To address this, some approaches have ap-plied an attention mechanism to weigh relations between entities differently (Mao et al., 2020; Wu et al., 2019a) or have selectively ignored neighbors that are detrimental to alignment (Wu et al., 2020; Cao et al., 2019; Li et al., 2019). Additionally, at-tributes of triples have been recognized as vital for alignment. Several strategies enhance alignment by embedding attributes such as names, types, or values alongside structural embeddings (Sun et al., 2017; Wang et al., 2018; Chen et al., 2020; Zhang et al., 2019; Trisedya et al., 2019; Wang et al., 2020; Tang et al., 2020; Zhong et al., 2022). In real-world datasets, issues such as high hetero-geneity, sparsity, and incompleteness are prevalent (Lisena et al., 2018; Venkatesan et al., 2018). Not only many corresponding entities have completely different neighbors (as illustrated in Figure 1), but numerous entities also lack attribute information. 5891 Macau        

> Macao(film)
> Sao Paulo Luanda
> The Man with the
> Golden Gun
> Fulltime Killer
> Asia
> Guangdong Linkoping
> Municipality
> No Risk,
> No Gain
> share
> border
> with
> twinned
> adminstrati
> ve body
> twinned
> adminstrati
> ve body
> twinned
> adminstrati
> ve body
> narrative
> location
> narrative
> location
> narrative
> location
> narrative
> location
> continent Macau
> Macao(film)
> Sao Paulo Luanda
> The Man with the
> Golden Gun
> Fulltime Killer
> Asia
> Guangdong Linkoping
> Municipality
> No Risk,
> No Gain
> share
> border
> with
> twinned
> adminstrati
> ve body
> twinned
> adminstrati
> ve body
> twinned
> adminstrati
> ve body
> narrative
> location
> narrative
> location
> narrative
> location
> narrative
> location
> continent Macau
> 2007_Asian_Indoor_
> Games
> So_Good
> (TV_Series)
> Ediso_Chen
> Macau_Asia_Satellite
> _Television
> South_China_Sea
> Macau_Tower
> broadc
> astArea citizenShip
> location
> location
> hostCity
> nearestCity
> Macau
> 2007_Asian_Indoor_
> Games
> So_Good
> (TV_Series)
> Ediso_Chen
> Macau_Asia_Satellite
> _Television
> South_China_Sea
> Macau_Tower
> broadc
> astArea citizenShip
> location
> location
> hostCity
> nearestCity
> Macau
> 2007_Asian_Indoor_
> Games
> So_Good
> (TV_Series)
> Ediso_Chen
> Macau_Asia_Satellite
> _Television
> South_China_Sea
> Macau_Tower
> broadc
> astArea citizenShip
> location
> location
> hostCity
> nearestCity
> DBpedia Wikidata

Figure 1: An example of entity alignment in real-world KGs (Wikidata 1and DBpedia 2). The yellow backgrounds represent the same entities in two KGs. The surrounding blue and green backgrounds represent their neighbor entities, while the solid lines with arrows represent the relations between entities. 

Therefore, relying solely on the information in-herent within KGs is insufficient for effectively learning and performing EA. This limitation signif-icantly leads to the degradation in performance of these models when applied to real-world datasets. To enhance EA performance on real-world datasets, we propose the Domain Adaptive Entity 

Alignment (DAEA) method. This innovative ap-proach aims to enhance the model’s adaptabil-ity and accuracy in diverse real-world environ-ments by leveraging rich knowledge from source datasets. We first propose a multi-source KGs se-lection mechanism that strategically selects rele-vant dataset from multiple source KGs. If source data is selected for transfer learning without care-ful consideration, it may cause negative transfer. Therefore, the mechanism selects the source KGs that are most similar to the target KGs for domain adaptation, taking into account both semantic and structural information. By incorporating insights gained from synthetic benchmarks, the mechanism strengthens the model’s ability to align entities more accurately, even in the face of complex and diverse KGs. Additionally, we design a domain adaptive entity alignment loss function that plays a crucial role dur-ing the training phase of the model by reducing the distance between corresponding entities, thereby aligning them more closely. Simultaneously, it also works to minimize the distributional disparities be-tween benchmark data, which is often idealized or standardized, and real-world data, which contains more variability and noise. In summary, the main contributions of this paper are as follows: • We propose a multi-source KGs selection mechanism that fully leverages the valuable information available in benchmark datasets to enhance entity alignment in real-world datasets. • We design a domain adaptive entity alignment loss function with a dual focus on both en-tity alignment and domain adaptation, which helps in achieving a more holistic improve-ment in model performance. • To the best of our knowledge, this is the first instance of applying domain adaptation tech-niques from transfer learning specifically to the task of EA. Extensive experiments demon-strate that our DAEA method outperforms SOTA models on real-world datasets. 

2 Related Work 

2.1 Entity alignment 

Currently, the majority of Entity Alignment (EA) methods are grounded in knowledge representa-tion learning, and can be primarily categorized into either translation based methods or based on GNNs/GCNs. Translation based methods, such as MTransE (Chen et al., 2017), JAPE (Sun et al., 2017), KECG (Li et al., 2019), BootEA (Sun et al., 2018), Multi-mapping Relations (Shi and Xiao, 2019), TransEdge (Sun et al., 2019), JarKA(Chen et al., 2020), and CTEA(Yan et al., 2020), princi-pally constrain the entity embeddings into a fixed distribution by translation-based knowledge graphs embedding methods. Based on the observation that entities sharing similar neighboring structures tend to be aligned, EA approaches based on GCNs dis-tribute and consolidate entity information across graphs. GCN-Align (Wang et al., 2018) is the first to use GCN to jointly embed the entity structure and entity attributes. Building upon this founda-tion, many approaches have enhanced GCNs to address issues such as noise propagation (HGCN 5892 (Wu et al., 2019b)), heterogeneity (MuGNN (Cao et al., 2019), Alinet (Sun et al., 2020), NMN (Wu et al., 2020), MRAEA (Mao et al., 2020)), and better utilization of relationship and attribute infor-mation (RDGCN (Wu et al., 2019a), RAGA (Zhu et al., 2021a), RNM (Zhu et al., 2021b), EPEA (Wang et al., 2020)). The ExEA (Tian et al., 2024) framework is designed to generate high-quality ex-planations for a given embedding-based EA model while also improving EA results through repair. CAECGAT (Xie et al., 2021) jointly learns cross-KG embeddings by propagating information across different KGs, and DuGa-DIT (Xie et al., 2020) bridges the semantic gap between KGs by lever-aging both neighborhood features and cross-KG alignment information. And some temporal entity alignment methods, like TS-align (Zhang et al., 2024), Simple-HHEA (Jiang et al., 2024). Simple-HHEA highlights the challenge of entity alignment in heterogeneous knowledge graphs and introduces a new time-aware heterogeneous knowledge graph entity alignment dataset. With the rise of pre-trained language mod-els like BERT (Kenton and Toutanova, 2019), HMAN+BERT (Yang et al., 2019), SDEA (Zhong et al., 2022), and BERT-INT (Tang et al., 2020) treat entity alignment as a downstream task for fine-tuning BERT. Due to the high heterogeneity and limited avail-able information in real-world datasets, existing entity alignment methods, despite showing supe-rior performance on benchmarks, experience sig-nificant performance degradation when applied to real-world datasets. Consequently, we propose DAEA approach, which incorporates domain adap-tation techniques to enhance entity alignment per-formance in real-world datasets. 

2.2 Domain Adaptation 

Domain adaptation (DA) is a key area within trans-fer learning (Pan and Yang, 2009), aiming to adapt models from a source domain to a target domain with differing distributions. Techniques in DA focus on extracting domain-invariant representa-tions by utilizing distance metrics like Maximum Mean Discrepancy (MMD) (Gretton et al., 2012) and Correlation Alignment (CORAL) (Sun and Saenko, 2016), as well as employing adversar-ial methods such as Domain-adversarial Neural Network (DANN) (Ganin et al., 2016) and Multi-adversarial Domain Adaptation (MADA) (Pei et al., 2018) to align these distributions. For more com-plex scenarios involving multiple sources, multi-source domain adaptation (MDA) is necessary. In entity linkage topic, AdaMEL (Jin et al., 2021) leverages attribute information to adapt labeled data from different source datasets to target dataset. Research in multi-source graph domain adaptation (GDA) includes models like NESTL (Fu et al., 2020), which trains individual models for each source based on topological similarity, and MSDS (He et al., 2023), which selects the most transfer-able sources using mixed discrepancy metrics. Ad-ditionally, Meta-GDN (Ding et al., 2021) facilitates few-shot network anomaly detection by transfer-ring meta-knowledge from multiple networks. Although there has been much research on GDA, there has been no research on domain adaptation for entity alignment where the datasets not only contain graph pairs, but also have heterogeneous structures, presenting more challenges. 

3 Task Definition 

Definition 1 (Knowledge Graph) A knowl-edge graph (KG) is denoted as G =(E, R, A, V, T r, T a), where E = {e1, e 2, ...e m},

R = {r1, r 2, ...r n}, A = {a1, a 2, ...a p}, and 

V = {v1, v 2, ..., v q} represent entity set, relation set, attribute set, and value set, respectively, and 

m, n, p, q are the number of entities, relations, attributes, and attribute values, respectively. 

Tr ⊆ E × R × E is the relation triple set, and 

Ta ⊆ E × A × V is the attribute triple set. Relational triples can also be represented as 

(h, r, t ), where h is called the head entity and t is called the tail entity. 

Definition 2 (Entity Alignment in KGs) Given two KGs G1 = ( E1, R 1, A 1, V 1, T 1 

> r

, T 1 

> a

), and G2 =(E2, R 2, A 2, V 2, T 2 

> r

, T 2 

> a

), the aligned entity pairs (training set) is denoted as S = {(e1 

> i

, e 2 

> j

)|e1 

> i

∈

E1, e 2 

> j

∈ E2, e 1 

> i

≡ e2 

> j

}, where ≡ stands for equiv-alence, i.e., the entity e1 

> i

and entity e2 

> j

refer to the same thing in the real world. The goal of the EA task is to find the remaining equivalent entity pairs of these two KGs. 

Definition 3 (Source and Target KGs) The source KGs Gsl refers to a graph pairs {(G1 

> sl

, G 2 

> sl

)}.Here l means source dataset number. The superscript of graph pairs means the order of graph. There are multiple source KGs: 

GS = {Gs1 = (G1 

> s1

, G 2 

> s1

), ..., G su =(G1 

> su

, G 2 

> su

)}, and target KGs GT = (G1 

> t

, G 2 

> t

),

u is the number of source KGs, where 5893 .

> .
> .
> Source KGs
> Target KG
> GAT
> ...
> Semantic Embeddings
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> .
> Structure Distance Semantic Distance

+ + +

+++

Min 

> Selected Source KG
> ...
> ...
> ...
> ...
> Structure Embeddings
> ...
> ...
> ...
> Loss
> Push
> Neighbours
> Away t

G1

> Gus

G1sG2

> G1
> G2
> G2
> G2
> G1
> G1
> G1
> G1
> G1
> G2
> G2
> G2
> Gt

GtGtGtGtGtG1sG1sG1sG1sG1sGusGusGusGusGusGFigure 2: Multi-source selection Basic BERT Unit 

> Seed Entity Pairs 2

G1

G

> ... ...
> Seed Entity Pairs 2

G1

G

> ... 1

G2

G

> Seed Entity Pairs
> ... ...
> Pairwise
> Loss
> Domain
> Adaptive
> Loss
> ... ...
> ... ...
> ...
> ...

+

> ... ...
> ... ...
> ...
> ...
> Model
> Train
> ... ...
> Final Results
> BERT -INT
> Interaction

Figure 3: Domain Adaptation 

G1 

> s1

= ( E1 

> s1

, R 1 

> s1

, A 1 

> s1

, V 1 

> s1

, T 1 

> rs 1

, T 1 

> as 1

) and G1 

> t

=(E1 

> t

, R 1 

> t

, A 1 

> t

, V 1 

> t

, T 1

> rt

, T 1

> at

). The aligned entity pairs (training set) are denoted as Ssl =

{(e1 

> is l

, e 2 

> js l

)|e1 

> is l

∈ E1 

> sl

, e 2 

> js l

∈ E2 

> sl

, e 1 

> is l

≡ e2 

> js l

}

and St = {(e1

> it

, e 2

> jt

)|e1 

> it

∈ E1 

> t

, e 2 

> jt

∈ E2 

> t

, e 1 

> it

≡

e2

> it

}, where ≡ stands for equivalence. 

4 Methodology 

The DAEA model primarily comprises of two com-ponents: Multi-Source KGs Selection (Figure 2) and Domain Adaptation (Figure 3). Multi-Source KGs Selection is employed to iden-tify which source KGs from the benchmark are most suitable to do transfer learning to the target KGs. In Figure 2, the optimal KGs for transfer learning are selected by calculating the semantic and structural distances between various KGs. Se-mantic and structural information are captured us-ing GloVe (Pennington et al., 2014) embeddings and Graph Attention Networks (GATs) (Velickovic et al., 2017) respectively, with the latter employing an unsupervised contrastive learning loss. A more detailed discussion will be provided in Section 4.1. Figure 3 details the process of domain adapta-tion. Initially, data input is expanded on the basis of BERT-INT architecture to include both source and target KGs. During the training phase, the model not only employs pairwise margin loss to approxi-mate the corresponding entities in the source and target KGs but also computes domain adaptive loss between the training sets of the source and target KGs. More details will be discussed in Section 4.2. 

4.1 Multi-source KGs selection 

To more comprehensively assess the similarity be-tween KGs, we consider both semantic and struc-tural information. Let DGsGt represent the distance between the source KGs ( GS ) and the target KGs (GT ). Specifically, we define DGsGt as follows: 

DGsGt = {D Gs1 Gt , . . . , DGsu Gt } (1) The smaller the distance between source and target KGs, the higher their similarity. Therefore, we select the source KGs with the smallest distance as the optimal. DGsi Gt for each individual component 

i = 1 , . . . , u is given by: 

DGsi Gt = dSE Gsi Gt + dST Gsi Gt (2) 5894 Here, dSE Gsi Gt and dST Gsi Gt represent the se-mantic and structural distances, respectively, and are computed as: 

dSE Gsi Gt = dSE G1  

> siG1
> t

+ dSE G2  

> siG2
> t

(3) 

dST Gsi Gt = dST G1  

> siG1
> t

+ dST G2  

> siG2
> t

(4) 

4.1.1 Semantic Distance 

We employ the widely-used word embedding tool, GloVe, to obtain the embedding representations of entity names within the KGs. The semantic embedding representations of the source and tar-get KGs are denoted by SE G1

> si

, SE G2

> si

, SE G1 

> t

,

SE G2 

> t

, respectively. We utilize the Jensen-Shannon (JS) distance (Fuglede and Topsoe, 2004), a widely adopted metric, to assess similarities across KGs. 

dSE G1  

> siG1
> t

is computed as: 

dSE G1  

> siG1
> t

=

q

JS (SE G1

> si

, SE G1 

> t

) (5) where JS (SE G1

> si

, SE G1 

> t

) can be computed as : 

JS (SE G1

> si

, SE G1 

> t

) = 12 D(SE G1

> si

∥ M ) + 12 D(SE G1 

> t

∥ M )

M = 12 (SE G1

> si

+ SE G1 

> t

)

(6) Here, D(P ∥ Q) for P and Q, can be computed as: 

D(P ∥ Q) = X

> i

Pilog ( Pi

Qi

) (7) The calculation method for dSE G2  

> siG2
> t

follows the same approach. 

4.1.2 Structural Distance 

A two-layer GAT is employed to extract the struc-tural information from KGs. Specifically, with a standard GAT layer, the hidden state hi for entity 

ei at each layer is performed as follows. 

hi = ReLU ( X

> j∈N i

αij W h j ) (8) where Ni denotes the set of neighbors of ei, hj

denotes the embedding of entity ej obtained by this layer, W is a trainable weight matrix, αij are the attention coefficients computed as: 

αij = exp (Γ( aT [W e i ⊕ W e j ])) 

P 

> k∈N i

exp (Γ( aT [W e i ⊕ W e k])) (9) where Γ is the LeakyReLU nonlinear activation function, a is a trainable parameter, ⊕ denotes the concatenation operation. In order to better accommodate the entity align-ment task, we utilize an unsupervised contrastive learning loss during the training process when ap-plying GAT to individual graph data. For each en-tity, the goal is to maximize the distance between it and its neighbouring entities. 

Lc = 1

|N i|

X 

> ej∈N i

max (0 , M − Eu (ei, e j )) (10) where |N i| is the number of Ni, and M is the mar-gin, Eu is the Euclidean distance. Structural embeddings, denoted as GAT G1

> si

,

GAT G1

> si

, can be obtained through the trained GAT. Subsequently, the structural distance dST G1  

> siG1
> t

can be calculated as described in Equation (5). 

4.2 Domain Adaptation 

In the domain adaptation stage, DAEA follows BERT-INT and treats entity alignment as the down-stream task to fine-tune a pre-trained BERT model. Initially, we expand the input data into source KGs and target KGs. Subsequently, we compute the pairwise losses for both the source KGs and the target KGs, as well as the domain adaptive loss between the source KGs and the target KGs. The sum of these three losses constitutes the total loss of the entire model. It can be denoted as: 

Loss = Ls + Lt + LDA (11) 

4.2.1 Pairwise Loss 

For each entity pairs (e1 

> i

, e 2 

> j

) in training set S, for entity e1 

> i

, we treat e2 

> j

as a positive example, and a negative example e2− 

> j

randomly sampled from E2.Let Ls and Lt respectively represent the pairwise loss for the source KGs and the target KGs. Ls can be computed as follows. 

Ls = X   

> (e1
> i,e 2
> j,e 2−
> j)∈S

max {0, l 1(e1 

> i

, e 2 

> j

) − l1(e1 

> i

, e 2− 

> j

) + M } (12) where M is the margin, l1(e1 

> i

, e 2 

> j

) is the L1 distance between e1 

> i

and e2 

> j

. The calculation of Lt follows the same methodology as above. 5895 4.2.2 Domain Adaptive Loss 

We compute the distribution distance between the training sets of the source KGs and the target KGs to serve as the domain adaptive loss. Given a source training set Ss =

{(e1

> is

, e 2

> is

, e 2− 

> is

)|e1 

> is

∈ E1 

> s

, e 2 

> is

∈ E2 

> s

, e 2− 

> is

∈ E2 

> s

, }

and a target training set St = {(e1

> jt

, e 2

> jt

, e 2− 

> jt

)|e1 

> jt

∈

E1 

> t

, e 2 

> jt

∈ E2 

> t

, e 2− 

> jt

∈ E2 

> t

, }. When computing the domain adaptive loss, we minimize the distance between positive examples from the source and target KGs, as well as the distance between negative examples from the source and target KGs. Let DA P and Let DA N denote the domain adaptive loss of one positive and negative pairs, respectively. They are denoted as: 

DA P =

> |Ss|

X

> i=1
> |St|

X

> j=1

(d(e1

> is

, e 1

> jt

) + d(e2

> is

, e 2

> jt

)) (13) 

DA N =

> |Ss|

X

> i=1
> |St|

X

> j=1

d(e2− 

> is

, e 2− 

> jt

) (14) where | · | represents the size of a set. To effectively measure the distance between source and target distributions, we employ MMD (Gretton et al., 2012), which is one of the most widely used metrics in domain adaptation. 

d(e1

> is

, e 1

> jt

) is computed as: 

d(e1

> is

, e 1

> jt

) = E[k(e1

> is

, e 1′

> is

)] + E[k(e1

> jt

, e 1′

> jt

)] 

− 2E[k(e1

> is

, e 1

> jt

)] (15) where k refers to kernel function, which is Gaus-sian kernel (Elen et al., 2022) in our case. e1′ 

> is

and 

e1′ 

> jt

are samples from source and target. E is the ex-pected value. d(e2

> is

, e 2

> jt

) and d(e2− 

> is

, e 2− 

> jt

) are com-puted with a similar way. Eventually, the domain adaptive loss is denoted as: 

LDA = DA P + DA N (16) 

5 Experiment 

5.1 Experiment Settings 5.1.1 Datasets 

The widely used benchmark, DBP15K, is consid-ered as an ideal synthetic dataset for entity align-ment, comprising three multilingual sub-datasets: ZH-EN, JA-EN, and FR-EN. In this study, we adopt DBP15K as the source KGs, while utilizing two real-world datasets, DOREMUS (Lisena et al., 2018) and AgroLD (Venkatesan et al., 2018), as the Datasets Entities Rel. Rel.Triples Attr. Attr.Triples Pairs DBP15K ZH-EN ZH 19388 1701 70414 7780 379684 15000 EN 19572 1323 95142 6933 567755 JA-EN JA 19814 1299 77241 5681 354619 15000 EN 19780 1153 93484 5850 497230 FR-EN FR 19661 903 105998 4431 528665 15000 EN 19993 1208 115722 6161 576543 Real-World Data DOREMUS G1 2057 19 5057 3 1775 238                  

> G21889 20 4659 4884 AGROLD G196117 721029 628895 11555
> G251488 4139546 12 225060

Table 1: Details of the datasets. Rel., Rel.Triples, Attr., Attr.Triples, and Pairs represent relations, rela-tion triples, attributes, attribute triples, and entity pairs respectively. 

target KGs, which are introduced by (Raoufi et al.) 3.DOREMUS is a multilingual dataset focused on classical music, and AGROLD is a large dataset for plant science. From Table 1, it is evident that nearly 80% of entities can find their corresponding counterparts in DBP15K, whereas only about 10% of entities have aligned counterparts in real-world data. 

5.1.2 Baselines 

Methods are classified into three categories based on differences in their embedding modules: translation-based methods, GNN-based methods, and BERT-based methods. We have chosen 7 SOTA EA methods that encompass diverse em-bedding modules. Translation-based methods: 

TransEdge (Sun et al., 2019), MultiKE (Zhang et al., 2019). GNN-based methods: RDGCN (Wu et al., 2019a), NMN (Wu et al., 2020). BERT-based methods: SDEA (Zhong et al., 2022), BERT-INT (Tang et al., 2020). We also compare the method in Attr-Int (Yang et al., 2024) that cal-culates only the overlap of attribute value sets. Although many recent multi-modal entity align-ment methods have been developed, like MCLEA (Lin et al., 2022), MEAformer (Chen et al., 2023a), UMEA (Chen et al., 2023b), we do not compare our approach with these methods due to the lack of images in real-world datasets. 

5.1.3 Implement details 

For each dataset, we divide the aligned entity pairs into training and test sets with a ratio of 3:7. To cover all data from both source and target KGs in one epoch, the batch size for the source KGs are set to 24, and for AGROLD, it is set to 19. 

> 3

https://github.com/EnsiyehRaoufi\Create_ Input_Data_to_EA_Models 5896 However, due to the significant disparity in data volume between the source KGs and DOREMUS, we expand the DOREMUS training set to six times its original size to ensure a thorough traversal of the source KGs. This is achieved by repeating the original training set six times without introducing new data, and the batch size is set to 1. 

5.1.4 Evaluation Metric 

To facilitate comparison with previous methods, we adopt ranking-based evaluation metrics for entity alignment, specifically Hits@ k and mean recipro-cal rank (MRR). Hits@ k measures the proportion of correct alignments among the top k matches (k = 1 , 10 ). Note that higher Hits@ k and MRR in-dicate better performance. We use H@1 and H@10 to present Hits@1 and Hits@10 in this paper. Methods DOREMUS AGROLD Emb.Modules Names H@1 H@10 MRR H@1 H@10 MRR TransE TransEdge 0.60 4.19 0.036 0.01 0.02 0.001 MultiKE 2.70 8.70 - 2.30 5.7 -GCN RDGCN 1.2 10.9 - 0.02 0.30 -NMN 0.0 4.14 - 0.01 0.12 -BERT SDEA 38.69 55.95 0.461 0.01 0.02 0.001 BERT-INT 47.9 59.28 0.515 21.50 25.03 0.229 None Attr-Int 48.74 76.47 0.587 14.33 20.36 0.167 BERT DAEA 77.84 88.62 0.815 27.14 34.85 0.300      

> ↑29.94 ↑29.34 ↑0.3 ↑5.64 ↑9.82 ↑0.071

Table 2: Entity alignment results on Real-World Data 

5.2 Experimental Results 5.2.1 Main Results 

The experimental results of DAEA compare to other methods on two real-world datasets are shown in Table 2. It is observable that, compared with other methods, DAEA achieves the best per-formance. Except for BERT-INT and Attr-Int, the performance of the other compared models is rela-tively suboptimal. The reason for this phenomenon is attributed to the fact that these models incorpo-rate the neighboring entities when calculating the embeddings of entities, whereas BERT-INT only utilizes entity names and descriptions for embed-ding representation, and Attr-Int merely computes the overlap of attribute value sets. This suggests that in real-world datasets, the neighboring entities of the corresponding entities are highly heteroge-neous, introducing noise when neighbor informa-tion is included, thus leading to poor alignment results. To further validate whether the real-world datasets are highly heterogeneous, we employ the method described in (Yang et al., 2024) to calculate the coverage rate of corresponding entities in the real-world datasets compared to those in the bench-mark. Let (e1 

> i

, e 2 

> j

) be an entity pair, N (e1 

> i

) and 

N (e2 

> j

) be the sets of neighboring entities of e1 

> i

and 

e2 

> j

respectively, then the coverage rate C(e1   

> i,e 2
> j)

of the entity pair (e1 

> i

, e 2 

> j

) is calculated by C(e1   

> i,e 2
> j)

=

|N (e1 

> i

) ∩ N (e2 

> j

)|/ min  |N (e1 

> i

)|, |N (e2 

> j

)|, where 

| · | represents the size of a set. As illustrated in Figure 4, it can be seen that the neighbours of the corresponding entities in the real-world datasets are completely different, whereas most corresponding entities in the benchmark have the same neighbors. However, most previous mod-els are based on the assumption that identical enti-ties have similar neighboring entities. As a result, these models experience a significant decline in performance on real-world datasets. 

Figure 4: Percentage of coverage rate of entity pairs in each stage of the benchmark datasets and real-world datasets. The x-axis represents the coverage rate of entity pairs, while the y-axis represents the proportion of all benchmark datasets. 

5.2.2 Ablation Study 

The DAEA model comprises of two main com-ponents: multi-source KGs selection and Domain Adaptation. To validate the effectiveness of these components, we conduct ablation studies. 

Multi-Source KGs Selection: In the multi-source KGs selection phase, we select source KGs based on the computed distance DGsGt described in Sec-tion 4.1, positing that a shorter distance indicates a closer relationship between source and target datasets. As illustrated in Table 3, we quantify the distances between three benchmark datasets (FR-EN, ZH-EN, JA-EN) and two target KGs. No-tably, the FR-EN source KGs are closest to the two target KGs and exhibit the best alignment per-formance. A trend is observed wherein increasing distances between source and target KGs correlated 5897 with decreasing results in entity alignment. This demonstrates the effectiveness of our multi-source KGs selection strategy. Methods DOREMUS AGROLD                                

> DGsGtH@1 H@10 MRR DGsGtH@1 H@10 MRR
> FR-EN 67.51 77.84 88.62 0.815 77.64 27.14 34.85 0.300
> ZH-EN 90.72 71.25 85.03 0.756 91.85 22.65 29.26 0.292 JA-EN 105.71 70.65 83.83 0.740 104.55 20.25 28.19 0.231

Table 3: Entity alignment results on Real-World Data with different source KGs. 

Domain Adaptation: During the domain adapta-tion phase, the training process involves the com-putation of the domain adaptive loss between pos-itive and negative examples from the source KGs and target KGs. To validate the efficacy of the domain adaptive loss and to assess the individ-ual impacts of positive and negative examples, we conduct various experiments. The results are pre-sented in Table 4, where ’DA’ denotes domain adap-tive loss, ’P’ indicates using only positive exam-ples, and ’N’ represents using only negative ex-amples. Table 4 illustrates that without domain adaptive loss results in a notable decrease in per-formance on DOREMUS, with a less significant decline observed on AGROLD. This variation in outcomes can be attributed to the differing sizes of the datasets; AGROLD possesses a considerably larger data volume compared to the source KGs, whereas DOREMUS has a smaller data set. We believe that smaller datasets exhibit simpler data distributions, while larger datasets feature more complex distributions. Consequently, when per-forming transfer learning with the same source KGs, smaller datasets align more easily with the source KGs, and experimental results tend to be relatively better. Additionally, on the DOREMUS dataset, the best H@1 score is achieved when both positive and negative examples are transferred. However, on the AGROLD dataset, using only negative ex-amples yields better results. This indicates that in practical transfer learning scenarios, different tar-get datasets cannot be treated uniformly. Instead, the transfer learning approach should be tailored to the specific characteristics and requirements of each target dataset to optimize outcomes. 

5.2.3 The impact of dataset size for domain adaptation 

To examine the impact of transferring different amounts of data from source KGs to target KGs on entity alignment, we conduct experiments using a Methods DOREMUS AGROLD H@1 H@10 MRR H@1 H@10 MRR                         

> DAEA 77.84 88.62 0.815 27.14 34.85 0.300 -w/o DA 71.86 83.23 0.750 26.24 36.04 0.299 -w P 76.05 89.82 0.801 26.87 36.11 0.303 -w N 72.46 84.43 0.762 27.97 37.37 0.315

Table 4: Ablation results. ’w/o’ means without and ’w’ means with. ’DA’ means domain adaptive loss. ’P’ indi-cates using only positive examples, and ’N’ represents using only negative examples. 

fixed training set (30%) in the target KGs, while varying the proportion of entity pairs selected from the source KGs at 30%, 50%, 80%, and 100%. The experimental results are depicted in Figure 5. On the DOREMUS dataset, optimal performance is achieved when 50% of the source data was trans-ferred. Performance do not improve and slightly declines as the transferred data exceeded 50%, sug-gesting that more source data does not necessarily lead to better alignment. This decline in perfor-mance when the source data substantially exceeds the target data may be attributed to an increase in noise within the transferred data. Conversely, on the AGROLD dataset, the perfor-mance improved with an increase in the amount of transferred data. Given the large volume of data in AGROLD, more source data is required for ef-fective transfer learning. In fact, even when 100% of the entity pairs from the source KGs are uti-lized, the source data volume do not significantly exceed the target data (as opposed to the case for DOREMUS dataset). This suggests that for ef-fective entity alignment through transfer learning, having a larger volume of source data compared to target data is beneficial, as long as the source data maintains a high level of quality and the volume remains within an optimal range. 

Figure 5: The impact of using training sets of varying sizes from the source KGs for domain adaptation on EA performance. 5898 5.3 Distribution visualization and analysis 

To assess the impact of domain adaptation on en-tity alignment, we compare the DOREMUS entity embeddings before and after the integration of do-main adaptation. We visualize the entity embed-dings using Principal Components Analysis (PCA) (Ma´ ckiewicz and Ratajczak, 1993), as shown in Figure 6. It can be observed that without domain adaptation (represented in red and blue), the entities are clustered together with almost indistinguishable distances between them, which is a primary cause of suboptimal entity alignment performance. Af-ter incorporating domain adaptation (represented in orange and purple), the distances between enti-ties significantly increased, facilitating easier iden-tification of corresponding target entities during alignment and thereby yielding improved entity alignment results. 

> Figure 6: PCA of entity embeddings in DOREMUS. BERT-INT-G1 and BERT-INT-G2 represent the en-tity embeddings obtained without domain adaptation, DAEA-G1 and DAEA-G2 represent the entity embed-dings obtained with domain adaptation.

6 Conclusion 

In this paper, we address the issue that current en-tity alignment models perform well on benchmarks but perform suboptimally on complex real-world datasets. We introduce the DAEA model, which enhances the performance of entity alignment in real-world datasets by leveraging data characteris-tics from benchmarks through multi-source KGs selection and domain adaptation strategies. Exten-sive experiments demonstrate that DAEA achieves state-of-the-art performance. 

Limitations 

While the DAEA model has demonstrated sig-nificant improvements in entity alignment perfor-mance on real-world datasets, there are still limita-tions that merit further exploration. Firstly, the current implementation of DAEA pri-marily computes the domain adaptive loss on the training sets of the source and target KGs, without extending this transfer learning to the neighboring entities or the entire entity set of the KGs. This constrained scope of domain adaptation may limit the model’s ability to fully leverage the structural and semantic richness of the entire KG, potentially affecting the robustness and generalizability of the alignment. Future work will investigate the impact of expanding transfer learning to encompass the complete graph data, aiming to enhance the com-prehensiveness and accuracy of entity alignment. Secondly, the improvements achieved by DAEA are more pronounced on the smaller dataset, DOREMUS, compared to the larger dataset, AGROLD. This disparity suggests that the current domain adaptation strategies may not scale as effec-tively with increasing data volume. Addressing this challenge, future research will focus on develop-ing new transfer strategies that are better suited to large-scale datasets, thereby improving the model’s performance across varying data sizes and com-plexities. These limitations highlight the need for ongoing refinement and adaptation of the DAEA model to better address the diverse and dynamic nature of real-world data environments. 

Acknowledgement 

We sincerely thank the anonymous reviewers for their valuable and insightful feedback, which has greatly contributed to improving the quality of this work. This work is supported by the National Nat-ural Science Foundation of China (62276057), and Sponsored by CAAI-MindSpore Open Fund, de-veloped on OpenI Community. Furthermore, we gratefully acknowledge the additional financial sup-port provided by the China Scholarship Council. Finally, we extend our appreciation to Baskerville for their resources and technical assistance, which played an essential role in the successful comple-tion of this research. 5899 References 

Antoine Bordes, Nicolas Usunier, Alberto Garcia-Duran, Jason Weston, and Oksana Yakhnenko. 2013. Translating embeddings for modeling multi-relational data. Advances in neural information pro-cessing systems .Yixin Cao, Zhiyuan Liu, Chengjiang Li, Juanzi Li, and Tat-Seng Chua. 2019. Multi-channel graph neural network for entity alignment. In Proceedings of the 57th Annual Meeting of the Association for Compu-tational Linguistics , pages 1452–1461. Bo Chen, Jing Zhang, Xiaobin Tang, Hong Chen, and Cuiping Li. 2020. Jarka: Modeling attribute inter-actions for cross-lingual knowledge alignment. In 

Pacific-Asia Conference on Knowledge Discovery and Data Mining , pages 845–856. Springer. Muhao Chen, Yingtao Tian, Mohan Yang, and Carlo Zaniolo. 2017. Multilingual knowledge graph em-beddings for cross-lingual knowledge alignment. In 

Proceedings of the 26th International Joint Confer-ence on Artificial Intelligence , pages 1511–1517. Zhuo Chen, Jiaoyan Chen, Wen Zhang, Lingbing Guo, Yin Fang, Yufeng Huang, Yichi Zhang, Yuxia Geng, Jeff Z Pan, Wenting Song, et al. 2023a. Meaformer: Multi-modal entity alignment transformer for meta modality hybrid. In Proceedings of the 31st ACM International Conference on Multimedia , pages 3317– 3327. Zhuo Chen, Lingbing Guo, Yin Fang, Yichi Zhang, Jiaoyan Chen, Jeff Z Pan, Yangning Li, Huajun Chen, and Wen Zhang. 2023b. Rethinking uncertainly miss-ing and ambiguous visual modality in multi-modal entity alignment. In International Semantic Web Con-ference , pages 121–139. Springer. Kaize Ding, Qinghai Zhou, Hanghang Tong, and Huan Liu. 2021. Few-shot network anomaly detection via cross-network meta-learning. In Proceedings of the Web Conference 2021 , pages 2448–2456. Xin Dong, Evgeniy Gabrilovich, Geremy Heitz, Wilko Horn, Ni Lao, Kevin Murphy, Thomas Strohmann, Shaohua Sun, and Wei Zhang. 2014. Knowledge vault: A web-scale approach to probabilistic knowl-edge fusion. In Proceedings of the 20th ACM SIGKDD international conference on Knowledge dis-covery and data mining , pages 601–610. Abdullah Elen, Selçuk Ba¸ s, and Cemil Közkurt. 2022. An adaptive gaussian kernel for support vector ma-chine. Arabian Journal for Science and Engineering ,47(8):10579–10588. Chenbo Fu, Yongli Zheng, Yi Liu, Qi Xuan, and Guanrong Chen. 2020. Nes-tl: Network em-bedding similarity-based transfer learning. IEEE Transactions on Network Science and Engineering ,7(3):1607–1618. Bent Fuglede and Flemming Topsoe. 2004. Jensen-shannon divergence and hilbert space embedding. In 

International symposium onInformation theory, 2004. ISIT 2004. Proceedings. , page 31. IEEE. Yaroslav Ganin, Evgeniya Ustinova, Hana Ajakan, Pas-cal Germain, Hugo Larochelle, François Laviolette, Mario March, and Victor Lempitsky. 2016. Domain-adversarial training of neural networks. Journal of machine learning research , 17(59):1–35. Arthur Gretton, Karsten M Borgwardt, Malte J Rasch, Bernhard Schölkopf, and Alexander Smola. 2012. A kernel two-sample test. The Journal of Machine Learning Research , 13(1):723–773. Hui He, Hongwei Yang, Weizhe Zhang, Yan Wang, Zhaonian Zou, and Tao Li. 2023. Msds: Anovel framework for multi-source data selection based cross-network node classification. IEEE Transactions on Knowledge and Data Engineering ,35(12):12799–12813. Xuhui Jiang, Chengjin Xu, Yinghan Shen, Yuanzhuo Wang, Fenglong Su, Zhichao Shi, Fei Sun, Zixuan Li, Jian Guo, and Huawei Shen. 2024. Toward practical entity alignment method design: Insights from new highly heterogeneous knowledge graph datasets. In 

Proceedings of the ACM on Web Conference 2024 ,pages 2325–2336. Di Jin, Bunyamin Sisman, Hao Wei, Xin Luna Dong, and Danai Koutra. 2021. Deep transfer learning for multi-source entity linkage via domain adaptation. 

arXiv preprint arXiv:2110.14509 .Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova. 2019. Bert: Pre-training of deep bidirec-tional transformers for language understanding. In 

Proceedings of NAACL-HLT , pages 4171–4186. Thomas N Kipf and Max Welling. 2017. Semi-supervised classification with graph convolutional networks. Chengjiang Li, Yixin Cao, Lei Hou, Jiaxin Shi, Juanzi Li, and Tat-Seng Chua. 2019. Semi-supervised entity alignment via joint knowledge embedding model and cross-graph model. In EMNLP-IJCNLP , pages 2723– 2732. Zhenxi Lin, Ziheng Zhang, Meng Wang, Yinghui Shi, Xian Wu, and Yefeng Zheng. 2022. Multi-modal con-trastive representation learning for entity alignment. In Proceedings of the 29th International Conference on Computational Linguistics , pages 2572–2584. Pasquale Lisena, Manel Achichi, Pierre Choffé, Cécile Cecconi, Konstantin Todorov, Bernard Jacquemin, and Raphaël Troncy. 2018. Improving (re-) usability of musical datasets: An overview of the doremus project. Bibliothek Forschung und Praxis , 42(2):194– 205. Andrzej Ma´ ckiewicz and Waldemar Ratajczak. 1993. Principal components analysis (pca). Computers & Geosciences , 19(3):303–342. 5900 Xin Mao, Wenting Wang, Huimin Xu, Man Lan, and Yuanbin Wu. 2020. Mraea: an efficient and robust entity alignment approach for cross-lingual knowl-edge graph. In Proceedings of the 13th International Conference on Web Search and Data Mining , pages 420–428. Sinno Jialin Pan and Qiang Yang. 2009. A survey on transfer learning. IEEE Transactions on knowledge and data engineering , 22(10):1345–1359. Zhongyi Pei, Zhangjie Cao, Mingsheng Long, and Jian-min Wang. 2018. Multi-adversarial domain adap-tation. In Proceedings of the AAAI conference on artificial intelligence , volume 32. Jeffrey Pennington, Richard Socher, and Christopher D Manning. 2014. Glove: Global vectors for word representation. In EMNLP , pages 1532–1543. Ensiyeh Raoufi, Bill Gates Happi Happi, Pierre Lar-mande, François Scharffe, and Konstantin Todorov. An analysis of the performance of representation learning methods for entity alignment: Benchmark vs. real-world data. Xiaofei Shi and Yanghua Xiao. 2019. Modeling multi-mapping relations for precise cross-lingual entity alignment. In EMNLP-IJCNLP , pages 813–822. Baochen Sun and Kate Saenko. 2016. Deep coral: Correlation alignment for deep domain adaptation. In Computer Vision–ECCV 2016 Workshops: Am-sterdam, The Netherlands, October 8-10 and 15-16, 2016, Proceedings, Part III 14 , pages 443–450. Springer. Zequn Sun, Wei Hu, and Chengkai Li. 2017. Cross-lingual entity alignment via joint attribute-preserving embedding. In International Semantic Web Confer-ence , pages 628–644. Springer. Zequn Sun, Wei Hu, Qingheng Zhang, and Yuzhong Qu. 2018. Bootstrapping entity alignment with knowl-edge graph embedding. In IJCAI , volume 18, pages 4396–4402. Zequn Sun, Jiacheng Huang, Wei Hu, Muhao Chen, Lingbing Guo, and Yuzhong Qu. 2019. Transedge: Translating relation-contextualized embeddings for knowledge graphs. In International Semantic Web Conference , pages 612–629. Springer. Zequn Sun, Chengming Wang, Wei Hu, Muhao Chen, Jian Dai, Wei Zhang, and Yuzhong Qu. 2020. Knowl-edge graph alignment network with gated multi-hop neighborhood aggregation. In Proceedings of the AAAI Conference on Artificial Intelligence , vol-ume 34, pages 222–229. Xiaobin Tang, Jing Zhang, Bo Chen, Yang Yang, Hong Chen, and Cuiping Li. 2020. Bert-int: A bert-based interaction model for knowledge graph alignment. In 

IJCAI , pages 3174–3180. Xiaobin Tian, Zequn Sun, and Wei Hu. 2024. Generat-ing explanations to understand and repair embedding-based entity alignment. In 2024 IEEE 40th Inter-national Conference on Data Engineering (ICDE) ,pages 2205–2217. IEEE. Bayu Distiawan Trisedya, Jianzhong Qi, and Rui Zhang. 2019. Entity alignment between knowledge graphs using attribute embeddings. In Proceedings of the AAAI Conference on Artificial Intelligence , vol-ume 33, pages 297–304. Petar Velickovic, Guillem Cucurull, Arantxa Casanova, Adriana Romero, Pietro Lio, Yoshua Bengio, et al. 2017. Graph attention networks. stat , 1050(20):10– 48550. Aravind Venkatesan, Gildas Tagny Ngompé, Nordine El Hassouni, Imene Chentli, Valentin Guignon, Clement Jonquet, Manuel Ruiz, and Pierre Larmande. 2018. Agronomic linked data (agrold): A knowledge-based system to enable integrative biology in agronomy. 

PLoS One , 13(11):e0198270. Zhichun Wang, Qingsong Lv, Xiaohan Lan, and Yu Zhang. 2018. Cross-lingual knowledge graph alignment via graph convolutional networks. In Pro-ceedings of the 2018 Conference on Empirical Meth-ods in Natural Language Processing , pages 349–357. Zhichun Wang, Jinjian Yang, and Xiaoju Ye. 2020. Knowledge graph alignment with entity-pair embed-ding. In EMNLP , pages 1672–1680. Y Wu, X Liu, Y Feng, Z Wang, R Yan, and D Zhao. 2019a. Relation-aware entity alignment for hetero-geneous knowledge graphs. In Proceedings of the Twenty-Eighth International Joint Conference on Ar-tificial Intelligence . International Joint Conferences on Artificial Intelligence. Yuting Wu, Xiao Liu, Yansong Feng, Zheng Wang, and Dongyan Zhao. 2019b. Jointly learning entity and relation representations for entity alignment. In 

EMNLP-IJCNLP , pages 240–249. Yuting Wu, Xiao Liu, Yansong Feng, Zheng Wang, and Dongyan Zhao. 2020. Neighborhood matching net-work for entity alignment. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics , pages 6477–6487. Zhiwen Xie, Runjie Zhu, Kunsong Zhao, Jin Liu, Guangyou Zhou, and Jimmy Xiangji Huang. 2021. Dual gated graph attention networks with dynamic iterative training for cross-lingual entity alignment. 

ACM Transactions on Information Systems (TOIS) ,40(3):1–30. Zhiwen Xie, Runjie Zhu, Kunsong Zhao, Jin Liu, Guangyou Zhou, and Xiangji Huang. 2020. A con-textual alignment enhanced cross graph attention net-work for cross-lingual entity alignment. In Proceed-ings of the 28th International Conference on Compu-tational Linguistics , pages 5918–5928. 5901 Kun Xu, Liwei Wang, Mo Yu, Yansong Feng, Yan Song, Zhiguo Wang, and Dong Yu. 2019. Cross-lingual knowledge graph alignment via graph matching neu-ral network. In Proceedings of the 57th Annual Meet-ing of the Association for Computational Linguistics ,pages 3156–3161. Zhihuan Yan, Rong Peng, Yaqian Wang, and Weidong Li. 2020. Ctea: Context and topic enhanced entity alignment for knowledge graphs. Neurocomputing ,410:419–431. Hsiu-Wei Yang, Yanyan Zou, Peng Shi, Wei Lu, Jimmy Lin, and Xu Sun. 2019. Aligning cross-lingual en-tities with multi-aspect information. In EMNLP-IJCNLP , pages 4431–4441. Linyan Yang, Jingwei Cheng, Chuanhao Xu, Xihao Wang, Jiayi Li, and Fu Zhang. 2024. Attr-int: A simple and effective entity alignment framework for heterogeneous knowledge graphs. In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) , pages 6315– 6319. IEEE. Qingheng Zhang, Zequn Sun, Wei Hu, Muhao Chen, Lingbing Guo, and Yuzhong Qu. 2019. Multi-view knowledge graph embedding for entity alignment. Ziyi Zhang, Luyi Bai, and Lin Zhu. 2024. Ts-align: A temporal similarity-aware entity alignment model for temporal knowledge graphs. Information Fusion ,112:102581. Ziyue Zhong, Meihui Zhang, Ju Fan, and Chenxiao Dou. 2022. Semantics driven embedding learning for effective entity alignment. In 2022 IEEE 38th Inter-national Conference on Data Engineering (ICDE) ,pages 2127–2140. IEEE. Renbo Zhu, Meng Ma, and Ping Wang. 2021a. Raga: Relation-aware graph attention networks for global entity alignment. In PAKDD (1) , pages 501–513. Springer. Yao Zhu, Hongzhi Liu, Zhonghai Wu, and Yingpeng Du. 2021b. Relation-aware neighborhood match-ing model for entity alignment. In Proceedings of the AAAI Conference on Artificial Intelligence , vol-ume 35, pages 4749–4756.