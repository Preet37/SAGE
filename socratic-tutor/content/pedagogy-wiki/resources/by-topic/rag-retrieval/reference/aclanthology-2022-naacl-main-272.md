# Source: https://aclanthology.org/2022.naacl-main.272/
# Title: ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction
# Fetched via: trafilatura
# Date: 2026-04-09

@inproceedings{santhanam-etal-2022-colbertv2,
title = "{C}ol{BERT}v2: Effective and Efficient Retrieval via Lightweight Late Interaction",
author = "Santhanam, Keshav and
Khattab, Omar and
Saad-Falcon, Jon and
Potts, Christopher and
Zaharia, Matei",
editor = "Carpuat, Marine and
de Marneffe, Marie-Catherine and
Meza Ruiz, Ivan Vladimir",
booktitle = "Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies",
month = jul,
year = "2022",
address = "Seattle, United States",
publisher = "Association for Computational Linguistics",
url = "https://aclanthology.org/2022.naacl-main.272/",
doi = "10.18653/v1/2022.naacl-main.272",
pages = "3715--3734",
abstract = "Neural information retrieval (IR) has greatly advanced search and other knowledge-intensive language tasks. While many neural IR methods encode queries and documents into single-vector representations, late interaction models produce multi-vector representations at the granularity of each token and decompose relevance modeling into scalable token-level computations. This decomposition has been shown to make late interaction more effective, but it inflates the space footprint of these models by an order of magnitude. In this work, we introduce ColBERTv2, a retriever that couples an aggressive residual compression mechanism with a denoised supervision strategy to simultaneously improve the quality and space footprint of late interaction. We evaluate ColBERTv2 across a wide range of benchmarks, establishing state-of-the-art quality within and outside the training domain while reducing the space footprint of late interaction models by 6{--}10x."
}
<?xml version="1.0" encoding="UTF-8"?>
<modsCollection xmlns="http://www.loc.gov/mods/v3">
<mods ID="santhanam-etal-2022-colbertv2">
<titleInfo>
<title>ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction</title>
</titleInfo>
<name type="personal">
<namePart type="given">Keshav</namePart>
<namePart type="family">Santhanam</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Omar</namePart>
<namePart type="family">Khattab</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Jon</namePart>
<namePart type="family">Saad-Falcon</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Christopher</namePart>
<namePart type="family">Potts</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Matei</namePart>
<namePart type="family">Zaharia</namePart>
<role>
<roleTerm authority="marcrelator" type="text">author</roleTerm>
</role>
</name>
<originInfo>
<dateIssued>2022-07</dateIssued>
</originInfo>
<typeOfResource>text</typeOfResource>
<relatedItem type="host">
<titleInfo>
<title>Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies</title>
</titleInfo>
<name type="personal">
<namePart type="given">Marine</namePart>
<namePart type="family">Carpuat</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Marie-Catherine</namePart>
<namePart type="family">de Marneffe</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<name type="personal">
<namePart type="given">Ivan</namePart>
<namePart type="given">Vladimir</namePart>
<namePart type="family">Meza Ruiz</namePart>
<role>
<roleTerm authority="marcrelator" type="text">editor</roleTerm>
</role>
</name>
<originInfo>
<publisher>Association for Computational Linguistics</publisher>
<place>
<placeTerm type="text">Seattle, United States</placeTerm>
</place>
</originInfo>
<genre authority="marcgt">conference publication</genre>
</relatedItem>
<abstract>Neural information retrieval (IR) has greatly advanced search and other knowledge-intensive language tasks. While many neural IR methods encode queries and documents into single-vector representations, late interaction models produce multi-vector representations at the granularity of each token and decompose relevance modeling into scalable token-level computations. This decomposition has been shown to make late interaction more effective, but it inflates the space footprint of these models by an order of magnitude. In this work, we introduce ColBERTv2, a retriever that couples an aggressive residual compression mechanism with a denoised supervision strategy to simultaneously improve the quality and space footprint of late interaction. We evaluate ColBERTv2 across a wide range of benchmarks, establishing state-of-the-art quality within and outside the training domain while reducing the space footprint of late interaction models by 6–10x.</abstract>
<identifier type="citekey">santhanam-etal-2022-colbertv2</identifier>
<identifier type="doi">10.18653/v1/2022.naacl-main.272</identifier>
<location>
<url>https://aclanthology.org/2022.naacl-main.272/</url>
</location>
<part>
<date>2022-07</date>
<extent unit="page">
<start>3715</start>
<end>3734</end>
</extent>
</part>
</mods>
</modsCollection>
%0 Conference Proceedings
%T ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction
%A Santhanam, Keshav
%A Khattab, Omar
%A Saad-Falcon, Jon
%A Potts, Christopher
%A Zaharia, Matei
%Y Carpuat, Marine
%Y de Marneffe, Marie-Catherine
%Y Meza Ruiz, Ivan Vladimir
%S Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies
%D 2022
%8 July
%I Association for Computational Linguistics
%C Seattle, United States
%F santhanam-etal-2022-colbertv2
%X Neural information retrieval (IR) has greatly advanced search and other knowledge-intensive language tasks. While many neural IR methods encode queries and documents into single-vector representations, late interaction models produce multi-vector representations at the granularity of each token and decompose relevance modeling into scalable token-level computations. This decomposition has been shown to make late interaction more effective, but it inflates the space footprint of these models by an order of magnitude. In this work, we introduce ColBERTv2, a retriever that couples an aggressive residual compression mechanism with a denoised supervision strategy to simultaneously improve the quality and space footprint of late interaction. We evaluate ColBERTv2 across a wide range of benchmarks, establishing state-of-the-art quality within and outside the training domain while reducing the space footprint of late interaction models by 6–10x.
%R 10.18653/v1/2022.naacl-main.272
%U https://aclanthology.org/2022.naacl-main.272/
%U https://doi.org/10.18653/v1/2022.naacl-main.272
%P 3715-3734
Markdown (Informal)
[ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://aclanthology.org/2022.naacl-main.272/) (Santhanam et al., NAACL 2022)
ACL
- Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei Zaharia. 2022.
[ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://aclanthology.org/2022.naacl-main.272/). In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 3715–3734, Seattle, United States. Association for Computational Linguistics.