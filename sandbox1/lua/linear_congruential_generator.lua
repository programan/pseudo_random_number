-- 線形合同法
-- X0 = seed
-- X(n+1) = (a * Xn + b) mod M
-- 以下の条件が満たされたとき、乱数の周期は最大M
-- 1. BとMが互いに素である。
-- 2. A-1が、Mの持つ全ての素因数で割りきれる。
-- 3. Mが4の倍数である場合は、A-1も4の倍数である。
-- とりあえずMは2^32にしておくのが良い
-- a,b,Mについては良い数字というものがいくつか発見されている
-- a = 1103515245, b = 12345, M = 2^32  GCC
-- a = 214013, b = 2531011, M = 2^32    VisualC++
-- a = 134775813, b = 1, M = 2^32       Borland Delphi

-- Lua5.1にはbit演算が無いのでライブラリを使う
-- Lua5.2にはbit演算が追加されている(bit32)
-- Lua5.3ではbit32が廃止され、<< >>の演算子追加されている
local bit32 = require('./lib/bit32')


-- 10進数の値を32桁の2進数に変換して返す
-- 32bitまでの範囲の値を扱える
-- https://note.cman.jp/convert/bit/
function dec2Bin(decimal)

  local binary = {}
  -- 少数切り捨てて絶対値を取得
  local d = math.abs(math.floor(decimal))

  if d == 0 then
    return string.format("%032d", d)

  end

  while d > 0 do
    binary[#binary + 1] = d % 2
    d = math.floor(d / 2)
  end

  local result = 0
  local count = #binary

  repeat
    result = result .. binary[count]
    count = count -1
  until count == 0

  -- print(type(result))
  -- print(result:len())
  if result:len() > 32 then
    result = result:sub((result:len() - 32) + 1)
  end

  if decimal < 0 then
    -- 反転して1を足す
    result = bit32.bxor(tonumber(result, 2), 0xffffffff)
    result = result + 1
    -- 32桁にする
    -- result = string.format("%132s", result)
    result = dec2Bin(result)
  else
    -- 32桁にする
    result = string.format("%032s", result)
  end

  return result
end

-- print(tonumber(4, 2) .. '<< 2 : ' .. tonumber(bit32.lshift(4,2), 2)) -->16
print(dec2Bin(0))
print(dec2Bin(1))
print(dec2Bin(2))
print(dec2Bin(3))
print(dec2Bin(4))
print(dec2Bin(5))
print(dec2Bin(6))
print(dec2Bin(7))

print(dec2Bin(-8))
print(dec2Bin(-7))
print(dec2Bin(-6))
print(dec2Bin(-5))
print(dec2Bin(-4))
print(dec2Bin(-3))
print(dec2Bin(-2))
print(dec2Bin(-1))

print(dec2Bin(11))
print(dec2Bin(-11))


-- b = 7
-- print(dec2Bin(b))
-- a = bit32.bxor(b, 0xf)
-- print(dec2Bin(a))
-- a = a + 1

-- print(dec2Bin(a))


local rnd_next = 1

function test_linear_rnd1(maximum)
  -- 乱数生成

  -- gccと同じ組み合わせで生成
  rnd_next = rnd_next * 1103515245 + 12345
  -- VCとかと同じように32bitに収まるようにする
  -- value % 2^32 == value & 2^32-1
  -- rnd_next = bit32.band(rnd_next, 0xffffffff)
  rnd_next = rnd_next % (2^32)

  -- 出てきた値をそのまま使うと、下1桁が奇数と偶数の繰り返しになる
  -- return int(rnd_next)
  -- return math.abs(math.floor(rnd_nextl))
  return math.abs(rnd_next)
end


for i=1,100 do
  print(i.." : "..test_linear_rnd1(10))
end


print(bit32.tobit(-1))

