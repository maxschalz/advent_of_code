import Bijections

function part1(fname)
  unique_digits = (1, 4, 7, 8)
  unique_digit_lengths = (2, 4, 3, 7)
  n_unique_digits = 0

  open(fname, "r") do f
    data = readlines(f)
    for entry in data
      outputs = split(split(entry, '|')[2])
      length_outputs = [length(digit) for digit in outputs]
      n_unique_digits += sum([digit in unique_digit_lengths
                              for digit in length_outputs])
    end
  end
  println("1, 4, 7 and 8 appear in total $n_unique_digits times.")
end

function part2(fname)
  #=
  Strategy:
    - get 'cf', the 1
    - get 'acf', the 7
    - get 'bcdf', the 4
    - get 'abcdefg', the 8
    - get 'abcdfg', the 9, having the 4 as subset
    - get 'acdfg', the 3, having the 7 as subset
    - get 'abcefg', the 0, having the 1 as subset
    - get 'abdefg', the 6, the remaining digit of length 6.


    - get 'abdfg', the 5, having the 4 as subset
    - get 'acdeg', the 2, the remaining one
  =#
  open(fname, "r") do f
    data = readlines(f)
    sum_output = 0
    for entry in data
      signals, outputs = split.(split(entry, '|'))
      # Ordering of chars in signals and outputs needed for later comparisons.
      signals = join.(sort.(collect.(signals)))
      outputs = join.(sort.(collect.(outputs)))
      decoded = Bijections.Bijection{String, Int}()

      for (val, cond) in zip((1, 7, 4, 8, 9, 3, 0, 6, 2, 5), (
          x -> length(x) == 2, x -> length(x) == 3, x -> length(x) == 4,
          x -> length(x) == 7,
          x -> length(x)==6 && all([occursin(char, x) for char in decoded(4)]),
          x -> length(x)==5 && all([occursin(char, x) for char in decoded(7)]),
          x -> length(x)==6 && all([occursin(char, x) for char in decoded(1)]),
          x -> length(x) == 6,
          x -> occursin(decoded(8)[findfirst(x -> !occursin(x, decoded(9)), decoded(8))], x),
          x -> true
         ))
        decode_value!(decoded, signals, val, cond)
      end
      decoded_output = ""
      for output in outputs
        decoded_output *= string(decoded[output])
      end
      sum_output += parse(Int, decoded_output)
    end
    println("Sum of all outputs: $sum_output")
  end
end

function decode_value!(decoded, signals, value, condition)
  idx = findfirst(condition, signals)
  decoded[signals[idx]] = value
  deleteat!(signals, idx)
end

part1("test_input.txt")
part2("test_input.txt")

part1("input.txt")
part2("input.txt")
