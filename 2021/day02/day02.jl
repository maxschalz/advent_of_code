mutable struct Submarine
  depth::Int
  position::Int
  aim::Int
end

function move(self::Submarine, instruction::String)
  action, n = split(strip(instruction))
  n = parse(Int, n)
  if action == "forward"
    self.position += n
  elseif action == "down"
    self.depth += n
  elseif action == "up"
    self.depth -= n
  else
    throw(RuntimeError("Wrong instruction"))
  end
end

function updated_movement(self::Submarine, instruction::String)
  action, n = split(strip(instruction))
  n = parse(Int, n)
  if action == "forward"
    self.position += n
    self.depth += self.aim * n
  elseif action == "down"
    self.aim += n
  elseif action == "up"
    self.aim-= n
  else
    throw(RuntimeError("Wrong instruction"))
  end
end

function codify_position(self::Submarine)
  return self.depth * self.position
end

function run(instructions, mode, init_depth=0, init_pos=0, init_aim=0)
  sub = Submarine(init_depth, init_pos, init_aim)
  for instruction in instructions
    if mode == 1
      move(sub, instruction)
    else
      updated_movement(sub, instruction)
    end
  end
  result = codify_position(sub)
  println("The result (in mode $mode) is $result")
end

test_input = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
test_output = run(test_input, 1)
test_output = run(test_input, 2)

open("input.txt", "r") do f
  data = [s for s in readlines(f)]
  run(data, 1)
  run(data, 2)
end

