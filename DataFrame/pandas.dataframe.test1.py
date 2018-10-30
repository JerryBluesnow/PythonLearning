import pandas as pd

import numpy as np

print pd.DataFrame([1, 2, 3, 4, 5], columns=['cols'], index=['a','b','c','d','e'])

print pd.DataFrame([[1, 2, 3],[4, 5, 6]], columns=['col1','col2','col3'], index=['a','b'])

print pd.DataFrame(np.array([[1,2],[3,4]]), columns=['col1','col2'], index=['a','b'])

print pd.DataFrame({'col1':[1,3],'col2':[2,4]},index=['a','b'])