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
RAND_MAX = 2 ** 32

# seed
# まとめて代入
# 各値は符号なし32bit整数に収まる範囲にする
x, y, z, w = (123456789, 362436069, 521288629, 88675123)


def seed(s):
    """
    乱数のseedを設定
    seed([123456789, 861932, 5671, 232123])
    """
    global x, y, z, w
    x, y, z, w = s

    x = int(x)
    y = int(y)
    z = int(z)
    w = int(w)

    # RAND_MAX未満にする
    x &= RAND_MAX - 1
    y &= RAND_MAX - 1
    z &= RAND_MAX - 1
    w &= RAND_MAX - 1

    if x + y + z + w <= 0:
        raise ValueError("Please do not substitute 0 for seed.")


def test_xorshift_rnd1():
    global x, y, z, w
    # Cとかみたいに変数にサイズとかある訳ではないので、
    # これだと32bitをオーバーする場合がある
    t = (x ^ (x << 11))
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w


def test_xorshift_rnd2():
    global x, y, z, w
    # 32bit以内になるようにする
    # x % 4294967296 = x & RAND_MAX - 1
    t = (x ^ (x << 11)) & (RAND_MAX - 1)
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    return w


def test_xorshift_rnd3():
    global x, y, z, w
    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & (RAND_MAX - 1)
    x, y, z = y, z, w
    # pythonには符号なしとか無いので、右シフトした場合にシフトした分だけ、
    # 左に0があるようにした値とマスクする。
    # でも、この処理いらないかも
    w = (w ^ (w >> 19 & 0x1fff)) ^ (t ^ (t >> 8 & 0xffffff))
    return w


def test_xorshift_rnd4(minimum, maximum):
    """
    最小値と最大値を指定
    """
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & (RAND_MAX - 1)
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))
    # 最小値から最大値未満にする
    # しかし、minimum + wが2 ** 32以上の場合は考慮されていない
    return (minimum + w) % maximum


def test_xor_rnd_generator():
    """
    乱数生成
    """

    global x, y, z, w

    # 32bit以内になるようにする
    # x % 4294967296
    t = (x ^ (x << 11)) & (RAND_MAX - 1)
    x, y, z = y, z, w
    w = (w ^ (w >> 19)) ^ (t ^ (t >> 8))

    return w


def test_xorshift_rnd5(minimum, maximum):
    global x, y, z, w

    if minimum < 0 or minimum > RAND_MAX:
        minimum = 0

    if maximum <= 0 or maximum > RAND_MAX:
        maximum = RAND_MAX

    if minimum > maximum:
        tmp = minimum
        minimum = maximum
        maximum = tmp

    # minimumからmaximumで乱数を生成
    # return int((test_xor_rnd_generator() % ((maximum + 1) - minimum)) + minimum)

    # minimumからmaximumで生成
    # return int((test_xor_rnd_generator() / float(RAND_MAX + 1.0) * maximum) + int(minimum))

    # minimumからmaximum未満で生成
    # return (minimum + test_xor_rnd_generator()) % maximum

    # minimumからmaximum未満で生成
    # minimum + 乱数値がRAND_MAXを超えないようにして、maximum内に収める
    # return ((minimum + test_xor_rnd_generator()) & (RAND_MAX - 1)) % maximum

    # minimumからmaximum未満で生成
    # minimum + 乱数値がRAND_MAXを超えないようにして、maximum内に収める
    return ((minimum + test_xor_rnd_generator()) & (RAND_MAX - 1)) % maximum


def test_xorshift_rnd6():
    global x, y, z, w

    # 0.0から1.0未満で乱数を生成
    # round()などで丸めこみはしない
    # return float((1.0 / (RAND_MAX + 1.0)) * test_linear_rnd_generator())
    return (1.0 / RAND_MAX) * test_xor_rnd_generator()


if __name__ == '__main__':

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd1()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd2()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd3()
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd4(1, 5)
        # print("%0b" % (ret))
        # value = "%010d" % (ret)
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(20):
        ret = test_xorshift_rnd5(1, 5)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(500):
        ret = test_xorshift_rnd5(10, 1024)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(10):
        ret = test_xorshift_rnd5(4294967290, 4294967295)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        # print("%s" % (bin(ret)))

    print('test---------')
    x, y, z, w = (123456789, 362436069, 521288629, 88675123)
    for i in range(200):
        ret = test_xorshift_rnd6()
        # print("%0b" % (ret))
        # value = "%f" % (ret)
        value = "%.16f" % (ret)
        print(str(value))
        # print(str(ret))
        # print("%s" % (bin(ret)))
