'''
    contruct a list of filter instance exists in this package
'''

import os

def instances(data_context):
    filters = []
    dir_name = os.path.dirname(os.path.abspath(__file__))
    pkg_name = dir_name.split('\\')[-1]
    for f in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        if f.endswith('_Filter.py'):
            module_name = f.replace('.py','')
            f_module = __import__(pkg_name + '.' + module_name, fromlist=module_name)
            f_class = getattr(f_module, module_name) # module is also the class name
            filters.append(f_class(data_context))
    return filters
    
if __name__ == '__main__':
    print(instances(None))

