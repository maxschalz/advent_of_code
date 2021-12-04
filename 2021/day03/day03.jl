function gamma_epsilon_rate(binaries::Array{Int,2})
  n_ones = sum(binaries, dims=1)
  gamma_rate = n_ones .> length(binaries[:,1]) / 2
  epsilon_rate = .!gamma_rate

  return bool_to_int(gamma_rate), bool_to_int(epsilon_rate)
end

function power_consumption(binaries::Array{String,1})
  binaries = parse_input(binaries)
  gamma, epsilon = gamma_epsilon_rate(binaries)
  power_consumption = gamma * epsilon
  println("Power consumption is $power_consumption")
end

function oxygen_rating(arr::Array{Int,2})
  bin_considered = 1
  length_arr = length(arr[:,1])
  while length(arr[:,1]) > 1
    n_ones = sum(arr[:, bin_considered])
    bit_to_keep = n_ones >= length_arr / 2 ? 1 : 0
    to_be_removed = Int[]
    for i = 1:1:length_arr
      if arr[i, bin_considered] != bit_to_keep
        push!(to_be_removed, i)
      end
    end
    arr = arr[setdiff(1:length_arr, to_be_removed),:]
    length_arr = length(arr[:,1])
    bin_considered += 1
  end
  return arr_to_int(arr)
end

function carbon_dioxide_rating(arr::Array{Int,2})
  bin_considered = 1
  length_arr = length(arr[:,1])
  while length(arr[:,1]) > 1
    n_ones = sum(arr[:, bin_considered])
    bit_to_keep = n_ones >= length_arr / 2 ? 0 : 1
    to_be_removed = Int[]
    for i = 1:1:length_arr
      if arr[i, bin_considered] != bit_to_keep
        push!(to_be_removed, i)
      end
    end
    arr = arr[setdiff(1:length_arr, to_be_removed),:]
    length_arr = length(arr[:,1])
    bin_considered += 1
  end
  return arr_to_int(arr)
end

function life_support_rating(arr::Array{String,1})
  parsed_input = parse_input(arr)
  oxygen = oxygen_rating(parsed_input)
  carbon_dioxide = carbon_dioxide_rating(parsed_input)
  life_support = oxygen * carbon_dioxide

  println("Life support rating is $life_support")
end

#=====================================
# Formatter and parser functions below
=====================================#
function parse_input(arr::Array{String,1})
  n_bits = length(arr[1])
  n_numbers = length(arr)
  rval = Array{Int,2}(undef, n_numbers, n_bits)
  for i in 1:1:n_numbers
    for j in 1:1:n_bits
      rval[i, j] = parse(Int, arr[i][j])
    end
  end
  return rval
end

function bool_to_int(arr)
  str = ""
  for bool in arr
    if bool
      str *= "1"
    else
      str *= "0"
    end
  end
  return parse(Int, str, base=2)
end

function arr_to_int(arr)
  str = ""
  for bit in arr
    str *= string(bit)
  end
  return parse(Int, str, base=2)
end

#=====================================
# Main
=====================================#
test_input = ["00100", "11110", "10110", "10111", "10101", "01111", "00111",
              "11100", "10000", "11001", "00010", "01010"]
power_consumption(test_input)
life_support_rating(test_input)

# Application to acutal input.
println()
open("input.txt", "r") do f
  data = readlines(f)
  power_consumption(data)
  life_support_rating(data)
end
