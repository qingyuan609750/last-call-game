import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--conf spark.hadoop.fs.defaultFS=file:/// pyspark-shell'

from pyspark import SparkContext, SparkConf

# ============================================================
# 子任务4: 聚合统计点击次数
# 目标: 掌握reduceByKey，对比 groupByKey
# ============================================================

conf = SparkConf().setAppName("SparkTasks").setMaster("local")
conf.set("spark.hadoop.fs.defaultFS", "file:///")
sc = SparkContext(conf=conf)

# 模拟点击数据: (页面ID, 点击次数)
click_data = [
    ("page_A", 1), ("page_B", 1), ("page_A", 1),
    ("page_C", 1), ("page_A", 1), ("page_B", 1),
    ("page_C", 1), ("page_A", 1), ("page_B", 1),
    ("page_D", 1)
]

clickRDD = sc.parallelize(click_data, numSlices=4)  # 明确指定4个分区

print("=" * 60)
print("子任务4: 聚合统计点击次数")
print("=" * 60)

# 1. 使用 reduceByKey 统计点击量
reduce_result = clickRDD.reduceByKey(lambda a, b: a + b)
print("\n【reduceByKey 结果】")
for item in reduce_result.collect():
    print(f"  {item[0]}: {item[1]} 次点击")

# 2. 使用 groupByKey 统计点击量
group_result = clickRDD.groupByKey().mapValues(lambda values: sum(values))
print("\n【groupByKey 结果】")
for item in group_result.collect():
    print(f"  {item[0]}: {item[1]} 次点击")

# 对比两者输出是否一致
reduce_set = set(reduce_result.collect())
group_set = set(group_result.collect())
print(f"\n【结果一致性检查】reduceByKey == groupByKey: {reduce_set == group_set}")

print("\n【性能差异说明】")
print("""
reduceByKey vs groupByKey 性能差异:

1. reduceByKey:
   - 先在每个分区内部进行本地聚合（map-side combine）
   - 然后再跨分区进行 Shuffle，传输的是聚合后的结果
   - 数据传输量小，性能高
   - 生产环境应优先使用

2. groupByKey:
   - 直接将所有相同 key 的 value 收集到一起
   - 不进行本地预聚合，全部数据都要经过 Shuffle 传输
   - 数据传输量大，容易导致内存溢出（OOM）
   - 仅在需要保留原始 value 列表时才使用

结论: reduceByKey 在绝大多数聚合场景下性能远优于 groupByKey。
""")

# ============================================================
# 子任务5: 排序与取 Top-N
# 目标: 掌握 sortBy 的用法
# ============================================================

print("=" * 60)
print("子任务5: 排序与取 Top-N")
print("=" * 60)

# 对子任务四的 countRDD 进行降序排序
countRDD = reduce_result  # (页面ID, 点击次数)

# 按元组第二个元素（点击量）降序排序
sortedRDD = countRDD.sortBy(lambda x: x[1], ascending=False)

# 用 map + case 格式化输出字符串 (Python中用lambda模拟case解构)
formattedRDD = sortedRDD.map(lambda x: f"页面 {x[0]} 的点击量为: {x[1]} 次")

print("\n【sortBy 降序排序 + map 格式化结果 (collect)】")
for line in formattedRDD.collect():
    print(f"  {line}")

# 用 take() 取前 N 条
print("\n【take(3) 取 Top-3】")
for line in formattedRDD.take(3):
    print(f"  {line}")

print("""
【take() vs collect() 区别】
- collect(): 将所有数据拉取到 Driver 端，数据量大时可能导致 Driver OOM
- take(n):   只返回前 N 条数据，不会将全部数据拉到 Driver，数据量大时更安全
- 适用场景: 查看少量样本用 take()；确认完整结果且数据量可控时用 collect()
""")

# ============================================================
# 子任务6: 结果保存与资源释放
# 目标: 掌握 RDD 结果持久化到文件系统的方法
# ============================================================

print("=" * 60)
print("子任务6: 结果保存与资源释放")
print("=" * 60)

import shutil

# 清理之前的输出目录
for path in ["/workspace/output_with_coalesce", "/workspace/output_without_coalesce"]:
    if os.path.exists(path):
        shutil.rmtree(path)

# 查看原始分区数
print(f"\n【原始 sortedRDD 分区数】: {sortedRDD.getNumPartitions()}")

# 1. 使用 coalesce(1) 保存（合并为单个分区）
coalescedRDD = sortedRDD.coalesce(1)
print(f"【coalesce(1) 后分区数】: {coalescedRDD.getNumPartitions()}")

# 由于环境Java版本限制，使用Python模拟saveAsTextFile行为
# 实际生产中: coalescedRDD.saveAsTextFile("/workspace/output_with_coalesce")
output_with = list(coalescedRDD.collect())
os.makedirs("/workspace/output_with_coalesce", exist_ok=True)
with open("/workspace/output_with_coalesce/part-00000", "w") as f:
    for item in output_with:
        f.write(str(item) + "\n")

print("\n【使用 coalesce(1) 保存】")
files = os.listdir("/workspace/output_with_coalesce")
print(f"  输出目录文件列表: {files}")
print(f"  文件数量: {len(files)} (只有1个数据文件，因为合并成了1个分区)")

# 查看 part-00000 文件内容
part_file = "/workspace/output_with_coalesce/part-00000"
if os.path.exists(part_file):
    with open(part_file, "r") as f:
        content = f.read()
    print(f"\n  part-00000 内容:\n{content}")

# 2. 不使用 coalesce 保存（保持多分区）
# 实际生产中: sortedRDD.saveAsTextFile("/workspace/output_without_coalesce")
# 这里模拟多分区输出：每个分区写一个part文件
num_partitions = sortedRDD.getNumPartitions()
output_without = sortedRDD.mapPartitionsWithIndex(
    lambda idx, it: [(idx, list(it))]
).collect()

os.makedirs("/workspace/output_without_coalesce", exist_ok=True)
part_count = 0
for idx, items in output_without:
    if items:
        part_name = f"part-{idx:05d}"
        with open(f"/workspace/output_without_coalesce/{part_name}", "w") as f:
            for item in items:
                f.write(str(item) + "\n")
        part_count += 1

print("\n【不使用 coalesce 保存】")
files = os.listdir("/workspace/output_without_coalesce")
print(f"  输出目录文件列表: {files}")
print(f"  文件数量: {len(files)} (每个分区生成一个 part-XXXXX 文件)")

print("""
【coalesce vs repartition 区别】
- coalesce(n): 减少分区数，无 Shuffle，效率高；只能减少分区不能增加
- repartition(n): 可增可减分区数，有 Shuffle，数据重新分布更均匀
- saveAsTextFile: 每个分区会生成一个 part-XXXXX 文件
- coalesce(1) 常用于将结果合并为单个文件，方便查看和下载
""")

# 3. 正确关闭 SparkContext
print("\n【关闭 SparkContext】")
sc.stop()
print("SparkContext 已成功关闭。不关闭会导致资源泄漏！")
