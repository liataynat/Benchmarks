import os

def convert_scp_to_maxsat(input_file, output_file):
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        lines = infile.readlines()

        # 第一行：物品数量和集合数量
        item_num, set_num = map(int, lines[0].strip().split())
        print(f"物品数量: {item_num}, 集合数量: {set_num}")

        # 第二行：集合的权重
        weights = list(map(int, lines[1].strip().split()))
        # print(f"集合权重: {weights}")

        # 写入 MaxSAT 文件头
        outfile.write(f"p wcnf {set_num} {item_num} {max(weights)}\n")

        # 写入集合权重
        for i, weight in enumerate(weights):
            outfile.write(f"{weight} {i + 1} 0\n")

        # 写入物品覆盖要求
        index = 2
        item_sets = []

        # 检测文件格式
        if lines[2].strip().isdigit():
            # 格式1：集合数量和集合编号分开
            for i in range(item_num):
                num_sets = int(lines[index].strip())
                index += 1
                sets = list(map(int, lines[index].strip().split()))
                index += 1
                item_sets.append(sets)
        else:
            # 格式2：集合数量和集合编号在同一行
            for i in range(item_num):
                parts = lines[index].strip().split()
                num_sets = int(parts[0])
                sets = list(map(int, parts[1:]))
                index += 1
                item_sets.append(sets)

        # 写入子句
        for sets in item_sets:
            outfile.write(f"{weights[0]} {' '.join(map(str, sets))} 0\n")

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_dir, file.replace(".txt", ".cnf"))
                try:
                    convert_scp_to_maxsat(input_file, output_file)
                    print(f"成功转换 {input_file} 到 {output_file}")
                except Exception as e:
                    print(f"转换 {input_file} 时出错: {e}")

# 定义输入和输出文件夹
input_directory = "Benchmarks"
output_directory = "Benchmarks_cnf"

# 处理文件夹中的所有文件
process_directory(input_directory, output_directory)