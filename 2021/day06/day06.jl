import DelimitedFiles
import Plots

function populate(fname::String, n_days::Int; n_init=-1)
  internal_timers = [n_init]
  if n_init == -1
    internal_timers = vec(DelimitedFiles.readdlm(fname, ',', Int))
  end

  n_size = Vector{Int}()
  for n in 1:1:n_days
    internal_timers .-= 1

    # Nomenclature misleading here. At 'zero' time, the fish continues to live
    # on and only *the following day* it breeds a new fish.
    zero_timers = internal_timers .== -1
    n_zeros = sum(zero_timers)
    internal_timers[zero_timers] .= 6
    internal_timers = vcat(internal_timers, zeros(Int, n_zeros) .+ 8)
    push!(n_size, size(internal_timers, 1))
  end
  n_fish = size(internal_timers, 1)
  println("$n_fish fishs after $n_days days.")
end



function more_efficient(fname, n_days)
  initial_timers = vec(DelimitedFiles.readdlm(fname, ',', Int))
  n_timers = vec(zeros(Int, 9))

  for initial_timer in initial_timers
    n_timers[initial_timer+1] += 1
  end

  for day in 1:1:n_days
    n_new_fishs = n_timers[1]
    n_timers[1:1:end-1] = n_timers[2:1:end]
    n_timers[end] = n_new_fishs
    n_timers[7] += n_new_fishs
  end
  n_fish = sum(n_timers)
  println("$n_fish fishs after $n_days days.")
end

populate("test_input.txt", 80)
populate("input.txt", 80)

more_efficient("test_input.txt", 18)
more_efficient("test_input.txt", 80)
more_efficient("test_input.txt", 256)
more_efficient("input.txt", 256)
