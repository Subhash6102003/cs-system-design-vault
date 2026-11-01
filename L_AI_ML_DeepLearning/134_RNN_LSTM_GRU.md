================================================================================
  FILE 134: Recurrent Neural Networks (RNN) & Sequence Modeling
  Section: L - AI/ML/Deep Learning/LLM/RAG
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Recurrent Neural Networks (RNNs) are designed to handle sequential data where context and order matter, such as time series, speech, and text. Unlike MLPs or CNNs, RNNs maintain an internal "hidden state" that acts as memory, passing information from one step in the sequence to the next. You will learn about the vanishing gradient problem in vanilla RNNs and how advanced architectures like Long Short-Term Memory (LSTM) networks and Gated Recurrent Units (GRUs) use gating mechanisms to preserve long-term dependencies. We'll also cover Bidirectional RNNs and Seq2Seq models.

  Prerequisites: ANN fundamentals, Backpropagation, basic understanding of gradients.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Sequence Modeling
    Dealing with data where inputs are not independent. E.g., predicting the next word in a sentence depends on the previous words.

  Recurrent Neural Network (RNN)
    A network with loops, allowing information to persist. For each element in a sequence, it takes the current input x_t and the previous hidden state h_{t-1} to produce the current hidden state h_t and (optionally) an output y_t.

  Hidden State (h_t)
    The "memory" of the RNN. It captures information about what has been calculated so far.

  Backpropagation Through Time (BPTT)
    How RNNs are trained. The RNN is unrolled for a set number of time steps, and standard backpropagation is applied to this unrolled network.

  Vanishing/Exploding Gradient Problem
    Because the same weights are multiplied repeatedly across time steps during BPTT, gradients can easily shrink to zero (vanish) or grow uncontrollably (explode), making it nearly impossible for vanilla RNNs to learn long-term dependencies.

  LSTM (Long Short-Term Memory)
    A special kind of RNN capable of learning long-term dependencies. It introduces a Cell State (C_t) along with the hidden state, and uses Gates to regulate information flow.
    - Forget Gate: Decides what information to throw away from the cell state.
    - Input Gate: Decides which values will be updated and creates new candidate values to add to the cell state.
    - Output Gate: Decides what the next hidden state should be based on the updated cell state.

  GRU (Gated Recurrent Unit)
    A simplified version of an LSTM. It combines the forget and input gates into a single Update Gate, and merges the cell state and hidden state. It is faster to train and often performs similarly to LSTMs.

  Bidirectional RNN (BiRNN)
    Processes the sequence in both directions (forward and backward) simultaneously, allowing the network to have context from both the past and the future at any given time step.

  Seq2Seq (Encoder-Decoder)
    An architecture mapping an input sequence to an output sequence of a different length (e.g., translation). An Encoder RNN processes the input into a fixed-size context vector, which a Decoder RNN uses to generate the output sequence.

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Unrolled Vanilla RNN                                                   │
  │                                                                         │
  │        x_{t-1}           x_t               x_{t+1}                      │
  │          |                |                  |                          │
  │      +---+---+        +---+---+          +---+---+                      │
  │  ... | RNN A | -----> | RNN A | -------> | RNN A | ...                  │
  │      +---+---+  h_{t-1} +---+---+   h_t    +---+---+                      │
  │          |                |                  |                          │
  │        y_{t-1}           y_t               y_{t+1}                      │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Inside an LSTM Cell                                                    │
  │                                                                         │
  │             C_{t-1} ----------------------------------------( + )----> C_t│
  │              |                                                ^         │
  │              v                                                |         │
  │            ( X ) <-----------------+                          |         │
  │              ^                     |                          |         │
  │              |                     |                          |         │
  │              | [Forget Gate]       | [Input Gate]             |         │
  │            (Sigmoid)             (Sigmoid) * (Tanh)           |         │
  │              ^                     ^           ^              |         │
  │              |                     |           |              |         │
  │  h_{t-1} ----+---------------------+-----------+------------------+     │
  │              |                                                |   |     │
  │   x_t -------+                                      [Output Gate] |     │
  │                                                       (Sigmoid)   |     │
  │                                                           |       |     │
  │                                                           v       v     │
  │                                                         ( X ) * (Tanh)  │
  │                                                           |             │
  │                                                           +----------> h_t│
  │                                                                         │
  │  Note: Sigmoid squashes between 0 and 1 (acting as a valve/gate), Tanh squashes between -1 and 1 (creating candidate values).│
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Time Series Prediction with LSTM (PyTorch)                           │
  │                                                                          │
  │  import torch                                                            │
  │  import torch.nn as nn                                                   │
  │  import numpy as np                                                      │
  │                                                                          │
  │  # 1. Prepare dummy sine wave data                                       │
  │  seq_length = 10                                                         │
  │  # Create a sine wave                                                    │
  │  data = np.sin(np.linspace(0, 100, 1000, dtype=np.float32))              │
  │                                                                          │
  │  # Create sequences of length 10 to predict the 11th value               │
  │  X = []                                                                  │
  │  y = []                                                                  │
  │  for i in range(len(data) - seq_length):                                 │
  │      X.append(data[i : i + seq_length])                                  │
  │      y.append(data[i + seq_length])                                      │
  │                                                                          │
  │  X = torch.tensor(X).unsqueeze(-1) # Shape: (samples, seq_length, 1 feature)│
  │  y = torch.tensor(y).unsqueeze(-1) # Shape: (samples, 1 output)          │
  │                                                                          │
  │  # 2. Define the LSTM Model                                              │
  │  class TimeSeriesLSTM(nn.Module):                                        │
  │      def __init__(self, input_size=1, hidden_size=32, num_layers=1, output_size=1):│
  │          super(TimeSeriesLSTM, self).__init__()                          │
  │          self.hidden_size = hidden_size                                  │
  │          self.num_layers = num_layers                                    │
  │                                                                          │
  │          # batch_first=True means inputs are (batch, seq, feature)       │
  │          self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)│
  │          self.fc = nn.Linear(hidden_size, output_size)                   │
  │                                                                          │
  │      def forward(self, x):                                               │
  │          # Initialize hidden state and cell state with zeros             │
  │          h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)  │
  │          c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)  │
  │                                                                          │
  │          # out: tensor of shape (batch_size, seq_length, hidden_size)    │
  │          out, (hn, cn) = self.lstm(x, (h0, c0))                          │
  │                                                                          │
  │          # We only want the output of the last time step for prediction  │
  │          out = self.fc(out[:, -1, :])                                    │
  │          return out                                                      │
  │                                                                          │
  │  # 3. Setup and Train                                                    │
  │  model = TimeSeriesLSTM()                                                │
  │  criterion = nn.MSELoss()                                                │
  │  optimizer = torch.optim.Adam(model.parameters(), lr=0.01)               │
  │                                                                          │
  │  # Training loop                                                         │
  │  epochs = 50                                                             │
  │  for epoch in range(epochs):                                             │
  │      model.train()                                                       │
  │      optimizer.zero_grad()                                               │
  │                                                                          │
  │      outputs = model(X)                                                  │
  │      loss = criterion(outputs, y)                                        │
  │                                                                          │
  │      loss.backward()                                                     │
  │      optimizer.step()                                                    │
  │                                                                          │
  │      if (epoch+1) % 10 == 0:                                             │
  │          print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')   │
  │                                                                          │
  │  # 4. Predict                                                            │
  │  model.eval()                                                            │
  │  with torch.no_grad():                                                   │
  │      test_seq = torch.tensor(np.sin(np.linspace(100, 101, 10, dtype=np.float32))).unsqueeze(0).unsqueeze(-1)│
  │      prediction = model(test_seq)                                        │
  │      print("Test Sequence True next value (approx):", np.sin(101.1))     │
  │      print("Model Prediction:", prediction.item())                       │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Multi-Layer Bidirectional GRU for Text Classification                │
  │                                                                          │
  │  import torch                                                            │
  │  import torch.nn as nn                                                   │
  │  from torch.utils.data import DataLoader, TensorDataset                  │
  │                                                                          │
  │  class TextClassifierBiGRU(nn.Module):                                   │
  │      def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, │
  │                   bidirectional, dropout, pad_idx):                      │
  │          super().__init__()                                              │
  │                                                                          │
  │          # 1. Embedding Layer: Converts token indices to dense vectors   │
  │          # padding_idx ensures the padding token doesn't affect gradients│
  │          self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_idx)│
  │                                                                          │
  │          # 2. GRU Layer                                                  │
  │          self.gru = nn.GRU(embedding_dim,                                │
  │                            hidden_dim,                                   │
  │                            num_layers=n_layers,                          │
  │                            bidirectional=bidirectional,                  │
  │                            batch_first=True,                             │
  │                            dropout=dropout if n_layers > 1 else 0)       │
  │                                                                          │
  │          # 3. Fully Connected Layer                                      │
  │          # If bidirectional, hidden_dim is doubled                       │
  │          self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)│
  │          self.dropout = nn.Dropout(dropout)                              │
  │                                                                          │
  │      def forward(self, text, text_lengths):                              │
  │          # text: (batch_size, max_seq_length)                            │
  │                                                                          │
  │          # embedded: (batch_size, max_seq_length, embedding_dim)         │
  │          embedded = self.dropout(self.embedding(text))                   │
  │                                                                          │
  │          # Pack sequence (Optimization for PyTorch RNNs to ignore padding)│
  │          packed_embedded = nn.utils.rnn.pack_padded_sequence(            │
  │              embedded, text_lengths.cpu(), batch_first=True, enforce_sorted=False)│
  │                                                                          │
  │          packed_output, hidden = self.gru(packed_embedded)               │
  │                                                                          │
  │          # Unpack sequence (not strictly needed if we only use final hidden state)│
  │          # output, output_lengths = nn.utils.rnn.pad_packed_sequence(packed_output, batch_first=True)│
  │                                                                          │
  │          # hidden state shape: (num_layers * num_directions, batch_size, hidden_dim)│
  │          # We need the final hidden state of the last layer (forward and backward)│
  │          if self.gru.bidirectional:                                      │
  │              # Concat the final forward (hidden[-2]) and backward (hidden[-1]) hidden layers│
  │              hidden = self.dropout(torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1))│
  │          else:                                                           │
  │              hidden = self.dropout(hidden[-1,:,:])                       │
  │                                                                          │
  │          # hidden shape: (batch_size, hidden_dim * num_directions)       │
  │          return self.fc(hidden)                                          │
  │                                                                          │
  │  # Dummy Usage                                                           │
  │  vocab_size = 5000                                                       │
  │  embedding_dim = 100                                                     │
  │  hidden_dim = 256                                                        │
  │  output_dim = 2 # Binary classification (e.g., positive/negative sentiment)│
  │  n_layers = 2                                                            │
  │  bidirectional = True                                                    │
  │  dropout = 0.3                                                           │
  │  pad_idx = 0 # Assume 0 is the index for <PAD>                           │
  │                                                                          │
  │  model = TextClassifierBiGRU(vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, bidirectional, dropout, pad_idx)│
  │                                                                          │
  │  # Mock data: Batch of 3 sentences, padded to length 10                  │
  │  # And their actual non-padded lengths                                   │
  │  mock_text = torch.tensor([                                              │
  │      [5, 12, 45, 123, 0, 0, 0, 0, 0, 0],  # length 4                     │
  │      [6, 33, 2, 4, 88, 9, 0, 0, 0, 0],    # length 6                     │
  │      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]      # length 10                    │
  │  ])                                                                      │
  │  mock_lengths = torch.tensor([4, 6, 10])                                 │
  │                                                                          │
  │  predictions = model(mock_text, mock_lengths)                            │
  │  print("Output logits shape:", predictions.shape) # Expected: (3, 2)     │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the core difference between an RNN and an MLP?

  ANSWER:
    MLPs assume all inputs are independent of each other. RNNs have a hidden state (memory) that retains context from previous inputs in a sequence, allowing them to process temporal/sequential data.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the Vanishing Gradient Problem in standard RNNs.

  ANSWER:
    During Backpropagation Through Time (BPTT), the gradient is repeatedly multiplied by the same weight matrix (associated with the hidden state transitions). If these weights (or their eigenvalues) are less than 1, the gradient shrinks exponentially as it travels back in time, preventing the network from learning long-range dependencies.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: How do LSTMs solve the vanishing gradient problem?

  ANSWER:
    LSTMs introduce a continuous "Cell State" (the conveyor belt) and use gating mechanisms. The cell state allows gradients to flow backwards uninterrupted (via an additive combination rather than just multiplicative), preserving long-term dependencies. The forget gate can decide to reset this state, but by default, information passes through.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What are the different gates in an LSTM and their functions?

  ANSWER:
    Forget Gate (decides what past info to discard), Input Gate (decides what new info to store in the cell state), Output Gate (decides what part of the cell state to reveal as the hidden state for the next step).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How is a GRU different from an LSTM?

  ANSWER:
    GRUs are simplified LSTMs. They merge the cell state and hidden state into one. They combine the forget and input gates into a single "Update Gate". They have fewer parameters, train faster, and often perform comparably to LSTMs on many tasks.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why would you use a Bidirectional RNN?

  ANSWER:
    In standard RNNs, prediction at step t only depends on past context. In many tasks (like POS tagging or translation), understanding the word depends on words that come after it as well. BiRNNs process the sequence forward and backward, concatenating the hidden states, providing full context.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is an Encoder-Decoder (Seq2Seq) architecture?

  ANSWER:
    Two RNNs connected together. The Encoder reads the input sequence and compresses it into a single, fixed-size "context vector" (the final hidden state). The Decoder takes this context vector and generates the output sequence step-by-step. Used for machine translation.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: What is the bottleneck problem in standard Seq2Seq models?

  ANSWER:
    The entire input sequence must be compressed into a single fixed-length context vector. For very long sentences, this single vector cannot hold all the necessary information, leading to poor translation quality. (This led to the invention of Attention).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Why is pack_padded_sequence used in PyTorch?

  ANSWER:
    When batching sequences of varying lengths, we pad shorter ones with zeros. Processing these zeros wastes computation and adds noise to the hidden state. pack_padded_sequence tells PyTorch to skip the padding tokens during the RNN forward pass, saving time and improving accuracy.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: Can CNNs be used for sequence data?

  ANSWER:
    Yes (e.g., 1D CNNs or Temporal Convolutional Networks). They slide a 1D filter over the sequence. They are highly parallelizable (unlike RNNs which are sequential) and can capture local patterns well, but usually require massive depth/dilation to capture very long-range dependencies.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Exploding Gradients

  # Training loop for vanilla RNN
  loss.backward()
  optimizer.step()

  SOLUTION:
    Standard RNNs are highly susceptible to exploding gradients (gradients becoming NaN). You must clip gradients before stepping the optimizer. 
    Fix: torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0) before optimizer.step().

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Silent State Leak

  class TextGenerator(nn.Module):
      # ... init ...
      def forward(self, x):
          # h0 initialized in __init__ as self.h = torch.zeros(...)
          out, self.h = self.rnn(x, self.h)
          return out

  SOLUTION:
    The hidden state self.h is persisted across batches. Unless the next batch is a direct continuation of the previous sequence (stateful RNN), maintaining the hidden state across unrelated batches will destroy learning. The hidden state should usually be re-initialized to zeros at the start of every new batch (as done in the Demo Code). Furthermore, self.h needs .detach() called on it between batches to prevent BPTT across batch boundaries, which would cause an Out Of Memory (OOM) error.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Extracting the Final State

  # lstm output shape: (batch, seq_len, hidden_size)
  out, (hn, cn) = self.lstm(x)
  final_prediction = self.fc(out[:, -1, :]) # Taking the last element

  SOLUTION:
    If the batch contains sequences of different lengths (padded with zeros), out[:, -1, :] will extract the output corresponding to a padding token, not the actual end of the sentence. You should use pack_padded_sequence or index using the actual sequence lengths. Alternatively, use hn (which handles packed sequences correctly) instead of out.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Legacy NLP & Speech: While Transformers dominate NLP now, LSTMs and GRUs are still used heavily in environments with strict latency/memory constraints where Transformers are too heavy (e.g., on-device speech recognition, wake-word detection like "Hey Siri").
  Time Series Data: For anomaly detection in server logs, stock market prediction, weather forecasting, and sensor data (IoT), LSTMs and 1D CNNs often remain the standard due to their ability to model continuous temporal dependencies efficiently.
  Hybrid Models: CNN-RNN architectures are used for Video Analysis (CNN extracts frame features, RNN models temporal movement) and Image Captioning.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 135_NLP_Foundations.md: Learn how words are converted into the dense embeddings required by these RNN models.
  -> File 136_Transformer_Architecture.md: The architecture that solved the Seq2Seq "bottleneck" problem using Attention, largely replacing RNNs for text.
  -> File 133_CNN.md: Compare the sequential processing of RNNs with the spatial processing of CNNs.

================================================================================
  END OF FILE 134
================================================================================
