
nums1 = [1,2,3,0,0,0]

nums2 = [2,5,6]

class Solution:
    def merge(self, nums1, m: int, nums2, n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        total = m + n - 1
        while m> 0 and n > 0:
            if nums1[m-1] > nums2[n-1]:
                nums1[total] = nums1[m-1]
                m -= 1
            else:
                nums1[total] = nums2[n-1]
                n -= 1
            total -= 1
        while n > 0:
            nums1[total] = nums2[n-1]
            n -= 1
            total -= 1
        return nums1


sol = Solution()
a = sol.merge(nums1,3,nums2,3)

print(a)

