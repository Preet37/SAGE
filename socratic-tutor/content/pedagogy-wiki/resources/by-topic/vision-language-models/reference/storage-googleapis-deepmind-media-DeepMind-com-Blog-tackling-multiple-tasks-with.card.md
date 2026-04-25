# Card: Flamingo — Perceiver Resampler & Gated Cross-Attention (XATTN-DENSE)
**Source:** https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Exact definitions of the Perceiver Resampler and the Flamingo gated cross-attention block (gating + insertion in LM stack)

## Key Content
- **Interleaved conditional LM objective (Eq. 1, Section 3):**  
  \[
  p(y\mid x)=\prod_{\ell=1}^{L} p\big(y_\ell \mid y_{<\ell}, x_{\le \ell}\big)
  \]
  where \(y_\ell\) is the \(\ell\)-th text token, \(y_{<\ell}\) preceding tokens, and \(x_{\le \ell}=\{x_i\mid i\le \phi(\ell)\}\) are images/videos preceding token \(\ell\) in the interleaved sequence.
- **Per-image/video attention indexing (Section 3.1.3):** define \(\phi:[1,L]\to[0,N]\) = index of the **last** image/video before token position \(\ell\) (0 if none). Cross-attn is masked so token \(\ell\) attends only to visual tokens of image/video \(x_{\phi(\ell)}\) (Fig. 6). Authors report this works better than attending to all previous images directly.
- **Perceiver Resampler algorithm (Fig. 4, Section 3.1.1):** input visual features \(x_f\in\mathbb{R}^{[T,S,d]}\) (time, space, dim), learned latents \(x\in\mathbb{R}^{[R,d]}\). Add learned **time** embeddings, flatten \([T,S,d]\to[T\!\cdot\!S,d]\). For each layer \(i\):  
  \(x \leftarrow x + \text{attn}_i(q=x,\ kv=\text{concat}([x_f,x]))\); then \(x \leftarrow x + \text{ffw}_i(x)\). Output is fixed \(R\) visual tokens (in practice **64**).
- **Gated XATTN-DENSE block (Fig. 5, Section 3.1.2):** inserted **between frozen pretrained LM layers**. For language features \(y\), visual tokens \(x\):  
  1) \(y \leftarrow y + \tanh(\alpha_{\text{xattn}})\cdot \text{attn}(q=y, kv=x)\)  
  2) \(y \leftarrow y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
  with learnable scalars \(\alpha_{\text{xattn}},\alpha_{\text{dense}}\) **initialized at 0** so the model initially matches the frozen LM; improves stability/performance.
- **Defaults/data pipeline snippets:** M3W training subsequence \(L=256\) tokens, up to \(N=5\) images; images resized \(320\times320\). Video frames sampled at **1 FPS**; paired-video uses \(T=8\) frames. Special token **<EOC>** added; literal “`<image>`” tag inserted in text.

## When to surface
Use when students ask: “How does Flamingo fuse vision into a frozen LM?”, “What is the Perceiver Resampler exactly?”, “What is the gating formula / where is cross-attention inserted?”, or “How does Flamingo handle multiple interleaved images/videos with causal masking?”