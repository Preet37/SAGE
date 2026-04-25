# Card: Convolution / Pooling / Transposed Conv Output-Size Arithmetic
**Source:** https://arxiv.org/pdf/1603.07285.pdf  
**Role:** explainer | **Need:** FORMULA_SOURCE  
**Anchor:** Output-size formulas for conv/pooling/transposed conv (incl. padding/stride/dilation), with canonical “same/full” cases.

## Key Content
- **Per-axis independence (Sec. 2):** compute output size separately for each axis \(j\) using input \(i_j\), kernel/window \(k_j\), stride \(s_j\), padding \(p_j\). (Paper often shows square 2D case: \(i,k,s,p\).)
- **Direct convolution output size**
  - **No padding, stride 1 (Rel. 1):** \(o = (i-k)+1\).
  - **Padding \(p\), stride 1 (Rel. 2):** \(o = (i-k)+2p+1\) (effective input \(i+2p\)).
  - **“Same” / half padding, stride 1, odd \(k=2n+1\) (Rel. 3):** \(p=\lfloor k/2\rfloor=n \Rightarrow o=i\).
  - **“Full” padding, stride 1 (Rel. 4):** \(p=k-1 \Rightarrow o=i+(k-1)\).
  - **No padding, stride \(s\) (Rel. 5):** \(o=\left\lfloor\frac{i-k}{s}\right\rfloor+1\).
  - **General padding + stride (Rel. 6):** \(o=\left\lfloor\frac{i+2p-k}{s}\right\rfloor+1\).
- **Pooling output size (Sec. 3, Rel. 7):** same as strided conv without padding: \(o=\left\lfloor\frac{i-k}{s}\right\rfloor+1\).
- **Transposed convolution output size**
  - **Stride 1 (Rel. 9):** for conv with kernel \(k\), padding \(p\): transposed has \(p' = k-p-1\), output \(o' = i' + (k-1) - 2p\). Special cases:  
    - **No padding (Rel. 8):** \(p=0 \Rightarrow p'=k-1,\ o'=i'+(k-1)\).  
    - **Same padding (Rel. 10):** \(p=\lfloor k/2\rfloor \Rightarrow o'=i'\).  
    - **Full padding (Rel. 11):** \(p=k-1 \Rightarrow p'=0,\ o'=i'-(k-1)\).
  - **Stride \(s>1\) (Rel. 14):** \(o' = s(i'-1) + a + k - 2p\), where \(a=(i+2p-k)\bmod s\) (disambiguates cases); conceptual “stretching” inserts \(s-1\) zeros between input units.
- **Dilated conv (Sec. 5.1):** effective kernel \(\hat{k}=k+(k-1)(d-1)\); output (Rel. 15):  
  \(o=\left\lfloor\frac{i+2p-k-(k-1)(d-1)}{s}\right\rfloor+1\).

## When to surface
Use when students ask “what is the output shape?” for conv/pooling/transposed conv (incl. SAME/FULL padding, stride effects, dilation, or why transposed conv needs inserted zeros / output ambiguity for \(s>1\)).