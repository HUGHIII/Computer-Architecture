# Variables are called "registers".
# * There are a fixed number
# * They have preset names: R0, R1, R2, R3 ... R7
#
# Registers can each hold a single byte
​
register = [0] * 8  # [0,0,0,0,0,0,0,0]
​
SP = 7
​
register[SP] = 0xf4   # Stack pointer
​
​
​
# Read program data
​
address = 0
​
if len(sys.argv) != 2:
	print("usage: comp.py progname")
	sys.exit(1)
​
try:
	with open(sys.argv[1]) as f:
		for line in f:
			line = line.strip()
​
			if line == '' or line[0] == "#":
				continue
​
			try:
				str_value = line.split("#")[0]
				value = int(str_value, 10)
​
			except ValueError:
				print(f"Invalid number: {str_value}")
				sys.exit(1)
​
			memory[address] = value
			address += 1
​
except FileNotFoundError:
	print(f"File not found: {sys.argv[1]}")
	sys.exit(2)
​
# Start execution at address 0
​
# Keep track of the address of the currently-executing instruction
pc = 0   # Program Counter, pointer to the instruction we're executing
​
halted = False
​
while not halted:
	instruction = memory[pc]
​
	#print(f"{pc:02x} | {instruction:02x}")
​
	if instruction == PRINT_BEEJ:
		print("Beej!")
		pc += 1
​
	elif instruction == HALT:
		halted = True
		pc += 1
​
	elif instruction == SAVE_REG:
		reg_num = memory[pc + 1]
		value = memory[pc + 2]
		register[reg_num] = value
		pc += 3
​
	elif instruction == PRINT_REG:
		reg_num = memory[pc + 1]
		print(register[reg_num])
		pc += 2
​
	elif instruction == PUSH:
		# Decrement the stack pointer
		register[SP] -= 1
​
		# Grab the value out of the given register
		reg_num = memory[pc + 1]
		value = register[reg_num] # this is what we want to push
​
		# Copy the value onto the stack
		top_of_stack_addr = register[SP]
		memory[top_of_stack_addr] = value
​
		pc += 2
​
		#print(memory[0xf0:0xf4])
		
	elif instruction == POP:
		# Get value from top of stack
		top_of_stack_addr = register[SP]
		value = memory[top_of_stack_addr] # Want to put this in a reg
​
		# Store in a register
		reg_num = memory[pc + 1]
		register[reg_num] = value
​
		# Increment the SP
		register[SP] += 1
​
		pc += 2
​
	else:
		print(f"unknown instruction {instruction} at address {pc}")
		sys.exit(1)
