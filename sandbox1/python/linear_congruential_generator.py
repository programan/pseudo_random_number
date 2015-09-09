# -*- coding: utf-8 -*-

# 線形合同法
# X0 = seed
# X(n+1) = (a * Xn + b) mod M
# 以下の条件が満たされたとき、乱数の周期は最大M
# 1. BとMが互いに素である。
# 2. A-1が、Mの持つ全ての素因数で割りきれる。
# 3. Mが4の倍数である場合は、A-1も4の倍数である。
# とりあえずMは2^32にしておくのが良い
# a,b,Mについては良い数字というものがいくつか発見されている
# a = 1103515245, b = 12345, M = 2^32  GCC
# a = 214013, b = 2531011, M = 2^32    VisualC++
# a = 134775813, b = 1, M = 2^32       Borland Delphi


# VCっぽく
RAND_MAX = 0x7fff

# 乱数seedの初期値
rnd_next = 1


def test_linear_rnd1(max):
    """
    乱数生成
    """
    # gccと同じ組み合わせで生成
    global rnd_next
    rnd_next = rnd_next * 1103515245 + 12345
    # VCとかと同じように32bitに収まるようにする
    # value % 2^32 == value & 2^32-1
    rnd_next &= 0xffffffff

    # 出てきた値をそのまま使うと、下1桁が奇数と偶数の繰り返しになる
    return int(rnd_next)


if __name__ == '__main__':
    print('test')

    for i in range(20):
        ret = test_linear_rnd1(128)
        # print("%0b" % (ret))
        value = "%d" % (ret)
        print(str(value))
        print("%s" % (bin(ret)))
