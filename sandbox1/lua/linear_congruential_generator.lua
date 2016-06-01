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
function dec2Bin(decimal)
  -- local binary = 0
  -- local base = 1
  -- while decimal > 0 do
  --   binary = binary + (decimal % 2) * base
  --   decimal = math.floor(decimal / 2)
  --   base = base * 10
  -- end
  -- return binary

  local binary = {}
  local d = math.abs(decimal)

  if d == 0 then
    return d
  end

  while d > 0 do
    binary[#binary + 1] = d % 2
    d = math.floor(d / 2)
  end

  local result = 0
  if table.getn(binary) > 0 then
    local count = #binary

    repeat
      result = result .. binary[count]
      count = count -1
    until count == 0

    -- 32桁にする
    result = string.format("%032d", result)
  end

  -- 負数の場合
  -- if decimal < 0 then
  --   -- 反転して1を足す
  --   result = bit32.bxor(tonumber(result, 2), 0xffffffff)
  --   result = result + 1
  -- end

  return result
end

-- print(tonumber(4, 2) .. '<< 2 : ' .. tonumber(bit32.lshift(4,2), 2)) -->16
print(dec2Bin(11))


-- b = 7
-- print(dec2Bin(b))
-- a = bit32.bxor(b, 0xf)
-- print(dec2Bin(a))
-- a = a + 1

-- print(dec2Bin(a))

