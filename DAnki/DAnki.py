import pandas as pd
from googletrans import Translator
import enchant
import requests
from bs4 import BeautifulSoup
import treetaggerwrapper
import unicodedata
from gtts import gTTS
import os
import genanki
import random
from random import randrange
from time import sleep

class DAnki(object):
    def __init__(self, 
                language,
                csv_filepath,
                deck_name,
                from_kindle = True,
                prefix_list = ['hin', 'an', 'nach', 'los', 'auf', 'ab', 'her', 'aus', 'ein', 'bei', 'zu', 'mit', 'vor', 'zurück', 'weg','herunter','hinunter','herauf','hinauf','herein','hinein','heraus','hinaus','herüber','hinüber'],
                noun_list = ['NN','NE'],
                verb_list = ['VVFIN','VMFIN','VAFIN','VVINF','VVPP','VVIZU'],
                adjective_adverb_list = ['ADV','ADJD','PIAT','ADJA','PAV'],
                preposition_list = ['APPR','PTKVZ','KOUI','KOUS','PIS','PDAT'],
                df_main_table = pd.DataFrame(columns={'word', 'without_declination', 'word_class', 'translation', 'tag', 'audio_file_name'}),
                model_id = None,
                deck_id = None,
                my_model = None
                ):
        self.language = language
        self.csv_filepath = csv_filepath
        self.deck_name = deck_name
        self.from_kindle = from_kindle
        self.prefix_list = prefix_list
        self.noun_list = noun_list
        self.verb_list = verb_list
        self.adjective_adverb_list =  adjective_adverb_list
        self.preposition_list = preposition_list
        self.df_main_table = df_main_table
        self.model_id = model_id
        self.deck_id = deck_id
        self.my_model = my_model

    def show_available_languages(self):
        available_languages = ["('pt' - portuguese)", "('en' - english)", "('fr' - french)", "('es' - spanich)", "('it' - italian)", "('ch' - chinese)", "('ru' - russian)", "('pl' - polish)"]
        return print(available_languages)

    def openCSV(self):

        if self.from_kindle == True:
            #Kindles table csv starts at line 8
            df = pd.read_csv(self.csv_filepath, encoding='utf-8', engine='python', skiprows=7)
        else:
            df = pd.read_csv(self.csv_filepath, encoding='utf-8', engine='python', skiprows=0)

        if (self.from_kindle == True) and (self.language == 'pt'):
            df.columns = df.columns.str.lower().str.replace('ç', 'c').str.replace(' ', '_').str.replace('ã', 'a').str.replace('?', '')
            df['posicao'] = df['posicao'].str.lower().str.replace(' ', '_').str.replace('á', 'a')
            df = df.query('tipo_de_anotacao.str.contains("Destaque")', engine='python').reset_index(drop=True)
            df['anotacao'] = df['anotacao'].apply(lambda x: x.replace('.','').replace(',','').replace('«','').replace('!','').replace('?','').replace('»','').replace(':','').replace(';','').replace('›','').replace('‹',''))
            df = df[['anotacao','posicao']]
            df = df.rename(columns={'anotacao':'deutsch', 'posicao':'tag'})

        elif (self.from_kindle == True) and (self.language != 'pt'):
            #Kindle language must be in english to export .csv in english
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.query('annotation_type.str.contains("Highlight")', engine='python').reset_index(drop=True)
            df['annotation'] = df['annotation'].apply(lambda x: x.replace('.','').replace(',','').replace('«','').replace('!','').replace('?','').replace('»','').replace(':','').replace(';','').replace('›','').replace('‹',''))
            df = df.rename(columns={'annotation':'deutsch', 'location':'tag'})
            df = df[['deutsch','tag']]
            df['tag'] = df['tag'].str.lower().str.replace(' ', '_')
        
        else:
            #Csv must have only to columns: word_in_german and tag
            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df = df.rename(columns={df.columns[0]:'deutsch', df.columns[1]:'tag'})
            df['tag'] = df['tag'].str.lower().str.replace(' ', '_')
        return df

    def traslate_with_google(self, text, lang):
        if lang == 'ch':
            lang_dest = 'zh-cn'
        else:
            lang_dest = lang
        translation = Translator().translate(text, dest=lang_dest, src='de').text
        if translation == text:
            print(f'>> Translation for {text} not found! <<\n')
            translation = 'not found'
        return translation

    def get_audio(self, row, text, audio_increment):
        currentDirectory = os.getcwd()
        dirName= f'{currentDirectory}/audio_files/'

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print(f'\n{dirName} created!\n')

        text = text.replace('Pl.:', '. Plural:').replace('Pl., kein Sg.', '').replace('kein Pl.','')

        speech_audio_obj = gTTS(text=text, lang='de', slow=False)  
        speech_audio_obj.save(f"{dirName}\\speech_audio_{audio_increment}.mp3")
        
        audio_file_name = f'[sound:speech_audio_{audio_increment}.mp3]'
        
        self.df_main_table.loc[row,'audio_file_name'] = audio_file_name
        
        audio_increment += 1
        
        return audio_increment

    def save_word(self, row, word, tag, lemma, word_class, translation):
        self.df_main_table.loc[row,'word'] = word
        self.df_main_table.loc[row,'tag'] = tag
        
        lemma = lemma.split(' - ')
        lemma = lemma[0].replace('(','').replace(')','')
        self.df_main_table.loc[row,'without_declination'] = lemma
        
        self.df_main_table.loc[row,'word_class'] = word_class
        self.df_main_table.loc[row,'translation'] = translation

    def find_trennbar_complement(self, word, row, df):
        #Must add 'de_DE_frami.dic' and 'de_DE_frami.aff' files in C:\Users\user\AppData\Local\Programs\Python\Python38\lib\site-packages\enchant\data\mingw64\share\enchant\hunspell
        #Dictionary link:  https://extensions.openoffice.org/en/project/german-de-de-frami-dictionaries
        #For more information: https://pyenchant.github.io/pyenchant/tutorial.html
        print(f'\nPREFIX DETECTED: {word}')
        roll_back = row - 1
        previous_word = df.loc[roll_back,'deutsch']
        trennbar = word + previous_word
        print(trennbar)

        while enchant.Dict('de_DE_frami').check(trennbar) == False:
            roll_back = roll_back - 1
            if roll_back == (row - 6):
                print(f'\n trennbar for {word} not found!')
                print(f'Adopting {word} as word!')
                trennbar = word
                break
            else:
                previous_word = df.loc[roll_back,'deutsch']
                trennbar = word+previous_word
                print(trennbar)
        print('')

        if enchant.Dict('de_DE_frami').check(trennbar) == True:
            excluded_word = self.df_main_table.loc[roll_back,'word']
            print(f'Line with word "{excluded_word}" that was a trennbar verb without prefix was deleted!\n')
            self.df_main_table = self.df_main_table.drop([roll_back])
        else:
            pass

        return trennbar

    def tag_word(self,word):
        tags = treetaggerwrapper.TreeTagger(TAGLANG='de').tag_text(word)
        tags_list = treetaggerwrapper.make_tags(tags)
        word_class = tags_list[0][1]
        lemma = tags_list[0][2]
        return word_class, lemma

    def concat_translations(self,df_leo_de):
    
        lemma = df_leo_de.loc[0,'deutsch'].split(' - ')
        lemma = lemma[0]
        
        # Exceptions treatment - if translation does not appear, treat it here
        # print(lemma)
        lemma = lemma.replace(' Präp. +Dat.','').replace(' +Dat. Präp.','').replace(' +Inf.','').replace(' Konj. Präp. +Gen.','').replace(' +Gen. Präp.','')

        df_aux = df_leo_de.query('deutsch.str.contains(@lemma)',engine='python').reset_index(drop=True)
        translation = ''
        count = 0

        for line in df_aux.index:
            translation = translation + df_aux.loc[line,'translation']
            count += 1
            if count != len(df_aux):
                # Added <br> to jump a line in card
                translation = translation + ';<br>'
            else:
                continue
        return lemma, translation

    def leo_parser(self, lang, html, lemma, table_name):
        content = html.content
        soup = BeautifulSoup(content, 'html.parser')

        table = soup.select_one(f'table:contains("{table_name}")')

        index_translation = -1
        index_de = -1

        df_leo_de = pd.DataFrame(columns={'deutsch', 'translation'}) 
        if table == None:
            print(f'There are no such table named {table_name} for {lemma} in Leo!')
            print(f'Getting translation by Google Translator!\n')
            translation = self.traslate_with_google(lemma, lang)
        else:
            for line in table.find_all('tr'):
                for column in line.find_all('td'):
                    if column.get('lang') == 'de':
                        index_de += 1
                        df_leo_de.loc[index_de,'deutsch'] = column.get_text().replace('(','').replace(')','').replace('\xa0','')
                    elif column.get('lang') == lang:
                        index_translation += 1
                        df_leo_de.loc[index_translation,'translation'] = column.get_text()
            lemma, translation = self.concat_translations(df_leo_de)
                    
        return lemma, translation

    def search_leo_de(self, lang, row, table_name, word, tag, lemma, word_class):
    
        try:
            if lang == 'pt':
                lang_site = 'portugiesisch-deutsch'
            elif lang == 'en':
                lang_site = 'englisch-deutsch'
            elif lang == 'fr':
                lang_site = 'französisch-deutsch'
            elif lang == 'es':
                lang_site = 'spanisch-deutsch'
            elif lang == 'it':
                lang_site = 'italienisch-deutsch'
            elif lang == 'ch':
                lang_site = 'chinesisch-deutsch'
            elif lang == 'ru':
                lang_site = 'russisch-deutsch'
            elif lang == 'pl':
                lang_site = 'polnisch-deutsch'
        except UnboundLocalError: 
            print('Error: Please choose one lang available!') #Not working yet - how to fix?
            raise

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        html = requests.get(f'https://dict.leo.org/{lang_site}/{lemma}', headers=headers, stream=True)

        if html.status_code == 429:
            sleep_seconds = 1500
            while html.status_code == 429:
                print(f'Too many requests! Sleeping for {sleep_seconds} seconds...')
                seconds_count = sleep_seconds
                while seconds_count > 0:
                    print(f'Countdown: {seconds_count}s... ')
                    sleep(1)
                    seconds_count -= 1
                html = requests.get(f'https://dict.leo.org/{lang_site}/{lemma}', headers=headers, stream=True)
                sleep_seconds = sleep_seconds/150
            
        else:
            pass

        if html.status_code != 200:
            print(f'\nConnection error for word {lemma}: {html.status_code}')
            print(f'Trying again for word {word}')
            html = requests.get(f'https://dict.leo.org/{lang_site}/{word}', stream=True)
            if html.status_code != 200:
                print(f'Connection error for word {word} too: {html.status_code}')
                print(f'Cant find such words as {lemma} or {word} in Leo!')
                print(f'Getting translation by Google Translator!\n')
                translation = self.traslate_with_google(lemma, lang) #colocar outros idiomas
                lemma = lemma + '*'
                self.save_word(row, word, tag, lemma, word_class, translation)
            else:
                print(f'Word {word} found!\n')
                lemma, translation = self.leo_parser(lang, html, word, table_name)
                self.save_word(row, word, tag, lemma, word_class, translation)
                
        else:
            lemma, translation = self.leo_parser(lang, html, lemma, table_name)
            self.save_word(row, word, tag, lemma, word_class, translation)
        return lemma

    def create_main_table(self):
        df = self.openCSV()
        audio_increment = 0

        for row in df.index:

            word = df.loc[row,'deutsch']
            tag = df.loc[row,'tag']

            number_of_words = len(word.split(' '))
            if number_of_words > 1:
                word_class = 'text'
                lemma = 'text'
                print(f'\nTEXT DETECTED: {word}\n')
                translation = self.traslate_with_google(word, self.language)
                audio_increment = self.get_audio(row, word, audio_increment)
                self.save_word(row, word, tag, lemma, word_class, translation)
            else:
                if word in self.prefix_list:
                    word = self.find_trennbar_complement(word, row, df)
                    word_class, lemma = self.tag_word(word)
                else:
                    word_class, lemma = self.tag_word(word)

                # print(f'Word: {word} | Word class: {word_class} | Without Declination: {lemma} | Audio #: {audio_increment}')

                # audio_increment = self.get_audio(row, lemma, audio_increment)

                if word_class in self.noun_list:
                    table_name = 'Substantive'
                    deutsch_word_in_leo = self.search_leo_de(self.language, row, table_name, word, tag, lemma, word_class)
                    audio_increment = self.get_audio(row, deutsch_word_in_leo, audio_increment)
                    print(f'Word: {word} | Word class: {word_class} | Without Declination: {deutsch_word_in_leo} | Audio #: {audio_increment-1}')
                    

                elif word_class in self.verb_list:
                    table_name = 'Verben'
                    deutsch_word_in_leo = self.search_leo_de(self.language, row, table_name, word, tag, lemma, word_class)
                    audio_increment = self.get_audio(row, lemma, audio_increment)
                    print(f'Word: {word} | Word class: {word_class} | Without Declination: {lemma} | Audio #: {audio_increment-1}')

                elif word_class in self.adjective_adverb_list:
                    table_name = 'Adjektive / Adverbien'
                    deutsch_word_in_leo = self.search_leo_de(self.language, row, table_name, word, tag, lemma, word_class)
                    audio_increment = self.get_audio(row, lemma, audio_increment)
                    print(f'Word: {word} | Word class: {word_class} | Without Declination: {lemma} | Audio #: {audio_increment-1}')

                elif word_class in self.preposition_list:
                    table_name = 'Präpositionen / Pronomen / ...'
                    deutsch_word_in_leo = self.search_leo_de(self.language, row, table_name, word, tag, lemma, word_class)
                    audio_increment = self.get_audio(row, lemma, audio_increment)
                    print(f'Word: {word} | Word class: {word_class} | Without Declination: {lemma} | Audio #: {audio_increment-1}')

                else:
                    translation = 'not found'
                    deutsch_word_in_leo = self.search_leo_de(self.language, row, table_name, word, tag, lemma, word_class)
                    audio_increment = self.get_audio(row, lemma, audio_increment)
                    print(f'Word: {word} | Word class: {word_class} | Without Declination: {lemma} | Audio #: {audio_increment-1}')
        self.df_main_table = self.df_main_table.reset_index(drop = True)

    def create_deck_ids(self):
        if self.model_id == None:
            self.model_id = random.randrange(1 << 30, 1 << 31)
        else:
            pass
        if self.deck_id == None:
           self.deck_id = random.randrange(1 << 30, 1 << 31)
        else:
            pass

    def create_model(self):
        
        if (self.my_model == None) and (self.language == 'pt') and (self.from_kindle == True):
            self.my_model = genanki.Model(self.model_id,
                                          'DAnkiModel',
                                            fields=[
                                                {'name': 'No texto'},
                                                {'name': 'Sem declinação'},
                                                {'name': 'Classe da palavra'},
                                                {'name': 'Tradução'},
                                                {'name': 'MyMedia'},                                 
                                            ],
                                            templates=[
                                                {
                                                'name': '{Card}',
                                                'qfmt': '{{MyMedia}}<div style="color:blue;text-align:center;font-size:20px"><b>{{Sem declinação}}</div></b><br><b>No texto:</b> {{No texto}}<br> <b>Classe da palavra:</b> {{Classe da palavra}}',              
                                                'afmt': '{{FrontSide}}<hr id="answer"><div style="color:black;text-align:center;font-size:12px"><b>Tradução</div></b>{{Tradução}}',
                                                },
                                            ])

        elif self.my_model == None:
            self.my_model = genanki.Model(self.model_id,
                                          'DAnkiModel',
                                            fields=[
                                                {'name': 'Word'},
                                                {'name': 'Whithout declination'},
                                                {'name': 'Word class'},
                                                {'name': 'Translation'},
                                                {'name': 'MyMedia'},                                 
                                            ],
                                            templates=[
                                                {
                                                'name': '{Card}',
                                                'qfmt': '{{MyMedia}}<div style="color:blue;text-align:center;font-size:20px"><b>{{Whithout declination}}</div></b><br><b>Word:</b> {{Word}}<br> <b>Word class:</b> {{Word class}}',              
                                                'afmt': '{{FrontSide}}<hr id="answer"><div style="color:black;text-align:center;font-size:12px"><b>Translation</div></b>{{Translation}}',
                                                },
                                            ])
        else:
            #Use model given
            pass
        
    def create_deck(self):
        my_deck = genanki.Deck(self.deck_id, self.deck_name)
        return my_deck

    def create_notes(self):
        my_deck = self.create_deck()
        audio_paths = []

        for line in self.df_main_table.index:

        #create a Note
            my_note = genanki.Note(model=self.my_model,
                                fields=[unicodedata.normalize('NFKC',self.df_main_table.loc[line,'word']),
                                        unicodedata.normalize('NFKC',self.df_main_table.loc[line,'without_declination']),
                                        unicodedata.normalize('NFKC',self.df_main_table.loc[line,'word_class']),
                                        unicodedata.normalize('NFKC',self.df_main_table.loc[line,'translation']),
                                        unicodedata.normalize('NFKC',self.df_main_table.loc[line,'audio_file_name'])],
                                tags=[unicodedata.normalize('NFKC',self.df_main_table.loc[line,'tag'])])
            
            #Add note to Deck
            my_deck.add_note(my_note)
            
            audio_file_name = unicodedata.normalize('NFKC',self.df_main_table.loc[line,'audio_file_name']).replace('[sound:','').replace(']','')
            path = f'audio_files/{audio_file_name}'
            audio_paths.append(path)
        return my_deck, audio_paths
        
    def save_deck(self):
        my_deck, audio_paths = self.create_notes()
        currentDirectory = os.getcwd()
        dirName= f'{currentDirectory}/output_decks/'

        if not os.path.exists(dirName):
            os.mkdir(dirName)
            print(f'\n{dirName} created!\n')

        deck_filename = self.deck_name.lower().replace(' ','_')

        my_package = genanki.Package(my_deck)
        my_package.media_files = audio_paths
        my_package.write_to_file(f'output_decks/{deck_filename}.apkg')
        print('Deck saved!')

    def create_translated_deck(self):
        dirName = os.getcwd()
        self.create_main_table()
        self.create_deck_ids()
        self.create_model()
        self.save_deck()
        print('\nYour new deck was successfully created!')
        print(f'You can find your deck in {dirName}\\output_decks\\ ')
        print(f'And your audio files in {dirName}\\audio_files\\ \n')
        print('Enjoy! ;D')

    def create_kahoot_templates_for_each_tag(self):
        currentDirectory = os.getcwd()
        kahoot_templates_path = f'{currentDirectory}\\kahoot_templates\\'

        if not os.path.exists(kahoot_templates_path):
            os.mkdir(kahoot_templates_path)
            print(f'\n{kahoot_templates_path} created!\n')

        tags_list = list(self.df_main_table['tag'].unique())

        for tag in tags_list:
            print(f'\nCreating Kahoot for {tag}...')
            main_table_aux = self.df_main_table[(self.df_main_table['tag']==tag) & (self.df_main_table['translation'].str!='not found')]
            
            if len(main_table_aux.index) < 4:
                print(f'Too few words to create Kahoot for {tag}')
                continue
                
            else:
                df_kahoot_template = pd.DataFrame(columns=['Question - max 120 characters','Answer 1 - max 75 characters','Answer 2 - max 75 characters','Answer 3 - max 75 characters','Answer 4 - max 75 characters','Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs','Correct answer(s) - choose at least one'])

                for row in main_table_aux.index:

                    random_number = randrange(1,5)

                    question = main_table_aux.loc[row,'without_declination'][:120]
                    correct_answer = main_table_aux.loc[row,'translation'].replace('<br>','')[:75]
                    time_to_answer = 10

                    data = {'Question - max 120 characters': [question],
                           'Answer 1 - max 75 characters': ['1'],
                            'Answer 2 - max 75 characters': ['2'],
                            'Answer 3 - max 75 characters': ['3'],
                            'Answer 4 - max 75 characters': ['4'],
                            'Time limit (sec) – 5, 10, 20, 30, 60, 90, 120, or 240 secs': [time_to_answer],
                            'Correct answer(s) - choose at least one': [random_number]   
                           }

                    df_aux = pd.DataFrame(data)

                    df_answers = main_table_aux.copy()
                    df_answers = df_answers.drop(row).reset_index(drop = True)

                    randon_answers_numbers_list=[]

                    wrong_answer_1 = randrange(0,df_answers.last_valid_index())
                    randon_answers_numbers_list.append(wrong_answer_1)

                    wrong_answer_2 = randrange(0,df_answers.last_valid_index())
                    while wrong_answer_2 in randon_answers_numbers_list:
                        wrong_answer_2 = randrange(0,df_answers.last_valid_index())
                    randon_answers_numbers_list.append(wrong_answer_2)

                    wrong_answer_3 = randrange(0,df_answers.last_valid_index())
                    while wrong_answer_3 in randon_answers_numbers_list:
                        wrong_answer_3 = randrange(0,df_answers.last_valid_index())
                    randon_answers_numbers_list.append(wrong_answer_3)

                    wrong_answer_1 = df_answers.loc[wrong_answer_1,'translation'].replace('<br>','')[:75]
                    wrong_answer_2 = df_answers.loc[wrong_answer_2,'translation'].replace('<br>','')[:75]
                    wrong_answer_3 = df_answers.loc[wrong_answer_3,'translation'].replace('<br>','')[:75]

                    if random_number == 1:
                        df_aux.loc[0,'Answer 1 - max 75 characters'] = correct_answer
                        df_aux.loc[0,'Answer 2 - max 75 characters'] = wrong_answer_1
                        df_aux.loc[0,'Answer 3 - max 75 characters'] = wrong_answer_2
                        df_aux.loc[0,'Answer 4 - max 75 characters'] = wrong_answer_3

                    elif random_number == 2:
                        df_aux.loc[0,'Answer 1 - max 75 characters'] = wrong_answer_1
                        df_aux.loc[0,'Answer 2 - max 75 characters'] = correct_answer
                        df_aux.loc[0,'Answer 3 - max 75 characters'] = wrong_answer_2
                        df_aux.loc[0,'Answer 4 - max 75 characters'] = wrong_answer_3

                    elif random_number == 3:
                        df_aux.loc[0,'Answer 1 - max 75 characters'] = wrong_answer_1
                        df_aux.loc[0,'Answer 2 - max 75 characters'] = wrong_answer_2
                        df_aux.loc[0,'Answer 3 - max 75 characters'] = correct_answer
                        df_aux.loc[0,'Answer 4 - max 75 characters'] = wrong_answer_3

                    elif random_number == 4:
                        df_aux.loc[0,'Answer 1 - max 75 characters'] = wrong_answer_1
                        df_aux.loc[0,'Answer 2 - max 75 characters'] = wrong_answer_2
                        df_aux.loc[0,'Answer 3 - max 75 characters'] = wrong_answer_3
                        df_aux.loc[0,'Answer 4 - max 75 characters'] = correct_answer

                    df_kahoot_template = df_kahoot_template.append(df_aux)
                
                df_kahoot_template = df_kahoot_template.reset_index(drop = True)
                template_filename = f'kahoot_sherlock_{tag}.xlsx'
                
                df_kahoot_template.to_excel(kahoot_templates_path+template_filename, sheet_name='Sheet1', startrow=7, startcol=0)

        print(f'You can find your Kahoot Templates in {currentDirectory}\\kahoot_templates\\ ')
        print('Enjoy! ;D')