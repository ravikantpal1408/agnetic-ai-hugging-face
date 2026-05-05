def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left: int = 0
    right: int = len(numbers) - 1

    while left < right:
        current_sum: int = numbers[left] + numbers[right]

        if current_sum == target:
            # Problem requirement: return 1-based indices
            return [left + 1, right + 1]

        if current_sum < target:
            # Sum is too small, move the left pointer forward
            left += 1
        else:
            # Sum is too large, move the right pointer backward
            right -= 1

    # Return an empty list if no solution is found (though the problem
    # usually guarantees exactly one solution).
    return []


# Example Usage
input_nums: list[int] = [2, 7, 11, 15]
target_val: int = 9

result = two_sum_sorted(input_nums, target_val)
print(f"Indices: {result}")  # Output: [1, 2]
