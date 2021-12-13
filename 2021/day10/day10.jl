import Bijections

BRACKET_PAIRS = Bijections.Bijection(Dict{Char, Char}('(' => ')', '[' => ']',
                                                      '{' => '}', '<' => '>'))

function part1_and_2(fname)
  corrupt_score = 0
  autocomplete_score = Vector{Int}()
  open(fname, "r") do f
    data = readlines(f)
    for line in data
      score = analyse_line(line)
      if score > 0
        push!(autocomplete_score, score)
      else
        corrupt_score += score
      end
    end
  end
  corrupt_score = abs(corrupt_score)
  middle_idx = Int(floor(length(autocomplete_score)/2) + 1)
  autocomplete_result = sort(autocomplete_score)[middle_idx]
  println("Total corruption score is $corrupt_score")
  println("Autocomplete score $autocomplete_result")
end

function analyse_line(line)
  penalties = Dict{Char, Int}(')' => 3, ']' => 57, '}' => 1197, '>' => 25137)
  to_be_closed = Vector{Char}()
  for character in line
    if character in Bijections.domain(BRACKET_PAIRS)
      push!(to_be_closed, character)
    elseif character != BRACKET_PAIRS[to_be_closed[end]]
      return -penalties[character]
    else
      pop!(to_be_closed)
    end
  end

  autocomplete_score = Dict{Char, Int}(')' => 1, ']' => 2, '}' => 3, '>' => 4)
  score = 0
  while !isempty(to_be_closed)
    score *= 5
    score += autocomplete_score[BRACKET_PAIRS[to_be_closed[end]]]
    pop!(to_be_closed)
  end
  return score
end

part1_and_2("test_input.txt")
part1_and_2("input.txt")
