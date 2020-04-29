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

Here is an exemple using a csv file from kindle.

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

## Available languages

DAnki uses [leo.org](leo.org) to find a translation from german, so the available languages are:

('pt' - portuguese) ('en' - english) ('fr' - french) ('es' - spanich) 
('it' - italian) ('ch' - chinese) ('ru' - russian) ('pl' - polish)

## Musts

### German Dictionary for enchant - hunspell

This dictionary is used to check *trennbare* verbs. When the programm finds a prefix as word (ex. ein - for einladen) it tries
to form a trennbar verb with the last 5 words. The dictionary says if it's a german existing word or not. It becomes usefull
highlighting trennbare verbs in Kindle.

You must download the dictionary, open with WinRar and extract the '*de_DE_frami.dic*' and '*de_DE_frami.aff*' files to:

`C:\Users\USER-NAME\AppData\Local\Programs\Python\Python38\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell`

If you are using Jupyter, the path to add the files is below:

`C:\ProgramData\Anaconda3\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell`

Dictionary link:  https://extensions.openoffice.org/en/project/german-de-de-frami-dictionaries

For more information about enchant: https://pyenchant.github.io/pyenchant/tutorial.html

### TreeTagger Programm

The TreeTagger is a tool for annotating text with part-of-speech and lemma information. It was developed by Helmut Schmid in the TC project at the Institute for Computational Linguistics of the University of Stuttgart.

For exemple, lets say you highlighted the word 'las' in your Kindle. TreeTagger says tha it's a verb and its lemma (or infinitiv form)
is 'lesen'. DAnki searches for translations using the word's lemma. In program, it will print this:

`Word: las | Word class: VVFIN | Without Declination: lesen `

You can find a table with these "Word class" [HERE](https://universaldependencies.org/tagset-conversion/de-stts-uposf.html)

So, to make that work, we must install TreeTagger. Here follows a small tutorial:

1) 

## Credits

My thanks to:

[genanki](https://github.com/kerrickstaley/genanki)

[HanTa](https://github.com/wartaal/HanTa) - I don't use this library, but allowed me to understand lemmatization.

[Vorverarbeitung von Texten mit Python und NLTK](http://textmining.wp.hs-hannover.de/Preprocessing.html)

[Tagset DE] (https://universaldependencies.org/tagset-conversion/de-stts-uposf.html)

[treetaggerwrapper](https://treetaggerwrapper.readthedocs.io/en/)

[gTTS](https://github.com/pndurette/gTTS)

[LEO GmbH](leo.org)
