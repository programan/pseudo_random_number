# -*- coding: utf-8 -*-

# from decimal import *

# xorshift
# # paper : http://www.jstatsoft.org/v08/i14/
# # 符号なしの32ビット整数を4つ使う
# # 4つの変数をシフトしてテンポラリに代入し、他の変数同士ずらして代入してと、
#   ぐるぐる回していくような感じで疑似乱数を生成する
# # seedのx,y,z,wは0でない整数ならば何でも良い
# # 周期は2^128 - 1となる

# seed
x, y, z, w = (123456789, 362436069, 521288629, 88675123)


def seed(s):
    global x, y, z, w
    x, y, z, w = s
    if x + y + z + w <= 0:
        return False
        # raise ValueError, "Please do not substitute 0 for seed."
    return True


def test_xorshift_rnd1(minimum, maximum):
    global x, y, z, w
    t = (x ^ (x << 11))
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w
    # return (minimum + w) % maximum


def test_xorshift_rnd2(minimum, maximum):
    global x, y, z, w
    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w
    # return (minimum + w) % maximum


def test_xorshift_rnd3(minimum, maximum):
    global x, y, z, w
    t = (x ^ (x << 11 & 0xffffffff))
    x, y, z = y, z, w
    w = (w ^ (w >> 19 & 0x1fff)) ^ (t ^ (t >> 8 & 0xffffff))
    # 32bit以内になるようにする
    # x % 4294967296
    # return w & 0xffffffff
    return w
    # return (minimum + w) % maximum


def test_xorshift_rnd4(minimum, maximum):
    global x, y, z, w
    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w
    # return (minimum + w) % maximum


def test_xorshift_rnd5(minimum, maximum):
    global x, y, z, w

    if minimum < 0:
        minimum = 0

    if maximum <= 0:
        maximum = 2 ** 32

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return (minimum + w) % maximum


def test_xor_rnd_generator():
    """
    乱数生成
    """

    global x, y, z, w

    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & 0xffffffff
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))

    return w


def test_xorshift_rnd6(minimum, maximum):
    global x, y, z, w

    if minimum < 0:
        minimum = 0

    if maximum <= 0:
        maximum = 2 ** 32

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # minimumからmaximum未満で乱数を生成
    return int((test_xor_rnd_generator() % ((maximum + 1) - minimum)) + minimum)


def test_xorshift_rnd7():
    global x, y, z, w

    RAND_MAX = 2 ** 32

    # 0.0から1.0未満で乱数を生成
    # round()などで丸めこみはしない
    # return float((1.0 / (RAND_MAX + 1.0)) * test_linear_rnd_generator())
    return (1.0 / (RAND_MAX + 1.0)) * test_xor_rnd_generator()


if __name__ == '__main__':

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd1(1, 10)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd2(1, 10)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd3(1, 10)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd4(1, 10)
        # print("%0b" % (ret))
        value = "%010d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(60):
        ret = test_xorshift_rnd5(1, 64)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(60):
        ret = test_xorshift_rnd6(1, 64)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(60):
        ret = test_xorshift_rnd7()
        # print("%0b" % (ret))
        # value = "%f" % (ret)
        value = "%.16f" % (ret)
        print(str(value))
        # print(str(ret))
        # print("%s" % (bin(ret)))
