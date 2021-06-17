# python -m spacy download en_core_web_sm
# To updates the stopwords and punktuation uncomment:
import nltk
# nltk.download("stopwords")
# nltk.download('punkt')
import os
import spacy

nlp = spacy.load('en_core_web_sm')


def cleaning_data(text):
    '''Revove special characters, emails, http links, numbers, stop words'''

    def _clean_text(text):
        """ Removes stopwords, special chars and tokkenizes a text"""
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        import re
        text = re.sub("\\W", " ", text)  # remove special chars
        text = re.sub("\S*@\S*\s?", " ", text)  # remove email
        text = re.sub('htt\S+', '', text)
        text = re.sub('[0-9]+', '', text)
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)
        str_clean = ''
        for w in word_tokens:
            if w not in stop_words:
                str_clean += ' ' + w
        return str_clean

    def _lemmatize(text):
        """
        Use of Lemmatization , it helps to topic modeling while stemming would result in unusable meaning.
        """
        document = nlp(text)
        str_lemma = ''
        for token in document:
            str_lemma += ' ' + token.lemma_
        return str_lemma

    def _remove_entities(text):
        '''
        Clean the text from the entities as person names, dates, locations..
        and keep words with more than 2 chars.
        '''
        doc_lemma = nlp(text)
        banned_words = [e.text for e in doc_lemma.ents if len(e.text) > 2]
        print('banned_words')
        print(banned_words)
        cleaned_entities = ''
        for word in doc_lemma:
            if word.text in banned_words:
                pass
            else:
                cleaned_entities += " " + word.text
        return cleaned_entities

    return _remove_entities(_lemmatize(_clean_text(text)))  # could use decorators same thing
