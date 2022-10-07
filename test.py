
# 問題2
# b = [1,2,3]
# c = [4,5,6]
# a = {"1": b, "2": c}
# b = [7,8,9]
# print(f'a: {a}\nb: {b}\nc: {c}')

# 問題3
# b = [1,2,3]
# c = [4,5,6]
# a = {"1": b, "2": c}
# b.pop(0)
# print(f'a: {a}\nb: {b}\nc: {c}')

# # 問題4
# b = [1,2,3]
# c = [4,5,6]
# a = {"1": b, "2": c}
# a["1"] = [7,8,9]
# print(f'a: {a}\nb: {b}\nc: {c}')

# 問題5
# b = [1,2,3]
# c = [4,5,6]
# a = {"1": b, "2": c}
# b = b[1:]
# print(f'a: {a}\nb: {b}\nc: {c}')

# 問題6
# b = [1,2,3]
# c = [4,5,6]
# a = {"1": b.copy(), "2": c}
# b.pop(0)
# print(f'a: {a}\nb: {b}\nc: {c}')

# 問題7
# a = "あ"
# def test(arg1):
#     arg1 = "い"
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# # 問題8
# a = [1,2,3]
# def test(arg1):
#     arg1.pop(0)
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# # 問題9
# a = [1,2,3]
# def test(arg1):
#     arg1 = [2,3]
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# 問題9.5
# a = [0,1,2]
# def test(arg1):
#     arg1.pop(0)
#     arg1 = [0,2]
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# # 問題10
# a = {"1": "あ", "2": "い"}
# def test(arg1):
#     arg1["1"] = "う"
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# # 問題11
# a = {"1": "あ", "2": "い"}
# def test(arg1):
#     arg1["3"] = "う"
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# # 問題12
# a = {"1": "あ", "2": "い"}
# def test(arg1):
#     arg1 = {"1": "う", "2": "い"}
#     print(f"a0: {a}")
#     print(f"a1: {arg1}")
# test(a)
# print(f"a2: {a}")

# 問題13
# a = {"1": 1}
# for key, value in a.items():
#     print(f"value1: {value}")
#     value+=1
#     print(f"value2: {value}")
# print(f"a: {a}")

# # 問題14
# a = {"1": 1}
# for key, value in a.items():
#     print(f"value1: {value}")
#     a[key] = value+1
#     print(f"value2: {value}")
# print(f"a: {a}")

# # 問題15(永久ループするかどうか)
# a = {"1": 1}
# count = 1
# for key, value in a.items():
#     print(f"value1: {value}")
#     count+=1
#     a[str(count)] = count
# print(f"a: {a}")

# 問題16
# class Test1():
#     a = "1"

# test1 = Test1()
# print(test1.a)

# class Test1():
#     def __init__(self):
#         self.a = "1"

# test1 = Test1()
# print(test1.a)

# class Test1():
#     def __init__(self):
#         self.a = "1"
#     a = "2"

# test1 = Test1()
# print(test1.a)


# ----------------クラスのテスト-----------------

# class Test():
#     def __init__(self):
#         self.value = "2"

# test = Test()
# test.value = "1"
# # インスタンスを同じ変数名で初期化
# test = Test()
# print(test.value)


# a = [1,2,3]
# class Test1():
#     def __init__(self):
#         self.a = a
# test = Test1()
# test.a.reverse()
# test = Test1()
# print(test.a)
# print(a)

# ------------------

c_template = "import cXXX from '../utils/card_small/cYYY.png';"

num_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13"]
for i in num_list:
    result = c_template.replace('XXX', i)
    result = result.replace('YYY', i)
    print(result)

    c_template = "import cXXX from '../utils/card_small/cYYY.png';"

d_template = "import dXXX from '../utils/card_small/dYYY.png';"

num_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13"]
for i in num_list:
    result = d_template.replace('XXX', i)
    result = result.replace('YYY', i)
    print(result)

    d_template = "import dXXX from '../utils/card_small/dYYY.png';"

h_template = "import hXXX from '../utils/card_small/hYYY.png';"

num_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13"]
for i in num_list:
    result = h_template.replace('XXX', i)
    result = result.replace('YYY', i)
    print(result)

    h_template = "import hXXX from '../utils/card_small/hYYY.png';"

s_template = "import sXXX from '../utils/card_small/sYYY.png';"

num_list = ["01","02","03","04","05","06","07","08","09","10","11","12","13"]
for i in num_list:
    result = s_template.replace('XXX', i)
    result = result.replace('YYY', i)
    print(result)

    s_template = "import sXXX from '../utils/card_small/sYYY.png';"