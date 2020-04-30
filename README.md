# DAnki: Automate deck creation for Anki to learn german

`DAnki` automate the work of creating decks for Anki to learn german. From the export of your Kindle's notes
or a csv file, DAnki can generate cards with the translation of the word for 8 different languages including
the german pronunciation sound.

*This library and its author(s) are not affiliated/associated with the main Anki project in any way.*

It was created for my german students to develop their vocabular. Using Kindle you can just highlight the
german words or expressions you want to practice, export these notes to your email and use the csv file
with this program. It also create tags for Anki with the page number.

*Note:* Your Kindle's language must be in *portuguese* or *english* .

## Installation

```python
pip install DAnki
```

## How to use

Here is an example using a csv file from kindle.

```python
from DAnki.DAnki import DAnki

language = 'en'
csv_filepath = r'csv_exemple_files/sherlock_highlights_from_kindle_english.csv'
deck_name = 'sherlock_en'
from_kindle = True

myDanki = DAnki(language, csv_filepath, deck_name, from_kindle)
myDanki.create_translated_deck()
```

Here is an exemple using a csv file with only 2 columns: German Word and Tag.

```python
from DAnki.DAnki import DAnki

language = 'ch'
csv_filepath = r'csv_exemple_files/not_from_kindle.csv'
deck_name = 'not_from_kindle'
from_kindle = False

myDanki = DAnki(language, csv_filepath, deck_name, from_kindle)
myDanki.create_translated_deck()
```

*You can find the csv exemple files [HERE](https://github.com/dileivas/DAnki/tree/master/DAnki/csv_exemple_files).*

## Musts

### German Dictionary for enchant - hunspell

This dictionary is used to check *trennbare* verbs. When the programm finds a prefix as word (ex. ein - for einladen) it tries
to form a trennbar verb with the last 5 words. The dictionary says if it's a german existing word or not. It becomes usefull
highlighting trennbare verbs in Kindle.

You must download the dictionary, open with WinRar and extract the '*de_DE_frami.dic*' and '*de_DE_frami.aff*' files to:

`C:\Users\USER-NAME\AppData\Local\Programs\Python\Python38\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell`

If you are using Jupyter, the path to add the files is below:

`C:\ProgramData\Anaconda3\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell`

Dictionary link [HERE](https://extensions.openoffice.org/en/project/german-de-de-frami-dictionaries).

For more information about enchant click [HERE](https://pyenchant.github.io/pyenchant/tutorial.html).

### TreeTagger Programm

The TreeTagger is a tool for annotating text with part-of-speech and lemma information. It was developed by Helmut Schmid in the TC project at the Institute for Computational Linguistics of the University of Stuttgart.

For exemple, lets say you highlighted the word 'las' in your Kindle. TreeTagger says tha it's a verb and its lemma (or infinitiv form)
is 'lesen'. DAnki searches for translations using the word's lemma. In program, it will print this:

`Word: las | Word class: VVFIN | Without Declination: lesen `

You can find a table with these "Word classes" [HERE](https://universaldependencies.org/tagset-conversion/de-stts-uposf.html)

The package *treetaggerwrapper* is a form to use TreeTagger in python.

So, to make all this magic works, we must install TreeTagger. Here follows a small tutorial for *Windows*. If you are not using
Windows, please follow [THIS](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger) tutorial.

1) Download TreeTagger : [64bits](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-windows-3.2.2.zip) or [32bits](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-windows32-3.2.2.zip).

2) Extract the zip file and move the TreeTagger directory to the root directory of drive C:\.

3) Install a Perl interpreter (if you have not already installed one). You can download it for Windows for free [HERE](http://www.activestate.com/activeperl/).

4) Add the path `C:\TreeTagger\bin` to the "Path" environment variable. [HERE](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) is a step-by-step tutorial how to do that.

5) You can test TreeTagger opening the command prompt (cmd) and typing `cd C:\TreeTagger` than `tag-english INSTALL.txt`. It should
start tagging the INSTALL.txt file from TreeTagger.

6) Download the [German Paramater file](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german.par.gz) and extract the
'*german.par*' file to:

`C:\TreeTagger\lib`

7) Now you can finally use DAnki! 

## Available languages

DAnki uses [leo.org](leo.org) to find a translation from german, so the available languages are:

('pt' - portuguese) ('en' - english) ('fr' - french) ('es' - spanich) 
('it' - italian) ('ch' - chinese) ('ru' - russian) ('pl' - polish)

## Credits

### My thanks to:

[genanki](https://github.com/kerrickstaley/genanki)

[TreeTagger](https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)

[treetaggerwrapper](https://treetaggerwrapper.readthedocs.io/en/)

[gTTS](https://github.com/pndurette/gTTS)

[LEO GmbH](leo.org)

[Christian Wartena (2019). A Probabilistic Morphology Model for German Lemmatization. In: Proceedings of the 15th Conference on Natural Language Processing (KONVENS 2019): Long Papers. Pp. 40-49, Erlangen.](https://corpora.linguistik.uni-erlangen.de/data/konvens/proceedings/papers/KONVENS2019_paper_10.pdf)

[Vorverarbeitung von Texten mit Python und NLTK](http://textmining.wp.hs-hannover.de/Preprocessing.html)

[Tagset DE](https://universaldependencies.org/tagset-conversion/de-stts-uposf.html)
