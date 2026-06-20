# LETTER GAME

A turn-based word formulation game played against computer. 

Written originally in Python, optimized and re-implemented on webpage in HTML with TypeScript. Under AI assistance.

<img width="935" height="559" alt="Screenshot 2026-06-08 204452" src="https://github.com/user-attachments/assets/61695930-5f38-4fcf-8711-1c6be0717d4d" />


# Windows Desktop Application

Using **PyInstaller** under AI assistance, I compiled the core Python game engine into a standalone Windows executable (`.exe`) console application.

* **Downloadable on [**GitHub Releases**](https://github.com/hardy-chan/letter-game/releases)**
* **How to Install:** 
  1. Download the **`AddLetter.zip`** folder from the latest release.
  2. Right-click the folder and choose **"Extract All"** (Unzip) to open it.
  3. Open the extracted folder and navigate into the **`\dist\AddLetter`** folder.
  4. Double-click the `AddLetter.exe` file inside to play the terminal version of the game instantly!
* **Independent Runtime:** Users do not need to install Python, libraries, or any code engines on their computer to run the game application.


# Web deployment

For instant availablity on a browser, the code is rewritten from backend Python to frontend TypeScript (logic) + HTML5 (structure) + CSS3 (styling) under AI assistance.

* **Playable on [**GitHub**](https://hardy-chan.github.io/letter-game/) or alternatively on [**CodePen**](https://codepen.io/editor/hardychan/pen/019ea935-6f9d-7609-9c36-9550d9286527)**

<img width="970" height="788" alt="Screenshot 2026-06-09 002730" src="https://github.com/user-attachments/assets/0256b269-fcb3-44c2-a6e3-01e06e6a0594" />

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



