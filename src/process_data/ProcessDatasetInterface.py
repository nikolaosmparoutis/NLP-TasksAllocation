import abc


class FormalProcessDatasetInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'client_process') and
                callable(subclass.client_process) and
                hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'filter_data') and
                callable(subclass.filter_data) and
                hasattr(subclass, 'dump_data') and
                callable(subclass.dump_data) or
                NotImplemented)

    @abc.abstractmethod
    def client_process(self, datasets_name_list: list, data_format: str):
        """Get the client's choice for the dataset to process"""
        raise NotImplementedError

    @abc.abstractmethod
    def load_data_source(self, path: str, file_name: str):
        """Load in the data set"""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def filter_data(self):
        raise NotImplementedError

    @filter_data.setter
    @abc.abstractmethod
    def filter_data(self, value:tuple):  # (column_id: str, keep_columns:list)
        raise NotImplementedError

    @abc.abstractmethod
    def dump_data(self, full_file_path: str):
        """Extract text from the data set"""
        raise NotImplementedError
