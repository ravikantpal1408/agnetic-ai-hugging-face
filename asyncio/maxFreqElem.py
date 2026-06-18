def getMaxFrequencyElement(nums):

    n = len(nums)

    maxFreq = 0
    maxEle = 0

    visited = [False] * n

    for i in range(n):

        if visited[i]:
            continue

        freq= 0

        for j in range(i, n):
            if nums[i] == nums[j]:
                freq += 1
                visited[j] = True

        
        if freq > maxFreq:
            maxFreq = freq
            maxEle = nums[i]
        elif freq == maxFreq:
            maxEle = min(maxEle, nums[i])

    return maxEle



nums = [4, 4, 5, 5, 6]
result = getMaxFrequencyElement(nums)
print(result)
