from configparser import ConfigParser
from ast import literal_eval

def ini_eval(file):
    ini = ConfigParser()
    ini.read(file)
    data = {}
    for section in dict(ini).keys():
        data[section] = dict(ini[section])    
    for section, item in data.items():
        for key, value in dict(item).items():
            try: item[key] = literal_eval(value)
            except ValueError: pass
            except SyntaxError: pass
        data[section] = item  
    return data