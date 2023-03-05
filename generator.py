from hashlib import sha256
import secrets


# Not my code, credits to: https://stackoverflow.com/questions/75160906/python-code-for-generating-valid-bip-39-mnemonic-words-for-a-bitcoin-wallet-not

# following the instructions here: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
# # depending on the number of words, we take the value for ENT, and CS.a

def generate_word_phrase():
    words_extracted = None

    word_number = 24
    size_ent = 256
    size_cs = int(size_ent / 32)

    with open("wordlist/english.txt", "r") as wordlist_file:
        words = [word.strip() for word in wordlist_file.readlines()]

    # First, an initial entropy of ENT bits is generated.
    n_bytes = int(size_ent / 8)
    random_bytes = secrets.token_bytes(n_bytes)
    random_bits = ''.join(['{:08b}'.format(b) for b in random_bytes])
    initial_entropy = random_bits[:size_ent]
    assert (len(initial_entropy) == size_ent)

    hash = sha256(random_bytes).digest()
    bhash = ''.join(format(byte, '08b') for byte in hash)

    assert (len(bhash) == 256)

    # the first ENT / 32 bits of its SHA256 hash
    cs = bhash[:size_cs]

    # This checksum is appended to the end of the initial entropy.
    final_entropy = initial_entropy + cs
    assert (len(final_entropy) == size_ent + size_cs)

    # Next, these concatenated bits are split into groups of 11 bits,
    # each encoding a number from 0-2047, serving as an index into a wordlist.
    for t in range(word_number):
        # split into groups of 11 bits,
        extracted_bits = final_entropy[11 * t:11 * (t + 1)]

        # each encoding a number from 0-2047,
        word_index = int(extracted_bits, 2)

        # serving as an index into a wordlist.
        if t == 0:
            words_extracted = words[word_index]
        else:
            words_extracted += ' ' + words[word_index]

    return words_extracted
