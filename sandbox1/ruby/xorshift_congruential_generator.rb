# -*- coding: utf-8 -*-

# xorshift
# # paper : http://www.jstatsoft.org/v08/i14/
# # 符号なしの32ビット整数を4つ使う
# # 4つの変数をシフトしてテンポラリに代入し、他の変数同士ずらして代入してと、
#   ぐるぐる回していくような感じで疑似乱数を生成する
# # seedのx,y,z,wは0でない整数ならば何でも良い
# # 周期は2 ** 128 - 1となる
# # 乱数の最大値は 2 ** 32で収まる値
# xorshift32,xorshift64,xorshift96,xorshift128と周期が違うものがある

# この値に収まる乱数になる
RAND_MAX = 0xffffffff

# seed
# まとめて代入
# 各値は符号なし32bit整数に収まる範囲にする
# 初期値は論文に書いてあった値にした
# 全てが0にならないのであればどんな値でも良い
$x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123

=begin
def seed(s)
  # 乱数のseedを設定
  # seed([123456789, 861932, 5671, 232123])

  $x, $y, $z, $w = s

  $x.to_i!
  $y.to_i!
  $z.to_i!
  $w.to_i!

  # RAND_MAX未満にする
  $x &= RAND_MAX - 1
  $y &= RAND_MAX - 1
  $z &= RAND_MAX - 1
  $w &= RAND_MAX - 1

  if $x + $y + $z + $w <= 0
    raise "Please do not substitute 0 for seed."
  end
end
=end

def seed(s)
  raise "argument is not integer" if not s.is_a?(Integer)
  if s < 0
    s *= -1
  end

  seedTmp = []
  for i in 1 ... 5
    # 32bitで収まるようにする
    s = (1812433253 * (s ^ (s >> 30)) + i) & 0xffffffff
    # puts("%02d %d" % [i, s])
    seedTmp.push(s)
  end

  $x = seedTmp[0]
  $y = seedTmp[1]
  $z = seedTmp[2]
  $w = seedTmp[3]
end


def test_xorshift32_rnd1
  # 32なので周期は2**32-1
  # yを32bit整数として扱う
  # シフトに使っている値は論文に書かれている優良パラメータのうちの一つ

  # Cとかみたいに変数にサイズとかある訳ではないので、
  # これだと32bitをオーバーする場合がある
  $y = $y ^ ($y << 13)
  $y = $y ^ ($y >> 17)
  $y = $y ^ ($y << 5)
  return $y
end


def test_xorshift32_rnd2
  # 32なので周期は2**32-1
  # yを32bit整数として扱う
  # シフトに使っている値は論文に書かれている優良パラメータのうちの一つ

  # 32bitに収まるようにする
  $y = ($y ^ ($y << 13)) & 0xffffffff
  $y = $y ^ ($y >> 17)
  $y = ($y ^ ($y << 5)) & 0xffffffff
  return $y
end


def test_xorshift32_rnd3
  # 32なので周期は2**32-1
  # yを32bit整数として扱う
  # シフトに使っている値は論文に書かれている優良パラメータのうちの一つ

  # 32bitに収まるようにする
  $y = ($y ^ ($y << 13)) & 0xffffffff

  # rubyには符号なしとか無いので、右シフトした場合にシフトした分だけ、
  # 左に0があるようにした値とマスクする。
  # でも、この処理いらないかも
  $y = $y ^ ($y >> 17 & 0x7fff)

  $y = ($y ^ ($y << 5)) & 0xffffffff
  return $y
end


def test_xorshift32_rnd4(minimum, maximum)
  # 引数が0ならRAND_MAXまでとする

  if minimum < 0 or minimum > RAND_MAX
    minimum = 0
  end

  if maximum <= 0 or maximum > RAND_MAX
    maximum = RAND_MAX
  end

  # 引数の値+1として、0から引数の値までの範囲で乱数を求める
  # maximum += 1

  if minimum > maximum
    tmp = minimum
    minimum = maximum
    maximum = tmp
  end

  # 32bitに収まるようにする
  $y = ($y ^ ($y << 13)) & 0xffffffff
  $y = $y ^ ($y >> 17)
  $y = ($y ^ ($y << 5)) & 0xffffffff

  #RAND_MAXまでの範囲でmin-maxの間に収まるようにする
  return minimum + (($y * (maximum - minimum + 1.0) / (1.0 + RAND_MAX))).to_i
end


def test_xorshift64_rnd1()
  # 64ビットの整数を1つ使うxorshift
  # 周期は2**64-1

  $y = ($y ^ ($y << 13))
  $y = $y ^ ($y >> 7)
  $y = ($y ^ ($y << 17))
  return $y
end


def test_xorshift64_rnd2()
  # 64ビットの整数を1つ使うxorshift
  # 周期は2**64-1
  # 乱数の最大は2**32で収まる値

  # 64bitに収まるようにする
  $y = ($y ^ ($y << 13)) & 0xffffffffffffffff
  $y = $y ^ ($y >> 7)
  # 最終的に32ビットに収まるようにする
  $y = ($y ^ ($y << 17)) & 0xffffffff
  return $y
end


def test_xorshift64_rnd3(minimum, maximum)
  # 引数が0ならRAND_MAXまでとする

  if minimum < 0 or minimum > RAND_MAX
    minimum = 0
  end

  if maximum <= 0 or maximum > RAND_MAX
    maximum = RAND_MAX
  end

  # 引数の値+1として、0から引数の値までの範囲で乱数を求める
  # maximum += 1

  if minimum > maximum
    tmp = minimum
    minimum = maximum
    maximum = tmp
  end

  # 64bitに収まるようにする
  $y = ($y ^ ($y << 13)) & 0xffffffffffffffff
  $y = $y ^ ($y >> 7)
  # 32bitに収まるようにする
  $y = ($y ^ ($y << 17)) & 0xffffffff

  #RAND_MAXまでの範囲でmin-maxの間に収まるようにする
  return minimum + (($y * (maximum - minimum + 1.0) / (1.0 + RAND_MAX))).to_i
end


def test_xorshift96_rnd1()
  # 32bitの整数を3つ使う
  # 周期は2**96-1

  t = ($x ^ ($x << 3)) ^ ($y ^ ($y >> 19)) ^ ($z ^ ($z << 6))
  $x = $y
  $y = $z
  $z = t
  return $z
end


def test_xorshift96_rnd2()
  # 32bitの整数を3つ使う
  # 周期は2**96-1
  # 乱数の最大は2**32で収まる値

  xtmp = ($x ^ ($x << 3)) & 0xffffffff
  ztmp = ($z ^ ($z << 6)) & 0xffffffff
  # t = ($x ^ ($x << 3)) ^ ($y ^ ($y >> 19)) ^ ($z ^ ($z << 6))
  t = xtmp ^ ($y ^ ($y >> 19)) ^ ztmp
  $x = $y
  $y = $z
  $z = t
  return $z
end


def test_xorshift96_rnd3(minimum, maximum)
  # 32bitの整数を3つ使う
  # 周期は2**96-1
  # 乱数の最大は2**32で収まる値

  # 引数が0ならRAND_MAXまでとする

  if minimum < 0 or minimum > RAND_MAX
    minimum = 0
  end

  if maximum <= 0 or maximum > RAND_MAX
    maximum = RAND_MAX
  end

  # 引数の値+1として、0から引数の値までの範囲で乱数を求める
  # maximum += 1

  if minimum > maximum
    tmp = minimum
    minimum = maximum
    maximum = tmp
  end

  xtmp = ($x ^ ($x << 3)) & 0xffffffff
  ztmp = ($z ^ ($z << 6)) & 0xffffffff
  # t = ($x ^ ($x << 3)) ^ ($y ^ ($y >> 19)) ^ ($z ^ ($z << 6))
  t = xtmp ^ ($y ^ ($y >> 19)) ^ ztmp
  $x = $y
  $y = $z
  $z = t

  #RAND_MAXまでの範囲でmin-maxの間に収まるようにする
  return minimum + (($z * (maximum - minimum + 1.0) / (1.0 + RAND_MAX))).to_i
end


def test_xorshift128_rnd1()
  # 32bitの整数を4つ使う
  # 周期は2**128-1

  # これだと32bitをオーバーする場合がある
  t = ($x ^ ($x << 11))
  $x, $y, $z = $y, $z, $w
  $w = ($w ^ ($w >> 19)) ^ (t ^ (t >> 8))
  return $w
end


def test_xorshift128_rnd2()
  # 32bitの整数を4つ使う
  # 周期は2**128-1

  # これだと32bitをオーバーする場合がある
  t = ($x ^ ($x << 11)) & 0xffffffff
  $x, $y, $z = $y, $z, $w
  $w = ($w ^ ($w >> 19)) ^ (t ^ (t >> 8))
  return $w
end


def test_xorshift128_rnd3()
  # 32bitの整数を4つ使う
  # 周期は2**128-1

  # これだと32bitをオーバーする場合がある
  t = ($x ^ ($x << 11)) & 0xffffffff
  $x, $y, $z = $y, $z, $w

  # rubyには符号なしとか無いので、右シフトした場合にシフトした分だけ、
  # 左に0があるようにした値とマスクする。
  # でも、この処理いらないかも
  $w = ($w ^ ($w >> 19 & 0x1fff)) ^ (t ^ (t >> 8 & 0xffffff))
  return $w
end


def test_xorshift128_rnd4(minimum, maximum)
  # 32bitの整数を4つ使う
  # 周期は2**128-1

  # 引数が0ならRAND_MAXまでとする

  if minimum < 0 or minimum > RAND_MAX
    minimum = 0
  end

  if maximum <= 0 or maximum > RAND_MAX
    maximum = RAND_MAX
  end

  # 引数の値+1として、0から引数の値までの範囲で乱数を求める
  # maximum += 1

  if minimum > maximum
    tmp = minimum
    minimum = maximum
    maximum = tmp
  end

  # 32bitに収まるようにする
  t = ($x ^ ($x << 11)) & 0xffffffff
  $x, $y, $z = $y, $z, $w
  $w = ($w ^ ($w >> 19)) ^ (t ^ (t >> 8))

  #RAND_MAXまでの範囲でmin-maxの間に収まるようにする
  return minimum + (($w * (maximum - minimum + 1.0) / (1.0 + RAND_MAX))).to_i
end


def test_xorshift128_rnd_generator
  # 32bitの整数を4つ使う
  # 周期は2**128-1

  # 32bit以内になるようにする
  t = ($x ^ ($x << 11)) & 0xffffffff
  $x, $y, $z = $y, $z, $w
  $w = ($w ^ ($w >> 19)) ^ (t ^ (t >> 8))
  return $w
end


def test_xorshift128_rnd5(minimum, maximum)
  # 引数が0ならRAND_MAXまでとする

  if minimum < 0 or minimum > RAND_MAX
    minimum = 0
  end

  if maximum <= 0 or maximum > RAND_MAX
    maximum = RAND_MAX
  end

  # 引数の値+1として、0から引数の値までの範囲で乱数を求める
  # maximum += 1

  if minimum > maximum
    tmp = minimum
    minimum = maximum
    maximum = tmp
  end

  return minimum + ((test_xorshift128_rnd_generator() * (maximum - minimum + 1.0) / (1.0 + RAND_MAX))).to_i
end


def test_xorshift128_rnd6
  # 0.0から1.0未満で乱数を生成
  # round()などで丸めこみはしない
  # return float((1.0 / (RAND_MAX + 1.0)) * test_linear_rnd_generator())
  return ((1.0 / (RAND_MAX + 1.0)) * test_xorshift128_rnd_generator()).to_f
end


if __FILE__ == $0

  puts('//---xorshift32--------')

  puts('test1---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift32_rnd1()
    puts(ret)
  end

  puts('test2---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift32_rnd2()
    puts(ret)
  end

  puts('test3---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift32_rnd3()
    puts(ret)
  end

  puts('test4---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift32_rnd4(20, 128)
    puts(ret)
  end

  puts('//---xorshift64--------')

  puts('test1---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift64_rnd1()
    puts(ret)
  end

  puts('test2---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift64_rnd2()
    puts(ret)
  end

  puts('test3---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift64_rnd3(20, 128)
    puts(ret)
  end

  puts('//---xorshift96--------')

  puts('test1---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift96_rnd1()
    puts(ret)
  end

  puts('test2---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift96_rnd2()
    puts(ret)
  end

  puts('test3---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift96_rnd3(20, 128)
    puts(ret)
  end

  puts('//---xorshift128--------')

  puts('test1---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift128_rnd1()
    puts(ret)
  end

  puts('test2---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift128_rnd2()
    puts(ret)
  end

  puts('test3---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift128_rnd3()
    puts(ret)
  end

  puts('test4---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift128_rnd4(20, 128)
    puts(ret)
  end

  puts('test5---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 20
    ret = test_xorshift128_rnd5(20, 128)
    puts(ret)
  end

  puts('test6---------')
  $x, $y, $z, $w = 123456789, 362436069, 521288629, 88675123
  for i in 0 ... 40
    ret = test_xorshift128_rnd6()
    puts("%.15f" % [ret])
  end

  puts('test7---------')
  seed(1978)
  puts($x)
  puts($y)
  puts($z)
  puts($w)
  for i in 0 ... 100
    ret = test_xorshift128_rnd5(1, 2048)
    if ret > 2048
      puts("error")
      break
    end
    puts("%06d %d" % [i, ret])
  end

  # puts('test8---------')
  # seed(1976)
  # puts($x)
  # puts($y)
  # puts($z)
  # puts($w)
  # for i in 0 ... 100000
  #   ret = test_xorshift128_rnd5(1, 6)
  #   if ret > 6
  #     puts("error")
  #     break
  #   end
  #   puts("%06d %d" % [i, ret])
  # end
end

