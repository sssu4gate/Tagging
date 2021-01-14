import kss 
import pykospacing
from hanspell import spell_checker
import soynlp.normalizer
import re
#from kahiii import KhaiiiApi


class Preprocessor :

    def __init__(self):
        # To make text list of sentences 
        self.sent_tokenizer = kss
        self.puncs = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
        self.punc_maps = {"‘": "'", "₹": "e", "´": "'", "°": "", "€": "e", "™": "tm", "√": " sqrt ", "×": "x", "²": "2", "—": "-", "–": "-", "’": "'", "_": "-", "`": "'", '“': '"', '”': '"', '“': '"', "£": "e", '∞': 'infinity', 'θ': 'theta', '÷': '/', 'α': 'alpha', '•': '.', 'à': 'a', '−': '-', 'β': 'beta', '∅': '', '³': '3', 'π': 'pi', }
        self.etcs = {'\u200b': ' ', '…': ' ... ', '\ufeff': '', 'करना': '', 'है': ''}

        # To check spacing 
        self.spacing_checker = pykospacing 

        # To check grammar 
        self.grammar_checker = spell_checker
  
        # To Normalize emoticon and reptitive phonology
        self.normalizer = soynlp.normalizer

        # Parsing dictionary of loan words mapping from miss spell to correction
        self.loanword_maps = dict()
        with open('./loan_words/confused_loanwords.txt') as loanword_file :
            lines = loanword_file.readlines()
            lines = [ line.strip() for line in lines ]
            # line.split[0] = miss spell of loanword
            # line.split[1] = correct spell of loanword
            split_lines = [ line.split('\t')[:2] for line in lines ]
            self.loanword_maps = { miss : corr for miss, corr in split_lines } 
        
    def clean_text(self, text) :
        clean = re.sub(r'[@%\\*=()/~#&\+á?\xc3\xa1\-\|\.\:\;\!\-\,\_\~\$\'\"]', '', text) #remove punctuation
        clean = re.sub(r'\d+','', text)# remove number
        clean = re.sub(r'\s+', ' ', text) #remove extra space
        clean = re.sub(r'\s+', ' ', text) #remove spaces
        clean = re.sub(r"^\s+", '', text) #remove space from start
        clean = re.sub(r'\s+$', '', text) #remove space from the end

        return clean

    def split_text_to_sentence(self, text):
        text = self.clean_punc(text)
        sent_list = self.sent_tokenizer.split_sentences(text)
        sent_list = [ sent.strip() for sent in sent_list]

        return sent_list

    def clean_punc(self, text):
        for punc_replace in self.punc_maps.keys() :
            text = text.replace(punc_replace, self.punc_maps[punc_replace])

        for punc_transform in self.puncs :
            text = text.replace(punc_transform, f' {punc_transform} ')

        for etc_replace in self.etcs.keys() :
            text = text.replace(etc_replace, self.etcs[etc_replace])

        return text.strip()
            
    def make_correct_spacing(self, sent_list):
        corrections = [ self.spacing_checker.spacing(sent) for sent in sent_list ] 
        return corrections  

    def make_correct_grammar(self, sent_list):
        corrections = [ self.grammar_checker.check(sent).checked for sent in sent_list ]
        return corrections
        
    def make_correct_loan_words(self, sent_list):
        corrections = list()
        for sent in sent_list :
            for miss_spell in self.loanword_maps.keys() :
                sent = sent.replace(miss_spell, self.loanword_maps[miss_spell])
            corrections.append(sent)
        return corrections



