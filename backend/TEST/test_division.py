def find_arrays_with_sum(n):
    def backtrack(start, path, target):
        # 如果目标和为0，说明当前路径满足条件，将其添加到结果集中
        if target == 0:
            result.append(path[:])  # 添加path的副本，以避免后续修改影响结果
            return
            # 如果目标和已经小于0，说明当前路径不可能满足条件，直接返回
        if target < 0:
            return
            # 尝试所有可能的正整数作为下一个元素
        for i in range(1, n + 1):
            # 将当前元素添加到路径中
            path.append(i)
            # 递归调用，目标和减去当前元素，下一个可能的元素至少为i（保证数组元素不重复）
            backtrack(i, path, target - i)
            # 回溯，移除当前元素，尝试其他可能性
            path.pop()

    result = []  # 存储结果集
    backtrack(1, [], n)  # 从1开始尝试，初始路径为空，目标和为n
    return result


# 示例
n = 7
arrays = find_arrays_with_sum(n)
for array in arrays:
    print(array)