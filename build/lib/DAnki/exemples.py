from DAnki import DAnki

# language = 'pt'
# csv_filepath = r'csv_exemple_files/sherlock_highlights_from_kindle_portuguese.csv'
# deck_name = 'sherlock_pt'
# from_kindle = True

# language = 'en'
# csv_filepath = r'csv_exemple_files/sherlock_highlights_from_kindle_english.csv'
# deck_name = 'sherlock_en'
# from_kindle = True

language = 'ch'
csv_filepath = r'csv_exemple_files/not_from_kindle.csv'
deck_name = 'not_from_kindle'
from_kindle = False

myDanki = DAnki(language, csv_filepath, deck_name, from_kindle)
myDanki.create_translated_deck()

# myDanki.show_available_languages()
#('pt' - portuguese) ('en' - english) ('fr' - french) ('es' - spanich) ('it' - italian) ('ch' - chinese) ('ru' - russian) ('pl' - polish)