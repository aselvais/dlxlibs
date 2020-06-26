#!/usr/bin/python3
import pandas as pd
import os
from math import floor

class DlxLogAnalyzer:
    """
    Class for analyzing the log files in JSON format
    produced by the DlxLogger
    """

    _files = []
    _df = None


    def __init__(self, files=[]):
        """
        Constructor
        :param files: array of filenames contained in the logs dir
        """
        self._files = files
        self._df = self._read_log_files(files)
        self._df = self._process_df(self._df)


    def _read_log_files(self, files=[], dirr='logs/'):
        """
        Read log files and return a dataframe
        """
        frames = []
        for thefile in files:
            fullpath=os.path.dirname(__file__) + '/../' + dirr + thefile
            print(fullpath)
            frames.append(pd.read_json(fullpath, lines=True))
        return pd.concat(frames)

    def _process_df(self, df):
        df.drop_duplicates()

        self.convertColumns(df, 'date', ['asctime'], ['asctimeDt'])
        self.convertColumns(df, 'datefnum', ['created'], ['createdDt'])
        self.convertColumns(df, 'ms2str', ['relativeCreated'], ['relativeCreatedFormated'])

        df['mselapsed'] = df['relativeCreated'] - df['relativeCreated'].shift(1)

        return df.sort_values(by='created')

    def get_logs_df(self):
        """
        Returns the dataframe containing the logs
        """
        return self._df
    
    def get_simple_df(self):
        """
        Returns a simplified dataframe with the data
        """
        return self._df[[
            'asctimeDt', 
            'relativeCreated',
            'mselapsed',
            'relativeCreatedFormated',
            'levelname',
            'message',
            'funcName',
            'filename',
        ]]
    
    
    def convertColumns(self, data, to_type='date', columns=[], newcolmns=None):
        '''
        Convert column to another type

        :param data: Dataframe
        :param to_type: To type date|str|yn|yesno|num|ms2str
        :param columns: Array of column
        :param newcolmns: Array of new columns to create, or None if we replace the current one
        :return: Void
        '''
        idx=0
        for i in columns:
            if to_type == 'date':
                v = pd.to_datetime(data[i], errors='coerce')
            elif to_type == 'datefnum':
                v = data[i].apply(lambda x: int(x*1000000000))
                v = pd.to_datetime(v, errors='coerce')
            elif to_type == 'str':
                v = str(data[i], errors='coerce')
            elif to_type == 'yn':
                v = data[i].apply(lambda x: 1 if x == 'Y' else 0)
            elif to_type == 'yesno':
                v = data[i].apply(lambda x: 1 if x == 'Yes' else 0)
            elif to_type == 'num':
                v = data[i].apply(lambda value: str(value)[-1:]+str(value)[:-1] if str(value)[-1:] == '-' else str(value) )
                v = pd.to_numeric(data[i], errors='coerce').fillna(0)
            elif to_type == 'ms2str':
                v = data[i].apply(lambda x: str(str(floor(x/1000/60/60)) + ' h ' + str(floor(x/1000/60) - floor(x/1000/60/60)*60) + ' min ' + str(floor(x/1000) - floor(x/1000/60)*60) + ' sec'))
            else:
                print('Error type unknown: use date | str | yn | yesno | num')
            if newcolmns == None:
                data[i] = v
            else:
                data[newcolmns[idx]] = v
            idx = idx+1
  



if __name__ == '__main__':
    # Usage: ./dlxlibs/DlxLogAnalyzer.py 'temp_main_deduplication_process.log'
    try:
        from tabulate import tabulate
        import sys
        dlxLogAnalyzer = DlxLogAnalyzer([str(sys.argv[1])])
        df = dlxLogAnalyzer.get_simple_df()
        print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
        # df.to_excel('./loganalizer_temp.xlsx')
    except e:
        print(e)
        print("Error displaying the logs, arguments missing like the filename ?")

        
