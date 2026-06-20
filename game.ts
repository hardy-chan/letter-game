// AI TypeScript implementation of AddLetter.py with Trie optimizations and direct GitHub streaming for word lists

// TrieNode definition for Trie data structure
interface TrieNode {
    [key: string]: TrieNode;
}

// Sandbox wrapper to encapsulate all game logic and state
(() => {
    // State variables
    let word_trie: TrieNode = {};
    let word_so_far: string = "";
    let player_wins: number = 0;
    let computer_wins: number = 0;
    const alphabet: string = 'abcdefghijklmnopqrstuvwxyz';

    // URL to GitHub repository text resources
    const repo_base_url = "https://rawcdn.githack.com/hardy-chan/letter_game/main/";
    const dict_urls: { [key: string]: string } = {
        "1": repo_base_url + "words_alpha.txt",
        "2": repo_base_url + "enable1_words.txt"
    };

    // Build Trie from word list. Time: O(N*L), N=number of words (370,000+), L=average word length.
    function build_trie(word_list: string[]): TrieNode {
        const trie: TrieNode = {};
        for (const word of word_list) {
            let current_node: TrieNode = trie;
            const clean_word = word.toLowerCase().trim();
            if (!clean_word) continue;

            for (const char of clean_word) {
                if (!current_node[char]) {
                    current_node[char] = {};
                }
                current_node = current_node[char];
            }
        }
        return trie;
    }

    // Check if a given prefix exists in the Trie. Time: O(L), L=length of prefix.
    function prefix_exists(trie: TrieNode, prefix: string): boolean {
        let current_node: TrieNode = trie;
        for (const char of prefix) {
            if (!current_node[char]) return false;
            current_node = current_node[char];
        }
        return true;
    }

    // Get valid next letters from Trie after a given prefix. Time: O(L+M), L=length of prefix, M=number of valid next letters.
    function get_valid_next_letters(trie: TrieNode, prefix: string): string[] {
        let current_node: TrieNode = trie;
        for (const char of prefix) {
            if (!current_node[char]) return [];
            current_node = current_node[char];
        }
        return Object.keys(current_node);
    }

    // HTML DOM Element Bindings
    const start_btn = document.getElementById('wp-start-btn') as HTMLButtonElement;
    const game_board = document.getElementById('wp-game-board') as HTMLDivElement;
    const word_display = document.getElementById('wp-word-display') as HTMLDivElement;
    const game_status = document.getElementById('wp-game-status') as HTMLParagraphElement;
    const user_letter_input = document.getElementById('wp-user-letter') as HTMLInputElement;
    const submit_btn = document.getElementById('wp-submit-letter') as HTMLButtonElement;
    const difficulty_select = document.getElementById('wp-difficulty') as HTMLSelectElement;
    const dict_select = document.getElementById('wp-dict-select') as HTMLSelectElement;

    // Game Setup & Remote Streaming Sequence
    start_btn.addEventListener('click', async () => {
        const dict_choice = dict_select.value;
        
        game_status.textContent = "Fetching remote dictionary from GitHub... Please wait.";
        start_btn.disabled = true;

        try {
            // Asynchronously fetch the raw text from GitHub repo stream
            const response = await fetch(dict_urls[dict_choice]);
            if (!response.ok) throw new Error("Network connection failure reaching dictionary files.");
            
            const raw_text = await response.text();
            
            // Cleanly slice down lines into an individual array stream of words
            const word_list = raw_text.split(/\r?\n/);
            
            // Construct the instant lookup character tree structure
            word_trie = build_trie(word_list);
            
            // Re-initialize local tracking values
            word_so_far = "";
            word_display.textContent = "-";
            game_status.textContent = "Dictionary loaded successfully! Your turn, pick a letter.";
            game_board.style.display = 'block';
            user_letter_input.disabled = false;
            submit_btn.disabled = false;
            user_letter_input.focus();
        } catch (error) {
            game_status.textContent = "Error down-streaming tracking data assets from GitHub branch.";
            console.error(error);
        } finally {
            start_btn.disabled = false;
        }
    });

    submit_btn.addEventListener('click', handle_turn);
    user_letter_input.addEventListener('keypress', (e: KeyboardEvent) => { 
        if (e.key === 'Enter') handle_turn(); 
    });

    // Main Gameplay Turning Mechanism
    function handle_turn(): void {
        const letter: string = user_letter_input.value.toLowerCase().trim();
        user_letter_input.value = "";
        
        if (letter.length !== 1 || !/[a-z]/.test(letter)) {
            alert("Please provide a single valid character alphabet token (A-Z).");
            return;
        }

        word_so_far += letter;
        word_display.textContent = word_so_far.toUpperCase();

        // Validate user selection route path via Trie tree
        if (!prefix_exists(word_trie, word_so_far)) {
            game_status.textContent = "No valid words can be formed! AI wins!";
            computer_wins++;
            const computer_wins_el = document.getElementById('wp-computer-wins');
            if (computer_wins_el) computer_wins_el.textContent = computer_wins.toString();
            end_game();
            return;
        }

        game_status.textContent = "AI calculation engine computing next turn...";
        user_letter_input.disabled = true;
        submit_btn.disabled = true;

        // Artificial thinking delay to keep pacing natural
        setTimeout(() => {
            const diff: string = difficulty_select.value;
            let chosen_char: string = "";

            if (diff === "1") {
                chosen_char = alphabet[Math.floor(Math.random() * alphabet.length)];
            } else {
                const valid_choices: string[] = get_valid_next_letters(word_trie, word_so_far);
                if (valid_choices.length > 0) {
                    chosen_char = valid_choices[Math.floor(Math.random() * valid_choices.length)];
                } else {
                    chosen_char = alphabet[Math.floor(Math.random() * alphabet.length)];
                }
            }

            word_so_far += chosen_char;
            word_display.textContent = word_so_far.toUpperCase();
            game_status.textContent = `AI dropped letter: "${chosen_char.toUpperCase()}". Your turn!`;
            user_letter_input.disabled = false;
            submit_btn.disabled = false;
            user_letter_input.focus();

            // Validate AI selection route path via Trie tree
            if (!prefix_exists(word_trie, word_so_far)) {
                game_status.textContent = "No valid words can be formed! You win! 🎉";
                player_wins++;
                const player_wins_el = document.getElementById('wp-player-wins');
                if (player_wins_el) player_wins_el.textContent = player_wins.toString();
                end_game();
            }
        }, 500);
    }

    function end_game(): void {
        user_letter_input.disabled = true;
        submit_btn.disabled = true;
    }
})();
