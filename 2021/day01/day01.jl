function n_depth_increments(depths)
  difference = depths[2:1:end] - depths[1:1:end-1]

  n_increments = 0
  for diff in difference
    if diff > 0
      n_increments += 1
    end
  end
  return n_increments
end

function three_measurement_window(depths)
  window = depths[1:1:end-2] + depths[2:1:end-1] + depths[3:1:end]
  difference = window[2:1:end] - window[1:1:end-1]

  n_increments = 0
  for diff in difference
    if diff > 0
      n_increments += 1
    end
  end
  return n_increments
end

# Test case
# Each entry is the sea floor depth in increasing distance from sub.
test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
n_test = n_depth_increments(test_input)
println("Number of increments in the test case: $n_test")

n_test_three_window = three_measurement_window(test_input)
println("Number of increments in the three window test case: $n_test_three_window")

# Application to actual input.
open("input.txt", "r") do f
  data = [parse(Int, s) for s in readlines(f)]
  n_increments = n_depth_increments(data)
  println("Number of increments: $n_increments")

  n_three_window = three_measurement_window(data)
  println("Number of increments in the three window case: $n_three_window")
end
