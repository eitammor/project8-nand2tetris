class CodeWriter:

    def __init__(self, output_file: str):
        self.output_file = output_file
        self.label_counter = 0
        self.call_counter = 0


    def write_bootstrap_code(self):
        self.writeBoot()
        self.writeCall( "Sys.init", 0)

    def writeArithmetic(self,command: str):
        with open(self.output_file, "a") as out:
            assembly_command = self.handleArithmetic(command.split()[0])
            out.write(assembly_command)

    def handleArithmetic(self, command: str) -> str:
        assembly_command = ""
        if command == "add":
            assembly_command = """@SP
AM=M-1
D=M
A=A-1
M=D+M
"""
        elif command == "sub":
            assembly_command = """@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@SP
A=M
M=D
@SP
M=M+1
"""

        elif command == "neg":
            assembly_command = """@SP
A=M-1
M=-M
"""
        elif command == "eq":
            assembly_command = f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@EQUAL{self.label_counter}
D;JEQ
D=0
@NOTEQUAL{self.label_counter}
0;JMP
(EQUAL{self.label_counter})
D=-1
(NOTEQUAL{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""
        elif command == "gt":
            assembly_command = f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@GREATERTHEN{self.label_counter}
D;JGT
D=0
@NGREAT{self.label_counter}
0;JMP
(GREATERTHEN{self.label_counter})
D=-1
(NGREAT{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""
        elif command == "lt":
            assembly_command = f"""@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@LOWERTHEN{self.label_counter}
D;JLT
D=0
@NLOWERTHEN{self.label_counter}
0;JMP
(LOWERTHEN{self.label_counter})
D=-1
(NLOWERTHEN{self.label_counter})
@SP
A=M
M=D
@SP
M=M+1
"""
        elif command == "and":
            assembly_command = """@SP
AM=M-1
D=M
A=A-1
M=D&M
"""
        elif command == "or":
            assembly_command = """@SP
AM=M-1
D=M
A=A-1
M=D|M
"""
        elif command == "not":
                assembly_command = """@SP
A=M-1
M=!M
"""
        self.label_counter += 1
        return assembly_command


    def handlePush(self, segment: str, index: int) -> str:
        assembly_command = ""
        if segment == "pointer":
            if index == 0:
                assembly_command = f"""@3
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
            elif index == 1:
                assembly_command = f"""@4
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
            return assembly_command
        modified_segment = self.getSegment(segment)
        if segment == "constant":
            assembly_command = f"""@{index}
D=A
@SP
A=M
M=D
@SP
M=M+1
"""
        elif segment == "temp":
            modified_segment = self.getSegment(segment)
            assembly_command=f"""@{modified_segment}
D=A
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
        elif segment == "static":
            output = self.output_file.split("\\")[-1].split(".")[0]
            assembly_command = f"""@{output}.{index}
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
        #elif segment == "that" or segment == "argument" or segment == "static":
        else: assembly_command = f"""@{modified_segment}
D=M
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
"""
        return assembly_command


    def handlePop(self, segment: str, index: int)-> str:
        assembly_command = ""
        if segment == "pointer":
            if index == 0:
                assembly_command = f"""@SP
AM=M-1
D=M
@3
M=D
"""
            elif index == 1:
                assembly_command = f"""@SP
AM=M-1
D=M
@4
M=D
"""
            return assembly_command
        modified_segment = self.getSegment(segment)
        if segment == "temp":
            assembly_command = f"""@5
D=A
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
"""
        elif segment == "static":
            output = self.output_file.split("\\")[-1].split(".")[0]
            assembly_command = f"""@SP
M=M-1
A=M
D=M
@{output}.{index}
M=D
"""

        elif segment == "local" or segment == "this" or segment == "that" or segment == "argument":
            modified_segment = self.getSegment(segment)
            assembly_command = f"""@{modified_segment}
D=M
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
"""
        return assembly_command

    def writeLabel(self, label: str):
        with open(self.output_file, "a") as out:
            assembly_command = f"({label})\n"
            out.write(assembly_command)

    def writeGoto(self, label: str):
        with open(self.output_file, "a") as out:
            assembly_command = f"""@{label}
0;JMP
"""
            out.write(assembly_command)

    def writeIf(self, label: str):
        with open(self.output_file, "a") as out:
            assembly_command = f"""@SP
AM=M-1
D=M
@{label}
D;JNE
"""
            out.write(assembly_command)
    def writeFunction(self, functionName: str, nVars: int):
       with open(self.output_file, "a") as out:
            out.write(f"({functionName})\n")
            if nVars == 0:
                return
            out.write(f"""@{nVars}
D=A
@R13
M=D
(INIT_LOCALS)
@R13
D=M
@END_LOCALS
D;JEQ
@SP
A=M
M=0
@SP
M=M+1
@R13
M=M-1
@INIT_LOCALS
0;JMP
(END_LOCALS)
""")

    def writeCall(self, functionName: str, nArgs: int):
        with open(self.output_file, "a") as out:
            # Create a unique return address label
            return_label = f"{functionName}$ret.{self.call_counter}"
            self.call_counter += 1  # Increment for uniqueness
            #Push the return address
            out.write(f"""@{return_label}
D=A
@SP
A=M
M=D
@SP
M=M+1
""")

            #Push LCL, ARG, THIS, THAT
            for segment in ["LCL", "ARG", "THIS", "THAT"]:
                out.write(f"""@{segment}
D=M
@SP
A=M
M=D
@SP
M=M+1
""")

            #Reposition ARG = SP - nArgs - 5
            out.write(f"""@SP
D=M
@{nArgs + 5}
D=D-A
@ARG
M=D
""")

            # Reposition LCL = SP
            out.write("""@SP
D=M
@LCL
M=D
""")

            # Jump to the function
            out.write(f"""@{functionName}
0;JMP
""")

            # Write the return address label
            out.write(f"({return_label})\n")
    def writeReturn(self):
        with open(self.output_file, "a") as out:
            # Save the frame (LCL) in R13
            out.write("""@LCL
D=M
@frame
M=D
""") # R13 = frame (LCL)
            # Save the return address in R14 (frame - 5)
            out.write("""@5
D=D-A
A=D
D=M
@return_address
M=D
""")  # R14 = return address
            # Move the return value to ARG[0]
            out.write("""@SP
AM=M-1 
D=M 
@ARG
A=M
M=D
""")
            # Restore SP = ARG + 1
            out.write("""@ARG
D=M+1
@SP
M=D
""")  # SP = ARG + 1
            # Restore THAT, THIS, ARG, LCL
            #for segment in ["THAT", "THIS", "ARG", "LCL"]:
            out.write(f"""@frame
D=M-1
A=D
D=M
@THAT
M=D
@2
D=A
@frame
D=M-D
A=D
D=M
@THIS
M=D // THIS = *(FRAME-2)
@3
D=A
@frame
D=M-D
A=D
D=M
@ARG
M=D // ARG = *(FRAME-3)
@4
D=A
@frame
D=M-D
A=D
D=M
@LCL
M=D // LCL = *(FRAME-4)
@return_address
A=M
0;JMP // goto RET

""") # Restore segment

    def getSegment(self, segment: str) -> str:
        dict_segment = {"local": "LCL", "this": "THIS", "that": "THAT", "argument": "ARG", "static": "16", "temp": "5", "constant": "constant"}
        return dict_segment[segment]

    def WritePushPop(self, command: str, segment: str, index: int):
        with open(self.output_file, "a") as out:
            if command == "push":
                assembly_command = self.handlePush(segment, index)
                out.write(assembly_command)
            if command == "pop":
                assembly_command = self.handlePop(segment, index)
                out.write(assembly_command)


    def writeBoot(self):
        with open(self.output_file, "a") as out:
            out.write("""@256
D=A
@SP
M=D
""")