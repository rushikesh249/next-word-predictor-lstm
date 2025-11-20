import matplotlib.pyplot as plt
import numpy as np

# Data
datasets = [500, 1000, 8000, 10000]
cpu_times = [0.68, 0.94, 7.18, 58.03]
openmp_times = [0.035, 0.076, 0.09, 0.104]
gpu_times = [0.00012, 0.00014, 0.00016, 0.00025]

x = np.arange(len(datasets))
width = 0.25

plt.figure(figsize=(10,6))
plt.bar(x - width, cpu_times, width, label='CPU')
plt.bar(x, openmp_times, width, label='OpenMP')
plt.bar(x + width, gpu_times, width, label='GPU')
plt.xlabel('Dataset Size')
plt.ylabel('Time (seconds)')
plt.title('Performance Comparison: CPU vs OpenMP vs GPU')
plt.xticks(x, datasets)
plt.legend()
plt.tight_layout()
plt.show()
