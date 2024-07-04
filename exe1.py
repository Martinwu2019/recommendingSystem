import json

# 打开JSON文件
with open('./data/food_classify.json', 'r') as f:
    # 加载JSON文件中的数据
    data = json.load(f)

# 打印字典
print(data)
print(type(data))