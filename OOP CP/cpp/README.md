# C++ Implementation

This directory contains the C++ implementations of the word prediction system with performance optimizations.

## Files

- `main.cpp` - Sequential implementation with timing analysis
- `openmp.cpp` - Parallel implementation using OpenMP
- `timing.cpp` - Performance benchmarking utilities

## Compilation

### Sequential Version
```bash
g++ -std=c++11 -O2 main.cpp -o main
```

### OpenMP Parallel Version
```bash
g++ -std=c++11 -O2 -fopenmp openmp.cpp -o openmp
```

### Timing Analysis
```bash
g++ -std=c++11 -O2 timing.cpp -o timing
```

## Usage

```bash
# Run sequential version
./main

# Run parallel version
./openmp

# Run timing analysis
./timing
```

## Performance Results

The OpenMP implementation shows significant speedup:

| Dataset Size | Sequential | OpenMP | Speedup |
|-------------|-----------|---------|---------|
| 500 words   | 0.68s     | 0.035s  | 19.4x   |
| 1000 words  | 0.94s     | 0.076s  | 12.4x   |
| 8000 words  | 7.18s     | 0.09s   | 79.8x   |
| 10000 words | 58.03s    | 0.104s  | 558x    |
