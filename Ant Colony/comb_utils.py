class CombUtils:
    @staticmethod
    def getCombs(arr, r):
        data = [0] * r
        acc = []
        acc = CombUtils.combinationUtil(arr, data, 0, len(arr) - 1, 0, r, acc)
        return acc

    @staticmethod
    def combinationUtil(arr, data, start, end, index, r, acc):
        if (index == r):
            res = []

            for j in range(r):
                res.append(data[j])

            return res

        i = start

        while (i <= end and end - i + 1 >= r - index):
            data[index] = arr[i]
            comb = CombUtils.combinationUtil(
                arr, data, i + 1, end, index + 1, r, acc)

            # чтобы не образовывалось вложенности листов
            if len(comb) == r and all(type(x) is int for x in comb):
                acc.append(comb)

            i += 1

        return acc
