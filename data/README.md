# Dataset Information

This directory contains the training datasets for the LSTM model.

## Files

- `dataset.txt` - Small dataset (1000 words) for quick testing
- `dataset_500.txt` - Minimal dataset (500 words) for development
- `dataset_1000.txt` - Medium dataset (1000 words) for testing
- `dataset_8000.txt` - Large dataset (8000 words) for training
- `dataset_10000.txt` - Full dataset (10000 words) for production training

## Usage

The model automatically uses `dataset_10000.txt` by default. You can change this by setting the `DATASET_FILE` environment variable:

```bash
export DATASET_FILE="dataset_500.txt"  # Linux/Mac
set DATASET_FILE="dataset_500.txt"     # Windows
```

## Format

Each dataset contains simple English sentences with various subjects, verbs, and objects to provide rich patterns for the LSTM model to learn sequential dependencies.
