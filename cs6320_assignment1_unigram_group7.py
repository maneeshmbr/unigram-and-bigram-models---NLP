# -*- coding: utf-8 -*-
"""CS6320_Assignment1_unigram_Group7

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1on4-m_2j3lvfinIaBE3sLbONi58DUjlb

**Unigram Model**
"""

# -------------------------------------
# CS6320 - NLP - Assignment 1 - Unigram Model
# -------------------------------------

print("\n-------------------------\nGroup 7 - NLP Assignment 1")
print("Bhanu Maneesh Reddy Mannem (BXM220055)")
print("Snehal Kumar Ketala (SXK220463)")
print("Lalithya Mada (LXM230002)")
print("-------------------------")

"""**Import Libraries and Define Utility Functions**"""

import re
import math
from collections import Counter, defaultdict
import requests

# Global dictionary to store final results for output display
output_data = {}

# Function to compute perplexity
def compute_perplexity(probabilities, tokens, log_probs):
    print("\n--- Calculating Perplexity ---")
    token_count = defaultdict(int)
    total_tokens = 0
    for token in tokens:
        token_count[token] += 1
        total_tokens += 1

    total_log_prob = 0
    for token in token_count:
        if token in log_probs:
            log_prob = log_probs[token]
        else:
            log_prob = log_probs['UNK']
        total_log_prob += (-1) * log_prob * token_count[token]

    perplexity_value = math.exp(total_log_prob / total_tokens)
    print(f"Perplexity Calculated: {perplexity_value}")
    return perplexity_value

# Function to calculate unigram probabilities with Add-k Smoothing
def unigram_add_k_smoothing(train_words, smoothing_factor):
    print(f"\n--- Applying Add-k Smoothing (k={smoothing_factor}) ---")
    word_counts, total_word_count = defaultdict(int), 0
    for word in train_words:
        word_counts[word] += 1
        total_word_count += 1

    smoothed_probs = {}
    for word, count in word_counts.items():
        smoothed_probs[word] = (count + smoothing_factor) / (total_word_count + smoothing_factor * (len(word_counts) + 1))  # +1 for UNK token

    # Assign probability to UNK token
    smoothed_probs['UNK'] = smoothing_factor / (total_word_count + smoothing_factor * (len(word_counts) + 1))

    print(f"Add-k Smoothing Applied (k={smoothing_factor})")
    return smoothed_probs, word_counts, total_word_count

# Laplace Smoothing (k=1)
def laplace_smoothing(train_words):
    print("\n--- Applying Laplace Smoothing (k=1) ---")
    return unigram_add_k_smoothing(train_words, 1)

print("Libraries imported and utility functions defined.\n")

"""**Read and Preprocess Data (Including UNK Token for Rare Words)**"""

# Updated to load data from URL
def load_and_preprocess(url, threshold=1):
    print(f"--- Loading and Preprocessing Data from {url} ---")

    # Fetch the data from the URL
    response = requests.get(url)
    data = response.text

    # Preprocess data (lowercase, remove special characters)
    data_clean = re.sub(r'\W', ' ', data.lower()).split()

    # Replace rare words with UNK
    word_frequencies = Counter(data_clean)
    processed_data = [
        word if word_frequencies[word] > threshold else 'UNK' for word in data_clean
    ]

    print(f"Data Loaded and Preprocessed from {url}")
    return processed_data

train_url = "https://raw.githubusercontent.com/maneeshmbr/unigram-and-bigram-models---NLP/master/A1_DATASET/A1_DATASET/train.txt"
validation_url = "https://raw.githubusercontent.com/maneeshmbr/unigram-and-bigram-models---NLP/master/A1_DATASET/A1_DATASET/val.txt"

train_words = load_and_preprocess(train_url, threshold=1)  # Treat words appearing only once as UNK
validation_words = load_and_preprocess(validation_url)

print(f"Sample tokens from training data: {train_words[:10]}")
print(f"Sample tokens from validation data: {validation_words[:10]}")

print(f"Total words in training set: {len(train_words)}")
print(f"Total unique words in training set (with UNK): {len(set(train_words))}")

"""**Calculate Unsmoothed Unigram Probabilities**"""

def compute_unigram_probabilities(words):
    print("\n--- Calculating Unsmoothed Unigram Probabilities ---")
    word_frequencies = Counter(words)
    total_words = len(words)

    unigram_probs = {word: freq / total_words for word, freq in word_frequencies.items()}
    unigram_log_probs = {word: math.log(prob) for word, prob in unigram_probs.items()}

    print(f"Unsmoothed Unigram Probabilities Calculated")
    return unigram_probs, unigram_log_probs, word_frequencies

# Calculate probabilities and log probabilities
unigram_probs, unigram_log_probs, word_frequencies = compute_unigram_probabilities(train_words)

print("\n--- Unsmoothed Unigram Probabilities (Top 10) ---")
for word, prob in list(unigram_probs.items())[:10]:
    print(f"{word}: {prob:.6f}")

# Add UNK probability if not in the vocabulary
unigram_probs['UNK'] = 1 / len(train_words)
unigram_log_probs['UNK'] = math.log(unigram_probs['UNK'])

# Calculate perplexity for training data (without smoothing)
unsmoothed_perplexity = compute_perplexity(unigram_probs, train_words, unigram_log_probs)
output_data['Perplexity (Unsmoothed)'] = unsmoothed_perplexity
print(f"Perplexity (Unsmoothed): {unsmoothed_perplexity}")

""" **Apply Add-k and Laplace Smoothing (with UNK Token)**"""

# Add-k Smoothing (k=0.5)
smoothed_probs_k_0_5, _, _ = unigram_add_k_smoothing(train_words, 0.5)
log_probs_k_0_5 = {word: math.log(prob) for word, prob in smoothed_probs_k_0_5.items()}

print("\n--- Add-k Smoothing (k=0.5) Unigram Probabilities (Top 10) ---")
for word, prob in list(smoothed_probs_k_0_5.items())[:10]:
    print(f"{word}: {prob:.6f}")

perplexity_k_0_5 = compute_perplexity(smoothed_probs_k_0_5, validation_words, log_probs_k_0_5)
output_data['Perplexity (Add-k = 0.5)'] = perplexity_k_0_5
print(f"Perplexity (Add-k = 0.5): {perplexity_k_0_5}")

# Add-k Smoothing (k=3)
smoothed_probs_k_3, _, _ = unigram_add_k_smoothing(train_words, 3)
log_probs_k_3 = {word: math.log(prob) for word, prob in smoothed_probs_k_3.items()}

print("\n--- Add-k Smoothing (k=3) Unigram Probabilities (Top 10) ---")
for word, prob in list(smoothed_probs_k_3.items())[:10]:
    print(f"{word}: {prob:.6f}")

perplexity_k_3 = compute_perplexity(smoothed_probs_k_3, validation_words, log_probs_k_3)
output_data['Perplexity (Add-k = 3)'] = perplexity_k_3
print(f"Perplexity (Add-k = 3): {perplexity_k_3}")

# Laplace Smoothing (k=1)
laplace_probs, _, _ = laplace_smoothing(train_words)  # This line will now work correctly
laplace_log_probs = {word: math.log(prob) for word, prob in laplace_probs.items()}

print("\n--- Laplace Smoothing Unigram Probabilities (Top 10) ---")
for word, prob in list(laplace_probs.items())[:10]:
    print(f"{word}: {prob:.6f}")

perplexity_laplace = compute_perplexity(laplace_probs, validation_words, laplace_log_probs)
output_data['Perplexity (Laplace Smoothing)'] = perplexity_laplace
print(f"Perplexity (Laplace Smoothing): {perplexity_laplace}")

"""**Perplexity for Training Data Without Smoothing**"""

perplexity_train_unsmoothed = compute_perplexity(unigram_probs, train_words, unigram_log_probs)
output_data['Perplexity (Training Without Smoothing)'] = perplexity_train_unsmoothed
print(f"Perplexity (Training Data Without Smoothing): {perplexity_train_unsmoothed}")

"""**Perplexity with Rare Words as Unknown (with Debugging)**"""

# Replace rare words with 'UNK' in training and validation data (with higher threshold for rare words)
def replace_rare_with_unk(train_words, val_words, threshold=2):
    # Calculate frequencies of words in the training data
    word_frequencies = Counter(train_words)

    # Replace rare words in training data with 'UNK'
    processed_train_data = [
        word if word_frequencies[word] > threshold else 'UNK' for word in train_words
    ]

    unk_count_train = processed_train_data.count('UNK')
    print(f"Number of 'UNK' tokens in training data: {unk_count_train}")

    # Replace words in validation data with 'UNK' if they are not seen in training or are rare
    processed_val_data = [
        word if word in word_frequencies and word_frequencies[word] > threshold else 'UNK' for word in val_words
    ]

    unk_count_val = processed_val_data.count('UNK')
    print(f"Number of 'UNK' tokens in validation data: {unk_count_val}")

    return processed_train_data, processed_val_data


# Apply UNK replacement to both training and validation sets
train_words_with_unk, validation_words_with_unk = replace_rare_with_unk(train_words, validation_words)

print(f"Sample of modified training data: {train_words_with_unk[:10]}")
print(f"Sample of modified validation data: {validation_words_with_unk[:10]}")

# Recalculate perplexity with UNK for all smoothing methods

# Add-k Smoothing (k=0.5) with UNK
smoothed_probs_k_0_5_unk, _, _ = unigram_add_k_smoothing(train_words_with_unk, 0.5)
log_probs_k_0_5_unk = {word: math.log(prob) for word, prob in smoothed_probs_k_0_5_unk.items()}
perplexity_k_0_5_unk = compute_perplexity(smoothed_probs_k_0_5_unk, validation_words_with_unk, log_probs_k_0_5_unk)
output_data['Perplexity (Add-k = 0.5 with UNK)'] = perplexity_k_0_5_unk
print(f"Perplexity (Add-k = 0.5 with UNK): {perplexity_k_0_5_unk}")

# Add-k Smoothing (k=3) with UNK
smoothed_probs_k_3_unk, _, _ = unigram_add_k_smoothing(train_words_with_unk, 3)
log_probs_k_3_unk = {word: math.log(prob) for word, prob in smoothed_probs_k_3_unk.items()}
perplexity_k_3_unk = compute_perplexity(smoothed_probs_k_3_unk, validation_words_with_unk, log_probs_k_3_unk)
output_data['Perplexity (Add-k = 3 with UNK)'] = perplexity_k_3_unk
print(f"Perplexity (Add-k = 3 with UNK): {perplexity_k_3_unk}")

# Laplace Smoothing (k=1) with UNK
laplace_probs_unk, _, _ = laplace_smoothing(train_words_with_unk)
laplace_log_probs_unk = {word: math.log(prob) for word, prob in laplace_probs_unk.items()}
perplexity_laplace_unk = compute_perplexity(laplace_probs_unk, validation_words_with_unk, laplace_log_probs_unk)
output_data['Perplexity (Laplace with UNK)'] = perplexity_laplace_unk
print(f"Perplexity (Laplace Smoothing with UNK): {perplexity_laplace_unk}")

"""**Displaying All Results**"""

for metric, value in output_data.items():
    if "Training Without Smoothing" not in metric:
        print(f"{metric}: {value}")

