import DelimitedFiles
import Optim

function part1(fname)
  initial_positions = vec(DelimitedFiles.readdlm(fname, ',', Int))

  f(x) = sum(abs.(initial_positions .- x))
  res = Optim.optimize(f, 0., maximum(initial_positions))

  optimal_position = ceil(Optim.minimizer(res))
  fuel_used = Int(minimum((f(optimal_position - 1), f(optimal_position))))
  println("Minimimal amount of fuel used: $fuel_used units.")
end

function part2(fname)
  initial_positions = vec(DelimitedFiles.readdlm(fname, ',', Int))

  f(x) = sum([sum(0:1:n_steps) for n_steps in (abs.(initial_positions .- x))])
  res = Optim.optimize(f, 0., maximum(initial_positions))

  optimal_position = ceil(Optim.minimizer(res))
  fuel_used = Int(minimum((f(optimal_position - 1), f(optimal_position))))
  println("Minimimal amount of fuel used: $fuel_used units.")
end

part1("test_input.txt")
part2("test_input.txt")

part1("input.txt")
part2("input.txt")
