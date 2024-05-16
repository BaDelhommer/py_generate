import os

# TODO: fix the function so the first command generated does not have the append flag set

def create_generate_file(root_dir, generate_file_path):

    file_exists = os.path.isfile(generate_file_path)

    with open(generate_file_path, "a") as generate_file:
        if not file_exists:
            generate_file.write("package main /n/n")
        
        for subdir, _, files in os.walk(root_dir):
            for file in files:
                relative_path = os.path.relpath(os.path.join(subdir, file), start=os.path.dirname(generate_file_path))
                relative_path = relative_path.replace("\\", "/")
                command = f"//go:generate fyne bundle -o bundled.go -append ./{relative_path}\n"
                generate_file.write(command)

    print(f"generate.go file updated at {generate_file_path}")

def main():
    create_generate_file(".\\aerials", ".\\generate.go")
    create_generate_file(".\\floorplans", ".\\generate.go")

if __name__ == "__main__":
    main()

        
