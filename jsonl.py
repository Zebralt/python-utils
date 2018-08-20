import pandas as pd

"""
A simple model to export a pandas dataframe to JSONL, with the right cleaning method.
"""

def clean_text_entry(ss):
    """
    This function cleans the entry, as in escaping characters that JSON do not like, 
    namely the backslash and the double quotes. It' also converted to text if it 
    wasn't text already.
    """
    ss = str(ss)
    ss = ss.replace('\\', '\\\\')
    ss = ss.replace('"', '\\"')
    ss = ss.replace("\'", "'")
    return ss

# Solution : write line by line
def row_to_jsonl(row):
    """
    This function converts a dataframe row into JSONL.
    """
    r = '{' + ', '.join([ "\"%s\" : \"%s\"" % (clean_text_entry(k), clean_text_entry(v)) for k, v in dict(row).items()]) + '}'
    return r

def to_jsonl(data, filepath, columns=[], names={}, defaultAnswer=True):
    """
    This functions converts a pandas DataFrame to JSONL format.
    You can select a subset of columns that you want to export.
    You can provide a rename dictionary to rename the columns in the
    export file. You can also do those two operations on the 
    dataframe itself before using this function.
    Every row being a dictionary, we simply recreate the dictionary
    as a JSONL line:
        
        text   Hello
        label  There
    
    becomes
    
        {"text" : "Hello", "label" : "There"}
        
    and so on.
    """
    if columns:
        data = data[columns]
        
    if names:
        if type(names) == dict:
            data = data.rename(columns=names)
        elif type(names) in [list, tuple]:
            data = data.rename(columns=dict(zip(data.columns.values, names)))
        
    if 'accept' in data.columns.values:
        defaultAnswer = False
    
    if defaultAnswer:
        print(data.shape)
        data['answer'] = pd.Series()
        data['answer'] = data['answer'].apply(lambda x : 'accept')
        
    data = data.apply(row_to_jsonl, axis=1)
    with open(filepath, 'w+') as mf:
        data.apply(lambda x : mf.write(x.replace('\n', '') + '\n'))
        
    return 'Written to {}'.format(filepath)
        
def series_to_jsonl(data, filepath, column):
    dd = pd.DataFrame(data).rename(columns={0 : column})
    to_jsonl(dd, filepath, defaultAnswer=False)