class Solution:
    def romanToInt(self, s: str) -> int:
        rtv = {'I':1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C':100,
        'D':500,
        'M':1000}
        ls = [x for x in s]
        numbers = []
        for i in ls:
            numbers.append(rtv[i])
        last = 0
        total = 0
        for val in numbers:
            if last < val and last != 0:
                total -= last
                total += val - last
            else:
                total += val
            last = val
        return total

s = "MCMXCIV"
test = Solution()
test.romanToInt(s)

