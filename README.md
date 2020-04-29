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
from DAnki import DAnki

language = 'en'
csv_filepath = r'csv_exemple_files/sherlock_highlights_from_kindle_english.csv'
deck_name = 'sherlock_en'
from_kindle = True

myDanki = DAnki(language, csv_filepath, deck_name, from_kindle)
myDanki.create_translated_deck()
```

Here is an exemple using a csv file with only 2 columns: German Word and Tag.

```python
from DAnki import DAnki

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

## Must

You must add 'de_DE_frami.dic' and 'de_DE_frami.aff' files in 
`C:\Users\user\AppData\Local\Programs\Python\Python38\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell`

Dictionary link:  https://extensions.openoffice.org/en/project/german-de-de-frami-dictionaries

For more information: https://pyenchant.github.io/pyenchant/tutorial.html

## Credits

My thanks to:

[genanki](https://github.com/kerrickstaley/genanki)

[HanTa](https://github.com/wartaal/HanTa) - I don't use this library, but allowed me to understand lemmatization.

[Vorverarbeitung von Texten mit Python und NLTK](http://textmining.wp.hs-hannover.de/Preprocessing.html)

[treetaggerwrapper](https://treetaggerwrapper.readthedocs.io/en/)

[gTTS](https://github.com/pndurette/gTTS)

[LEO GmbH](leo.org)
