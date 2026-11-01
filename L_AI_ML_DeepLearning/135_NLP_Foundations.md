================================================================================
  FILE 135: Natural Language Processing (NLP) Foundations
  Section: L - AI/ML/Deep Learning/LLM/RAG
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Natural Language Processing (NLP) bridges the gap between human communication and machine understanding. Before text can be fed into deep learning models like LSTMs or Transformers, it must be cleaned, split into manageable pieces, and converted into mathematical representations (vectors). This module covers the evolution of text representation: from basic frequency-based methods like TF-IDF, to static dense embeddings like Word2Vec and GloVe, along with fundamental NLP tasks such as Sentiment Analysis and Named Entity Recognition (NER).

  Prerequisites: Basic text processing in Python, understanding of Vector/Matrix math, ML fundamentals.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  Tokenization
    The process of breaking text into smaller units (tokens). Tokens can be words, characters, or subwords.

  BPE (Byte-Pair Encoding)
    A popular subword tokenization algorithm (used in GPT models). It starts with individual characters and iteratively merges the most frequently occurring adjacent pairs into new tokens. Handles out-of-vocabulary words beautifully.

  Stop Words
    Common words (like "the", "is", "in") that often carry little semantic meaning and are frequently removed in traditional NLP pipelines.

  Stemming / Lemmatization
    Reducing words to their base form. Stemming chops off suffixes (running -> run), while lemmatization uses dictionary rules to find the proper morphological root (better -> good).

  Bag of Words (BoW)
    Represents text by counting the frequency of each word in a document. Ignores word order completely.

  TF-IDF (Term Frequency-Inverse Document Frequency)
    A statistical measure to evaluate how important a word is to a document in a collection or corpus.
    - TF: How frequently a word appears in a document.
    - IDF: Logarithmically scaled inverse fraction of the documents that contain the word (penalizes common words like "the").

  Word Embeddings
    Dense, low-dimensional, continuous vector representations of words where words with similar meanings have similar representations (vectors are close in space).

  Word2Vec (2013)
    A predictive model by Google to create word embeddings. Two flavors:
    - CBOW (Continuous Bag of Words): Predicts the target word based on its context (surrounding words).
    - Skip-Gram: Predicts the surrounding context words given a target word.

  GloVe (Global Vectors, 2014)
    By Stanford. Creates embeddings by factorizing a global word-word co-occurrence matrix. Combines the benefits of matrix factorization (like LSA) and local context windows (like Word2Vec).

  Sentiment Analysis
    Determining the emotional tone behind a body of text (Positive, Negative, Neutral).

  Named Entity Recognition (NER)
    Identifying and classifying key information (entities) in text into predefined categories (Person, Organization, Location, Date).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TF-IDF Intuition                                                       │
  │                                                                         │
  │   Document: "The cat sat on the mat"                                    │
  │                                                                         │
  │   Word   | TF (Frequency) | IDF (Rarity across all docs) | TF-IDF Score │
  │   --------------------------------------------------------------------- │
  │   The    | High (2)       | Very Low (common word)       | Low          │
  │   cat    | Medium (1)     | High (rare word)             | High         │
  │   sat    | Medium (1)     | Medium                       | Medium       │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Word2Vec: Skip-Gram Architecture                                       │
  │                                                                         │
  │             [ Context Word 1 ]                                          │
  │                  ^                                                      │
  │                  | (Softmax)                                            │
  │    [ Target ] -> [ Hidden Layer (Linear) ] -> [ Context Word 2 ]        │
  │     (One-Hot)    (Embedding Matrix)                                     │
  │                  | (Softmax)                                            │
  │                  v                                                      │
  │             [ Context Word 3 ]                                          │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Word Embedding Space (Conceptual)                                      │
  │                                                                         │
  │   (King) -------------------------> (Man)                               │
  │      |                                |                                 │
  │      |                                |                                 │
  │      |                                |                                 │
  │      v                                v                                 │
  │   (Queen) ------------------------> (Woman)                             │
  │                                                                         │
  │   Vector Math: Vector(King) - Vector(Man) + Vector(Woman) ≈ Vector(Queen)│
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // TF-IDF + Logistic Regression for Sentiment Analysis (Scikit-Learn)   │
  │                                                                          │
  │  from sklearn.feature_extraction.text import TfidfVectorizer             │
  │  from sklearn.linear_model import LogisticRegression                     │
  │  from sklearn.metrics import accuracy_score                              │
  │  import numpy as np                                                      │
  │                                                                          │
  │  # 1. Dataset                                                            │
  │  corpus_train = [                                                        │
  │      "I love this movie, it is fantastic.",                              │
  │      "Terrible acting, total waste of time.",                            │
  │      "The plot was brilliant and engaging.",                             │
  │      "I hated every minute of it.",                                      │
  │      "A wonderful experience overall."                                   │
  │  ]                                                                       │
  │  y_train = [1, 0, 1, 0, 1] # 1: Positive, 0: Negative                    │
  │                                                                          │
  │  corpus_test = [                                                         │
  │      "I really enjoyed the film.",                                       │
  │      "Worst movie I have ever seen."                                     │
  │  ]                                                                       │
  │  y_test = [1, 0]                                                         │
  │                                                                          │
  │  # 2. Vectorization using TF-IDF                                         │
  │  vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)      │
  │  X_train_tfidf = vectorizer.fit_transform(corpus_train)                  │
  │  X_test_tfidf = vectorizer.transform(corpus_test)                        │
  │                                                                          │
  │  print("Vocabulary:", vectorizer.get_feature_names_out())                │
  │  print("TF-IDF Matrix Shape:", X_train_tfidf.shape)                      │
  │                                                                          │
  │  # 3. Model Training                                                     │
  │  clf = LogisticRegression()                                              │
  │  clf.fit(X_train_tfidf, y_train)                                         │
  │                                                                          │
  │  # 4. Evaluation                                                         │
  │  predictions = clf.predict(X_test_tfidf)                                 │
  │  print(f"Predictions: {predictions}")                                    │
  │  print(f"Accuracy: {accuracy_score(y_test, predictions)}")               │
  │                                                                          │
  │  # Predict a new sentence                                                │
  │  new_text = ["This was quite awful"]                                     │
  │  print(f"Prediction for '{new_text[0]}': {clf.predict(vectorizer.transform(new_text))[0]}")│
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Language: Python

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  // Training Word2Vec using Gensim and extracting embeddings             │
  │                                                                          │
  │  import gensim                                                           │
  │  from gensim.models import Word2Vec                                      │
  │  import string                                                           │
  │                                                                          │
  │  def preprocess(text):                                                     │
  │      # Extremely basic preprocessing: lowercase and remove punctuation   │
  │      text = text.lower()                                                 │
  │      text = text.translate(str.maketrans('', '', string.punctuation))    │
  │      return text.split()                                                 │
  │                                                                          │
  │  # 1. Prepare Corpus (List of lists of tokens)                           │
  │  raw_corpus = [                                                          │
  │      "The quick brown fox jumps over the lazy dog.",                     │
  │      "Machine learning is the future of artificial intelligence.",       │
  │      "The dog barked loudly at the fox.",                                │
  │      "Artificial intelligence will change the world.",                   │
  │      "The fox is a smart animal."                                        │
  │  ]                                                                       │
  │                                                                          │
  │  tokenized_corpus = [preprocess(sentence) for sentence in raw_corpus]    │
  │  print(f"Tokenized Example: {tokenized_corpus[0]}")                      │
  │                                                                          │
  │  # 2. Train Word2Vec Model                                               │
  │  # vector_size: Dimensionality of the word vectors                       │
  │  # window: Maximum distance between current and predicted word within a sentence│
  │  # min_count: Ignores all words with total frequency lower than this     │
  │  # workers: Number of worker threads to train the model                  │
  │  # sg: 1 for skip-gram, 0 for CBOW                                       │
  │  model = Word2Vec(sentences=tokenized_corpus,                            │
  │                   vector_size=10,                                        │
  │                   window=2,                                              │
  │                   min_count=1,                                           │
  │                   workers=4,                                             │
  │                   sg=1)                                                  │
  │                                                                          │
  │  # 3. Use the Model                                                      │
  │  # Get the vector for a specific word                                    │
  │  word = "fox"                                                            │
  │  if word in model.wv:                                                    │
  │      word_vector = model.wv[word]                                        │
  │      print(f"\nVector for '{word}':\n{word_vector}")                     │
  │                                                                          │
  │  # Find most similar words (cosine similarity)                           │
  │  print("\nWords similar to 'intelligence':")                             │
  │  similar_words = model.wv.most_similar("intelligence", topn=2)           │
  │  for w, sim in similar_words:                                            │
  │      print(f"- {w}: {sim:.4f}")                                          │
  │                                                                          │
  │  # 4. Save and Load for Production                                       │
  │  model.save("word2vec.model")                                            │
  │  # loaded_model = Word2Vec.load("word2vec.model")                        │
  └──────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the difference between stemming and lemmatization?

  ANSWER:
    Stemming applies heuristic rules to chop off ends of words (e.g., "better" might stay "better" or become "bet"), often resulting in non-words. Lemmatization uses vocabulary and morphological analysis to return the base dictionary form of a word (e.g., "better" becomes "good").

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Explain the TF-IDF formulation and why it's useful.

  ANSWER:
    TF-IDF stands for Term Frequency-Inverse Document Frequency. TF measures how often a word occurs in a document. IDF penalizes words that occur in many documents. Multiplying them highlights words that are frequent in a specific document but rare globally, acting as excellent keywords for that document.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Why did Word2Vec represent a massive leap over TF-IDF?

  ANSWER:
    TF-IDF creates sparse, high-dimensional vectors that capture no semantic meaning or word order (only frequencies). Word2Vec creates dense, low-dimensional vectors where semantic relationships are captured geometrically (e.g., King - Man + Woman = Queen).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is the difference between CBOW and Skip-gram architectures in Word2Vec?

  ANSWER:
    Continuous Bag of Words (CBOW) predicts the target word from a window of surrounding context words. Skip-gram does the reverse: it uses the target word to predict the surrounding context words. Skip-gram generally performs better for infrequent words.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: How is GloVe different from Word2Vec?

  ANSWER:
    Word2Vec is a predictive model that learns embeddings by predicting local contexts. GloVe (Global Vectors) is a count-based model. It constructs a massive global word-word co-occurrence matrix and learns embeddings by performing dimensionality reduction (matrix factorization) on this matrix.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: What is the "Out of Vocabulary" (OOV) problem, and how do subword tokenizers (like BPE) solve it?

  ANSWER:
    OOV occurs when a model encounters a word during testing that it didn't see during training. Word2Vec/GloVe assign it a generic <UNK> vector. BPE solves this by breaking unknown words into known subword units (e.g., "unhappiness" -> "un", "happi", "ness"), allowing the model to piece together meaning from subwords.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is Named Entity Recognition (NER)? Give an example.

  ANSWER:
    NER locates and classifies named entities in unstructured text into predefined categories. E.g., "Apple [ORG] is looking at buying U.K. [GPE] startup for $1 billion [MONEY]."

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How would you handle text classification if you have very little training data?

  ANSWER:
    TF-IDF with a linear model (like Naive Bayes or SVM) is a strong baseline that requires very little data. Alternatively, use pre-trained Word2Vec/GloVe embeddings, or zero-shot classification using modern LLMs. Training an RNN/CNN from scratch on small data will severely overfit.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: Why do we use Cosine Similarity instead of Euclidean Distance to compare word vectors?

  ANSWER:
    Cosine similarity measures the angle between two vectors, completely ignoring their magnitude (length). In NLP, a word might appear many times, making its vector longer, but its semantic direction remains the same. Cosine similarity correctly captures this semantic alignment regardless of word frequency.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is a major limitation of static embeddings like Word2Vec and GloVe?

  ANSWER:
    They are context-independent. The word "bank" gets the exact same vector representation whether the sentence is "I went to the bank to deposit money" or "I sat by the river bank". (This limitation was solved by contextual embeddings like ELMo and BERT).

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Data Leakage

  vectorizer = TfidfVectorizer()
  X_train_tfidf = vectorizer.fit_transform(corpus_train)
  # ... training model ...
  
  # Evaluation time!
  X_test_tfidf = vectorizer.fit_transform(corpus_test) 
  predictions = model.predict(X_test_tfidf)

  SOLUTION:
    fit_transform is called on the test set. This re-calculates the IDF statistics based on the test data (data leakage) and completely rebuilds the vocabulary mapping. Column 5 in the train set might represent "apple", but column 5 in the test set might represent "zebra". You must use vectorizer.transform(corpus_test) for inference.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Silent UNK

  word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
  
  def sentence_to_avg_vector(sentence):
      words = sentence.split()
      vectors = [word_vectors[w] for w in words]
      return np.mean(vectors, axis=0)
  
  print(sentence_to_avg_vector("The quickkk fox jumps"))

  SOLUTION:
    "quickkk" is a typo and will not be in the pre-trained Word2Vec vocabulary. word_vectors[w] will throw a KeyError. You must handle Out-of-Vocabulary words gracefully (e.g., ignoring them, or providing a default zero vector).
    Fix: vectors = [word_vectors[w] for w in words if w in word_vectors]

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: The Orderless Bag

  text1 = "John loves Mary"
  text2 = "Mary loves John"
  vectorizer = CountVectorizer() # Bag of Words
  X = vectorizer.fit_transform([text1, text2])

  SOLUTION:
    While not a syntax error, this demonstrates a critical flaw in BoW/TF-IDF. X[0] and X[1] will be identical vectors (e.g., [1, 1, 1]). Bag of Words destroys word order, so the model cannot distinguish between these two sentences which have entirely different meanings. (Solution: N-grams or sequential models).

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  Search Engines & ElasticSearch: TF-IDF (and its advanced variant BM25) is still the absolute backbone of keyword search and document retrieval in systems like Elasticsearch and Solr.
  Spam & Intent Detection: Fast, lightweight intent classifiers in chatbots or spam filters often rely on TF-IDF + SVMs rather than heavy deep learning models due to ultra-low latency requirements and low compute costs.
  Data Preparation: Tokenization, stemming, and dealing with OOV words are daily tasks for ML engineers. You cannot utilize advanced architectures without first understanding how to properly digitize text.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 134_RNN_LSTM_GRU.md: How sequence models take the word embeddings generated here and process them over time.
  -> File 136_Transformer_Architecture.md: How the limitations of Word2Vec (context-independence) were solved by self-attention mechanisms.
  -> File 138_RAG.md: Retrieval-Augmented Generation relies heavily on embeddings (though contextual ones) to perform semantic similarity search.

================================================================================
  END OF FILE 135
================================================================================
