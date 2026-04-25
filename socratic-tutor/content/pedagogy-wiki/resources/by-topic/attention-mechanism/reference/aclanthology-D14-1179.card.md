# Card: Seq2Seq conditional likelihood + fixed-context bottleneck (Cho et al., 2014)
**Source:** https://aclanthology.org/D14-1179/  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Canonical encoder–decoder conditional likelihood objective \(p(\mathbf{y}\mid\mathbf{x})=\prod_t p(y_t\mid y_{<t},\mathbf{x})\), trained with teacher-forced conditioning on gold prefixes; motivation for the fixed-vector context bottleneck.

## Key Content
- **Model factorization (Seq2Seq NLL objective)**: For input sequence \(\mathbf{x}=(x_1,\dots,x_{T_x})\) and output \(\mathbf{y}=(y_1,\dots,y_{T_y})\),
  \[
  p(\mathbf{y}\mid \mathbf{x})=\prod_{t=1}^{T_y} p(y_t \mid y_{<t}, \mathbf{x})
  \]
  where \(y_{<t}=(y_1,\dots,y_{t-1})\). Training maximizes \(\log p(\mathbf{y}\mid\mathbf{x})=\sum_t \log p(y_t\mid y_{<t},\mathbf{x})\) over paired data \((\mathbf{x},\mathbf{y})\). (Core encoder–decoder objective; see model description sections.)
- **Encoder–decoder workflow**:
  - **Encoder RNN** reads \(\mathbf{x}\) sequentially and compresses it into a **fixed-dimensional context vector** \(c\) (often the final hidden state or a function of hidden states).
  - **Decoder RNN** generates tokens autoregressively: at step \(t\), it conditions on \(c\) and previous target tokens \(y_{<t}\) to produce \(p(y_t\mid y_{<t},c)\).
- **Teacher forcing (training procedure)**: During training, the decoder is conditioned on the **gold** previous tokens \(y_{<t}\) when predicting \(y_t\) (i.e., uses ground-truth prefixes rather than its own sampled outputs).
- **Design rationale: fixed-vector bottleneck**: Compressing all source information into a single vector \(c\) creates an **information bottleneck**, making long/complex sequences harder (long-range dependencies must be stored in \(c\)); this motivates later mechanisms (e.g., attention) that relax the fixed-context constraint.

## When to surface
Use when students ask how seq2seq models define \(p(\mathbf{y}\mid\mathbf{x})\), what “teacher forcing” means mathematically, or why early encoder–decoder models struggle with long inputs due to the fixed context vector bottleneck.