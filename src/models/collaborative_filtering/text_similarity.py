import spacy

nlp = spacy.load('en_core_web_sm')

from src.process_data.process_dataset import Builder_ProcessDatasetProject
from src.process_data.builder_preprocess_userdata import UserDataProcessing
import os

execute_module = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/src/process_data/scrap_users_data.py'
os.system('python ' + execute_module)

files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw'
store_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal'

datasets_name = ['Projects_datasets.xlsx', 'Projects2.xlsx']

p = Builder_ProcessDatasetProject()
u = UserDataProcessing()


def texts_similarity():
    train_X = u.preprocess_user_data()
    print('train_X')
    print(train_X)

    features_train, features_test, vocabulary = u.extract_BoW(train_X, 5000)
    print(features_train)

    df_projects = p.process_projects_data()
    print(df_projects.shape)

    # for df in df_projects:
    #     print('df')
    #     print(df)
        # text_cleaned = module_clean.cleaning_data(df[1])
    # print(text_cleaned)
    print('df_projects')
    print(df_projects)

    # 1. Rank the top N words per cv
    # 2. Used BERT as Semantic Similarity:  https: // keras.io / examples / nlp / semantic_similarity_with_bert /

    # OR Use Spacy
    # similarity = text_pers.similarity(text_proj)

    # for text in texts_df:
    #     similarity = doc1.similarity(doc2)
    #     print('similarity')
    #     print(similarity)


texts_similarity()
