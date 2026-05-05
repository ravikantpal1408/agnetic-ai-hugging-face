def two_sum_two(numbers: list[int], target: int) -> list[int]:
    right = len(numbers) - 1
    left = 0

    while left <= right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left, right]

        if current_sum < target:
            left += 1
        else:
            right -= 1

    return []


input_nums: list[int] = [2, 8, 11, 15]
target_val: int = 9

result = two_sum_two(input_nums, target_val)
print(f"Indices: {result}")  # Output: [1, 2]
