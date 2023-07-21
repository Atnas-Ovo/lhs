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
        if 'data_type' in param_data:   # 有类型且符合上一行条件 490个

            data_type_set.add(param_data['data_type'])
            param = Parameter(param_id,param_data['data_type'],param_data['min'],param_data['max'],param_data['enum_values'],param_key)
            data_range.append(param)
            count += 1

            print(f"参数ID: {param_id}")
            print(f"参数Key: {param_key}")

    # param_min = param_data['min']
    # param_max = param_data['max']
    # print(f"参数范围: {param_min} - {param_max}")

print("出现过的 data_type 类型:")
print(count)
for data_type in data_type_set:
    print(data_type)


# 定义样本数量
sample_size = len(data_range)
print(sample_size)

# 生成LHS样本
size = 10   # 组数  1k, 2.5k, 5k
samples = lhs(sample_size, samples=size)

# 特殊值临界点
special = 0.2

for sample in samples:
    print(len(sample))

# 根据参数范围进行缩放
scaled_samples = []

nullErr = "空"

for i in range(size):
    # for k in range(len(samples[i])):
    for k in range(len(samples)):
        scaled_sample = []
        for param in data_range:
            print("id ",param.id)
            if param.id in ["72", "79", "90", "142", "143", "160", "301", "362", "380","401","408","416"
                            ,"417","421","424","428","429","430","435","436","490","512","522","531","553","565","568","582","638","639"]:
                scaled_sample.append(nullErr)
                continue

            if (param.min is None and param.data_type != "bool") or param.data_type == "string":
                if param.id in ("77"):
                    if samples[i][k] > 1 - special:
                        scaled_sample.append(param.enum_values[-1])
                    elif samples[i][k] > 1 - 2 * special:
                        scaled_sample.append((param.enum_values[-2]))
                    else:
                        modified = (samples[i][k] - 2 * special)/(1 - 2 * special)
                        flag = False
                        for j in range(1, len(param.enum_values) - 1):
                            interval_start = j / (len(param.enum_values)-2)
                            interval_end = (j + 1) / (len(param.enum_values)-2)
                            if interval_start <= modified < interval_end:
                                scaled_sample.append(param.enum_values[j])
                                flag = True
                                break
                        if not flag:
                            scaled_sample.append(nullErr)
                elif param.id in ["232"]:
                    if samples[i][k] > special:
                        scaled_sample.append(param.enum_values[1])
                    elif samples[i][k] > special + (1- special)/2:
                        scaled_sample.append(param.enum_values[0])
                    else:
                        scaled_sample.append(param.enum_values[2])
                else:
                    flag = False
                    for j in range(1, len(param.enum_values) + 1):
                        interval_start = j / len(param.enum_values)
                        interval_end = (j + 1) / len(param.enum_values)
                        if interval_start <= samples[i][k] < interval_end:
                            scaled_sample.append(param.enum_values[j])
                            flag = True
                            break
                    if not flag:
                        scaled_sample.append(nullErr)

            elif param.data_type == "int":
                if param.id in ["1","63","64","65","67","85","88","92","134","136",
                                "144","145","147","149","154","158","220","224",
                                "309","366","377","411","425","426","442","450",
                                "468","485","504","515","516","523","539","580","584","632","636","644","657","674"]:
                    if samples[i][k] < special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k]-special)/(1-special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                elif param.id in ["26","36","201","375","376","382","393","452","454","528","532"]:
                    if samples[i][k] < special:
                        scaled_sample.append(-1)
                    else:
                        modified = (samples[i][k]-special)/(1-special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                elif param.id in ["230","231"]:
                    if samples[i][k] < special:
                        scaled_sample.append(1)
                    else:
                        modified = (samples[i][k] - special) / (1 - special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                elif param.id in ["51"]:
                    if samples[i][k] > 1-special:
                        scaled_sample.append(3)
                    else:
                        modified = (samples[i][k])/(1-special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                elif param.id in ["262","405","414","534"]:
                    if samples[i][k] < special:
                        scaled_sample.append(-1)
                    elif samples[i][k] < 2 * special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k] - 2 * special) / (1 - 2 * special)
                        scaled_sample.append(
                            int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                elif param.id in ["227"]:
                    if samples[i][k] < special:
                        scaled_sample.append(int(np.round(samples[i][k]/special * (0 - int(param.min)) + int(param.min), decimals=5)))
                    else:
                        modified = (samples[i][k]-special)/(1-special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
                else:
                    scaled_sample.append(int(np.round(samples[i][k] * (int(param.max) - int(param.min)) + int(param.min), decimals=5)))
            elif param.data_type == "float":
                if param.id in ["130","150","153"]:
                    if samples[i][k] < special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k]-special)/(1-special)
                        scaled_sample.append(np.round(modified * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
                elif param.id in ["444"]:
                    if samples[i][k] < special:
                        scaled_sample.append(1)
                    else:
                        modified = (samples[i][k] - special) / (1 - special)
                        scaled_sample.append(
                            np.round(modified * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
                else:
                    scaled_sample.append(np.round(samples[i][k] * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
            elif param.data_type == "long":
                if param.id in ["306","307"]:
                    if samples[i][k] < special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k] - special) / (1 - special)
                        scaled_sample.append(np.round(modified * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
                elif param.id in ["593"]:
                    if samples[i][k] < special:
                        scaled_sample.append(-1)
                    elif samples[i][k] < 2 * special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k] - 2 * special) / (1 - 2 * special)
                        scaled_sample.append(
                            (np.round(modified, decimals=5) * (float(param.max) - float(param.min)) + float(param.min)))
                else:
                    scaled_sample.append(np.round(samples[i][k] * (float(param.max) - float(param.min)) + float(param.min), decimals=1))
            elif param.data_type == "longlong":
                if param.id in ["441","443"]:
                    if samples[i][k] < special:
                        scaled_sample.append(0)
                    else:
                        modified = (samples[i][k] - special) / (1 - special)
                        scaled_sample.append(int(np.round(modified * (int(param.max) - int(param.min)) + int(param.min))))
                else:
                    scaled_sample.append(int(np.round(samples[i][k] * (int(param.max) - int(param.min)) + int(param.min))))
            elif param.data_type == "bool":
                if param.id in ["183","398"]:
                    # 根据阈值将连续值转换为二元值
                    if samples[i][k] < 0.5+special:
                        scaled_sample.append(param.enum_values[0])
                    else:
                        scaled_sample.append(param.enum_values[1])
                else:
                    # 根据阈值将连续值转换为二元值
                    if samples[i][k] < 0.5:
                        scaled_sample.append(param.enum_values[0])
                    else:
                        scaled_sample.append(param.enum_values[1])
            print("--------------")
            print(len(scaled_sample))
            print("--------------")

    scaled_samples.append(scaled_sample)

# # 打印生成的样本
for sample in scaled_samples:
    print(len(sample))


import pandas as pd
# 将匹配的记录转换为DataFrame对象
matched_df = pd.DataFrame(scaled_samples)

# 导出到XLSX文件
matched_df.to_excel('test.xlsx', index=False)
