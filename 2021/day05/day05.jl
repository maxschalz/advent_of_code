
function part1(fname::String)
  open(fname, "r") do f
    data = readlines(f)

    vent_map = Dict{Tuple{Int, Int}, Int}()
    for entry in data
      p1, _, p2 = split.(split(entry), ',')
      p1 = parse.(Int, p1)
      p2 = parse.(Int, p2)

      if p1[1] != p2[1] && p1[2] != p2[2]
        continue
      end

      for x in min(p1[1], p2[1]):1:max(p1[1], p2[1])
        for y in min(p1[2], p2[2]):1:max(p1[2], p2[2])
          vent_map[(x, y)] = get(vent_map, (x, y), 0) + 1
        end
      end
    end
    n_danger = sum((values(vent_map) .> 1))
    println("Number of dangerous spots: $n_danger")
  end
end

function part2(fname::String)
  open(fname, "r") do f
    data = readlines(f)

    vent_map = Dict{Tuple{Int, Int}, Int}()
    for entry in data
      p1, _, p2 = split.(split(entry), ',')
      p1 = parse.(Int, p1)
      p2 = parse.(Int, p2)

      if p1[1] != p2[1] && p1[2] != p2[2]
        for (x, y) in zip(p1[1]:sign(p2[1] - p1[1]):p2[1],
                          p1[2]:sign(p2[2] - p1[2]):p2[2])
          vent_map[(x, y)] = get(vent_map, (x, y), 0) + 1
        end
      else
        for x in min(p1[1], p2[1]):1:max(p1[1], p2[1])
          for y in min(p1[2], p2[2]):1:max(p1[2], p2[2])
            vent_map[(x, y)] = get(vent_map, (x, y), 0) + 1
          end
        end
      end
    end
    n_danger = sum((values(vent_map) .> 1))
    println("Number of dangerous spots: $n_danger")
  end
end



part1("test_input.txt")
part1("input.txt")

part2("test_input.txt")
part2("input.txt")
