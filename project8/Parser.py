C_ARITHMETIC = "C_ARITHMETIC"
C_PUSH = "C_PUSH"
C_POP = "C_POP"
C_LABEL = "C_LABEL"
C_GOTO = "C_GOTO"
C_IF_GOTO = "C_IF_GOTO"
C_CALL = "C_CALL"
C_FUNCTION = "C_FUNCTION"
C_RETURN = "C_RETURN"





class Parser:
    def __init__(self, file_name: str):
        try:
            # Open the file in read mode
            self.file = open(file_name, "r+")
            # Read all lines into a list
            lines = self.file.readlines()
            # Initialize the current line index
            self.current_index = 0
            #go over the file and remove comments and empty lines
            self.file_lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("//")]
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            self.file = None
            self.file_lines = []
            self.current_index = 0

    def __del__(self):
        """
        Destructor: Ensures the file is closed when the Parser object is destroyed.
        """
        if self.file:
            self.file.close()

    def hasMoreLines(self) -> bool:
        """
        function returns true if there are more lines in the file.
        """
        return self.current_index  < len(self.file_lines)

    def advance(self):
        """
        advances the current line by one and returns the next line as a string.
        :return:
        """
        if self.hasMoreLines():
            current_line = self.file_lines[self.current_index]
            self.current_index += 1
            return current_line
        return None

    def commandType(self) -> str:
        """
        returns the command type by the beginning of the line
        """
        #check if the current command starts like an A push command
        if self.file_lines[self.current_index].startswith('push'):
            return C_PUSH
        # check if the current command starts like an A pop command
        elif self.file_lines[self.current_index].startswith('pop'):
            return C_POP
        elif self.file_lines[self.current_index].startswith('label'):
            return C_LABEL
        elif self.file_lines[self.current_index].startswith('goto'):
            return C_GOTO
        elif self.file_lines[self.current_index].startswith('if-goto'):
            return C_IF_GOTO
        elif self.file_lines[self.current_index].startswith('function'):
            return C_FUNCTION
        elif self.file_lines[self.current_index].startswith('call'):
            return C_CALL
        elif self.file_lines[self.current_index].startswith('return'):
            return C_RETURN
        else: #else it's an arithmatic command
            return C_ARITHMETIC



    def arg1(self) -> str:
        if self.commandType() == C_ARITHMETIC:
            return self.file_lines[self.current_index]
        else:
            return self.file_lines[self.current_index].split()[1]

    def arg2(self) -> int:
        if self.commandType() == C_POP or self.commandType() == C_PUSH:
            return self.file_lines[self.current_index].split()[2]
        else: #if the command is not push or pop return -1
            return -1

    def setIndex(self):
        self.current_index = 0
    def getCurrentLine(self) -> str:
        return self.file_lines[self.current_index]