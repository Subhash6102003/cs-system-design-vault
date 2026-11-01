================================================================================
  FILE 136: The Transformer Architecture: Attention is All You Need
  Section: L - AI/ML/Deep Learning/LLM/RAG
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  The Transformer architecture, introduced by Google in 2017, completely revolutionized AI. By discarding recurrent layers (RNNs/LSTMs) and relying entirely on an "Attention" mechanism, Transformers allow for massive parallelization and the modeling of extremely long-range dependencies. This architecture forms the foundation of modern Large Language Models (LLMs) like GPT, BERT, and LLaMA. You will learn the mechanics of Self-Attention (Queries, Keys, Values), Positional Encoding, and how the Encoder and Decoder blocks function.

  Prerequisites: NLP Foundations (Embeddings, Tokenization), Neural Networks (MLPs, Softmax), basic understanding of Seq2Seq limitations.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Self-Attention
    A mechanism that allows a model to look at other words in the input sequence to gather context as it processes a specific word. It answers: "When I process the word 'bank', how much attention should I pay to 'river' vs. 'money'?"

  Q, K, V (Query, Key, Value)
    The three matrices used in self-attention.
    - Query (Q): What the current token is looking for.
    - Key (K): What each token in the sequence offers.
    - Value (V): The actual content/meaning of each token.
    - Analogy: Searching YouTube. Your search term is the Query. Video titles/tags are the Keys. The video you actually watch is the Value.

  Scaled Dot-Product Attention
    The mathematical formula for attention: Attention(Q, K, V) = softmax((QK^T) / \sqrt{d_k})V. The scaling factor \sqrt{d_k} prevents the dot products from growing too large and pushing the softmax into regions with extremely small gradients.

  Multi-Head Attention
    Instead of computing attention once, the Transformer splits the Q, K, and V into multiple "heads," computes attention in parallel, and concatenates the results. This allows the model to attend to information from different representation subspaces (e.g., one head focuses on grammar, another on semantic meaning).

  Positional Encoding
    Because Transformers process all words simultaneously (no recurrence), they have no inherent sense of word order. Positional encodings (usually sine/cosine functions) are added to the input embeddings to inject positional information.

  Encoder
    A stack of layers that reads the input sequence and creates a continuous representation containing the context of the entire sequence. (Used standalone in BERT).

  Decoder
    A stack of layers that generates the output sequence one token at a time, using Masked Self-Attention (so it can't look into the future) and Cross-Attention (to look at the Encoder's output). (Used standalone in GPT).

  Pre-training Objectives
    - MLM (Masked Language Modeling): Used by BERT (Encoder-only). 15% of words are masked, and the model must predict them based on surrounding context (bidirectional).
    - CLM (Causal Language Modeling): Used by GPT (Decoder-only). The model is trained to predict the next token given all previous tokens (unidirectional).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Scaled Dot-Product Attention                                           │
  │                                                                         │
  │        Q       K                                                        │
  │         \     /                                                         │
  │         (MatMul)                                                        │
  │            |                                                            │
  │       (Scale by √d_k)                                                   │
  │            |                                                            │
  │      (Apply Mask opt.)                                                  │
  │            |                                                            │
  │        (Softmax)       V                                                │
  │            \          /                                                 │
  │             (MatMul)                                                    │
  │                |                                                        │
  │             Output                                                      │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Transformer Encoder Block                                              │
  │                                                                         │
  │            [ Output ]                                                   │
  │                ^                                                        │
  │                |                                                        │
  │        [ Layer Normalization ]                                          │
  │                | <---------------------+                                │
  │        [ Feed Forward (MLP)  ]         | (Residual Connection)          │
  │                |                       |                                │
  │                +-----------------------+                                │
  │                |                                                        │
  │        [ Layer Normalization ]                                          │
  │                | <---------------------+                                │
  │        [ Multi-Head Attention ]        | (Residual Connection)          │
  │                |                       |                                │
  │                +-----------------------+                                │
  │                |                                                        │
  │     [ Positional Encoding + Word Embedding ]                            │
  │                |                                                        │
  │            [ Input ]                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Self-Attention from Scratch (PyTorch)                                │
  │                                                                          │
  │  import torch                                                            │
  │  import torch.nn as nn                                                   │
  │  import torch.nn.functional as F                                         │
  │  import math                                                             │
  │                                                                          │
  │  class SelfAttention(nn.Module):                                         │
  │      def __init__(self, embed_size, heads):                              │
  │          super(SelfAttention, self).__init__()                           │
  │          self.embed_size = embed_size                                    │
  │          self.heads = heads                                              │
  │          self.head_dim = embed_size // heads                             │
  │                                                                          │
  │          assert (self.head_dim * heads == embed_size), "Embed size needs to be divisible by heads"│
  │                                                                          │
  │          # Linear layers to project input to Q, K, V                     │
  │          self.values = nn.Linear(embed_size, embed_size, bias=False)     │
  │          self.keys = nn.Linear(embed_size, embed_size, bias=False)       │
  │          self.queries = nn.Linear(embed_size, embed_size, bias=False)    │
  │                                                                          │
  │          # Final linear layer                                            │
  │          self.fc_out = nn.Linear(embed_size, embed_size)                 │
  │                                                                          │
  │      def forward(self, values, keys, query, mask=None):                  │
  │          # Get number of training examples                               │
  │          N = query.shape[0]                                              │
  │                                                                          │
  │          value_len, key_len, query_len = values.shape[1], keys.shape[1], query.shape[1]│
  │                                                                          │
  │          # Pass through Linear layers                                    │
  │          values = self.values(values)                                    │
  │          keys = self.keys(keys)                                          │
  │          queries = self.queries(query)                                   │
  │                                                                          │
  │          # Split embedding into self.heads pieces                        │
  │          # Shape: (N, seq_len, heads, head_dim)                          │
  │          values = values.reshape(N, value_len, self.heads, self.head_dim)│
  │          keys = keys.reshape(N, key_len, self.heads, self.head_dim)      │
  │          queries = queries.reshape(N, query_len, self.heads, self.head_dim)│
  │                                                                          │
  │          # MatMul: Q * K^T                                               │
  │          # queries shape: (N, query_len, heads, heads_dim)               │
  │          # keys shape: (N, key_len, heads, heads_dim)                    │
  │          # energy shape: (N, heads, query_len, key_len)                  │
  │          energy = torch.einsum("nqhd,nkhd->nhqk", [queries, keys])       │
  │                                                                          │
  │          # Masking (for decoder or padding)                              │
  │          if mask is not None:                                            │
  │              energy = energy.masked_fill(mask == 0, float("-1e20"))      │
  │                                                                          │
  │          # Softmax and scaling                                           │
  │          # attention shape: (N, heads, query_len, key_len)               │
  │          attention = torch.softmax(energy / math.sqrt(self.head_dim), dim=-1)│
  │                                                                          │
  │          # MatMul: Attention * V                                         │
  │          # attention shape: (N, heads, query_len, key_len)               │
  │          # values shape: (N, value_len, heads, heads_dim)                │
  │          # out shape: (N, query_len, heads, head_dim)                    │
  │          out = torch.einsum("nhql,nlhd->nqhd", [attention, values]).reshape(│
  │              N, query_len, self.embed_size                               │
  │          )                                                               │
  │                                                                          │
  │          out = self.fc_out(out)                                          │
  │          return out                                                      │
  │                                                                          │
  │  # --- Test the Self Attention ---                                       │
  │  if __name__ == "__main__":                                              │
  │      embed_size = 256                                                    │
  │      heads = 8                                                           │
  │      seq_length = 10                                                     │
  │      batch_size = 2                                                      │
  │                                                                          │
  │      attention_layer = SelfAttention(embed_size, heads)                  │
  │                                                                          │
  │      # Dummy input sequence                                              │
  │      x = torch.randn(batch_size, seq_length, embed_size)                 │
  │                                                                          │
  │      # In Self-Attention, Q, K, and V all come from the same input       │
  │      out = attention_layer(values=x, keys=x, query=x)                    │
  │      print("Self Attention Output Shape:", out.shape) # Expected: (2, 10, 256)│
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Full Transformer Block (Encoder)                                     │
  │                                                                          │
  │  import torch                                                            │
  │  import torch.nn as nn                                                   │
  │                                                                          │
  │  class TransformerBlock(nn.Module):                                      │
  │      def __init__(self, embed_size, heads, dropout, forward_expansion):  │
  │          super(TransformerBlock, self).__init__()                        │
  │                                                                          │
  │          # 1. Multi-Head Attention (Using PyTorch's optimized built-in module)│
  │          self.attention = nn.MultiheadAttention(embed_dim=embed_size, num_heads=heads, batch_first=True)│
  │                                                                          │
  │          # 2. Layer Normalization                                        │
  │          self.norm1 = nn.LayerNorm(embed_size)                           │
  │          self.norm2 = nn.LayerNorm(embed_size)                           │
  │                                                                          │
  │          # 3. Feed Forward Network                                       │
  │          self.feed_forward = nn.Sequential(                              │
  │              nn.Linear(embed_size, forward_expansion * embed_size),      │
  │              nn.GELU(), # GELU is preferred over ReLU in Transformers (BERT, GPT)│
  │              nn.Linear(forward_expansion * embed_size, embed_size)       │
  │          )                                                               │
  │                                                                          │
  │          self.dropout = nn.Dropout(dropout)                              │
  │                                                                          │
  │      def forward(self, value, key, query, mask=None):                    │
  │          # --- Attention Part ---                                        │
  │          # PyTorch MultiheadAttention expects (query, key, value)        │
  │          # It also returns attention weights, which we ignore here using _│
  │          attention_out, _ = self.attention(query, key, value, attn_mask=mask)│
  │                                                                          │
  │          # Add & Norm (Residual connection)                              │
  │          x = self.norm1(attention_out + query)                           │
  │          x = self.dropout(x)                                             │
  │                                                                          │
  │          # --- Feed Forward Part ---                                     │
  │          forward_out = self.feed_forward(x)                              │
  │                                                                          │
  │          # Add & Norm (Residual connection)                              │
  │          out = self.norm2(forward_out + x)                               │
  │          out = self.dropout(out)                                         │
  │                                                                          │
  │          return out                                                      │
  │                                                                          │
  │  if __name__ == "__main__":                                              │
  │      embed_size = 512                                                    │
  │      heads = 8                                                           │
  │      forward_expansion = 4                                               │
  │      dropout = 0.1                                                       │
  │                                                                          │
  │      block = TransformerBlock(embed_size, heads, dropout, forward_expansion)│
  │                                                                          │
  │      # Batch=32, Seq_len=128, Embed=512                                  │
  │      x = torch.randn(32, 128, 512)                                       │
  │                                                                          │
  │      # Forward pass                                                      │
  │      output = block(value=x, key=x, query=x)                             │
  │      print("Transformer Block Output:", output.shape) # Expected: (32, 128, 512)│
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: Why do Transformers use Positional Encoding?

  ANSWER:
    Unlike RNNs that process tokens sequentially step-by-step, attention mechanisms process the entire sequence in parallel (as a set). Without positional encoding, the model would treat "The dog chased the cat" exactly the same as "The cat chased the dog". Positional embeddings inject sequence order into the model.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the roles of Query, Key, and Value in Self-Attention.

  ANSWER:
    The Query is the current word looking for context. The Key represents what other words have to offer. The dot product of Query and Key determines the attention score (how relevant they are to each other). The Value is the actual semantic content of those words, which is weighted by the attention score to produce the final output.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why do we divide by \sqrt{d_k} in the scaled dot-product attention?

  ANSWER:
    As the embedding dimension d_k grows, the dot products of vectors become very large. This pushes the softmax function into regions where gradients are extremely small (vanishing gradients), making learning slow or impossible. Scaling down by \sqrt{d_k} keeps the variance of the dot products stable.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between Encoder-only, Decoder-only, and Encoder-Decoder architectures?

  ANSWER:
    - Encoder-only (BERT): Uses bidirectional attention. Great for classification, NER, understanding context.
    - Decoder-only (GPT): Uses masked unidirectional attention (can only look at past words). Great for text generation.
    - Encoder-Decoder (T5, BART): Encoder processes input, Decoder generates output based on Encoder's context. Great for translation, summarization.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the purpose of the Mask in Decoder attention?

  ANSWER:
    During training, the Decoder receives the full target sequence. Without a mask, a token could "look ahead" at future tokens (the answer) to predict the next word. The mask (a lower triangular matrix of -\infty) ensures that position i can only attend to positions \le i.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why use Multi-Head Attention instead of a single attention head with larger dimensions?

  ANSWER:
    Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. For example, one head might track grammatical relationships (subject-verb), while another tracks coreference (pronoun-noun). A single head would average these out.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the computational complexity of Self-Attention with respect to sequence length?

  ANSWER:
    It is O(N^2 \cdot d), where N is sequence length and d is embedding dimension. This quadratic complexity with respect to sequence length (N^2) is the main bottleneck for Transformers handling very long documents.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: Why do Transformers use Layer Normalization instead of Batch Normalization?

  ANSWER:
    In NLP, sequence lengths vary greatly across a batch. Batch Norm computes statistics across the batch dimension, which becomes unstable with padding and varying lengths. Layer Norm computes statistics across the features (embedding dimension) for each token independently, making it invariant to sequence length and batch size.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What are the pre-training objectives for BERT vs. GPT?

  ANSWER:
    BERT uses Masked Language Modeling (MLM - predict randomly masked words) and Next Sentence Prediction (NSP). GPT uses Causal Language Modeling (CLM - predict the next token given all previous tokens).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: Explain how the residual connections (x + f(x)) help in Transformers.

  ANSWER:
    Transformers are incredibly deep. Residual connections provide a direct, unmodified path for gradients to flow backwards through the network, preventing the vanishing gradient problem and allowing the training of models with dozens or hundreds of layers.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Peeking Decoder

  # Inside a Decoder training loop
  predictions = decoder(target_sequence)
  loss = criterion(predictions, target_sequence)

  SOLUTION:
    If a causal attention mask is not explicitly passed into the decoder's multi-head attention layer, the self-attention will peek into the future. The model will achieve 100% accuracy during training by simply copying the next token, and will fail completely during real inference.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Softmax Overflow

  # Custom attention calculation
  scores = torch.matmul(Q, K.transpose(-2, -1))
  # Missing scaling factor here!
  attention_weights = torch.softmax(scores, dim=-1)

  SOLUTION:
    Omitting / math.sqrt(d_k) causes the scores variance to scale with the dimension size. For large dimensions (e.g., 512), scores will have extreme values. Softmax will push the largest value to near 1.0 and everything else to 0.0, creating an extremely sharp distribution with near-zero gradients. The model will stop learning.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Layer Norm Placement

  # Post-LN (Original Transformer paper)
  x = self.norm1(x + self.attention(x))
  # vs Pre-LN (Modern implementations like GPT-2/3)
  x = x + self.attention(self.norm1(x))

  SOLUTION:
    Nothing is technically "wrong" syntactically, but historically significant. The original paper used Post-LayerNorm, which often requires careful learning rate warmup schedules to converge. Modern LLMs use Pre-LayerNorm because it stabilizes training gradients and allows for much deeper networks without warmup hacks.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  The LLM Era: Transformers are the architecture behind ChatGPT, Claude, Gemini, and LLaMA. Understanding this architecture is non-negotiable for modern AI engineers.
  Beyond NLP: The architecture has successfully crossed over into Computer Vision (Vision Transformers - ViT), Audio (Whisper), and structural biology (AlphaFold).
  Infrastructure Costs: Understanding the O(N^2) complexity of attention explains why generating 100,000 tokens of context is exponentially more expensive and slower than 1,000 tokens, directly driving cloud computing costs.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 137_LLM.md: How billions of parameters are added to this base architecture to create Large Language Models.
  -> File 134_RNN_LSTM_GRU.md: Compare the O(N^2) parallel attention to the O(N) sequential processing of RNNs.
  -> File 135_NLP_Foundations.md: Learn about the subword tokenization used to feed text into the embedding layer of the Transformer.

================================================================================
  END OF FILE 136
================================================================================
