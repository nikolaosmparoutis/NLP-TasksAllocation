
import pandas as pd
import os
import src.process_data.clean_data as module_clean

txt_data_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/external/txt'
cache_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/final_processed'
utils_dir = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/utils'


class UserDataProcessing:

    def _read_user_data(self, data_dir):
        data = {}
        data['train'] = {}
        for user_file in os.listdir(data_dir):
            data['train'][user_file] = []
            txt_file = os.path.join(txt_data_dir, user_file)
            with open(txt_file) as user_info:
                data['train'][user_file].append(user_info.read())
        return data



    """
    Stores the text files from users to compressed file format; read from cache if available.
    Input:
        data_dir: directory to read the text files
        cache_dir: directory to store the compressed data
        cache_file: the compressed file name
        
    Return: 
        Dictionary of dataframes with data ( which will be used for trainning, testing, eval or processing)
    """
    def preprocess_user_data(self, data_dir=txt_data_dir, cache_dir=cache_dir, cache_file="preprocessed_data.pkl"):
        words_train = []
        import pickle
        cache_data = None

        files = os.listdir(cache_dir)
        # check for cached file
        if files:
            cache_data = [True for fl in files if cache_file == fl].pop()

        if cache_data is True:
            try:
                with open(os.path.join(cache_dir, cache_file), "rb") as f:
                    cache_data = pickle.load(f)
                print("Read preprocessed data from cache file:", cache_file)
            except:
                pass  # unable to read from cache, but that's okay

        # If cache data is missing, then do the heavy lifting and store them
        if cache_data is None:
            data = UserDataProcessing._read_user_data(self, data_dir)
            # Preprocess training and test data to obtain words for each review
            for user_file in os.listdir(txt_data_dir):
                cleaned_cv = module_clean.cleaning_data(data['train'][user_file][0])
                words_train.append(cleaned_cv)
                # words_train.append(data['train'][user_file][0])
                # Write to cache file for future runs
                if cache_file is not None:
                    cache_data = dict(words_train=words_train, words_test=None)
                    with open(os.path.join(cache_dir, cache_file), "wb") as f:
                        pickle.dump(cache_data, f)
            print("Wrote preprocessed data to cache file <{}>, in folder <{}>".format(cache_file,
                                                                                      cache_dir.split('/')[-1]))
        else:
            # Unpack data loaded from cache file
            words_train = (cache_data['words_train'])

        return words_train

    '''
    Creates and extracts the BoW with TF-IDF; if the file exists reads the compressed file, else
    it creates the compressed file.
        Input: 
            docs: the texts 
            vocabulary_size: integer to limit the max number of words if we have too many
            cache_dir: path to read or write the data  
            cache_file: compressed file name
        Returns: 
          Dataframes of TF-IDFs;  features_train, features_test, vocabulary
    '''

    def extract_BoW(self, docs, vocabulary_size, cache_dir=cache_dir, cache_file="bow_features.pkl"):
        import joblib
        # If cache_file is not None, try to read from it first
        cache_data = None
        if cache_file is not None:
            try:
                with open(os.path.join(cache_dir, cache_file), "rb") as f:
                    cache_data = joblib.load(f)

                print("Read features from cache file:", cache_file)
            except:
                pass  # unable to read from cache, but that's okay

        # If cache is missing, then do the heavy lifting
        if cache_data is None:
            from sklearn.feature_extraction.text import TfidfVectorizer

            tfidf_vectorizer = TfidfVectorizer(use_idf=True)
            tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(docs)

            # place tf-idf values for each document in a pandas data frame
            columns_names = ['DataUser_' + str(i) for i in range(len(docs))]
            features_train = pd.DataFrame(tfidf_vectorizer_vectors.T.todense(),
                                          index=tfidf_vectorizer.get_feature_names(),
                                          columns=columns_names)
            features_train.to_csv(os.path.join(utils_dir, 'tf-idf'), sep=',')
            features_test = None
            vocabulary = tfidf_vectorizer.vocabulary_
            # NOTE: Remember to convert the features using .toarray() for a compact representation
            # Write to cache file for future runs (store vocabulary as well)
            if cache_file is not None:
                vocabulary = tfidf_vectorizer.vocabulary_
                cache_data = dict(features_train=features_train, features_test=None,
                                  vocabulary=vocabulary)
                with open(os.path.join(cache_dir, cache_file), "wb") as f:
                    joblib.dump(cache_data, f)
                print("Wrote features to cache file:", cache_file)
        else:
            # Unpack data loaded from cache file
            features_train, features_test, vocabulary = (cache_data['features_train'],
                                                         cache_data['features_test'],
                                                         cache_data['vocabulary'])

        # Return both the extracted features as well as the vocabulary
        return features_train, features_test, vocabulary

    # stemmed_features_train = _data_to_words(features_train.index)
