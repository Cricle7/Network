# 打开保存的输出文件
file_path = "traversing.txt"
with open(file_path, "r") as file:
    # 读取文件内容
    content = file.read()
    # 统计特定字符串出现的次数
    count = content.count("udp_send_data_valid is high")

# 打印出现次数
print("udp_send_data_valid is high 打印了", count, "次")
