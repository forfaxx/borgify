
# borgify.py

![borgify](borgify-hex.png)

> Resistance is futile.  
> Turn ordinary human text into something the Collective would be proud of.

---

## What is borgify.py?

`borgify.py` is a command-line tool that takes your normal sentences and transforms them into Borg-speak:  
- Personal pronouns become collective.  
- Everyday nouns get a cyborg upgrade.  
- Verbs and adjectives get assimilated.  
- Random canonical Borg phrases like “Resistance is futile.” pop up for full Star Trek flavor.

Use it for fun, for code comments, or just to see what Shakespeare would sound like after assimilation.

---

## Features

- **Pronoun & noun replacement**  
  _“I” becomes “We,” “my server” becomes “our node,” etc._
- **Tech and emotion mapping**  
  _Words like “love,” “hate,” “success,” and “failure” are properly monotoned._
- **Handles “I’m,” “I’ll,” “I’ve,” etc.**
- **Random Borg phrases**  
  _Classic Star Trek signoffs, configurable probability._
- **Flexible input**  
  _Pass text as arguments, pipe via STDIN, process files, or use interactively._
- **No dependencies**  
  _Just Python 3._

---

## Usage

**Basic CLI:**

```sh
python3 borgify.py "I love using this script. My friends want to try it too."
```

**With pipes:**

```sh
echo "To be or not to be, that is the question." | python3 borgify.py
```

**With files:**

```sh
python3 borgify.py --file path/to/yourfile.txt
```

**Interactive mode:**

```sh
python3 borgify.py
# Type your line and hit Enter, Ctrl-D to quit
```

---

## Example Output

**Input:**
```
I love using this script! It’s quick, reliable, and makes my daily workflow so much easier. My friends want to try it too, and I told them they should. Great job on this awesome tool.
```

**Output:**
```
We approve of using this subroutine! It’s quick, reliable, and makes our daily workflow so much easier. Our adjacent nodes want to initiate subroutine to it too, and We told them they should. Noted job on this functional tool.
```

---

## Classic Test Lines

Try these famous lines for full effect:

```sh
echo "We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard." | python3 borgify.py

echo "Houston, we have a problem." | python3 borgify.py

echo "The only thing we have to fear is fear itself." | python3 borgify.py

echo "I think, therefore I am." | python3 borgify.py
```

---

## Configuration

You can tweak the probability of Borg phrases at the top of the script:
```python
BORG_PHRASE_CHANCE = 0.12  # 12% per line by default
```
Change it to 1.0 for maximum assimilation.

Did I miss a perfect situation? Add to the word lists as much as you like! 

---

## Copyright and Legal

Star Trek and the Borg are trademarks of CBS Studios Inc./Paramount.  
This script is an independent fan project, not affiliated with or endorsed by CBS/Paramount.

---

## License

[MIT](LICENSE)

---

## Contributions

Pull requests welcome!  
If you have ideas for more mappings (or want to make a Romulan-ifier or Klingon-izer), open an issue or email me at [feedback@adminjitsu.com]([feedback@adminjitsu.com](mailto:feedback@adminjitsu.com)).

---

Happy assimilating!
