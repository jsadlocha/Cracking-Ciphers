import requests
import re
import math as m
from typing import Iterator, Dict, List, Tuple
from collections import defaultdict

MIN_PROB = .0

def download_book(url: str, filename: str = 'book.txt'):
    """Download book from url and store in file."""
    response = requests.get(url, timeout=15)
    if response.status_code == 200:
        with open(filename, 'w') as file:
            file.write(response.text)
    else:
        print('Download Error!')

    print(f'Download status: {response.status_code}')

def read_corps(filename: str, encoding="utf-8") -> str:
    """Read and return corpus of data from file."""
    with open(filename, 'r', encoding=encoding) as file:
        corps = file.read()
    return corps

def preprocess_text(corps: str) -> str:
    """Clean text from uncecessary characters."""
    pattern = r'[^a-z ]'
    text = corps.lower()
    text = re.sub(pattern, "", text)
    text = re.sub(r'\s{2,}', " ", text)
    return text

def generate_letters_pairs(corps: str) -> Iterator[str]:
    """Return generator pairs for given corpus of data."""
    for idx in range(len(corps)-1):
        yield corps[idx:idx+2]

def calc_probability_for_pairs(corps: str) -> Dict[str, float]:
    """Calculate transition probability of pairs for given corpus of data."""
    global MIN_PROB
    freq_pair: Dict[str, float] = defaultdict(float)
    iterator = generate_letters_pairs(corps)
    for pair in iterator:
        freq_pair[pair] += 1

    norm = sum(freq_pair.values())
    MIN_PROB = 1/norm
    freq_pair.update((k, v / norm) for (k, v) in freq_pair.items())

    return freq_pair

def calc_probability_for_letters(corps: str) -> Dict[str, float]:
    """Calculate probability of the given letters."""
    freq: Dict[str, float] = defaultdict(float)
    for letter in corps:
        freq[letter] += 1

    freq.pop(' ')
    norm = sum(freq.values())
    freq.update((k, v / norm) for k, v in freq.items())
    return freq

def get_sorted_probability(freq: Dict[str, float]) -> List[Tuple[float, str]]:
    """Return sorted dictionary given probability."""
    return sorted([(value, key) for (key, value) in freq.items()], reverse=True)

def get_loglikelihood_from_dict(pair: str, pair_freq: Dict[str, float]) -> float:
    """Return log probability for given pair."""
    log_prob = 0.0
    if pair in pair_freq:
        log_prob = m.log(pair_freq[pair])
    else:
        log_prob = MIN_PROB

    return log_prob

def calc_likelihood_for_sequence(sequence: str, pair_freq: Dict[str, float]) -> float:
    """Calculate likelihood for given sequence."""
    iterator = generate_letters_pairs(sequence)
    likelihood = sum((get_loglikelihood_from_dict(x, pair_freq) for x in iterator))
    return m.exp(likelihood)

def download_default_english_book():
    """Download example book."""
    url = "https://www.gutenberg.org/cache/epub/2600/pg2600.txt"
    download_book(url, 'book.txt')

def encrypt_substitution(sequence: str, key: str, alphabet: str) -> str:
    if len(key) != len(alphabet):
        print("Key and alphabet should be equal in length!")
        return ''

    mapping: Dict[str, str] = defaultdict(str)
    mapping.update([(alphabet[x], key[x]) for x in range(len(alphabet))])

    cipher = ''.join(map(lambda x: mapping[x], sequence))
    return cipher

def decrypt_substitution(sequence: str, key: str, alphabet: str) -> str:
    if len(key) != len(alphabet):
        print("Key and alphabet should be equal in length!")
        return ''

    mapping: Dict[str, str] = defaultdict(str)
    mapping.update([(key[x], alphabet[x]) for x in range(len(alphabet))])

    text = ''.join(map(lambda x: mapping[x], sequence))
    return text

if __name__ == "__main__":
    pass
