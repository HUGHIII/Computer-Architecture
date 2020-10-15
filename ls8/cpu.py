  
"""CPU functionality."""

import sys
# fileN = sys.argv[1]
# print(fileN,'sys argv')

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True




    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py examples/file")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    # print(line)
                    if line == "" or line[0] == "#":
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)
                        

                    except ValueError:
                        print(f"Invalid Number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"FileNotFound: {sys.argv[1]}")
            sys.exit(2)

        for i in self.ram:

            print(i)




        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def ram_read(self,MAR):
        return self.ram[MAR]

    def ram_write(self,MDR,MAR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        while self.running:
            # instruction register, read memory address stored in register
            # for i in range(256):
            #     print(self.ram[i],end = "--")

            # self.trace()
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                # exit
                self.running = False
            elif IR == LDI:
                # set specified register to specified value
                self.reg[operand_a] = operand_b
                self.pc += 3
                
            elif IR == PRN:
                # print value from specified register
                print(self.reg[operand_a])
                self.pc += 2
            else:
                print(f'unknown instruction {IR} at address {self.pc}')
                self.running = False 