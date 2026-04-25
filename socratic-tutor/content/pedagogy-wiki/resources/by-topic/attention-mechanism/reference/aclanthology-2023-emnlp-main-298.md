# Source: https://aclanthology.org/2023.emnlp-main.298/
# Title: GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints
# Fetched via: trafilatura
# Date: 2026-04-09

@inproceedings{ainslie-etal-2023-gqa,
title = "{GQA}: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints",
author = "Ainslie, Joshua and
Lee-Thorp, James and
de Jong, Michiel and
Zemlyanskiy, Yury and
Lebron, Federico and
Sanghai, Sumit",
editor = "Bouamor, Houda and
Pino, Juan and
Bali, Kalika",
booktitle = "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing",
month = dec,
year = "2023",
address = "Singapore",
publisher = "Association for Computational Linguistics",
url = "https://aclanthology.org/2023.emnlp-main.298/",
doi = "10.18653/v1/2023.emnlp-main.298",
pages = "4895--4901",
abstract = "Multi-query attention (MQA), which only uses a single key-value head, drastically speeds up decoder inference. However, MQA can lead to quality degradation, and moreover it may not be desirable to train a separate model just for faster inference. We (1) propose a recipe for uptraining existing multi-head language model checkpoints into models with MQA using 5{\%} of original pre-training compute, and (2) introduce grouped-query attention (GQA), a generalization of multi-query attention which uses an intermediate (more than one, less than number of query heads) number of key-value heads. We show that uptrained GQA achieves quality close to multi-head attention with comparable speed to MQA."
}
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="ainslie-etal-2023-gqa">
<titleInfo>
<title>GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints</title>
</titleInfo>
<name type="personal">
<namePart type="given">Joshua</namePart>
<namePart type="family">Ainslie</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">James</namePart>
<namePart type="family">Lee-Thorp</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Michiel</namePart>
<namePart type="family">de Jong</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Yury</namePart>
<namePart type="family">Zemlyanskiy</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Federico</namePart>
<namePart type="family">Lebron</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Sumit</namePart>
<namePart type="family">Sanghai</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<originInfo>
<dateIssued>2023-12</dateIssued>
</originInfo>
<typeOfResource>text</typeOfResource>
<relatedItem type="host">
<titleInfo>
<title>Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing</title>
</titleInfo>
<name type="personal">
<namePart type="given">Houda</namePart>
<namePart type="family">Bouamor</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Juan</namePart>
<namePart type="family">Pino</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Kalika</namePart>
<namePart type="family">Bali</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<originInfo>
<publisher>Association for Computational Linguistics</publisher>
<place>
<placeTerm type="text">Singapore</placeTerm>
</place>
</originInfo>
<genre authority="marcgt">conference publication</genre>
</relatedItem>
<abstract>Multi-query attention (MQA), which only uses a single key-value head, drastically speeds up decoder inference. However, MQA can lead to quality degradation, and moreover it may not be desirable to train a separate model just for faster inference. We (1) propose a recipe for uptraining existing multi-head language model checkpoints into models with MQA using 5% of original pre-training compute, and (2) introduce grouped-query attention (GQA), a generalization of multi-query attention which uses an intermediate (more than one, less than number of query heads) number of key-value heads. We show that uptrained GQA achieves quality close to multi-head attention with comparable speed to MQA.</abstract>
<identifier type="citekey">ainslie-etal-2023-gqa</identifier>
<identifier type="doi">10.18653/v1/2023.emnlp-main.298</identifier>
<location>
<url>https://aclanthology.org/2023.emnlp-main.298/</url>
</location>
<part>
<date>2023-12</date>
<extent unit="page">
<start>4895</start>
<end>4901</end>
</extent>
</part>
</mods>
</modsCollection>
%0 Conference Proceedings
%T GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints
%A Ainslie, Joshua
%A Lee-Thorp, James
%A de Jong, Michiel
%A Zemlyanskiy, Yury
%A Lebron, Federico
%A Sanghai, Sumit
%Y Bouamor, Houda
%Y Pino, Juan
%Y Bali, Kalika
%S Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing
%D 2023
%8 December
%I Association for Computational Linguistics
%C Singapore
%F ainslie-etal-2023-gqa
%X Multi-query attention (MQA), which only uses a single key-value head, drastically speeds up decoder inference. However, MQA can lead to quality degradation, and moreover it may not be desirable to train a separate model just for faster inference. We (1) propose a recipe for uptraining existing multi-head language model checkpoints into models with MQA using 5% of original pre-training compute, and (2) introduce grouped-query attention (GQA), a generalization of multi-query attention which uses an intermediate (more than one, less than number of query heads) number of key-value heads. We show that uptrained GQA achieves quality close to multi-head attention with comparable speed to MQA.
%R 10.18653/v1/2023.emnlp-main.298
%U https://aclanthology.org/2023.emnlp-main.298/
%U https://doi.org/10.18653/v1/2023.emnlp-main.298
%P 4895-4901
Markdown (Informal)
[GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://aclanthology.org/2023.emnlp-main.298/) (Ainslie et al., EMNLP 2023)
ACL