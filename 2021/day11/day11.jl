GRID_LENGTH = 10
FLASH_THRESHOLD = 9
NEGATIVE_INF_INT = -10000000

function printarr(arr)
  for x in eachrow(arr)
    println(x)
  end
  println()
end

function part1(fname, n_steps)
  octopuses = Array{Int}(undef, (GRID_LENGTH, GRID_LENGTH))
  open(fname, "r") do f
    data = readlines(f)
    for (row_idx, row) in enumerate(data),
        (column_idx, number) in enumerate(row)
        octopuses[row_idx, column_idx] = parse(Int, number)
    end
  end
  n_flashes = 0
  for step in 1:1:n_steps
    octopuses .+= 1
    flashing = octopuses .> FLASH_THRESHOLD
    new_flashes = any(flashing)
    n_flashes += sum(flashing)
    octopuses[flashing] .= NEGATIVE_INF_INT
    while new_flashes
      # This loop is ugly but I did not manage to find an elegant method using,
      # e.g., array slicing.
      for col_idx in 1:1:size(flashing, 1), row_idx in 1:1:size(flashing, 2)
        if !flashing[col_idx, row_idx]
          continue
        end
        for dx in (-1, 0, 1), dy in (-1, 0, 1)
          if (dx == 0) && (dy == 0)
            continue
          end
          try
            octopuses[col_idx+dy, row_idx+dx] += 1
          catch e
            if isa(e, BoundsError)
              continue
            else
              throw(e)
            end
          end
        end
      end
      flashing = octopuses .> FLASH_THRESHOLD
      new_flashes = any(flashing)
      n_flashes += sum(flashing)
      octopuses[flashing] .= NEGATIVE_INF_INT
    end
    if all(octopuses .< 0)
      println("All octopuses flashing at step $step")
      break
    end
    octopuses[octopuses .< 0] .= 0
  end
  println("number of flashes: $n_flashes")
end

part1("test_input.txt", 100)
part1("test_input.txt", 1000)

part1("input.txt", 100)
part1("input.txt", 10000)
