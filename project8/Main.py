from VMTranslator import VMTranslator
from CodeWriter import CodeWriter
import os
import sys

def main():

    input_path = sys.argv[1]

    #file input
    if os.path.isfile(input_path):
        # Process the single .vm file
        translator = VMTranslator(input_path)
        translator.translate()
        # Notify the user of successful translation
        output_file = input_path.replace('.vm', '.asm')
        print(f"Output file: {output_file}")

    #dir input
    elif os.path.isdir(input_path):
        # Process all .vm files in the directory
        vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        counter = 0
        for vm_file in vm_files:
            vm_file_path = os.path.join(input_path, vm_file)
            translator = VMTranslator(vm_file_path)
            if(not counter):
                translator.writeBootstrap()
            translator.translate()
            counter += 1
        #to_output = [f for f in os.listdir(input_path) if f.endswith('.asm')]
        # Get the directory name to use as the output file name
        directory_name = os.path.basename(input_path)
        output_file_name = f"{directory_name}.asm"
        output_file_path = os.path.join(input_path, output_file_name)
        
        # Open the output file in write mode
        with open(output_file_path, 'w') as output_file:
            # Iterate over all files in the directory
            for filename in os.listdir(input_path):
                file_path = os.path.join(input_path, filename)
                # Only process .asm files
                if filename.endswith('.asm') and os.path.isfile(file_path):
                    if file_path != output_file_path:
                        with open(file_path, 'r') as input_file:
                            # Read the content and write it to the output file
                            content = input_file.read()
                            output_file.write(content + "\n")  # Add a newline between files
                        os.remove(file_path)

        






if __name__ == "__main__":
    main()