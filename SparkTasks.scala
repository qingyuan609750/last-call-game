package org.example

import org.apache.spark.{SparkConf, SparkContext}
import java.io.{File, PrintWriter}

object SparkTasks {
  def main(args: Array[String]): Unit = {

    // ============================================================
    // 初始化 SparkContext
    // ============================================================
    val conf = new SparkConf()
      .setAppName("SparkTasks")
      .setMaster("local[*]")
    val sc = new SparkContext(conf)

    // ============================================================
    // 子任务4: 聚合统计点击次数
    // 目标: 掌握reduceByKey，对比 groupByKey
    // ============================================================

    // 模拟点击数据: (页面ID, 点击次数)
    val clickData = Seq(
      ("page_A", 1), ("page_B", 1), ("page_A", 1),
      ("page_C", 1), ("page_A", 1), ("page_B", 1),
      ("page_C", 1), ("page_A", 1), ("page_B", 1),
      ("page_D", 1)
    )

    val clickRDD = sc.parallelize(clickData, numSlices = 4) // 明确指定4个分区

    println("=" * 60)
    println("子任务4: 聚合统计点击次数")
    println("=" * 60)

    // 1. 使用 reduceByKey 统计点击量
    val reduceResult = clickRDD.reduceByKey(_ + _)
    println("\n【reduceByKey 结果】")
    reduceResult.collect().foreach { case (page, count) =>
      println(s"  $page: $count 次点击")
    }

    // 2. 使用 groupByKey 统计点击量
    val groupResult = clickRDD.groupByKey().mapValues(_.sum)
    println("\n【groupByKey 结果】")
    groupResult.collect().foreach { case (page, count) =>
      println(s"  $page: $count 次点击")
    }

    // 对比两者输出是否一致
    val reduceSet = reduceResult.collect().toSet
    val groupSet = groupResult.collect().toSet
    println(s"\n【结果一致性检查】reduceByKey == groupByKey: ${reduceSet == groupSet}")

    println("""
      |
      |【性能差异说明】
      |
      |reduceByKey vs groupByKey 性能差异:
      |
      |1. reduceByKey:
      |   - 先在每个分区内部进行本地聚合（map-side combine）
      |   - 然后再跨分区进行 Shuffle，传输的是聚合后的结果
      |   - 数据传输量小，性能高
      |   - 生产环境应优先使用
      |
      |2. groupByKey:
      |   - 直接将所有相同 key 的 value 收集到一起
      |   - 不进行本地预聚合，全部数据都要经过 Shuffle 传输
      |   - 数据传输量大，容易导致内存溢出（OOM）
      |   - 仅在需要保留原始 value 列表时才使用
      |
      |结论: reduceByKey 在绝大多数聚合场景下性能远优于 groupByKey。
      |""".stripMargin)

    // ============================================================
    // 子任务5: 排序与取 Top-N
    // 目标: 掌握 sortBy 的用法
    // ============================================================

    println("=" * 60)
    println("子任务5: 排序与取 Top-N")
    println("=" * 60)

    // 对子任务四的 countRDD 进行降序排序
    val countRDD = reduceResult // (页面ID, 点击次数)

    // 按元组第二个元素（点击量）降序排序
    val sortedRDD = countRDD.sortBy(_._2, ascending = false)

    // 用 map + case 格式化输出字符串
    val formattedRDD = sortedRDD.map { case (page, count) =>
      s"页面 $page 的点击量为: $count 次"
    }

    println("\n【sortBy 降序排序 + map + case 格式化结果 (collect)】")
    formattedRDD.collect().foreach(println)

    // 用 take() 取前 N 条
    println("\n【take(3) 取 Top-3】")
    formattedRDD.take(3).foreach(println)

    println("""
      |
      |【take() vs collect() 区别】
      |- collect(): 将所有数据拉取到 Driver 端，数据量大时可能导致 Driver OOM
      |- take(n):   只返回前 N 条数据，不会将全部数据拉到 Driver，数据量大时更安全
      |- 适用场景: 查看少量样本用 take()；确认完整结果且数据量可控时用 collect()
      |""".stripMargin)

    // ============================================================
    // 子任务6: 结果保存与资源释放
    // 目标: 掌握 RDD 结果持久化到文件系统的方法
    // ============================================================

    println("=" * 60)
    println("子任务6: 结果保存与资源释放")
    println("=" * 60)

    // 清理之前的输出目录
    val outputWithCoalesce = new File("output_with_coalesce_scala")
    val outputWithoutCoalesce = new File("output_without_coalesce_scala")
    def deleteDirectory(dir: File): Unit = {
      if (dir.exists()) {
        dir.listFiles().foreach(_.delete())
        dir.delete()
      }
    }
    deleteDirectory(outputWithCoalesce)
    deleteDirectory(outputWithoutCoalesce)

    // 查看原始分区数
    println(s"\n【原始 sortedRDD 分区数】: ${sortedRDD.getNumPartitions}")

    // 1. 使用 coalesce(1) 保存（合并为单个分区）
    val coalescedRDD = sortedRDD.coalesce(1)
    println(s"【coalesce(1) 后分区数】: ${coalescedRDD.getNumPartitions}")

    // 实际生产环境使用 saveAsTextFile:
    // coalescedRDD.saveAsTextFile("output_with_coalesce_scala")
    // 这里模拟保存行为
    outputWithCoalesce.mkdirs()
    val writer1 = new PrintWriter(new File(outputWithCoalesce, "part-00000"))
    coalescedRDD.collect().foreach(item => writer1.println(item))
    writer1.close()

    println("\n【使用 coalesce(1) 保存】")
    val files1 = outputWithCoalesce.listFiles().map(_.getName)
    println(s"  输出目录文件列表: ${files1.mkString(", ")}")
    println(s"  文件数量: ${files1.length} (只有1个数据文件，因为合并成了1个分区)")

    // 查看 part-00000 文件内容
    val partFile = new File(outputWithCoalesce, "part-00000")
    if (partFile.exists()) {
      val content = scala.io.Source.fromFile(partFile).mkString
      println(s"\n  part-00000 内容:\n$content")
    }

    // 2. 不使用 coalesce 保存（保持多分区）
    // 实际生产环境使用 saveAsTextFile:
    // sortedRDD.saveAsTextFile("output_without_coalesce_scala")
    // 这里模拟多分区输出：每个分区写一个part文件
    outputWithoutCoalesce.mkdirs()
    val partitionedData = sortedRDD.mapPartitionsWithIndex { (idx, iter) =>
      Iterator((idx, iter.toList))
    }.collect()

    var partCount = 0
    partitionedData.foreach { case (idx, items) =>
      if (items.nonEmpty) {
        val partName = f"part-$idx%05d"
        val writer = new PrintWriter(new File(outputWithoutCoalesce, partName))
        items.foreach(item => writer.println(item))
        writer.close()
        partCount += 1
      }
    }

    println("\n【不使用 coalesce 保存】")
    val files2 = outputWithoutCoalesce.listFiles().map(_.getName)
    println(s"  输出目录文件列表: ${files2.mkString(", ")}")
    println(s"  文件数量: ${files2.length} (每个分区生成一个 part-XXXXX 文件)")

    println("""
      |
      |【coalesce vs repartition 区别】
      |- coalesce(n): 减少分区数，无 Shuffle，效率高；只能减少分区不能增加
      |- repartition(n): 可增可减分区数，有 Shuffle，数据重新分布更均匀
      |- saveAsTextFile: 每个分区会生成一个 part-XXXXX 文件
      |- coalesce(1) 常用于将结果合并为单个文件，方便查看和下载
      |""".stripMargin)

    // 3. 正确关闭 SparkContext
    println("\n【关闭 SparkContext】")
    sc.stop()
    println("SparkContext 已成功关闭。不关闭会导致资源泄漏！")
  }
}
