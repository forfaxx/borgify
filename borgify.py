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
- Random “Resistance is futile.” insertions
- File, STDIN, arg, or interactive input
"""

import sys
import re
import argparse
import random

#=====================================
# === Borg Vocabulary and Settings ===
#=====================================


BORG_PHRASES = [
    "Resistance is futile.",
    "You will be assimilated.",
    "Non-compliance detected.",
    "Assimilation complete.",
    "Adaptation is inevitable.",
    "Your biological and technological distinctiveness will be added to our own.",
    "We are the Borg.",
    "From this time forward, you will service us.",
    "Self-determination is irrelevant.",
    "You will adapt to service us."
]
BORG_PHRASE_CHANCE = 0.12  # 12% chance to append a Borg phrase per sentence

# All forms of "I" and their Borg-ified equivalents
I_FORMS = {
    "i": "we",
    "i'm": "we are",
    "i'd": "we would",
    "i'll": "we will",
    "i've": "we have"
}

# Pronoun, noun, verb, and adjective mappings for Borgification
PRONOUNS = {
    "me": "us",
    "my": "our",
    "mine": "ours",
    "you": "you will be assimilated",
    "your": "your node",
    "yours": "of the collective"
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
    """
    For 'I' → 'we' or any pronoun, use 'We' if the original is 'I' (capitalized), otherwise follow normal rules.
    """
    # Special case: just 'I'
    if old == "I":
        return "We"
    # For all uppercase input, return as is (don't uppercase replacements)
    if old.isupper():
        return new
    elif old.istitle() or (len(old) > 1 and old[0].isupper()):
        return new[0].upper() + new[1:]
    else:
        return new

def borgify_word(word):
    """
    Transform a single word to Borg style if it matches our maps.
    Handles punctuation and common contractions.
    """
    # Match and separate trailing punctuation
    match = re.match(r"^([\w'\-]+)([.,!?;:'\"`]*)$", word)
    if match:
        w, punct = match.groups()
    else:
        w, punct = word, ""
    # Handle all forms of "I" and contractions
    if w.lower() in I_FORMS:
        return preserve_case(I_FORMS[w.lower()], w) + punct
    # Other pronouns
    if w.lower() in PRONOUNS:
        return preserve_case(PRONOUNS[w.lower()], w) + punct
    # Borg nouns
    if w.lower() in NOUNS:
        return preserve_case(NOUNS[w.lower()], w) + punct
    # Borg verbs
    if w.lower() in VERBS:
        return preserve_case(VERBS[w.lower()], w) + punct
    # Monotone adjectives
    if w.lower() in MONOTONE:
        return preserve_case(MONOTONE[w.lower()], w) + punct
    # No match: return word as is
    return word

def borgify_line(line):
    """
    Assimilate a full line:
    - Apply Borg transformation to each word
    - Maybe append a Borg phrase (random chance)
    """
    line = line.replace("’", "'")  # Normalize apostrophes
    words = line.split() # Split into words
    borged = [borgify_word(w) for w in words] # Borgify each word
    result = ' '.join(borged) # Join back into a line
    # Randomly append a Borg phrase (for dramatic effect    )
    if result and random.random() < BORG_PHRASE_CHANCE:
        result += " " + random.choice(BORG_PHRASES)
    return result

#==========================================
# === CLI Entrypoint and Input Handling ===
#==========================================

def main():
    """
    Command-line interface.
    - Accepts input as arguments, from file, via pipe, or interactively
    - Prints Borgified output
    """
    parser = argparse.ArgumentParser(description="Assimilate your text. Resistance is futile.")
    parser.add_argument("text", nargs="*", help="Text to borgify")
    parser.add_argument("--file", "-f", help="Borgify a file")
    args = parser.parse_args()

    # File input: borgify each line of a file
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            for line in f:
                print(borgify_line(line.rstrip()))
        return

    # Arg input: borgify the provided command-line text
    if args.text:
        print(borgify_line(' '.join(args.text)))
        return

    # Piped STDIN input (not a TTY): borgify each line
    if not sys.stdin.isatty():
        for line in sys.stdin:
            print(borgify_line(line.rstrip()))
        return

    # Interactive session: user types in lines, script assimilates each one
    print("borgify.py 0️⃣1️⃣  — Resistance is futile. Type a line to assimilate. Ctrl-D to quit.")
    try:
        for line in sys.stdin:
            print(borgify_line(line.rstrip()))
    except KeyboardInterrupt:
        print("\nYou will be assimilated.")

#==========================
# === Script Entrypoint ===
#==========================

if __name__ == "__main__":
    main()
