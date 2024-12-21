from Parser import Parser
from CodeWriter import CodeWriter
#from CodeWriter2 import CodeWriter2
import sys

class VMTranslator:
    def __init__(self, input_file: str):
        """
        Initialize the HackAssembler.
        Opens the input file and prepares for processing.
        Constructs a symbol table and adds predefined symbols.
        """
        # Initialize Parser
        self.parser = Parser(input_file)
        self.output_file = input_file.replace(".vm", ".asm") #creates the output file
        self.code = CodeWriter(self.output_file)

    def writeBootstrap(self):
        self.code.write_bootstrap_code()

    def translate(self):
        while self.parser.hasMoreLines():
            #check for commands:
            if self.parser.commandType() == "C_ARITHMETIC":
                self.code.writeArithmetic(self.parser.getCurrentLine())
             #self.parser.commandType() == "C_PUSH" or self.parser.commandType() == "C_POP":
            elif self.parser.commandType() == "C_LABEL":
                label = self.parser.getCurrentLine().split()
                self.code.writeLabel(label[1])
            elif self.parser.commandType() == "C_GOTO":
                label = self.parser.getCurrentLine().split()
                self.code.writeGoto(label[1])
            elif self.parser.commandType() == "C_IF_GOTO":
                label = self.parser.getCurrentLine().split()
                self.code.writeIf(label[1])
            elif self.parser.commandType() == "C_FUNCTION":
                function = self.parser.getCurrentLine().split()
                self.code.writeFunction(function[1], int(function[2]))
            elif self.parser.commandType() == "C_CALL":
                call = self.parser.getCurrentLine().split()
                self.code.writeCall(call[1], int(call[2]))
            elif self.parser.commandType() == "C_RETURN":
                self.code.writeReturn()
            else:
                command = self.parser.getCurrentLine().split()
                self.code.WritePushPop(command[0], command[1], int(command[2]))
            self.parser.advance()

