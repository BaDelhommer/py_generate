import os
import tkinter as tk
from graphics import Window
from tkinter import filedialog

current_step = "source"

def select_source_directory():
    global current_step
    directory_path = filedialog.askdirectory(title="Select source directory")
    if directory_path:
        print(f"Source destination: {directory_path}")
        current_step = "destination"
        select_destination_directory(directory_path)

def select_destination_directory(source):
    global current_step
    directory_path = filedialog.askdirectory(title="Select destintation directory")
    if directory_path:
        rel_path = directory_path + "/generate.go"
        print(f"Destination directory: {rel_path}")
        create_generate_file(source, rel_path)

def create_generate_file(source_directory, destination_directory):
    root_dir = source_directory
    generate_file_path = destination_directory

    file_exists = os.path.isfile(generate_file_path)
    initial_content = ""
    package_written = False
    generate_commands_written = False

    if file_exists:
        with open(generate_file_path, "r") as generate_file:
            initial_content = generate_file.read()
            package_written = "package main" in initial_content
            generate_commands_written = "//go:generate" in initial_content

    with open(generate_file_path, "a") as generate_file:

        if not package_written:
            generate_file.write("package main \n\n")
        
        for subdir, _, files in os.walk(root_dir):
            for file in files:

                relative_path = os.path.relpath(os.path.join(subdir, file), start=os.path.dirname(generate_file_path))
                relative_path = relative_path.replace("\\", "/")

                if generate_commands_written:
                    command_option = "bundled.go -append"
                else:
                    command_option = "bundled.go"
                    generate_commands_written = True


                command = f"//go:generate fyne bundle -o {command_option} ./{relative_path}\n"
                generate_file.write(command)

    print(f"generate.go file updated at {generate_file_path}")

def main():

    screen_x = 400
    screen_y = 300
    win = Window(screen_x, screen_y)

    if current_step == "source":
        win.create_button(command=select_source_directory)
    else:
        win.create_button(command=select_destination_directory)

    win.wait_for_close()
    # create_generate_file()

if __name__ == "__main__":
    main()

        
