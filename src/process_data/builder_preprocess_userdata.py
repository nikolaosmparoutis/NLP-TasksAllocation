import pandas as pd
import os
import clean_data
from preprocess_datasets_interface import BuilderPreprocessDatasets
import joblib


class BuilderPreprocessUsers(BuilderPreprocessDatasets):

    def __init__(self, txt_data_dir, cache_dir, utils_dir):
        self.txt_data_dir = txt_data_dir
        self.cache_dir = cache_dir
        self.utils_dir = utils_dir
        self.words_train, self.words_test = [], []
        self.cache_data = None
        self.features_train, self.features_test, self.vocabulary = None, None, None
        self._reset()

    def _read_user_data(self):
        data = {'train': {}}
        for user_file in os.listdir(self.txt_data_dir):
            data['train'][user_file] = []
            txt_file = os.path.join(self.txt_data_dir, user_file)
            with open(txt_file) as user_info:
                data['train'][user_file].append(user_info.read())
        return data

    @classmethod
    def _reset(cls):
        cls.instance = None
        cls.instance = BuilderPreprocessUsers(
            None,
            None,
            None)

    def client_load_datasource(self, data_format):
        dataset_type = self._get_dataset_type(data_format)
        return dataset_type

    # creator
    def _get_dataset_type(self, data_format):
        if data_format == 'plk':
            self._read_BoW(data_format['cache_file_bow'])
        else:
            raise ValueError(data_format)

    def _read_preprocessed_data(self, cache_file_preproc):
        import pickle

        files = os.listdir(self.cache_dir)
        # check for cached file
        if files:
            self.cache_data = [True for fl in files if cache_file_preproc == fl].pop()

        if self.cache_data is True:
            try:
                with open(os.path.join(self.cache_dir, cache_file_preproc), "rb") as f:
                    self.cache_data = pickle.load(f)
                print("Read preprocessed data from cache file:", cache_file_preproc)
            except IOError:
                print("Unable to read from cache, but that's okay")

    def _preprocess_user_data(self):
        """
        Stores the text files from users to compressed file format; read from cache if available.
        Input:
        data_dir: directory to read the text files
        cache_dir: directory to store the compressed data
        cache_file: the compressed file name

        Return:
        Dictionary of dataframes with data ( which will be used for trainning, testing, eval or processing)
        """
        # If cache data is missing, then do the heavy lifting and store them
        if self.cache_data is None:
            data = self._read_user_data()
            # Preprocess training and test data to obtain words for each review
            for user_file in os.listdir(self.txt_data_dir):
                cleaned_cv = clean_data.cleaning_data(data['train'][user_file][0])
                self.words_train.append(cleaned_cv)
                # words_train.append(data['train'][user_file][0])

        else:
            # Unpack data loaded from cache file
            self.words_train = (self.cache_data['words_train'])

    def _read_BoW(self, cache_file_bow):
        # If cache_file is not None, try to read from it first
        if cache_file_bow is not None:
            try:
                with open(os.path.join(self.cache_dir, cache_file_bow), "rb") as f:
                    self.cache_data = joblib.load(f)

                # Unpack data loaded from cache file
                self.features_train, self.features_test, self.vocabulary = (self.cache_data['features_train'],
                                                                            self.cache_data['features_test'],
                                                                            self.cache_data['vocabulary'])
                print("Read features from cache file:", cache_file_bow)
            except IOError:
                print("Unable to read from cache, but that's okay")

    def _extract_BoW(self, vocabulary_size, cache_file_bow):
        """
        Creates and extracts the BoW with TF-IDF; if the file exists reads the compressed file, else
        it creates the compressed file.
        Input:
        docs: the texts (words_train)
        vocabulary_size: integer to limit the max number of words if we have too many
        cache_dir: path to read or write the data
        cache_file: compressed file name
        Returns: Dataframes of TF-IDFs;  features_train, features_test, vocabulary
        """

        # If cache is missing, then do the heavy lifting
        if self.cache_data is None:
            from sklearn.feature_extraction.text import TfidfVectorizer

            tfidf_vectorizer = TfidfVectorizer(use_idf=True)
            tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(self.words_train)

            # place tf-idf values for each document in a pandas data frame
            columns_names = ['DataUser_' + str(i) for i in range(len(self.words_train))]
            self.features_train = pd.DataFrame(tfidf_vectorizer_vectors.T.todense(),
                                               index=tfidf_vectorizer.get_feature_names(),
                                               columns=columns_names)

            self.vocabulary = tfidf_vectorizer.vocabulary_
            # NOTE: Remember to convert the features using .toarray() for a compact representation
            # Write to cache file for future runs (store vocabulary as well)
            if cache_file_bow is not None:
                self.vocabulary = tfidf_vectorizer.vocabulary_
                self.cache_data = dict(features_train=self.features_train, features_test=self.features_test,
                                       vocabulary=self.vocabulary)

    # stemmed_features_train = _data_to_words(features_train.index)

    @property
    def filter_data(self):
        return self.words_train, \
               self.features_train, self.features_test, self.vocabulary  # Return both the extracted features as well
        # as the vocabulary

    @filter_data.setter
    def filter_data(self, **values):
        self._read_preprocessed_data(cache_file_preproc=values['cache_file_preproc'])
        self._preprocess_user_data()
        self._extract_BoW(vocabulary_size=values['vocabulary_size'],
                          cache_file_bow=values['cache_file_bow'])

    def _dump_preprocessed_data(self, cache_file_preproc):
        import pickle
        # Write to cache file for future runs
        if cache_file_preproc is not None:
            self.cache_data = dict(words_train=self.words_train, words_test=self.words_test)
            with open(os.path.join(self.cache_dir, cache_file_preproc), "wb") as f:
                pickle.dump(self.cache_data, f)
        print("Wrote preprocessed data to cache file <{}>, in folder <{}>".format(cache_file_preproc,
                                                                                  self.cache_dir.split('/')[-1]))

    def _dump_Bow_features(self, cache_file_bow):

        self.features_train.to_csv(os.path.join(self.utils_dir, 'tf-idf'), sep=',')
        with open(os.path.join(self.cache_dir, cache_file_bow), "wb") as f:
            joblib.dump(self.cache_data, f)
        print("Wrote features to cache file:", cache_file_bow)

    def dump_data(self, **datafiles):
        self._dump_preprocessed_data(datafiles['cache_file_preproc'])
        self._dump_Bow_features(datafiles['cache_file_bow'])
