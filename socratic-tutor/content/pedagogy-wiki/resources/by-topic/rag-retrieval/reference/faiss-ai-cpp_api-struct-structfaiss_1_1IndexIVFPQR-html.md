# Source: https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexIVFPQR.html
# Title: Struct faiss::IndexIVFPQR - Faiss documentation
# Fetched via: trafilatura
# Date: 2026-04-09

Struct faiss::IndexIVFPQR[](#struct-faiss-indexivfpqr)
-
struct IndexIVFPQR : public
[faiss](../file/AdditiveQuantizer_8h.html#_CPPv45faiss)::[IndexIVFPQ](../file/IndexIVFPQ_8h.html#_CPPv4N5faiss10IndexIVFPQE) [Index](structfaiss_1_1Index.html#structfaiss_1_1Index)with an additional level of PQ refinementPublic Types
-
using component_t = float
-
using distance_t = float
Public Functions
-
IndexIVFPQR(
[Index](../file/Index_8h.html#_CPPv4N5faiss5IndexE)*quantizer, size_t d, size_t nlist, size_t M, size_t nbits_per_idx, size_t M_refine, size_t nbits_per_idx_refine)
-
virtual void reset() override
removes all elements from the database.
-
virtual size_t remove_ids(const
[IDSelector](../file/IDSelector_8h.html#_CPPv4N5faiss10IDSelectorE)&sel) override Dataset manipulation functions.
-
virtual void train_encoder(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*assign) override trains the two product quantizers
-
virtual
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)train_encoder_num_vectors() const override can be redefined by subclasses to indicate how many training vectors they need
-
virtual void add_with_ids(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*xids) override default implementation that calls encode_vectors
-
virtual void add_core(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*xids, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*precomputed_idx, void *inverted_list_context = nullptr) override same as add_with_ids, but optionally use the precomputed list ids
-
virtual void reconstruct_from_offset(int64_t list_no, int64_t offset, float *recons) const override
Reconstruct a vector given the location in terms of (inv list index + inv list offset) instead of the id.
Useful for reconstructing when the direct_map is not maintained and the inv list offset is computed by
[search_preassigned()](#structfaiss_1_1IndexIVFPQR_1a681e937fcfd9bd93cac5f9eff9d6021a)withstore_pairs
set.
-
virtual void merge_from(
[Index](../file/Index_8h.html#_CPPv4N5faiss5IndexE)&otherIndex,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)add_id) override moves the entries from another dataset to self. On output, other is empty. add_id is added to all moved ids (for sequential ids, this would be this->ntotal)
-
virtual void search_preassigned(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)k, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*assign, const float *centroid_dis, float *distances,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*labels, bool store_pairs, const[IVFSearchParameters](../file/IndexIVF_8h.html#_CPPv4N5faiss19IVFSearchParametersE)*params = nullptr,[IndexIVFStats](../file/IndexIVF_8h.html#_CPPv4N5faiss13IndexIVFStatsE)*stats = nullptr) const override search a set of vectors, that are pre-quantized by the IVF quantizer. Fill in the corresponding heaps with the query results. The default implementation uses InvertedListScanners to do the search.
- Parameters:
n – nb of vectors to query
x – query vectors, size nx * d
assign – coarse quantization indices, size nx * nprobe
centroid_dis – distances to coarse centroids, size nx * nprobe
distance – output distances, size n * k
labels – output labels, size n * k
store_pairs – store inv list index + inv list offset instead in upper/lower 32 bit of result, instead of ids (used for reranking).
params – used to override the object’s search parameters
-
IndexIVFPQR()
-
virtual void encode_vectors(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*list_nos, uint8_t *codes, bool include_listnos = false) const override Encodes a set of vectors as they would appear in the inverted lists
- Parameters:
list_nos – inverted list ids as returned by the quantizer (size n). -1s are ignored.
codes – output codes, size n * code_size
include_listno – include the list ids in the code (in this case add ceil(log8(nlist)) to the code size)
-
virtual void sa_decode(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const uint8_t *bytes, float *x) const override decode a set of vectors
- Parameters:
n – number of vectors
bytes – input encoded vectors, size n *
[sa_code_size()](structfaiss_1_1IndexIVFSpectralHash.html#structfaiss_1_1IndexIVF_1a89b7f3a7b35db764bc071aa5ab302b1d)x – output vectors, size n * d
-
void add_core_o(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*xids, float *residuals_2, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*precomputed_idx = nullptr, void *inverted_list_context = nullptr) same as add_core, also:
output 2nd level residuals if residuals_2 != NULL
accepts precomputed_idx = nullptr
-
size_t find_duplicates(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*ids, size_t *lims) const Find exact duplicates in the dataset.
the duplicates are returned in pre-allocated arrays (see the max sizes).
- Parameters:
lims – limits between groups of duplicates (max size ntotal / 2 + 1)
ids – ids[lims[i]] : ids[lims[i+1]-1] is a group of duplicates (max size ntotal)
- Returns:
n number of groups found
-
void encode(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)key, const float *x, uint8_t *code) const
-
void encode_multiple(size_t n,
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*keys, const float *x, uint8_t *codes, bool compute_keys = false) const Encode multiple vectors
- Parameters:
n – nb vectors to encode
keys – posting list ids for those vectors (size n)
x – vectors (size n * d)
codes – output codes (size n * code_size)
compute_keys – if false, assume keys are precomputed, otherwise compute them
-
void decode_multiple(size_t n, const
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*keys, const uint8_t *xcodes, float *x) const inverse of encode_multiple
-
virtual
[InvertedListScanner](../file/IndexIVF_8h.html#_CPPv4N5faiss19InvertedListScannerE)*get_InvertedListScanner(bool store_pairs, const[IDSelector](../file/IDSelector_8h.html#_CPPv4N5faiss10IDSelectorE)*sel) const override Get a scanner for this index (store_pairs means ignore labels)
The default search implementation uses this to compute the distances
-
void precompute_table()
build precomputed table
-
virtual void train(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x) override Trains the quantizer and calls train_encoder to train sub-quantizers.
-
virtual void add(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x) override Calls add_with_ids with NULL ids.
-
virtual void add_sa_codes(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const uint8_t *codes, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*xids) override Add vectors that are computed with the standalone codec
- Parameters:
codes – codes to add size n *
[sa_code_size()](structfaiss_1_1IndexIVFSpectralHash.html#structfaiss_1_1IndexIVF_1a89b7f3a7b35db764bc071aa5ab302b1d)xids – corresponding ids, size n
-
virtual void range_search_preassigned(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)nx, const float *x, float radius, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*keys, const float *coarse_dis,[RangeSearchResult](../file/AuxIndexStructures_8h.html#_CPPv4N5faiss17RangeSearchResultE)*result, bool store_pairs = false, const[IVFSearchParameters](../file/IndexIVF_8h.html#_CPPv4N5faiss19IVFSearchParametersE)*params = nullptr,[IndexIVFStats](../file/IndexIVF_8h.html#_CPPv4N5faiss13IndexIVFStatsE)*stats = nullptr) const override Range search a set of vectors, that are pre-quantized by the IVF quantizer. Fill in the RangeSearchResults results. The default implementation uses InvertedListScanners to do the search.
- Parameters:
n – nb of vectors to query
x – query vectors, size nx * d
assign – coarse quantization indices, size nx * nprobe
centroid_dis – distances to coarse centroids, size nx * nprobe
result – Output results
store_pairs – store inv list index + inv list offset instead in upper/lower 32 bit of result, instead of ids (used for reranking).
params – used to override the object’s search parameters
-
virtual void search(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)k, float *distances,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*labels, const[SearchParameters](../file/Index_8h.html#_CPPv4N5faiss16SearchParametersE)*params = nullptr) const override assign the vectors, then call search_preassign
-
virtual void range_search(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, float radius,[RangeSearchResult](../file/AuxIndexStructures_8h.html#_CPPv4N5faiss17RangeSearchResultE)*result, const[SearchParameters](../file/Index_8h.html#_CPPv4N5faiss16SearchParametersE)*params = nullptr) const override query n vectors of dimension d to the index.
return all vectors with distance < radius. Note that many indexes do not implement the range_search (only the k-NN search is mandatory).
- Parameters:
n – number of vectors
x – input vectors to search, size n * d
radius – search radius
result – result table
-
virtual void reconstruct(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)key, float *recons) const override reconstruct a vector. Works only if maintain_direct_map is set to 1 or 2
-
virtual void update_vectors(int nv, const
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*idx, const float *v) Update a subset of vectors.
The index must have a direct_map
- Parameters:
nv – nb of vectors to update
idx – vector indices to update, size nv
v – vectors of new values, size nv*d
-
virtual void reconstruct_n(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)i0,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)ni, float *recons) const override Reconstruct a subset of the indexed vectors.
Overrides default implementation to bypass
[reconstruct()](structfaiss_1_1IndexIVFSpectralHash.html#structfaiss_1_1IndexIVF_1a3b3270dcfa248dc30117644382a54e39)which requires direct_map to be maintained.- Parameters:
i0 – first vector to reconstruct
ni – nb of vectors to reconstruct
recons – output array of reconstructed vectors, size ni * d
-
virtual void search_and_reconstruct(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)k, float *distances,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*labels, float *recons, const[SearchParameters](../file/Index_8h.html#_CPPv4N5faiss16SearchParametersE)*params = nullptr) const override Similar to search, but also reconstructs the stored vectors (or an approximation in the case of lossy coding) for the search results.
Overrides default implementation to avoid having to maintain direct_map and instead fetch the code offsets through the
store_pairs
flag in[search_preassigned()](structfaiss_1_1IndexIVFSpectralHash.html#structfaiss_1_1IndexIVF_1aa5cf61c63eb9ccc68edc13fe8f5ba854).- Parameters:
recons – reconstructed vectors size (n, k, d)
-
void search_and_return_codes(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)k, float *distances,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*labels, uint8_t *recons, bool include_listno = false, const[SearchParameters](../file/Index_8h.html#_CPPv4N5faiss16SearchParametersE)*params = nullptr) const Similar to search, but also returns the codes corresponding to the stored vectors for the search results.
- Parameters:
codes – codes (n, k, code_size)
include_listno – include the list ids in the code (in this case add ceil(log8(nlist)) to the code size)
-
virtual void check_compatible_for_merge(const
[Index](../file/Index_8h.html#_CPPv4N5faiss5IndexE)&otherIndex) const override check that the two indexes are compatible (ie, they are trained in the same way and have the same parameters). Otherwise throw.
-
virtual
[CodePacker](../file/CodePacker_8h.html#_CPPv4N5faiss10CodePackerE)*get_CodePacker() const
-
virtual void copy_subset_to(
[IndexIVF](../file/IndexIVF_8h.html#_CPPv4N5faiss8IndexIVFE)&other,[InvertedLists](../file/InvertedLists_8h.html#_CPPv4N5faiss13InvertedListsE)::[subset_type_t](../file/InvertedLists_8h.html#_CPPv4N5faiss13InvertedLists13subset_type_tE)subset_type,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)a1,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)a2) const copy a subset of the entries index to the other index see Invlists::copy_subset_to for the meaning of subset_type
-
inline size_t get_list_size(size_t list_no) const
-
bool check_ids_sorted() const
are the ids sorted?
-
void make_direct_map(bool new_maintain_direct_map = true)
initialize a direct map
- Parameters:
new_maintain_direct_map – if true, create a direct map, else clear it
-
void replace_invlists(
[InvertedLists](../file/InvertedLists_8h.html#_CPPv4N5faiss13InvertedListsE)*il, bool own = false) replace the inverted lists, old one is deallocated if own_invlists
-
virtual size_t sa_code_size() const override
size of the produced codes in bytes
-
virtual void sa_encode(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x, uint8_t *bytes) const override encode a set of vectors sa_encode will call encode_vector with include_listno=true
- Parameters:
n – nb of vectors to encode
x – the vectors to encode
bytes – output array for the codes
- Returns:
nb of bytes written to codes
-
virtual void assign(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *x,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*labels,[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)k = 1) const return the indexes of the k vectors closest to the query x.
This function is identical as search but only return labels of neighbors.
- Parameters:
n – number of vectors
x – input vectors to search, size n * d
labels – output labels of the NNs, size n*k
k – number of nearest neighbours
-
virtual void reconstruct_batch(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*keys, float *recons) const Reconstruct several stored vectors (or an approximation if lossy coding)
this function may not be defined for some indexes
- Parameters:
n – number of vectors to reconstruct
keys – ids of the vectors to reconstruct (size n)
recons – reconstucted vector (size n * d)
-
virtual void compute_residual(const float *x, float *residual,
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)key) const Computes a residual vector after indexing encoding.
The residual vector is the difference between a vector and the reconstruction that can be decoded from its representation in the index. The residual can be used for multiple-stage indexing methods, like
[IndexIVF](structfaiss_1_1IndexIVF.html#structfaiss_1_1IndexIVF)’s methods.- Parameters:
x – input vector, size d
residual – output residual vector, size d
key – encoded index, as returned by search and assign
-
virtual void compute_residual_n(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)n, const float *xs, float *residuals, const[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)*keys) const Computes a residual vector after indexing encoding (batch form). Equivalent to calling compute_residual for each vector.
The residual vector is the difference between a vector and the reconstruction that can be decoded from its representation in the index. The residual can be used for multiple-stage indexing methods, like
[IndexIVF](structfaiss_1_1IndexIVF.html#structfaiss_1_1IndexIVF)’s methods.- Parameters:
n – number of vectors
xs – input vectors, size (n x d)
residuals – output residual vectors, size (n x d)
keys – encoded index, as returned by search and assign
-
virtual
[DistanceComputer](../file/DistanceComputer_8h.html#_CPPv4N5faiss16DistanceComputerE)*get_distance_computer() const Get a
[DistanceComputer](structfaiss_1_1DistanceComputer.html#structfaiss_1_1DistanceComputer)(defined in AuxIndexStructures) object for this kind of index.[DistanceComputer](structfaiss_1_1DistanceComputer.html#structfaiss_1_1DistanceComputer)is implemented for indexes that support random access of their vectors.
-
void train_q1(size_t n, const float *x, bool verbose,
[MetricType](../file/MetricType_8h.html#_CPPv4N5faiss10MetricTypeE)metric_type) Trains the quantizer and calls train_residual to train sub-quantizers.
-
size_t coarse_code_size() const
compute the number of bytes required to store list ids
-
void encode_listno(
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)list_no, uint8_t *code) const
-
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)decode_listno(const uint8_t *code) const
Public Members
-
[ProductQuantizer](../file/ProductQuantizer_8h.html#_CPPv4N5faiss16ProductQuantizerE)refine_pq 3rd level quantizer
-
[std](../namespace/namespacestd.html#_CPPv4St)::vector<uint8_t> refine_codes corresponding codes
-
float k_factor
factor between k requested in search and the k requested from the IVFPQ
-
[ProductQuantizer](../file/ProductQuantizer_8h.html#_CPPv4N5faiss16ProductQuantizerE)pq produces the codes
-
bool do_polysemous_training
reorder PQ centroids after training?
-
[PolysemousTraining](../file/PolysemousTraining_8h.html#_CPPv4N5faiss18PolysemousTrainingE)*polysemous_training if NULL, use default
-
size_t scan_table_threshold
use table computation or on-the-fly?
-
int polysemous_ht
Hamming thresh for polysemous filtering.
-
int use_precomputed_table
Precompute table that speed up query preprocessing at some memory cost (used only for by_residual with L2 metric)
-
[AlignedTable](../file/AlignedTable_8h.html#_CPPv4I0_iEN5faiss12AlignedTableE)<float> precomputed_table if use_precompute_table size nlist * pq.M * pq.ksub
-
[InvertedLists](../file/InvertedLists_8h.html#_CPPv4N5faiss13InvertedListsE)*invlists = nullptr Access to the actual data.
-
bool own_invlists = false
-
size_t code_size = 0
code size per vector in bytes
-
int parallel_mode = 0
Parallel mode determines how queries are parallelized with OpenMP
0 (default): split over queries 1: parallelize over inverted lists 2: parallelize over both 3: split over queries with a finer granularity
PARALLEL_MODE_NO_HEAP_INIT: binary or with the previous to prevent the heap to be initialized and finalized
-
const int PARALLEL_MODE_NO_HEAP_INIT = 1024
-
[DirectMap](../file/DirectMap_8h.html#_CPPv4N5faiss9DirectMapE)direct_map optional map that maps back ids to invlist entries. This enables
[reconstruct()](structfaiss_1_1IndexIVFSpectralHash.html#structfaiss_1_1IndexIVF_1a3b3270dcfa248dc30117644382a54e39)
-
bool by_residual = true
do the codes in the invlists encode the vectors relative to the centroids?
-
int d
vector dimension
-
[idx_t](../file/MetricType_8h.html#_CPPv4N5faiss5idx_tE)ntotal total nb of indexed vectors
-
bool verbose
verbosity level
-
bool is_trained
set if the
[Index](structfaiss_1_1Index.html#structfaiss_1_1Index)does not require training, or if training is done already
-
[MetricType](../file/MetricType_8h.html#_CPPv4N5faiss10MetricTypeE)metric_type type of metric this index uses for search
-
float metric_arg
argument of the metric type
-
size_t nprobe = 1
number of probes at query time
-
size_t max_codes = 0
max nb of codes to visit to do a query
-
[Index](../file/Index_8h.html#_CPPv4N5faiss5IndexE)*quantizer = nullptr quantizer that maps vectors to inverted lists
-
size_t nlist = 0
number of inverted lists
-
char quantizer_trains_alone = 0
= 0: use the quantizer as index in a kmeans training = 1: just pass on the training set to the train() of the quantizer = 2: kmeans training on a flat index + add the centroids to the quantizer
-
bool own_fields = false
whether object owns the quantizer
-
[ClusteringParameters](../file/Clustering_8h.html#_CPPv4N5faiss20ClusteringParametersE)cp to override default clustering params
-
[Index](../file/Index_8h.html#_CPPv4N5faiss5IndexE)*clustering_index = nullptr to override index used during clustering
-
using component_t = float