# Source: https://blog.paperspace.com/introduction-to-neural-machine-translation/
# Title: Introduction to Neural Machine Translation with Bahdanau's Attention

Self-attention, also known as intra-attention, relates different positions of
a single sequence in order to compute a representation of that sequence.

In the original Transformer paper, self-attention is used in three ways:
encoder self-attention, decoder self-attention (masked), and encoder-decoder
cross-attention.

Masked self-attention ensures that predictions for position i can depend only
on the known outputs at positions less than i, preserving the autoregressive
property needed for generation.

This content is a test fixture for self-attention concepts including masked
self-attention and cross-attention relationships for testing purposes only.
