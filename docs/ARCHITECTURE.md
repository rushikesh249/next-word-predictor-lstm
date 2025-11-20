# System Architecture

## Overview

The Next Word Predictor LSTM is a full-stack application with multiple implementation approaches for text prediction.

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   ML Model      │
│   (Web UI)      │◄──►│   (Flask API)   │◄──►│   (LSTM)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                      │                      │
│ • HTML/CSS/JS        │ • REST API          │ • TensorFlow      │
│ • Real-time UI       │ • CORS enabled      │ • Keras LSTM      │
│ • Status monitoring  │ • JSON responses    │ • Word embeddings │
│ • Error handling     │ • Health checks     │ • Sequence model  │
└─────────────────────┘└─────────────────────┘└─────────────────┘

┌─────────────────┐    ┌─────────────────┐
│   C++ Version   │    │   Performance   │
│   (OpenMP)      │    │   Analysis      │
└─────────────────┘    └─────────────────┘
│                      │
│ • Parallel compute   │ • Timing analysis │
│ • Frequency-based    │ • Speedup metrics │
│ • Multi-threading    │ • Visualization   │
└─────────────────────┘└─────────────────┘
```

## Components

### 1. Frontend (Web Interface)
- **Technology**: HTML5, CSS3, Vanilla JavaScript
- **Features**: 
  - Real-time backend connectivity monitoring
  - Interactive text input with validation
  - Example prompts for quick testing
  - Responsive design for all devices
  - Rich result display with word breakdown

### 2. Backend (Flask API)
- **Technology**: Python Flask, TensorFlow/Keras
- **Features**:
  - RESTful API with JSON responses
  - CORS enabled for cross-origin requests
  - Health check endpoint
  - Automatic model training on first run
  - Model persistence (saves trained weights)

### 3. LSTM Model
- **Architecture**:
  - Embedding Layer: 64 dimensions
  - LSTM Layer: 128 hidden units
  - Dense Output: Softmax over vocabulary
- **Training**:
  - Sequence length: 5 words
  - Vocabulary size: 5000 words max
  - Optimizer: Adam
  - Loss: Sparse categorical crossentropy

### 4. C++ Implementation
- **Sequential Version**: Basic frequency-based prediction
- **Parallel Version**: OpenMP-optimized multi-threading
- **Performance**: Up to 558x speedup on large datasets

## Data Flow

### Prediction Request Flow
1. User enters text in frontend
2. Frontend validates input and sends POST request
3. Backend receives request and preprocesses text
4. LSTM model generates probability distribution
5. Backend applies greedy decoding to select words
6. Response sent back to frontend with predictions
7. Frontend displays results with rich formatting

### Training Flow
1. Backend checks for existing model files
2. If not found, loads dataset from file
3. Tokenizes text and creates word mappings
4. Generates training sequences (sliding windows)
5. Trains LSTM model for specified epochs
6. Saves model weights and tokenizer for future use

## File Structure

```
next-word-predictor-lstm/
├── frontend/           # Web interface
│   ├── index.html     # Main HTML page
│   ├── app.js         # JavaScript logic
│   └── style.css      # Styling
├── cpp/               # C++ implementations
│   ├── main.cpp       # Sequential version
│   ├── openmp.cpp     # Parallel version
│   └── timing.cpp     # Performance analysis
├── data/              # Training datasets
│   ├── dataset_500.txt
│   ├── dataset_1000.txt
│   ├── dataset_8000.txt
│   └── dataset_10000.txt
├── scripts/           # Utility scripts
│   ├── start_project.py
│   ├── test_integration.py
│   └── graph.py
├── docs/              # Documentation
├── assets/            # Screenshots and media
├── server.py          # Flask backend
└── requirements.txt   # Python dependencies
```

## Scalability Considerations

### Performance Optimizations
- Model caching and persistence
- Efficient tokenization with pickle serialization
- Parallel processing in C++ implementation
- Asynchronous frontend updates

### Future Enhancements
- GPU acceleration for training
- Distributed training for larger datasets
- Caching layer for frequent predictions
- Load balancing for multiple instances
- Database integration for user sessions
