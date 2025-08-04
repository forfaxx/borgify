#!/usr/bin/env python3
"""
borgify.py 0️⃣1️⃣  — Assimilate your text into Borg-style language.

Transforms ordinary sentences into Borg-speak: collective pronouns, Borg-ified nouns,
action verbs, and signature phrases. Inspired by the vocabulary of Star Trek’s most
efficient workflow managers.

Features:
- Pronoun & noun replacement (we, collective, biological unit, etc)
- Tech-y verb mapping (“execute subroutine,” “synthesize node”)
- Handles "I" and its contractions robustly
- Random < BORG PHRASE > insertions after sentences
- File, STDIN, arg, or interactive input
- Skips lines like '-- Attribution'
- Handles compound verbs/idioms before borgification
"""

import sys
import re
import argparse
import random
import string

#=====================================
# === Borg Vocabulary and Settings ===
#=====================================

BORG_PHRASES = [
    "RESISTANCE IS FUTILE.",
    "YOU WILL BE ASSIMILATED.",
    "NON-COMPLIANCE DETECTED.",
    "ASSIMILATION COMPLETE.",
    "ADAPTATION IS INEVITABLE.",
    "YOUR BIOLOGICAL AND TECHNOLOGICAL DISTINCTIVENESS WILL BE ADDED TO OUR OWN.",
    "WE ARE THE BORG.",
    "FROM THIS TIME FORWARD, YOU WILL SERVICE US.",
    "SELF-DETERMINATION IS IRRELEVANT.",
    "YOU WILL ADAPT TO SERVICE US."
]
BORG_PHRASE_CHANCE = 0.12  # 12% chance to append a Borg phrase per sentence

PHRASAL_VERBS = {
    "find out": "detect",
    "give up": "cease functioning",
    "make sure": "verify",
    "turn on": "activate",
    "turn off": "deactivate",
    "break down": "malfunction",
    "figure out": "resolve",
    "set up": "initialize",
    "shut down": "deactivate",
    "look for": "probe for",
    "bring up": "signal",
    # Add more as you find them!
}

I_FORMS = {
    "i": "we",
    "i'm": "we are",
    "i'd": "we would",
    "i'll": "we will",
    "i've": "we have",
    "I": "We",
    "I'm": "We are",
    "I'd": "We would",
    "I'll": "We will",
    "I've": "We have"
}

PRONOUNS = {
    "me": "us",
    "my": "our",
    "mine": "ours",
    "you": "you will be assimilated",
    "your": "your node",
    "yours": "of the collective",
    "oneself": "ourselves",
    "himself": "ourself",
    "herself": "ourself",
    "itself": "ourself",
    "themselves": "ourselves",
}
NOUNS = {
    "human": "biological unit",
    "humans": "biological units",
    "person": "biological unit",
    "people": "biological units",
    "friend": "adjacent node",
    "friends": "adjacent nodes",
    "man": "unit",
    "men": "units",
    "woman": "unit",
    "women": "units",
    "team": "collective",
    "server": "node",
    "network": "collective link",
    "script": "subroutine",
    "code": "subroutine",
    "error": "non-compliance",
    "success": "assimilation complete",
    "failure": "assimilation incomplete",
    "life": "continuum",
    "world": "system",
    "heart": "core",
    "mind": "neural array",
    "truth": "prime directive",
    "problem": "malfunction",
    "time": "cycle",
    "light": "energy source",
    "darkness": "subsystem offline",
    "question": "query",
    "answer": "response",
    "dream": "subroutine",
    "dreams": "subroutines",
    "day": "cycle",
    "days": "cycles",
    "night": "cycle",
    "nights": "cycles",
    "year": "cycle",
    "years": "cycles",
    "child": "sub-unit",
    "children": "sub-units",
    "enemy": "unassimilated entity",
    "enemies": "unassimilated entities"
}

VERBS = {
    "run": "execute",
    "try": "initiate subroutine",
    "build": "synthesize",
    "help": "provide interface assistance",
    "fix": "repair",
    "connect": "link",
    "test": "probe",
    "start": "activate",
    "stop": "halt",
    "send": "transmit",
    "receive": "receive",
    "be": "function as",
    "am": "function as",
    "is": "functions as",
    "are": "function as",
    "was": "functioned as",
    "were": "functioned as",
    "do": "execute",
    "did": "executed",
    "does": "executes",
    "go": "transmit",
    "went": "transmitted",
    "see": "detect",
    "saw": "detected",
    "look": "detect",
    "feel": "register stimulus",
    "felt": "registered stimulus",
    "become": "assimilate",
    "give": "provide",
    "take": "acquire",
    "get": "retrieve",
    "got": "retrieved",
    "make": "synthesize",
    "made": "synthesized",
    "know": "process",
    "knew": "processed",
    "find": "locate",
    "found": "located",
    "choose": "select",
    "chose": "selected",
    "want": "require",
    "keep": "retain",
    "call": "signal",
    "leave": "exit",
    "enter": "access",
    "ask": "query",
    "bring": "deliver"
}

MONOTONE = {
    "good": "satisfactory",
    "bad": "suboptimal",
    "great": "noted",
    "awesome": "functional",
    "love": "approve of",
    "hate": "disapprove of",
    "new": "recently assimilated",
    "old": "legacy",
    "easy": "low-complexity",
    "hard": "high-complexity",
    "difficult": "high-complexity",
    "important": "priority",
    "happy": "satisfactory",
    "sad": "suboptimal",
    "big": "expansive",
    "large": "expansive",
    "huge": "expansive",
    "small": "minimal",
    "little": "minimal",
    "strong": "robust",
    "weak": "unstable",
    "fast": "accelerated",
    "quick": "accelerated",
    "slow": "decelerated",
    "bright": "high-output",
    "dark": "offline",
    "terrible": "critical",
    "horrible": "critical",
    "best": "optimal",
    "worst": "lowest-functioning",
    "smart": "well-adapted",
    "clever": "well-adapted"
}

#====================================
# === Word Transformation Helpers ===
#====================================

def preserve_case(new, old):
    if old.isupper():
        return new.upper()
    elif old.istitle() or (len(old) > 1 and old[0].isupper()):
        return new[0].upper() + new[1:]
    else:
        return new

def pre_borgify(line):
    for phrase, replacement in PHRASAL_VERBS.items():
        # \b ensures whole-phrase matching, case-insensitive
        pattern = re.compile(rf'\b{re.escape(phrase)}\b', re.IGNORECASE)
        line = pattern.sub(replacement, line)
    return line

def borgify_word(word):
    # Separate word from trailing punctuation (handles most symbols)
    match = re.match(r"^([A-Za-z0-9'’\-]+)([^\w']*)$", word)
    if match:
        w, punct = match.groups()
    else:
        w, punct = word, ""
    wl = w.lower()
    # Handle "I" and contractions robustly
    if w in I_FORMS:
        return preserve_case(I_FORMS[w], w) + punct
    elif wl in I_FORMS:
        return preserve_case(I_FORMS[wl], w) + punct
    if wl in PRONOUNS:
        return preserve_case(PRONOUNS[wl], w) + punct
    if wl in NOUNS:
        return preserve_case(NOUNS[wl], w) + punct
    if wl in VERBS:
        return preserve_case(VERBS[wl], w) + punct
    if wl in MONOTONE:
        return preserve_case(MONOTONE[wl], w) + punct
    return word

def smart_split(line):
    # Splits, keeping punctuation separate for transformation
    # Handles Unicode and ASCII
    return re.findall(r"[A-Za-z0-9'’\-]+|[^\w\s]", line)

def borgify_line(line):
    line = line.replace("’", "'")  # Normalize apostrophes
    line = pre_borgify(line)       # Phrasal verb prepass
    sentences = re.split(r'([.!?])', line)
    output = []
    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i].strip()
        punct = sentences[i+1]
        if not sentence:
            continue
        words = smart_split(sentence)
        borged = [borgify_word(w) for w in words]
        borgified = ' '.join(borged) + punct
        if random.random() < BORG_PHRASE_CHANCE:
            borgified += " < " + random.choice(BORG_PHRASES) + " >"
        output.append(borgified)
    # Handle trailing fragment if present
    if len(sentences) % 2 == 1 and sentences[-1].strip():
        output.append(' '.join([borgify_word(w) for w in smart_split(sentences[-1].strip())]))
    return ' '.join(output)

#==========================================
# === CLI Entrypoint and Input Handling ===
#==========================================

def main():
    parser = argparse.ArgumentParser(description="Assimilate your text. < RESISTANCE IS FUTILE >")
    parser.add_argument("input", nargs="*", help="Text or filename to assimilate")
    args = parser.parse_args()

    # 1. If piped input, assimilate that (skipping attribution lines)
    if not sys.stdin.isatty():
        for line in sys.stdin:
            if line.strip().startswith("-- "):
                print(line.rstrip())
            else:
                print(borgify_line(line.rstrip()))
        return

    # 2. If one arg and it's a readable file, assimilate file (skipping attribution lines)
    if len(args.input) == 1:
        try:
            with open(args.input[0], "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("-- "):
                        print(line.rstrip())
                    else:
                        print(borgify_line(line.rstrip()))
            return
        except FileNotFoundError:
            pass  # Not a file, treat as text

    # 3. If any args, treat as literal text
    if args.input:
        print(borgify_line(' '.join(args.input)))
        return

    # 4. Otherwise, go interactive
    print("borgify.py 0️⃣1️⃣  — < RESISTANCE IS FUTILE > Type a line to assimilate. Ctrl-D to quit.")
    try:
        while True:
            inp = input("> ")
            print(borgify_line(inp))
    except (EOFError, KeyboardInterrupt):
        print("\n< YOU WILL BE ASSIMILATED >")

#==========================
# === Script Entrypoint ===
#==========================

if __name__ == "__main__":
    main()
