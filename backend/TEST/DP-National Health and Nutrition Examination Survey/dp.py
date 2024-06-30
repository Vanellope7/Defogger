import json

import pandas as pd

with open('data/front/categorical_attr.json', 'r') as f:
    caMap = json.load(f)

# 读取 CSV 文件
df1 = pd.read_csv('data/questionnaire.csv')[['SEQN', 'HEQ010', 'HEQ030', 'HUQ020', 'HUQ051', 'HUQ071', 'HUQ090']]
df2 = pd.read_csv('data/labs.csv')[['SEQN', 'PHQ020', 'PHQ040', 'PHQ050', 'PHQ060']]
df3 = pd.read_csv('data/examination.csv')[['SEQN', 'BMXWT', 'BPXPULS']]
df4 = pd.read_csv('data/demographic.csv')[['SEQN', 'DMDHHSIZ', 'DMDHHSZA', 'DMDHHSZB', 'DMDHHSZE', 'DMDHRGND']]
temp = pd.merge(df1, df2, on='SEQN', how='inner')
temp = pd.merge(temp, df3, on='SEQN', how='inner')
ret = pd.merge(temp, df4, on='SEQN', how='inner')
ret.dropna(inplace=True)
ret.drop('SEQN', axis=1, inplace=True)


for column in ret.columns:
    if column != 'BMXWT':
        unique_values = ret[column].unique()
        unique_values.sort()
        for i, v in enumerate(unique_values):
            ret[column].replace(unique_values[i], caMap[column][i], inplace=True)

partial_column_map = {
    'HEQ010': 'hepatitis_B',
    'HEQ030': 'hepatitis_C',
    'HUQ020': 'health_state',
    'HUQ051': 'healthcare_times',
    'HUQ071': 'overnight_hospital',
    'HUQ090': 'mental_healthcare',

    'PHQ020': 'coffee_sugar',
    'PHQ040': 'gum',
    'PHQ050': 'antacids',
    'PHQ060': 'dietary_supp',

    'BMXWT': 'weight',
    'BPXPULS': 'pulse_regular',

    'DMDHHSIZ': 'family_c',
    'DMDHHSZA': 'children_c',
    'DMDHHSZB': 'teenager_c',
    'DMDHHSZE': 'elder_c',
    'DMDHRGND': "gender"
}
ret = ret.rename(columns=partial_column_map)
ret.to_csv('data/NHNES.csv', index=False)







# ret.to_csv('data/NHNES.csv', index=False)
# 获取每列非空值的数量
# non_empty_counts = df.count()

# 按非空值数量排序
# sorted_counts = non_empty_counts.sort_values(ascending=False)

# print("每个列的非空值数量并排序：")
# print(sorted_counts)
# print(sorted_counts['HEQ010']) # 乙肝
# print(sorted_counts['HEQ030']) # 丙肝


# 使用merge方法通过'id'列连接两个DataFrame
