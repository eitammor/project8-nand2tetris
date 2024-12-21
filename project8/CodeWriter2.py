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
        # Get the name of the directory
        dir_name = os.path.basename(os.path.normpath(input_path))
        # Combine all .vm files into a single file
        combined_vm_path = os.path.join(input_path, f"{dir_name}.vm")
        with open(combined_vm_path, 'w') as combined_vm:
            for vm_file in vm_files:
                vm_file_path = os.path.join(input_path, vm_file)
                with open(vm_file_path, 'r') as vm:
                    """
                                #Add comment in the beginning of reading each file
                    combined_vm.write(f"// File: {vm_file}\n")
                    """

                    combined_vm.write(vm.read() + "\n")

        # Notify the user of successful translation
        output_file = input_path.replace('.vm', '.asm')
        print(f"Output file: {output_file}")

        # Translate the combined .vm file
        translator = VMTranslator(combined_vm_path)
        translator.translate()

    # Notify the user of successful translation
    print(f"Translation complete! Output file: {input_path.replace('.vm', '.asm')}")




#if __name__ == "__main__":
#main()