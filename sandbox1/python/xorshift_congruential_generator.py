# -*- coding: utf-8 -*-

# xorshift
# # paper : http://www.jstatsoft.org/v08/i14/
# # 符号なしの32ビット整数を4つ使う
# # 4つの変数をシフトしてテンポラリに代入し、他の変数同士ずらして代入してと、
#   ぐるぐる回していくような感じで疑似乱数を生成する
# # seedのx,y,z,wは0でない整数ならば何でも良い
# # 周期は2 ** 128 - 1となる
# # 乱数の最大値は 2 ** 32で収まる値

# この数に収まる乱数になる
RAND_MAX = 0xffffffff

# seed
# まとめて代入
# 各値は符号なし32bit整数に収まる範囲にする
x, y, z, w = (123456789, 362436069, 521288629, 88675123)


# def seed(s):
#     """
#     乱数のseedを設定
#     seed([123456789, 861932, 5671, 232123])
#     """
#     global x, y, z, w
#     x, y, z, w = s
#
#     x = int(x)
#     y = int(y)
#     z = int(z)
#     w = int(w)
#
#     # RAND_MAX未満にする
#     x &= RAND_MAX - 1
#     y &= RAND_MAX - 1
#     z &= RAND_MAX - 1
#     w &= RAND_MAX - 1
#
#     if x + y + z + w <= 0:
#         raise ValueError("Please do not substitute 0 for seed.")

# 乱数のseedを設定
def seed(s):
    global x, y, z, w

    if not isinstance(s, int):
        raise ValueError("argument is not integer")

    if s < 0:
        s = s * -1

    seed = []
    for i in range(1, 5):
        # 32bitで収まるようにする
        s = (1812433253 * (s ^ (s >> 30)) + i) & 0xffffffff
        # no = "%02d" % (i)
        # value = "%d" % (s)
        # print(str(no) + " " + str(value))
        seed.append(s)

    x = seed[0]
    y = seed[1]
    z = seed[2]
    w = seed[3]


# xorshift32
def test_xorshift32_rnd1():
    """
    乱数生成
    32なので周期は2**32-1
    yを32bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    """
    global x, y, z, w

    # Cとかみたいに変数にサイズとかある訳ではないので、
    # これだと32bitをオーバーする場合がある
    y = y ^ (y << 13)
    y = y ^ (y >> 17)
    y = y ^ (y << 5)
    return y


# xorshift32
def test_xorshift32_rnd2():
    """
    乱数生成
    32なので周期は2**32-1
    yを32bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w

    # 32bitに収まるようにする
    y = y ^ (y << 13) & 0xffffffff
    y = y ^ (y >> 17)
    y = y ^ (y << 5) & 0xffffffff
    return y


# xorshift3
def test_xorshift32_rnd3():
    """
    乱数生成
    32なので周期は2**32-1
    yを32bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w

    # 32bitに収まるようにする
    y = y ^ (y << 13) & 0xffffffff

    # rubyには符号なしとか無いので、右シフトした場合にシフトした分だけ、
    # 左に0があるようにした値とマスクする。
    # でも、この処理いらないかも
    y = y ^ (y >> 17 & 0x7ffff)
    y = y ^ (y << 5) & 0xffffffff
    return y


# xorshift32
def test_xorshift32_rnd4(minimum, maximum):
    """
    乱数生成
    32なので周期は2**32-1
    yを32bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    minからmaxまでの範囲の乱数を返す
    引数が0ならRAND_MAXまでとする
    """
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    # 引数の値+1として、0から引数の値までの範囲で乱数を求める
    # maximum += 1

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # 32なので周期は2**32-1
    # yを32bit整数として扱う
    # シフトに使っている値は論文に書かれている優良パラメータのうちの一つ

    # 32bitに収まるようにする
    y = y ^ (y << 13) & 0xffffffff
    y = y ^ (y >> 17)
    y = y ^ (y << 5) & 0xffffffff

    # RAND_MAXまでの範囲でmin-maxの間に収まるようにする
    return minimum + int((y * (maximum - minimum + 1.0) / (1.0 + RAND_MAX)))


# xorshift64
def test_xorshift64_rnd1():
    """
    乱数生成
    64なので周期は2**64-1
    yを64bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    """
    global x, y, z, w

    # Cとかみたいに変数にサイズとかある訳ではないので、
    # これだと32bitをオーバーする場合がある
    y = (y ^ (y << 13))
    y = y ^ (y >> 7)
    y = (y ^ (y << 17))
    return y


# xorshift64
def test_xorshift64_rnd2():
    """
    乱数生成
    64なので周期は2**64-1
    yを64bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w

    # 64bitに収まるようにする
    y = (y ^ (y << 13)) & 0xffffffffffffffff
    y = y ^ (y >> 7)
    # 最終的に32ビットに収まるようにする
    y = (y ^ (y << 17)) & 0xffffffff
    return y


# xorshift64
def test_xorshift64_rnd3(minimum, maximum):
    """
    乱数生成
    64なので周期は2**64-1
    yを64bit整数として扱う
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    minからmaxで収まる範囲の乱数を返す
    """
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    # 引数の値+1として、0から引数の値までの範囲で乱数を求める
    # maximum += 1

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # 64bitに収まるようにする
    y = (y ^ (y << 13)) & 0xffffffffffffffff
    y = y ^ (y >> 7)
    # 最終的に32ビットに収まるようにする
    y = (y ^ (y << 17)) & 0xffffffff
    # RAND_MAXまでの範囲でmin-maxの間に収まるようにする
    return minimum + int((y * (maximum - minimum + 1.0) / (1.0 + RAND_MAX)))


# xorhisft96
def test_xorshift96_rnd1():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    """
    global x, y, z, w

    t = (x ^ (x << 3)) ^ (y ^ (y >> 19)) ^ (z ^ (z << 6))
    x = y
    y = z
    z = t
    return z


# xorshift96
def test_xorshift96_rnd2():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w

    xtmp = (x ^ (x << 3)) & 0xffffffff
    ztmp = (z ^ (z << 6)) & 0xffffffff
    # t = (x ^ (x << 3)) ^ (y ^ (y >> 19)) ^ (z ^ (z << 6))
    t = xtmp ^ (y ^ (y >> 19)) ^ ztmp
    x = y
    y = z
    z = t
    return z


# xorshift96
def test_xorshift96_rnd3(minimum, maximum):
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    minからmaxで収まる範囲の乱数を返す
    """
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    # 引数の値+1として、0から引数の値までの範囲で乱数を求める
    # maximum += 1

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    xtmp = (x ^ (x << 3)) & 0xffffffff
    ztmp = (z ^ (z << 6)) & 0xffffffff
    # t = (x ^ (x << 3)) ^ (y ^ (y >> 19)) ^ (z ^ (z << 6))
    t = xtmp ^ (y ^ (y >> 19)) ^ ztmp
    x = y
    y = z
    z = t
    # RAND_MAXまでの範囲でmin-maxの間に収まるようにする
    return minimum + int((z * (maximum - minimum + 1.0) / (1.0 + RAND_MAX)))


# xorshift128
def test_xorshift128_rnd1():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    """
    global x, y, z, w
    # Cとかみたいに変数にサイズとかある訳ではないので、
    # これだと32bitをオーバーする場合がある
    t = (x ^ (x << 11))
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w


# xorshift128
def test_xorshift128_rnd2():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w
    # 32bit以内になるようにする
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w


# xorshift128
def test_xorshift128_rnd3():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w
    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    # pythonには符号なしとか無いので、右シフトした場合にシフトした分だけ、
    # 左に0があるようにした値とマスクする。
    # でも、この処理いらないかも
    w = (w ^ (w >> 19 & 0x1fff)) ^ (t ^ (t >> 8 & 0xffffff))
    return w


# xorshift128
def test_xorshift128_rnd4(minimum, maximum):
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    minからmaxで収まる範囲の乱数を返す
    """

    # 乱数の最大は2**32で収まる値
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    # 引数の値+1として、0から引数の値までの範囲で乱数を求める
    # maximum += 1

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))

    # RAND_MAXまでの範囲でmin-maxの間に収まるようにする
    return minimum + int((w * (maximum - minimum + 1.0) / (1.0 + RAND_MAX)))


# xorshift128
def test_xorshift128_rnd_generator():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から2**32で収まる範囲の乱数を返す
    """
    global x, y, z, w

    # 32bit以内になるようにする
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))

    return w


# xorshift128
def test_xorshift128_rnd5(minimum, maximum):
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    minからmaxで収まる範囲の乱数を返す
    """
    # 乱数の最大は2**32で収まる値
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    # 引数の値+1として、0から引数の値までの範囲で乱数を求める
    # maximum += 1

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    range = maximum - minimum + 1.0
    rmax = 1.0 + RAND_MAX
    return minimum + int((test_xorshift128_rnd_generator() * range / rmax))


# xorshift128
def test_xorshift128_rnd6():
    """
    乱数生成
    32bitの整数を3つ使う
    96なので周期は2**96-1
    シフトに使っている値は論文に書かれている優良パラメータのうちの一つ
    0から1.0未満の範囲の乱数を返す
    """
    global x, y, z, w

    # 0.0から1.0未満で乱数を生成
    # round()などで丸めこみはしない
    # return float((1.0 / (RAND_MAX + 1.0)) * test_linear_rnd_generator())
    return (1.0 / (RAND_MAX + 1.0)) * test_xorshift128_rnd_generator()


if __name__ == '__main__':
    # global x, y, z, w

    print('//--xorshift32---------')

    print('test1---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift32_rnd1()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test2---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift32_rnd2()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test3---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift32_rnd3()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test4---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift32_rnd4(20, 128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('//--xorshift64---------')

    print('test1---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift64_rnd1()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test2---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift64_rnd2()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test3---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift64_rnd3(20, 128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('//--xorshift96---------')

    print('test1---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift96_rnd1()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test2---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift96_rnd2()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test3---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift96_rnd3(20, 128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('//--xorshift128---------')

    print('test1---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift128_rnd1()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test2---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift128_rnd2()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test3---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift128_rnd3()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test4---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift128_rnd4(20, 128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test5---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift128_rnd5(20, 128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test6--------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(40):
        ret = test_xorshift128_rnd6()
        # print("%0b" % (ret))
        # value = "%f" % (ret)
        value = "%.15f" % (ret)
        print(str(value))
        # print(str(ret))
        # print("%s" % (bin(ret)))

    print('test7--------')
    seed(1978)
    print(str(x))
    print(str(y))
    print(str(z))
    print(str(w))
    for i in range(100):
        ret = test_xorshift128_rnd5(1, 2048)
        if ret > 2048:
            print("error")
            break

        # print("%0b" % (ret))
        # value = "%f" % (ret)
        no = "%06d" % (i)
        value = "%d" % (ret)
        print(str(no) + " " + str(value))
        # print(str(ret))
        # print("%s" % (bin(ret)))

""""
    print('test8--------')
    seed(1976)
    print(str(x))
    print(str(y))
    print(str(z))
    print(str(w))
    for i in range(100000):
        ret = test_xorshift128_rnd5(1, 6)
        if ret > 6:
            print("error")
            break

        # print("%0b" % (ret))
        # value = "%f" % (ret)
        no = "%06d" % (i)
        value = "%d" % (ret)
        print(str(no) + " " + str(value))
        # print(str(ret))
        # print("%s" % (bin(ret)))
"""
