import os
import urllib.request

file_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(file_dir, 'input')
input_path = os.path.join(input_dir, 'input.txt')


MAX_CNT = 20000
INPUT_PROMPT = "Please enter the command:\n"


def ensure_input():
    if not os.path.exists(input_path):
        urllib.request.urlretrieve('https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt', input_path)
    ret = list()
    with open(input_path) as f:
        for line in f:
            ret.append(line.strip().upper())
    return ret


words = ensure_input()


def is_done(cmd):
    return cmd == 'Q'


def is_start(cmd):
    return cmd == 'S'


def valid_cmd(cmd):
    return len(cmd) == 10 and cmd[0:5].isalpha() and set(cmd[5]) < set('012')


def valid_word(word, char_map, char_set):
    for c in char_set:
        if c not in word:
            return False
    for i in range(0, len(word)):
        c = word[i].upper()
        ci = ord(c) - ord('A')
        if char_map[ci][i] != 1:
            return False
    return True


def cracker():
    # 2D list [char][pos]
    char_map = [[1 for _ in range(5)] for __ in range(26)]
    char_set = set()
    for i in range(26):
        char_map
    while True:
        cmd = input(INPUT_PROMPT)
        cmd = cmd.strip().upper()
        if is_done(cmd):
            return
        if is_start(cmd):
            char_map = [[1 for _ in range(5)] for __ in range(26)]
            continue
        # ABCDE01122
        if not valid_cmd(cmd):
            print("Please provide a command like this - ABCDE01122\n"
                  ", where ABCDE is the guess, 01122 is the feedback.\n"
                  "0 means no such letter;\n"
                  "1 means letter included but pos is wrong;\n"
                  "2 means letter included and pos in right.\n")
            continue
        for i in range(5, 10):
            letter_idx = ord(cmd[i - 5]) - ord('A')
            if cmd[i] == '0':
                char_map[letter_idx] = [0] * 5
                continue
            if cmd[i] == '1':
                char_map[letter_idx][i - 5] = 0
                char_set.add(cmd[i - 5])
                continue
            for ch in range(26):
                if ch != letter_idx:
                    char_map[ch][i - 5] = 0
        answers = list()
        for word in words:
            if valid_word(word, char_map, char_set):
                answers.append(word)
                if len(answers) >= MAX_CNT:
                    break
        print(answers)
        assert (len(answers) > 0)


if __name__ == '__main__':
    cracker()
