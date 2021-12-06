import collections
from itertools import islice
import math
import random
import string

import pandas as pd
import matplotlib.pyplot as plt

# Helper function we'll use to preview dictionaries
def take(n, iterable):
    return list(islice(iterable, n))

# Get all the text from a file, converting to lowercase
#   and removing everything except letters and spaces
def get_simple_text(filename):
    with open(filename) as file_in:
        all_text = file_in.read()
    # Remove all punctuation + numbers
    out = []
    for c in all_text.lower():
        # Make sure we don't add double spaces
        if c in (' ', '\n', '\t', '\r'):
            if out and out[-1] != ' ':
                out.append(' ')
        if c in string.ascii_lowercase:
            out.append(c)
    return ''.join(out)


alice = 'the hot day made her feel very sleepy and stupid whether the pleasure of making a daisychain'
frank = 'rks in a little boat with his holiday mates on an expedition of discovery up his native river but su'
print(alice[1012:1105])
print(frank[3000:3100])

def make_random_key():
    out_letters = list(string.ascii_lowercase)
    random.shuffle(out_letters)
    key = dict(zip(string.ascii_lowercase, out_letters))
    return key

encrypt_key = make_random_key()
take(5, encrypt_key.items())


def decrypt(code, key):
    trans = str.maketrans(key)
    return code.translate(trans)

alice_encrypted = decrypt(alice, encrypt_key)
alice_encrypted[1012:1105]

def make_letter_probs(text):
    counts = collections.Counter(text)
    total = sum(counts.values())

    probs = {}
    for c in counts:
        # Ignore space
        if c == ' ':
            continue
        probs[c] = counts[c] / total
    return probs

def make_bigram_probs(text):
    freqs = collections.defaultdict(collections.Counter)
    for c1, c2 in zip(text[:-1], text[1:]):
        freqs[c1][c2] += 1

    prob_table = collections.defaultdict(dict)
    for c1, c1_counts in freqs.items():
        total = sum(c1_counts.values())
        for c2, freq in c1_counts.items():
            prob_table[c1][c2] = freq / total
    return prob_table


letter_probs = make_letter_probs(frank)
take(5, letter_probs.items())

bigram_probs = make_bigram_probs(frank)
take(5, bigram_probs['a'].items())



bi_df = pd.DataFrame.from_dict(bigram_probs)
bi_df.sort_index(axis = 'columns', inplace=True)

fig, ax = plt.subplots()
im = ax.imshow(bi_df, cmap=plt.cm.viridis, vmin=0, vmax=1)
fig.colorbar(im)
ax.set_title("Bigram probabilities")
ax.xaxis.tick_top()
ax.set_xlabel('First letter')
ax.set_ylabel('Second letter')
ax.xaxis.set_label_position('top')
ax.set_xticks(range(27))
ax.set_yticks(range(27))
ax.set_xticklabels(' ' + string.ascii_lowercase)
ax.set_yticklabels(' ' + string.ascii_lowercase)
fig.set_size_inches((9, 7))


def score_text(text, letter_probs, bigram_probs,
               letter_weight=1.0,
               bigram_weight=1.0):
    # Normalise weights to sum to 1
    total_weight = letter_weight + bigram_weight
    letter_weight = letter_weight / total_weight
    bigram_weight = bigram_weight / total_weight

    total_logprob = 0
    for c1, c2 in zip(text[:-1], text[1:]):
        # Use a default of 1 for letter prob, basically
        #   ignore spaces
        letter_prob = letter_probs.get(c1, 1)
        bigram_prob = bigram_probs[c1].get(c2, 0.001)
        total_logprob += math.log(
            letter_weight * letter_prob +
            bigram_weight * bigram_prob
        )

    return total_logprob

score_text(alice_encrypted, letter_probs, bigram_probs)


letter_weight = 1.0
bigram_weight = 1.0
iterations = int(1e4)
print_every = 1000

decrypt_key = make_random_key()
best_decrypt = decrypt(alice_encrypted, decrypt_key)
best_score = score_text(best_decrypt, letter_probs, bigram_probs,
                        letter_weight = letter_weight,
                        bigram_weight = bigram_weight)

for iter_num in range(iterations):
    a, b = random.choices(string.ascii_lowercase, k=2)
    # Swap two letters
    decrypt_key[a], decrypt_key[b] = decrypt_key[b], decrypt_key[a]
    current_decrypt = decrypt(alice_encrypted, decrypt_key)
    new_score = score_text(current_decrypt, letter_probs, bigram_probs,
                           letter_weight = letter_weight,
                           bigram_weight = bigram_weight)
    if new_score > best_score:
        best_score = new_score
    else:
        # Swap back
        decrypt_key[a], decrypt_key[b] = decrypt_key[b], decrypt_key[a]
    # Check progress
    if iter_num % print_every == 0:
        print('{n}: {d}'.format(n=iter_num,
                                d=current_decrypt[1012:1105]))
print(current_decrypt[1012:1105])


def reverse_key(key):
    return {c2: c1 for c1, c2 in key.items()}

true_decrypt_key = reverse_key(encrypt_key)
decrypt_key == true_decrypt_key