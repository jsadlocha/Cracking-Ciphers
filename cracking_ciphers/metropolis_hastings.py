import text_utils as utils
import string
import random
import math as m

def main():
    # plain_text = "The little princess had grown stouter during this time"
    plain_text = """The little princess went round the table with quick, short, swaying
steps, her workbag on her arm, and gaily spreading out her dress sat
down on a sofa near the silver samovar, as if all she was doing was a
pleasure to herself and to all around her"""
    plain_text = utils.preprocess_text(plain_text)
    alphabet = string.ascii_lowercase+' ,'
    key = [x for x in alphabet]
    random.shuffle(key)
    key = ''.join(key)
    encrypted = utils.encrypt_substitution(plain_text, key, alphabet)
    #decrypted = utils.decrypt_substitution(encrypted, key, alphabet)

    corps = utils.read_corps("book.txt")
    corps = utils.preprocess_text(corps)
    pair_freq = utils.get_probability_for_pairs(corps)

    current = [x for x in alphabet]
    random.shuffle(current)
    i = 0
    decoded_letters = 0
    best_decoded = 0
    while i < 10000:
        proposed = utils.random_mutate_swap(current)

        cur_decrypt = utils.decrypt_substitution(encrypted, ''.join(current), alphabet)
        prop_decrypt = utils.decrypt_substitution(encrypted, ''.join(proposed), alphabet)

        cur_like = utils.get_likelihood_for_sequence(cur_decrypt, pair_freq)
        prop_like = utils.get_likelihood_for_sequence(prop_decrypt, pair_freq)

        alfa = random.uniform(0, 1)
        accept_prob = min(1, m.exp(prop_like - cur_like))
        accept = accept_prob >= alfa

        if accept:
            current = proposed
            print(f'Decoded: { prop_decrypt }')
            i += 1
            # debug
            decoded_letters = sum([1 if proposed[j] == key[j] else 0 for j in range(len(key))])
            best_decoded = max(best_decoded, decoded_letters)
            if decoded_letters == best_decoded:
                best_key = proposed

    # debug
    print(best_decoded)
    print(''.join(best_key))
    print(key)
    print(plain_text)
    print(utils.decrypt_substitution(encrypted, proposed, alphabet))

if __name__ == "__main__":
    main()

