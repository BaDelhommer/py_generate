import os
import tkinter as tk
from tkinter import filedialog

class GenerateTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.current_step = "source"
        self.source_directory = ""
        self.destination_directory = ""

        self.label = tk.Label(self.root, text="Select the source directory containing resources:")
        self.label.pack(pady=20)

        self.button = tk.Button(self.root, text="Select Source Directory", command=self.select_source_directory)
        self.button.pack()

    def select_source_directory(self):
        self.source_directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Source DIrectory")
        if self.source_directory:
            print(f"Source Directory: {self.source_directory}")
            self.current_step = "destintation"
            self.label.config(text="Select destination directory for generate.go:")
            self.button.config(text="Select Destination Directory", command=self.select_destination_directory)

    def select_destination_directory(self):
        self.destination_directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Destination DIrectory")
        if self.destination_directory:
            rel_path = os.path.join(self.destination_directory, "generate.go")
            print(f"Destination directory{rel_path}")
            self.create_generate_file(self.source_directory, rel_path)

    def create_generate_file(self, source_directory, generate_file_path):
        root_dir = source_directory

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
                generate_file.write("package main\n\n")

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
        self.label.config(text="Process Complete!!")
        self.button.config(text="Done", state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    tool = GenerateTool()
    tool.run()