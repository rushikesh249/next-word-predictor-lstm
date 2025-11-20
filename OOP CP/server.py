import os
import json
import pickle
from typing import List

from flask import Flask, request, jsonify
from flask_cors import CORS

import numpy as np

# TensorFlow / Keras
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense


# ---------------------- Config ----------------------
DATASET_FILE = os.environ.get("DATASET_FILE", "data/dataset_10000.txt")
MODEL_FILE = os.environ.get("MODEL_FILE", "model.h5")
TOKENIZER_FILE = os.environ.get("TOKENIZER_FILE", "tokenizer.pkl")

MAX_VOCAB = int(os.environ.get("MAX_VOCAB", "5000"))
SEQ_LEN = int(os.environ.get("SEQ_LEN", "5"))
EMBED_DIM = int(os.environ.get("EMBED_DIM", "64"))
LSTM_UNITS = int(os.environ.get("LSTM_UNITS", "128"))
EPOCHS = int(os.environ.get("EPOCHS", "3"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "64"))


app = Flask(__name__)
CORS(app)


def read_dataset(path: str) -> str:
    if not os.path.exists(path):
        # fallback sample text so app can start
        return (
            "the quick brown fox jumps over the lazy dog. "
            "the quick brown cat sleeps on the warm mat. "
            "the smart student studies hard and learns quickly. "
        )
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def build_or_load_tokenizer(text: str) -> Tokenizer:
    if os.path.exists(TOKENIZER_FILE):
        with open(TOKENIZER_FILE, "rb") as f:
            return pickle.load(f)

    tokenizer = Tokenizer(num_words=MAX_VOCAB, oov_token="<OOV>")
    tokenizer.fit_on_texts([text])
    with open(TOKENIZER_FILE, "wb") as f:
        pickle.dump(tokenizer, f)
    return tokenizer


def make_sequences(tokenizer: Tokenizer, text: str):
    tokens = tokenizer.texts_to_sequences([text])[0]
    # Build sliding windows of length SEQ_LEN -> next token target
    inputs, targets = [], []
    for i in range(SEQ_LEN, len(tokens)):
        seq = tokens[i - SEQ_LEN : i]
        target = tokens[i]
        inputs.append(seq)
        targets.append(target)
    if not inputs:
        return None, None
    x = np.array(inputs)
    y = np.array(targets)
    return x, y


def build_or_load_model(vocab_size: int):
    if os.path.exists(MODEL_FILE):
        return load_model(MODEL_FILE)

    model = Sequential(
        [
            Embedding(vocab_size, EMBED_DIM, input_length=SEQ_LEN),
            LSTM(LSTM_UNITS),
            Dense(vocab_size, activation="softmax"),
        ]
    )
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy")
    return model


def train_if_needed(model, tokenizer: Tokenizer, text: str):
    if os.path.exists(MODEL_FILE):
        return
    x, y = make_sequences(tokenizer, text)
    if x is None:
        return
    model.fit(x, y, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)
    model.save(MODEL_FILE)


def greedy_predict(tokenizer: Tokenizer, model, prompt: str, num_words: int) -> List[str]:
    word_index = tokenizer.word_index
    index_word = {v: k for k, v in word_index.items()}

    result = []
    tokens = tokenizer.texts_to_sequences([prompt])[0]
    for _ in range(num_words):
        seq = tokens[-SEQ_LEN:]
        seq = pad_sequences([seq], maxlen=SEQ_LEN, padding="pre")
        preds = model.predict(seq, verbose=0)[0]
        next_id = int(np.argmax(preds))
        next_word = index_word.get(next_id, None)
        if not next_word or next_word == "<OOV>":
            break
        result.append(next_word)
        tokens.append(next_id)
    return result


# ---------------------- App bootstrap ----------------------
_raw_text = read_dataset(DATASET_FILE)
_tokenizer = build_or_load_tokenizer(_raw_text)
_vocab_size = min(MAX_VOCAB, len(_tokenizer.word_index) + 1)
_model = build_or_load_model(_vocab_size)
train_if_needed(_model, _tokenizer, _raw_text)


# ---------------------- Routes ----------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        text = (data.get("text") or "").strip()
        num_words = int(data.get("num_words") or 1)
        num_words = max(1, min(num_words, 10))
        if not text:
            return jsonify({"error": "text is required"}), 400

        words = greedy_predict(_tokenizer, _model, text, num_words)
        completion = " ".join(words)
        return jsonify({"completion": completion, "words": words})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)


