# USER TODO:
# Install the correct requirements.
# Substitute      /home/nikoscf/PycharmProjects/  => your directory
# pip install -r '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/requirements.txt'

import pandas as pd
import os.path
from ProcessDatasetInterface import FormalProcessDatasetInterface as DataIface

files_path = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/raw'
path_data_internal = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal'
path_internal_txt = '/home/nikoscf/PycharmProjects/PM-Tasks-Allocation-NLP/data/internal/txt/'

datasets_name_list = ['Projects_datasets.xlsx', 'Projects2.xlsx']

'''Create a dictionary of dataframes reading all the csv files.
      Return the dictionary.'''


def _read_CSVs(store_path, datasets_names):
    d = {}
    for file_name in datasets_names:
        prefix_name = os.path.splitext(file_name)[0]
        stored_csv = os.path.join(store_path, prefix_name + '.csv')
        df_name = 'df_' + file_name
        d[df_name] = pd.read_csv(stored_csv)
        assert isinstance(d[df_name], pd.DataFrame)
        assert d[df_name].empty is False
    return d


class ConcreteBuilderProcessProjectData(DataIface):

    def __init__(self, datasets_name_list, files_path, path_data_internal, path_data_internal_txt):
        self.datasets_name_list = datasets_name_list
        self.files_path = files_path
        self.path_data_internal = path_data_internal
        self.path_data_internal_txt = path_data_internal_txt
        self._df_merged_columns = None
        self._reset()

    @classmethod
    def _reset(cls):
        cls.instance = None
        cls.instance = ConcreteBuilderProcessProjectData(
                        None,
                        None,
                        None,
                        None)


    def client_load_datasource(self, data_format):
        dataset_type = self._get_dataset_type(data_format)
        return dataset_type

    # creator
    def _get_dataset_type(self, data_format):
        if data_format == 'xlsx':
            return self.dump_data(data_format)
        else:
            raise ValueError(data_format)

    '''
    Now we want to take as much as useful data in a form of text as possible. 
    This method from a selection of columns concatenates their text into one column, 
    then stores the merged text along with the project id in a new dataframe
    and extracts to a txt file.
    
    Input:
        dic_data: is the dictionary with the dataframes, one dataframe per file
        proj_id: the unique id per project
        keep_columns: a tuple with the columns from the files that we want to concatenate their texts. 
                    Texts separeted with '. '.  
    Output: 
        a data frame: id, column names concatenated on first five letters.
        example: 'title', 'objective' -> 'title_objec'
    '''

    @property
    def filter_data(self):
        return self._df_merged_columns

    @filter_data.setter
    def filter_data(self, filter_columns):
        proj_id, keep_columns = filter_columns[0], filter_columns[1:]
        short_header = [first_n[0:5] for first_n in keep_columns]  # create header:concat first 5 letters of each column
        column_name = '_'.join(short_header)
        all_columns = [proj_id] + [column_name]
        self._df_merged_columns = pd.DataFrame(columns=all_columns)
        create_data = [proj_id] + keep_columns

        dic_project = _read_CSVs(self.path_data_internal, self.datasets_name_list)

        for key, value in dic_project.items():
            df = dic_project[key][create_data]
            self._df_merged_columns[column_name] = df[keep_columns].agg('. '.join, axis=1)
            self._df_merged_columns.to_csv(self.path_data_internal_txt + 'merged_project_text')
            self._df_merged_columns[proj_id] = df[proj_id]

    ''' Convert all the xslx to csv and store them to 'internal' directory '''

    def _read_xslx(self):
        for file_name in self.datasets_name_list:
            xl_file = os.path.join(files_path, file_name)
            read_xl_file = pd.read_excel(xl_file)
            yield file_name, read_xl_file

    def _xslx_dump_to_csv(self):
        file_name, read_xl_file = self._read_xslx()
        prefix_name = os.path.splitext(file_name)[0]
        csv_path = os.path.join(self.path_data_internal, prefix_name + '.csv')
        read_xl_file.to_csv(csv_path, index=None, header=True)

    def _df_to_txt(self):
        """ df with filtered and merged data to txt"""
        for file_name in os.listdir(self.path_data_internal_txt):
            if file_name is not None:
                file_dir = os.path.join(self.path_data_internal_txt, file_name)
                with open(file_dir + '.txt', "w") as file:
                    file.write(self._df_merged_columns)
            else:
                pass
        if os.listdir(self.path_data_internal) is None:
            print("Not acceptable file format for data processing.")
        else:
            print("Dataframe of CSV stored to txt files.")

    def dump_data(self, data_format):
        if data_format == 'xslx':
            self._xslx_dump_to_csv()
            self._df_to_txt()
            self._reset()
        else:
            raise ValueError(data_format)

