from pyDOE import lhs
import numpy as np
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
            param = Parameter(param_id,param_data['data_type'],param_data['min'],param_data['max'],param_data['enum_values'])
            data_range.append(param)
            count += 1
        # # 打印参数信息
        # print(f"参数ID: {param_id}")
        # print(f"参数Key: {param_key}")

    # param_min = param_data['min']
    # param_max = param_data['max']
    # print(f"参数范围: {param_min} - {param_max}")

print("出现过的 data_type 类型:")
print(count)
for data_type in data_type_set:
    print(data_type)
#
# for a in data_range:
#     print(a.id,a.data_type,a.max,a.min)

# print(len(data_range))

# 定义样本数量
sample_size = len(data_range)

# 生成LHS样本
samples = lhs(sample_size, samples=sample_size)

# 根据参数范围进行缩放
scaled_samples = []

for i in range(len(samples)):
    scaled_sample = []
    for k in range(len(samples)):
        for param in data_range:
            print(param.id)
            if param.id in ("72", "79", "90", "142", "143", "160", "301", "362", "380","401","408","416"
                            ,"417","421","424","428","429","430","435","436","490","512","522","531","553","565","568","582","638","639"):
                continue

            if param.min is None or param.data_type == "string":
                for j in range(1, len(param.enum_values) + 1):
                    interval_start = j / len(param.enum_values)
                    interval_end = (j + 1) / len(param.enum_values)
                    if interval_start <= samples[i][k] < interval_end:
                        scaled_sample.append(param.enum_values[j])
                        break
            elif param.data_type == "int":
                scaled_sample.append(int(np.round(samples[i][k] * (int(param.max) - int(param.min)) + int(param.min))))
            elif param.data_type == "float":
                scaled_sample.append(np.round(samples[i][k] * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
            elif param.data_type == "long":
                # if "e" in param.max:
                #     max = float(param.max)
                #     scaled_sample.append(np.round(samples[i][k] * (int(max) - float(param.min)) + int(param.min), decimals=1))
                # else:
                scaled_sample.append(np.round(samples[i][k] * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
            elif param.data_type == "longlong":
                scaled_sample.append(int(np.round(samples[i][k] * (int(param.max) - int(param.min)) + int(param.min))))
            elif param.data_type == "bool":
                # 根据阈值将连续值转换为二元值
                if samples[i][k] < 0.5:
                    scaled_sample.append(param.enum_values[0])
                else:
                    scaled_sample.append(param.enum_values[1])
    scaled_samples.append(scaled_sample)

# 打印生成的样本
for sample in scaled_samples:
    print(sample)

