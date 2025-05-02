import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re


input_filename = 'cuda_24840874.txt'

cleaned_lines = []
with open(input_filename, 'r') as f:
    header = f.readline().strip()
    cleaned_lines.append(header)
    for line in f:
        if re.match(r'^\d', line):
            cleaned_lines.append(line.strip())

cleaned_data_io = io.StringIO('\n'.join(cleaned_lines))

df = pd.read_csv(cleaned_data_io)

numeric_cols = ['mean_temp', 'std_temp', 'pct_above_18', 'pct_below_15']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')


plt.figure(figsize=(10, 6))
sns.histplot(df['mean_temp'], bins=30, kde=True)
plt.title('Distribution of Mean Temperatures Across Buildings')
plt.xlabel('Mean Temperature')
plt.ylabel('Number of Buildings')
plt.grid(axis='y', alpha=0.5)
plt.savefig('mean_temp_distribution.png')

avg_mean_temp = df['mean_temp'].mean()
print(f"\nAverage Mean Temperature: {avg_mean_temp:.3f}")

avg_std_temp = df['std_temp'].mean()
print(f"Average Temperature Standard Deviation: {avg_std_temp:.3f}")

count_above_18_50pct = df[df['pct_above_18'] >= 50].shape[0]
print(f"Number of buildings with >= 50% above 18: {count_above_18_50pct}")

count_below_15_50pct = df[df['pct_below_15'] >= 50].shape[0]
print(f"Number of buildings with >= 50% below 15: {count_below_15_50pct}")
