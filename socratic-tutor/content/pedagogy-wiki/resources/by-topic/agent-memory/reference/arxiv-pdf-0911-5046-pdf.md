# Source: https://arxiv.org/pdf/0911.5046.pdf
# Author: Joaquín Pérez-Iglesias et al.
# Title: BM25 and Beyond: Implementing and Evaluating a Search Engine (BM25 ranking functions compilation/implementation notes)
# Fetched via: jina
# Date: 2026-04-09

Title: 0911.5046v2.pdf



Number of Pages: 6

> arXiv:0911.5046v2 [cs.IR] 1 Dec 2009

# Integrating the Probabilistic Model BM25/BM25F into Lucene. 

Joaqu´ ın P´ erez-Iglesias 1, Jos´ e R. P´ erez-Ag¨ uera 2, V´ ıctor Fresno 1 and Yuval Z. Feinstein 3 

> 1

NLP&IR Group, Universidad Nacional de Educaci´ on a Distancia, Spain  

> 2

University of North Carolina at Chapel Hill, USA  

> 3

Answers Corporation, Jerusalem 91481, Israel 

joaquin.perez@lsi.uned.es, jaguera@email.unc.edu, vfresno@lsi.uned.es, yuvalf@answers.com 

Abstract. This document describes the BM25 and BM25F implemen-tation using the Lucene Java Framework. The implementation described here can be downloaded from [ P´ erez-Iglesias 08a ]. Both models have stood out at TREC by their performance and are considered as state-of-the-art in the IR community. BM25 is applied to retrieval on plain text documents, that is for documents that do not contain fields, while BM25F is applied to documents with structure. 

## Introduction 

Apache Lucene is a high-performance and full-featured text search engine library written entirely in Java. It is a technology suitable for nearly any application that requires full-text search. Lucene is scalable and offers high-performance indexing, and has become one of the most used search engine libraries in both academia and industry [ Lucene 09 ]. Lucene ranking function, the core of any search engine applied to determine how relevant a document is to a given query, is built on a combination of the Vector Space Model (VSM) and the Boolean model of Information Retrieval. The main idea behind Lucene approach is the more times a query term appears in a document relative to the number of times the term appears in the whole collection, the more relevant that document will be to the query [ Lucene 09 ]. Lucene uses also the Boolean model to first narrow down the documents that need to be scored based on the use of boolean logic in the query specification. In this paper, the implementation of BM25 probabilistic model and its ex-tension for semi-structured IR, BM25F, is described in detail. One of the main Lucene’s constraints to be widely used by IR community is the lack of different retrieval models implementations. Our goal with this work is to offer to IR community a more advanced ranking model which can be compared with other IR software, like Terrier, Lemur, CLAIRlib or Xapian. 1 Motivation 

There exists previous implementations of alternative Information Retrieval Mod-els for Lucene. The most representative case of that is the Language Model im-plementation 4 from Intelligent Systems Lab Amsterdam. Another example is described at [ Doron 07 ] where Lucene is compared with Juru system. In this case Lucene document length normalization is changed in order to improve the Lucene ranking function performance. BM25 has been widely use by IR researchers and engineers to improve search engine relevance, so from our point of view, a BM25/BM25F implementation for Lucene becomes necessary to make Lucene more popular for IR community. 

## Included Models 

The developed models are based in the information that can be found at [ Robertson 07 ]. More specifically the implemented ranking functions are as next: 

BM25 

R(q, d ) = ∑

> t∈q

occurs dt

k1((1 − b) + b ld 

> avl d

) + occurs dt

where occurs dt is the term frequency of t in d; ld is the document d length; avl d is the document average length along the collection; k1 is a free parameter usually chosen as 2 and b ∈ [0 , 1] (usually 0.75). Assigning 0 to b is equivalent to avoid the process of normalisation and therefore the document length will not affect the final score. If b takes 1, we will be carrying out a full length normalisation. The classical inverse document frequency is computed as next: 

idf (t) = log N − df (t) + 0 .5

df (t) + 0 .5where N is the number of documents in the collection and df is the number of documents where appears the term t.A different version of this formula, as can be found at Wikipedia 5, multiplies the obtained bm25 weight by the constant ( k1 + 1) in order to normalize the weight of terms with a frequency equals to 1 that occurs in documents with an average length. 

BM25F 

First we obtain the accumulated weight of a term over all fields as next:      

> 4http://ilps.science.uva.nl/resources/lm-lucene
> 5http://en.wikipedia.org/wiki/Probabilistic relevance model (BM25)

weight(t,d) = ∑

> c in d

occurs dt,c · boost c

((1 − bc) + bc · lc 

> avl c

)where lc is the field length; avl c is the average length for the field c; bc is a constant related to the field length, similar to b in BM25 and boost c is the boost factor applied to field c.Next, a non-linear saturation weight  

> k1+weight

, in order to reduce the effect of term frequency to the final score is applied. 

R(q,d) = ∑

> t in q

idf (t) · weight (t, d )

k1 + weight (t, d ) (1) 

idf (t) is computed as in the BM25 case 

idf (t) = log N − df (t) + 0 .5

df (t) + 0 .5 (2) where N is the number of documents in the collection and df is the number of documents where appears the term t.

Implementation 

The main goal of this implementation was to integrate the new ranking model into the search Lucene functionalities. In order to accomplish this objective a new Query, Weight, and several Scorers were developed. The main functional-ities are implemented at Scorer level, since the main responsibilities of Query and Weight are to prepare the necessary parameters for the Scorers, and create Scorers instances when the search method is invoked. More information in the Query-Weight-Scorer model can be found at .

Query The execution of a query can be divided in two parts, a boolean filtering and the documents ranking. The boolean filtering is carried out by the Scorers ShouldBooleanScorer, MustBooleanScorer and NotBooleanScorer depending on the logic operators applied, while ranking functions are implemented in the score method of BM25TermScorer and BM25FTermScorer. BM25BooleanScorer will create BM25TermScorer or BM25FTermScorer in-stances depending on the invoked constructor, as next: 

– To use BM25 ranking function 

public BM25BooleanQuery(String query, String field, Analyzer analyzer) throws ParseException, IOException 

– To use BM25F ranking function public BM25BooleanQuery(String query, String[] fields, Analyzer analyzer) throws ParseException,IOException 

BM25BooleanScorer will ignore any information related to fields that is treated by Lucene QueryParser, thus the search will be carried out only with the field(s), passed as parameters in the constructor. Besides only boolean queries are supported, any other query type will be split into terms and executed as a boolean query. It should be noted that both ranking functions do not use query weights, therefore all computation can be done at scorer level. 

Scoring – Almost all necessary information in order to compute BM25 relevance can be obtained through the Lucene expert API (termdocs, numdocs, docfreq,...), apart from the document average length that can not be obtained directly from the API supplied. This value, can be obtained at index time, implement-ing a specific Similarity that counts and store the length of the document fields. As next 

public class CollectionSimilarityIndexer extends DefaultSimilarity { private static Map< String,Long> length = new HashMap<String, Long>(); @Override public float lengthNorm(String fieldName, int numTokens) { Long aux = CollectionSimilarityIndexer.length.get(fieldName); if (aux==null) aux = new Long(0); aux+=numTokens; CollectionSimilarityIndexer.length.put(fieldName,aux); return super.lengthNorm(fieldName, numTokens); }public static long getLength(String field){ return CollectionSimilarityIndexer.length.get(field); }}

After the indexing process we can retrieve the length of a specific field, and following can be divided by collection numdocs and save the com-puted value to a file. This value can be read when a Searcher is opened. In the provided implementation a method load(String filePath) is supplied in BM25Parameters in order to load average lengths, more details about the file format can be found in the javadoc documentation at [ P´ erez-Iglesias 08b ]. 

– The specific BM25 parameters are fixed within the BM25Parameters class, where by default are set at k1 = 2 and b = 0 .75. The BM25F case is more complex, since it needs more specific parameters, mainly an array of string that includes the fields where the term should be searched. All the parame-ters can be found at BM25FParameters, the same k1 is applied. Related to 

b is set to 0.75 for each field, but is recommended to use better parameters (supplied as a float array) that can be set when the Query is initialised. Fix-ing boost for each field is carried out in a similar fashion, these have been initialised with a value of 1, but it may be supplied with a float array. All BM25F based arrays parameters as boost f ield and bf ield must be supplied ordered, that means that for field i into the array of fields, the boost and the 

b parameter for that field will be at i position in both arrays. 

– In both models IDF is computed in BM25Similarity and must be calculated at document level with docFreq and numdocs . Lucene returns docFreq at field level,that is the number of fields (within documents) where a term t

appears. This functionality is not a problem for BM25 since the search is accomplished just in a field. For the BM25F case this is a serious problem, because IDF can not be computed at document level, unless a new field that contains all terms is indexed. The supplied implementation (as an heuristic) computes docFreq in the field with the longest average length. 

How to use it 

The supplied implementation can be used in a similar way as searches are car-ried out with Lucene, except that BM25Parameters or BM25FParameters must be set before the query is executed, this has to be done in order to set the average length(s) , other parameters can be omitted since they are set to default values. Examples of the BM25 and BM25F raking function appear below: 

BM25 

IndexSearcher searcher = new IndexSearcher("IndexPath"); //Load average length BM25Parameters.load(avgLengthPath); BM25BooleanQuery query = new BM25BooleanQuery("This is my Query", "Search-Field", new StandardAnalyzer()); TopDocs top = searcher.search(query, null, 10); ScoreDoc[] docs = top.scoreDocs; //Print results for (int i = 0; i $<$ top.scoreDocs.length; i++) { System.out.println(docs[i].doc + ":"+docs[i].score); }BM25F 

String[] fields ={"FIELD1","FIELD2"}; IndexSearcher searcher = new IndexSearcher("IndexPath"); //Set explicit average Length for each field BM25FParameters.setAverageLength("FIELD1", 123.5f); BM25FParameters.setAverageLength("FIELD2", 42.2f); //Set explicit k1 parameter BM25FParameters.setK1(1.2f); //Using boost and b defaults parameters BM25BooleanQuery queryF = new BM25BooleanQuery("This is my query", fields, new StandardAnalyzer()); //Retrieving NOT normalized scorer values TopDocs top = searcher.search(queryF, null, 10); ScoreDoc[] docs = top.scoreDocs; //Print results for (int i = 0; i $<$ top.scoreDocs.length; i++) { System.out.println(docs[i].doc + ":"+docs[i].score); }

## Acknowledgement 

Authors want to thank Hugo Zaragoza for his review and comments. 

## References 

Lucene 09. Website. http://lucene.apache.org/java/docs/ .Robertson 07. Stephen Robertson, Hugo Zaragoza The Probabilistic Relevance Model: BM25 and beyond . The 30th Annual International ACM SIGIR Conference 23-27 July 2007, Amsterdam P´ erez-Iglesias 08a. Integrating BM25 & BM25F into Lucene . Website 2008. 

http:nlp.uned.es jpereziLucene-BM25jarmodels.jar 

P´ erez-Iglesias 08b. Integrating BM25 & BM25F into Lucene - Javadoc . Website 2008. 

http://nlp.uned.es/ jperezi/Lucene-BM25/javadoc 

Doron 07. Doron Cohen, Einat Amitay and David Carmel Lucene and Juru at TREC 2007 : 1 -Million Queries Track , TREC 2007, http://trec.nist.gov/pubs/trec16/papers/ibm-haifa.mq.final.pdf ]