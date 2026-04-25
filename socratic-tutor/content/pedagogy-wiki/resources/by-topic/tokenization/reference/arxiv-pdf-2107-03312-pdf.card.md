# Card: SoundStream RVQ tokenization & bitrate–quality benchmarks
**Source:** https://arxiv.org/pdf/2107.03312.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Bitrate ↔ perceptual/objective quality curves; RVQ ablations (Nq, codebook size); comparisons vs Opus/EVS/Lyra; scalable (dropout) vs bitrate-specific.

## Key Content
- **Encoder frame rate / bitrate math (Sec. III-A, III-C):** With sampling rate \(f_s=24\,\text{kHz}\) and total stride \(M\), frames/sec \(S=f_s/M\). Default strides \((2,4,5,8)\Rightarrow M=320\Rightarrow S=75\) frames/sec (13.3 ms/frame). Bits/frame \(r=R/S\). Example \(R=6000\) bps ⇒ \(r=80\) bits/frame.
- **Plain VQ infeasible (Sec. III-C):** single codebook size \(N=2^r\). At \(r=80\), \(N=2^{80}\) vectors (infeasible).
- **Residual Vector Quantization algorithm (Alg. 1):** For quantizers \(Q_i\), \(i=1..N_q\):  
  init \(\hat y=0\), residual \(=y=\text{enc}(x)\); loop: \(\hat y \mathrel{+}=Q_i(\text{residual})\); residual \(\mathrel{-}=Q_i(\text{residual})\). Output \(\hat y\).  
  Rate split: \(r_i=r/N_q=\log_2 N\) (uniform); total bits/frame \(=N_q\log_2 N\).
- **Bitrate scalability via quantizer dropout (Sec. III-C):** sample \(n_q\sim\text{Uniform}\{1..N_q\}\) per example; use only \(Q_1..Q_{n_q}\). At inference choose \(n_q\) for desired bitrate; embedding dimensionality unchanged (additive refinement).
- **Training objective (Eq. 1–6):** hinge GAN discriminator loss \(L_D\) (Eq.1), generator adversarial \(L_G^{adv}\) (Eq.2), feature loss \(L_G^{feat}\) (Eq.3), multi-scale mel-spectrogram recon \(L_G^{rec}\) (Eq.4–5). Weights: \(\lambda_{adv}=1,\lambda_{feat}=100,\lambda_{rec}=1\) (Eq.6).
- **Subjective benchmark (Fig. 5):** SoundStream **3 kbps** significantly > Opus **6 kbps** and EVS **5.9 kbps**; to match SoundStream quality: **EVS ≥9.6 kbps**, **Opus ≥12 kbps** (≈3.2×–4× more bits). SoundStream @3 kbps > Lyra @3 kbps.
- **Objective metric:** ViSQOL used; at **3 kbps** ViSQOL ≈ **3.76**; at **6 kbps** ≈ **3.96**; quality remains > **3.7** even at lowest bitrate (Fig.7a).
- **Ablation—learned encoder matters (Sec. V-D):** replacing encoder with fixed mel-filterbank drops ViSQOL **3.96 → 3.33** at 6 kbps.
- **RVQ depth vs codebook (Table II, 6 kbps):**  
  \(N_q=8,N=1024\): ViSQOL **4.01±0.03**; \(N_q=16,N=32\): **3.98±0.03**; \(N_q=80,N=2\): **3.92±0.03**.
- **Latency trade-off (Table III, 6 kbps):** strides \((1,4,5,8)\) latency **7.5 ms**, \(N_q=4\), ViSQOL **4.01±0.02**; default \((2,4,5,8)\) **13 ms**, \(N_q=8\), **4.01±0.03**; \((4,4,5,8)\) **26 ms**, \(N_q=16\), **4.01±0.03**.

## When to surface
Use when students ask how RVQ enables “audio tokenization” at fixed bitrate, how bitrate maps to tokens/frame, or when comparing neural codecs’ quality vs Opus/EVS/Lyra and discussing scalable (dropout) vs bitrate-specific models.