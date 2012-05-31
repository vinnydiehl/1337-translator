# 1337 Translator

1337 is an alternative alphabet for the English language that uses various combinations of characters to replace letters. The translation alphabet is located at ```src/alphabet.json``` and is based off of [Wikipedia's 1337 translation table](http://en.wikipedia.org/wiki/Leet#Orthography).

## Installation

No automated installation process has been implemented as of yet. It is planned for the future.

## Usage

1337 Translator comes with an array of command line options to customize the translation process.

### Input Options

Only one of the following input options can be selected at once. If no input option is selected, you will be prompted to enter the input by keyboard.

    -c
    --clipboard

Take the input directly from the clipboard.

    -f FILE
    --file FILE

Take the input directly from the specified file (replace FILE).

### Fakeout Options

Sometimes a direct translation isn't enough; if you want to obfuscate the 1337 even more, try one or more of the following.

    -l INTERVAL
    --fake-letters INTERVAL

Insert a random phoney letter at each interval. For example, ```my hovercraft is full of eels``` with the option ```-l4``` or ```--fake-letters 4``` would output something to the effect of ```my hoEvercNraft Yis fuPll of Peels```.

    -w INTERVAL
    --fake-words INTERVAL

Insert a random phoney word at each interval, in a similar fashion to ```--fake-letters```. The list of words selected from is at ```src/fakewords.txt```, modify it to your liking.

    -s
    --full-stop

Translate all full stops to STOP, as in a telegram. ```First sentence. Second sentence.``` would give ```First sentence STOP Second sentence STOP```. This may also help greatly to differentiate periods from other 1337 symbols when it is being decoded. The STOPs do not count toward the interval for ```--fake-words```.

### Output Options

These options allow output to places other than the console output. As many of these may be selected as you please.

    -C
    --out-clipboard

Output the translation to the clipboard.

    -o FILE
    --output FILE

Output the translation to the designated file (replace FILE).

### Miscellaneous Options

    -h
    --help

Shows a set of instructions for command line usage of 1337 Translator.

    -q
    --quiet
    --silent

Does not display anything on the console output during the translation. It is recommended to use an output option with this, otherwise you won't be able to see the translation! This will not silence any error messages, should they arise.

    -t
    --no-trim

By default, whitespace is trimmed from the beginning and end of the input; this includes spaces, tabs, newlines, etc. Use this option if you wish to not disturb the whitespace.

## Contributing

Don't be afraid to send a pull request if you have a contribution to make to the code. Even if you are unable to contribute to the code of 1337 Translator, reports of any bugs that you may find are appreciated.
