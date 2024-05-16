import os

def create_generate_file():
    root_dir = input("Input the relative path to dir containing resources: ")
    generate_file_path = input("Input the relative path for generate.go: ")


    file_exists = os.path.isfile(generate_file_path)

    with open(generate_file_path, "a") as generate_file:
        command_option = ""
        if not file_exists:
            generate_file.write("package main\n\n")

        
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                generate_file.seek(0, os.SEEK_END)
                file_size = generate_file.tell()

                if file_size > 20:
                    command_option = "bundled.go -append"
                else: command_option = "bundled.go"

                relative_path = os.path.relpath(os.path.join(subdir, file), start=os.path.dirname(generate_file_path))
                relative_path = relative_path.replace("\\", "/")
                command = f"//go:generate fyne bundle -o {command_option} ./{relative_path}\n"
                generate_file.write(command)

    print(f"generate.go file updated at {generate_file_path}")

def main():
    create_generate_file()

if __name__ == "__main__":
    main()

        
