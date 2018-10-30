import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s1=np.array([1,2,3,4])
s2=np.array([5,6,7,8])
df=pd.DataFrame([s1,s2])
print df

s1=pd.Series(np.array([1,2,3,4]))
s2=pd.Series(np.array([5,6,7,8]))
df=pd.DataFrame([s1,s2])
print df


s1=pd.Series(np.array([1,2,3,4]))
s2=pd.Series(np.array([5,6,7,8]))
df=pd.DataFrame({"a":s1,"b":s2})
print df