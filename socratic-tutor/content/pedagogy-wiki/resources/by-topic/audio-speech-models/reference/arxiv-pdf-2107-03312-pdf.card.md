# Card: SoundStream RVQ + adversarial/perceptual training objective
**Source:** https://arxiv.org/pdf/2107.03312.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Explicit RVQ formulation + end-to-end training objective (reconstruction + adversarial/feature losses), plus bitrate/latency tradeoffs

## Key Content
- **Model pipeline (Section III):** waveform \(x\in\mathbb{R}^T\) → encoder \(y=\mathrm{enc}(x)\in\mathbb{R}^{S\times D}\) with \(S=T/M\) → residual vector quantizer \(Q(\cdot)\) → decoder \(\hat{x}=\mathrm{dec}(Q(y))\). Generator \(G(x)=\mathrm{dec}(Q(\mathrm{enc}(x)))\).
- **Architectural latency via strides (Sec. III-A):** causal convs; resampling ratio \(M=\prod \text{strides}\). Example strides \((2,4,5,8)\Rightarrow M=320\) samples → embeddings at \(24\text{kHz}/320=75\) Hz → **13.3 ms** per frame.
- **Residual Vector Quantization (Algorithm 1, Sec. III-C):**  
  Initialize \(\hat{y}=0\), \(r=y\). For \(i=1..N_q\): \(\hat{y}\mathrel{+}=Q_i(r)\); \(r\mathrel{-}=Q_i(r)\). Output \(\hat{y}\).  
  Per-frame bits \(r = N_q\log_2 N\). Example: target \(R=6000\) bps, \(S=75\) fps ⇒ \(r=80\) bits/frame; plain VQ needs \(N=2^{80}\) (infeasible). With \(N_q=8\): \(N=2^{80/8}=1024\).
- **Bitrate scalability via quantizer dropout (Sec. III-C):** sample \(n_q\sim\mathrm{Unif}\{1,\dots,N_q\}\) per example; use only \(Q_1..Q_{n_q}\). Inference chooses \(n_q\) for desired bitrate; embedding dimensionality unchanged (additive refinement).
- **Training objective (Sec. III-E):** multi-discriminator hinge GAN + feature + multi-scale mel losses.  
  Discriminator loss **Eq. (1)**:  
  \[
  L_D=\mathbb{E}_x\Big[\frac1K\sum_k\frac1{T_k}\sum_t \max(0,1-D_{k,t}(x))\Big]+\mathbb{E}_x\Big[\frac1K\sum_k\frac1{T_k}\sum_t \max(0,1+D_{k,t}(G(x)))\Big]
  \]
  Generator adversarial **Eq. (2)**: \(L_G^{adv}=\mathbb{E}_x[\frac1K\sum_{k,t}\frac1{T_k}\max(0,1-D_{k,t}(G(x)))]\).  
  Feature loss **Eq. (3)**: average \(\ell_1\) diff of discriminator internal activations \(D_k^{(l)}\).  
  Multi-scale spectral recon **Eq. (4–5):** 64-bin mel-spectrograms with window \(s\in\{2^6,\dots,2^{11}\}\), hop \(s/4\): \(\|S^s(x)-S^s(G(x))\|_1 + \alpha_s\|\log S^s(x)-\log S^s(G(x))\|_2\), \(\alpha_s=\sqrt{s/2}\).  
  Total **Eq. (6):** \(L_G=\lambda_{adv}L_G^{adv}+\lambda_{feat}L_G^{feat}+\lambda_{rec}L_G^{rec}\) with **\(\lambda_{adv}=1,\lambda_{feat}=100,\lambda_{rec}=1\)**.
- **Key empirical comparisons (Abstract + Sec. V-A):** subjective @24 kHz: **SoundStream 3 kbps > Opus 12 kbps**, approaches **EVS 9.6 kbps**; to match SoundStream@3 kbps, EVS needs ≥9.6 kbps and Opus ≥12 kbps (≈3.2–4× bits).
- **Latency/RTF tradeoff (Table III, 6 kbps):** strides \((1,4,5,8)\) latency **7.5 ms**, \(N_q=4\), RTF(enc) **1.6×**, RTF(dec) **1.5×**, ViSQOL **4.01**; \((2,4,5,8)\) latency **13 ms**, \(N_q=8\), RTF(enc) **2.4×**, RTF(dec) **2.3×**, ViSQOL **4.01**; \((4,4,5,8)\) latency **26 ms**, \(N_q=16\), RTF(enc) **4.1×**, RTF(dec) **4.0×**, ViSQOL **4.01**.
- **RVQ depth vs codebook size (Table II, 6 kbps):** \(N_q=8,N=1024\Rightarrow\) ViSQOL **4.01**; \(N_q=16,N=32\Rightarrow 3.98\); \(N_q=80,N=2\Rightarrow 3.92\).

## When to surface
Use when students ask how neural audio tokenizers/codecs (e.g., EnCodec/SoundStream) implement RVQ, compute bitrate from frames, or train with adversarial + perceptual/feature + spectral reconstruction losses, including latency/bitrate tradeoffs.