import pandas as pd
import json
from parameter import Parameter

# 从 JSON 文件中读取数据
with open('option_list.json', encoding='utf-8') as file:
    data = json.load(file)

# 遍历每个参数
count = 0
data_type_set = set()
data_range = []
for param_id, param_data in data['option_list'].items():
    # 提取参数信息
    param_key = param_data['key']

    if param_data['context'] in ['sighup', 'user', 'superuser']:
        if 'data_type' in param_data:

            data_type_set.add(param_data['data_type'])
            param = Parameter(param_id,param_data['data_type'],param_data['min'],param_data['max'],param_data['enum_values'],param_key)
            data_range.append(param)
            count += 1
            # print(f"参数ID: {param_id}")
            # print(f"参数Key: {param_key}")

# 读取Excel文件
df = pd.read_excel('a.xlsx')

# 定义要匹配的name列表
names_to_match = ['John', 'Alice', 'Bob']


# 遍历每一行

# 创建一个列表来存储匹配的记录
matched_records = []

special_count = 0
for p in data_range:
    for index, row in df.iterrows():
        name = row['配置项名称']
        value = row['特殊值说明']
        if p.key == name and not pd.isnull(value):
            special_count += 1
            matched_records.append({'id': p.id, 'Name': name, 'Value': value})
            print(f"{p.id}  {name}: {value}")
            break

print(special_count)

# 将匹配的记录转换为DataFrame对象
matched_df = pd.DataFrame(matched_records)

# 导出到XLSX文件
matched_df.to_excel('matched_records.xlsx', index=False)