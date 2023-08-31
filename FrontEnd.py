import threading
import tkinter as tk
import BackEnd

class FrontendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Data Entry")

        self.search_data = []

        # Create an instance of the WebScraper class
        self.web_scraper = BackEnd.WebScraper()

        # Define the desired font and font color
        self.font_style = ("Segoe UI", 11, "bold")
        self.font_color = "#393939"

        self.create_widgets()

    def create_widgets(self):
        # Part Numbers
        part_label = tk.Label(self.root, text="Part Numbers:", font=self.font_style, fg=self.font_color)
        part_label.grid(row=0, column=0, sticky="w")
        self.part_entry = tk.Entry(self.root, width=40, font=self.font_style)
        self.part_entry.grid(row=0, column=1, padx=5, pady=5)
        self.part_clear_button = tk.Button(self.root, text="Clear", command=self.clear_part_entry, font=self.font_style)
        self.part_clear_button.grid(row=0, column=2, padx=5, pady=5)

        # Cross Reference Numbers
        cross_ref_label = tk.Label(self.root, text="Cross Reference Numbers:", font=self.font_style, fg=self.font_color)
        cross_ref_label.grid(row=1, column=0, sticky="w")
        self.cross_ref_entry = tk.Entry(self.root, width=40, font=self.font_style)
        self.cross_ref_entry.grid(row=1, column=1, padx=5, pady=5)
        self.cross_ref_clear_button = tk.Button(self.root, text="Clear", command=self.clear_cross_ref_entry, font=self.font_style)
        self.cross_ref_clear_button.grid(row=1, column=2, padx=5, pady=5)

        # Fitments
        fitments_label = tk.Label(self.root, text="Fitments:", font=self.font_style, fg=self.font_color)
        fitments_label.grid(row=2, column=0, sticky="w")
        self.fitments_entry = tk.Entry(self.root, width=40, font=self.font_style)
        self.fitments_entry.grid(row=2, column=1, padx=5, pady=5)
        self.fitments_clear_button = tk.Button(self.root, text="Clear", command=self.clear_fitments_entry, font=self.font_style)
        self.fitments_clear_button.grid(row=2, column=2, padx=5, pady=5)

        # Clear All Button
        clear_all_button = tk.Button(self.root, text="Clear All", command=self.clear_all_entries, font=self.font_style)
        clear_all_button.grid(row=3, column=0, padx=5, pady=10)

        # Submit Button
        submit_button = tk.Button(self.root, text="Submit", command=self.save_search_data, font=self.font_style)
        submit_button.grid(row=3, column=1, padx=5, pady=5)

        # Exit Button
        exit_button = tk.Button(self.root, text="Exit", command=self.exit_application, font=self.font_style)
        exit_button.grid(row=3, column=2, padx=5, pady=5)

        # Create the menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create the Documentation menu
        documentation_menu = tk.Menu(menubar, tearoff=0)
        documentation_menu.add_command(label="Documentation", command=self.open_documentation_window, font=self.font_style)

        # Add Documentation menu to the menu bar
        menubar.add_cascade(label="Help", menu=documentation_menu)

    def open_documentation_window(self):
        documentation_text = """
            This is the Web Scraper for the company's internal site.\n
            \n
            The function for this project is to allow for easier searching and filtering through the Bosda Catalog datatable.\n
            \n
            To start off, here are the features of the application and their function:\n
            \t-The "Part Numbers" search query is used for inputting Part Numbers like item id's and SKUs.\n
            \t-The "Cross Reference Numbers" search query is used for inputting Cross Reference numbers.\n
            \t-The "Fitments" search query is used for inputting Cross reference numbers.\n
            \t-The "Clear" buttons are used to clear or reset the corresponding search query.\n
            \t-The "Clear All" button will clear or reset all three search queries.\n
            \t-The "Submit" button will pass the inputted filters/searching into the program and the filtering will begin.\n
            \t-The "Exit" button will safely shut down the application when the user is done using it.\n
            Some things to consider:\n
            \t-For multiple inputs, entries must be separated by "/". For instance: 515096/513121. 
            \n\t The reason for this is that fitments, and some item id's have dashes and commas in them.\n
            \t-If an invalid entry is made, the application will still run the search as usual, but nothing will be found and no filter will be selected.\n
            \t-If no inputs are made, the program will still run the search as usual, but nothing will be searched.\n
            NOTE: It would be recommended to click the "Exit" button upon use of the application as this would safely\n
            \t      close both the program and the chrome window. 
            """

        documentation_window = tk.Toplevel(self.root)
        documentation_window.title("Documentation")
        documentation_label = tk.Label(documentation_window, text=documentation_text, padx=10, pady=10, justify="left",
                                       font=self.font_style)
        documentation_label.pack()
    def exit_application(self):
        self.root.destroy()  # Close the application window

    def save_search_data(self):
        part_numbers = self.parse_input(self.part_entry.get())
        cross_ref_numbers = self.parse_input(self.cross_ref_entry.get())
        fitments = self.parse_input(self.fitments_entry.get())

        self.search_data = [
            {
                "xpath": '//*[@id="table_1_1_filter"]',
                "queries": part_numbers
            },
            {
                "xpath":'//*[@id="table_1_5_filter"]',
                "queries": cross_ref_numbers
            },
            {
                "xpath":'//*[@id="table_1_14_filter"]',
                "queries": fitments
            }
        ]

        # Run the search_and_click method in a separate thread
        threading.Thread(target=self.web_scraper.search_and_click, args=(self.search_data,)).start()

        # Clear text fields
        self.part_entry.delete(0, tk.END)
        self.cross_ref_entry.delete(0, tk.END)
        self.fitments_entry.delete(0, tk.END)

    def clear_part_entry(self):
        self.part_entry.delete(0, tk.END)

    def clear_cross_ref_entry(self):
        self.cross_ref_entry.delete(0, tk.END)

    def clear_fitments_entry(self):
        self.fitments_entry.delete(0, tk.END)

    def clear_all_entries(self):
        self.part_entry.delete(0, tk.END)
        self.cross_ref_entry.delete(0, tk.END)
        self.fitments_entry.delete(0, tk.END)
    def parse_input(self, input_string):
        inputs = input_string.split("/")
        cleaned_inputs = [input.strip() for input in inputs]
        return cleaned_inputs

if __name__ == "__main__":
    root = tk.Tk()
    app = FrontendApp(root)
    root.mainloop()
