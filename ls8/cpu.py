"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH  = 0b01000101
ADD = 0b10100000
CALL = 0b01010000 
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.running = True
        self.branchtable = {
            HLT : self.handleHLT,
            LDI : self.handleLDI,
            PRN : self.handlePRN
        }



    def load(self):
        """Load a program into memory."""

        address = 0
        fl = sys.argv[1]

        if fl:
            with open(fl) as f:
                for ln in f:
                    ln = ln.split('#')
                    if ln[0] == '':
                        continue
                    self.ram[address] = int(ln[0],2)
                    address += 1

        else:
            print('no argv') 

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


    def ram_read(self,MAR):
        return self.ram[MAR]

    def ram_write(self,MAR,MDR):
        self.ram[MAR] = MDR

    def handleHLT(self):
        self.running = False

    def handleLDI(self,)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        # IR local variable in run method
        # make IR = mem address in pc reg
        
        IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        if IR not in self.branchtable:
            print('no IR at mar')
        else:
            run = self.branchtable[IR]
            run(operand_a, operand_b)
        
