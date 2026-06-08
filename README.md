# LETTER GAME

A turn-based word formulation game played against an AI. 

# Performance Optimization (Trie)

The game engine is backed by a highly optimized **Trie (Prefix Tree)** data structure to achieve ultra-fast runtime lookups.

Loading time: O(N*L), N = number of words listed (370,000+), L = length of a word

Running time: O(L), L = length of a word

# Python Implementation (Desktop Engine)

This is the backend implementation used to power the standalone executable console application.

```python
def build_trie(word_list) -> dict:
    # Realize words as prefix tree (Trie). Time: O(N*L)=O(number_of_words * word_length)
    # Optimize performance for later prefix checks and next letter retrieval as O(L).
    trie = {}
    for word in word_list:
        current_node = trie
        for char in word:
            if char not in current_node:
                current_node[char] = {}
            current_node = current_node[char]
    return trie

def prefix_exists(trie, prefix) -> bool:
    # Checks if a prefix exists in the Trie. Time: O(L).
    current_node = trie
    for char in prefix:
        if char not in current_node:
            return False
        current_node = current_node[char]
    return True

def get_valid_next_letters(trie, prefix) -> list:
    # Returns characters that can continue the prefix. Time: O(L). 
    current_node = trie
    for char in prefix:
        if char not in current_node:
            return []
        current_node = current_node[char]
    return list(current_node.keys())
```