from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

from .. import calculate

class App(Tk):
    """Class that represents the main app."""


    def __init__(self):
        super().__init__()

        # Configure window
        self.geometry("400x400")
        self.title("Lines of Code")

        self.directory = ""

        self.draw()


    def draw(self):
        """Put components to the window"""

        # Title bar
        title = ttk.Label(self, text="Lines of Code")
        title.config(font=("*", 25))
        title.pack()

        # Choose directory
        self.show_directory_var = StringVar(value="Choose directory")

        directory_button = ttk.Button(self, textvariable=self.show_directory_var, command=self.handle_choose_directory_button)
        directory_button.pack()

        # Options
        self.options_frame = Frame(self, padx=5, pady=5, highlightbackground="black", highlightthickness=1)
        self.options_frame.pack()

        # Whitelist/blacklist file extensions
        Label(self.options_frame, text="File extensions/directories\nSeparate by spaces (eg: \".py .java node_modules\")\nLeave blank to ignore").pack()
        self.file_extensions_input = Text(self.options_frame, height=5, width=30)
        self.file_extensions_input.pack()

        self.whitelist_extensions_var = BooleanVar(value=False)
        self.blacklist_extensions_var = BooleanVar(value=False)
        
        whitelist_checkbutton = ttk.Checkbutton(self.options_frame, text="Whitelist extensions", variable=self.whitelist_extensions_var, command=lambda: self.handle_switch_whitelist_blacklist(True))
        whitelist_checkbutton.pack()
        blacklist_checkbutton = ttk.Checkbutton(self.options_frame, text="Blacklist extensions/directories", variable=self.blacklist_extensions_var, command=lambda: self.handle_switch_whitelist_blacklist(False))
        blacklist_checkbutton.pack()

        # Calculate button
        calculate_button = ttk.Button(self, text="Calculate", command=self.calculate)
        calculate_button.pack()

        # Results
        self.results_frame = ttk.Frame(self)
        self.results_frame.pack(padx=5, pady=5)


    def handle_switch_whitelist_blacklist(self, whitelist: bool):
        """
        Switch whitelist/blacklist selection checkbuttons.
        
        If clicked already selected checkbutton, disable both.
        """
        if whitelist:
            self.whitelist_extensions_var.set(True)
            self.blacklist_extensions_var.set(False)
        
        else:
            self.whitelist_extensions_var.set(False)
            self.blacklist_extensions_var.set(True)


    def handle_choose_directory_button(self):
        """
        Handles the choose directory button click.

            - Opens file dialog
            - Saves directory path to string
            - Change button text
        """

        self.directory = filedialog.askdirectory(initialdir=self.directory)
        if self.directory:
            self.show_directory_var.set(f"Directory: {calculate.get_directory_name(self.directory)}")
        else:
            messagebox.showwarning("Warning", "No directory selected.")


    def calculate(self):
        try:
            file_extensions = self.file_extensions_input.get("1.0", END).strip().split()

            # Validate file extensions (start with .)
            if self.directory:

                # Get results
                results = calculate.get_lines_of_code(self.directory, self.whitelist_extensions_var.get(), file_extensions)

                lines_of_code = results[0]
                blanklines_of_code = results[1]
                characters_of_code = results[2]

                # Remove existing results from results frame
                for child in self.results_frame.winfo_children():
                    child.destroy()

                # Display results
                lines_of_code_label = ttk.Label(self.results_frame, text=f"Lines of code: {lines_of_code}")
                blanklines_of_code_label = ttk.Label(self.results_frame, text=f"Blank lines of code: {blanklines_of_code}")
                nonblanklines_of_code_label = ttk.Label(self.results_frame, text=f"Non-blank lines of code: {lines_of_code - blanklines_of_code}")
                characters_of_code_label = ttk.Label(self.results_frame, text=f"Characters of code: {characters_of_code}")

                lines_of_code_label.pack()
                blanklines_of_code_label.pack()
                nonblanklines_of_code_label.pack()
                characters_of_code_label.pack()


        except AttributeError:
            messagebox.showerror("Error", "No directory selected.")
        
        except ValueError as e:
            messagebox.showerror("Error", e)