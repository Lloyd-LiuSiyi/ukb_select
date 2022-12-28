#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from IPython.display import display


# In[15]:


#设定要挑选的答案列表，yes or no问题形如[1,0]，ICD诊断编码形如["F320", "F321"]
#设定新列的名字,同样用''框起来
def select_fitted_ukb(select_list, new_col_name, input_path, output_path):
    #读入csv并去掉最后一列(根据格式自行调整)
    df = pd.read_csv(input_path, sep="\t")
    #df = df.iloc[:, :-1]
    T_F = df.isin(select_list)
    #按行统计True个数，大于0的标注为1
    T_F.loc[T_F.sum(axis=1) > 0, new_col_name] = 1
    T_F.loc[T_F.sum(axis=1) == 0, new_col_name] = 0
    #将标注的浮点数转为整数
    T_F[new_col_name] = T_F[new_col_name].astype(int)
    #将最后一列拼接到原df中
    final_df = pd.merge(df, T_F.iloc[:,[-1]], left_index=True, right_index=True)
    #写入csv，不保留行名
    final_df.iloc[:,[-1]].to_csv(output_path, sep="\t", na_rep="NA", index=False)


# In[ ]:


#设定要挑选的答案数字,默认挑选＞传入数字的答案
#设定新列的名字,同样用''框起来
def select_unfitted_ukb(select_number, new_col_name, input_path, output_path, want_greater=True):
    #读入csv并去掉最后一列(根据格式自行调整)
    df = pd.read_csv(input_path, sep="\t")
    if want_greater == True:
        T_F = df > select_number
        #按行统计True个数，大于0的标注为1
        T_F.loc[T_F.sum(axis=1) > 0, new_col_name] = 1
        T_F.loc[T_F.sum(axis=1) == 0, new_col_name] = 0
        #将标注的浮点数转为整数
        T_F[new_col_name] = T_F[new_col_name].astype(int)
    else:
        T_F = df < select_number
        T_F.loc[T_F.sum(axis=1) > 0, new_col_name] = 1
        T_F.loc[T_F.sum(axis=1) == 0, new_col_name] = 0
        #将标注的浮点数转为整数
        T_F[new_col_name] = T_F[new_col_name].astype(int)
    #将最后一列拼接到原df中
    final_df = pd.merge(df, T_F.iloc[:,[-1]], left_index=True, right_index=True)
    #写入csv，不保留行名
    final_df.iloc[:,[-1]].to_csv(output_path, sep="\t", na_rep="NA", index=False)


# In[6]:


#此函数用于获取ukb中某个field所在列数
#传递的col_name参数要带'',如'f.2090.0.0'
def get_index(col_name):
    header = pd.read_csv("./ukb_header.csv", sep='\t')
    #实际在ukb中的列数是get_loc+1
    display(header.columns.get_loc(col_name) + 1 )

