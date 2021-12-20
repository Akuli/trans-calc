import json
import tkinter
import math
from tkinter import ttk
from typing import Dict, Any, Union


class TransCalcGui:
    def __init__(self) -> None:
        self.client_dict = self.get_clients()
        self.root = tkinter.Tk()
        self.root.resizable(False, False)
        self.root.title("Trans-Calc")
        self.root.geometry("550x700")

        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill="both", expand=True)

        self.header = ttk.Label(
            self.mainframe, text="Trans-Calc", font=("TkDefaultFont", 18), justify="center")

        self.clients_label = ttk.Label(
            self.mainframe, text="Client", font=("TkDefaultFont", 16))
        self.clients_dropdown = ttk.Combobox(
            self.mainframe, state="readonly")

        if self.client_dict:
            self.clients_dropdown["values"] = list(self.client_dict.keys())
        else:
            self.clients_dropdown["values"] = None

        if self.client_dict:
            self.clients_dropdown.set(list(self.client_dict.keys())[0])

        self.clients_dropdown.bind(
            "<<ComboboxSelected>>", self.create_matrix_rows)

        self.button_frame = ttk.Frame(self.mainframe)

        self.add_client_button = ttk.Button(
            self.button_frame, command=self.add_new_client, text="Add Client")
        self.edit_client_button = ttk.Button(
            self.button_frame, text="Edit Client")
        self.delete_client_button = ttk.Button(
            self.button_frame, text="Delete Client")

        self.matrix_rows_frame = ttk.Frame(self.mainframe)

        self.create_ui_grid()
        if self.client_dict:
            self.create_matrix_rows()

    def create_matrix_rows(self, event=None) -> None:
        self.matrix_rows_frame.grid(column=0, columnspan=3)

        tm_match_label = ttk.Label(
            self.matrix_rows_frame, text="TM Match", font=("TkDefaultFont", 16))
        word_count_label = ttk.Label(
            self.matrix_rows_frame, text="Word Count", font=("TkDefaultFont", 16))
        match_discount_label = ttk.Label(
            self.matrix_rows_frame, text="Match Discount", font=("TkDefaultFont", 16))

        tm_match_label.grid(column=0, row=0, padx=(20, 30), pady=(
            0, 30))
        word_count_label.grid(column=1, row=0, padx=(0, 30), pady=(
            0, 30))
        match_discount_label.grid(sticky="e", column=2, row=0, padx=(0, 30), pady=(
            0, 30))

        for enum, matrix_row in enumerate(self.client_dict[self.clients_dropdown.get()]["matrix"], start=1):
            discount_current_row = str(int(self.client_dict[self.clients_dropdown.get(
            )]["matrix"][matrix_row] * 100))
            row_percentage_label = ttk.Label(
                self.matrix_rows_frame, text=matrix_row + "%")
            row_word_count_input = ttk.Entry(self.matrix_rows_frame, width=25)
            row_match_discount_label = ttk.Label(
                self.matrix_rows_frame, text=f"({discount_current_row}% of full rate)")

            row_percentage_label.grid(
                sticky="nes", column=0, row=enum, padx=(0, 30), pady=(0, 20))
            row_word_count_input.grid(sticky="wn", column=1,
                                      row=enum, padx=(0, 30))
            row_match_discount_label.grid(sticky="nw", column=2,
                                          row=enum, padx=(0, 30))

    def create_ui_grid(self) -> None:
        self.mainframe.columnconfigure(3)
        self.header.grid(sticky="n", column=0, columnspan=3,
                         padx=(0, 0), pady=(30, 30))
        self.clients_label.grid(sticky="we", column=0, columnspan=1,
                                padx=(20, 0), pady=(30, 10))

        self.clients_dropdown.grid(sticky="we", column=0, columnspan=1,
                                   padx=(20, 0), pady=(0, 20))
        self.button_frame.grid(sticky="we", column=0, columnspan=3,
                               padx=(20, 20), pady=(0, 40))

        self.add_client_button.grid(column=0, row=0, padx=(5, 5))
        self.edit_client_button.grid(column=1, row=0, padx=(5, 5))
        self.delete_client_button.grid(column=2, row=0, padx=(5, 5))

    def add_new_client(self) -> None:
        add_client_window = tkinter.Toplevel()
        add_client_content = AddClient(add_client_window, self.client_dict)
        add_client_content.mainframe.pack(fill="both", expand=True)

    def get_clients(self) -> Dict:
        try:
            with open("client-data.json", "r") as client_data:
                client_dict: Dict[Any] = json.load(client_data)["clients"]
            return client_dict
        except json.decoder.JSONDecodeError:
            print("JSON empty")
            return None


class AddClient:
    def __init__(self, add_client_window: tkinter.Toplevel, client_dict) -> None:
        self.add_client_window = add_client_window
        self.add_client_window.resizable(False, False)
        self.add_client_window.title("Add Client")
        self.add_client_window.geometry("400x700")
        self.client_dict = client_dict

        self.mainframe = ttk.Frame(self.add_client_window)

        self.header = ttk.Label(self.mainframe, text="Add Client",
                                font=("TkDefaultFont", 18), justify="center")

        self.client_name_label = ttk.Label(self.mainframe, text="Client Name")
        self.client_name_entry = ttk.Entry(
            self.mainframe, width=25)

        self.client_currency_label = ttk.Label(
            self.mainframe, text="Currency")
        self.client_currency_entry = ttk.Entry(
            self.mainframe, width=8)
        self.client_currency_example = ttk.Label(
            self.mainframe, text="(ex. \"EUR\" or \"USD\")")

        self.client_full_rate_label = ttk.Label(
            self.mainframe, text="Full Rate\nper Word")
        self.client_full_rate_entry = ttk.Entry(
            self.mainframe, width=8)
        self.client_full_rate_example = ttk.Label(
            self.mainframe, text="(ex. \"0.15\")")

        self.tm_match_range_label = ttk.Label(
            self.mainframe, text="TM Match\nRanges")
        self.tm_match_discount_label = ttk.Label(
            self.mainframe, text="Disccount\n(% of full price)")

        self.matrix_frame = ttk.Frame(self.mainframe)

        self.save_client_button = ttk.Button(
            self.mainframe, command=self.save_client, text="Save Client")

        self.create_ui_grid()

    def add_matrix_row(self) -> None:
        new_row_num = self.matrix_frame.grid_size()[1]
        if new_row_num >= 8:
            return
        new_row_tm_range = ttk.Entry(self.matrix_frame, width=8)
        new_row_tm_discount = ttk.Entry(self.matrix_frame, width=8)
        new_row_tm_range.grid(
            sticky="ne", column=1, row=new_row_num, padx=(0, 30), pady=(0, 5))
        new_row_tm_discount.grid(
            sticky="nw", column=2, row=new_row_num, padx=(0, 0), pady=(0, 5))

    def delete_matrix_row(self) -> None:
        pass

    def create_ui_grid(self) -> None:
        self.mainframe.rowconfigure(7, weight=1)
        self.header.grid(sticky="n", column=0, columnspan=3,
                         padx=(0, 0), pady=(30, 30))
        self.client_name_label.grid(
            sticky="ne", column=0, row=1, padx=(10, 20), pady=(0, 20))
        self.client_name_entry.grid(
            sticky="nw", column=1, columnspan=2, row=1, padx=(0, 0), pady=(0, 20))
        self.client_currency_label.grid(
            sticky="ne", column=0, row=2, padx=(10, 20), pady=(0, 20))
        self.client_currency_entry.grid(
            sticky="nw", column=1, row=2, padx=(0, 0), pady=(0, 20))
        self.client_currency_example.grid(
            sticky="nw", column=2, row=2, padx=(0, 20), pady=(0, 20))
        self.client_full_rate_label.grid(
            sticky="ne", column=0, row=3, padx=(10, 20), pady=(0, 30))
        self.client_full_rate_entry.grid(
            sticky="nw", column=1, row=3, padx=(0, 0), pady=(0, 30))
        self.client_full_rate_example.grid(
            sticky="nw", column=2, row=3, padx=(0, 20), pady=(0, 30))

        self.tm_match_range_label.grid(
            sticky="nw", column=1, row=4, padx=(0, 50), pady=(0, 5))
        self.tm_match_discount_label.grid(
            sticky="nw", column=2, row=4, padx=(0, 0), pady=(0, 5))

        self.matrix_frame.grid(
            sticky="nw", column=1, columnspan=3, row=5, padx=(0, 0), pady=(0, 20))

        for i in range(8):
            tm_match_range = ttk.Entry(self.matrix_frame, width=8)
            tm_match_discount = ttk.Entry(self.matrix_frame, width=8)
            tm_match_range.grid(
                sticky="ne", column=1, row=i, padx=(0, 30), pady=(0, 5))
            tm_match_discount.grid(
                sticky="nw", column=2, row=i, padx=(0, 0), pady=(0, 5))

        self.save_client_button.grid(
            sticky="se", column=2, row=7, padx=(0, 0), pady=(0, 20))

        self.client_name_entry.focus()

    def save_client(self) -> None:
        print(self.client_dict)
        # Not sure why grid_slaves is returned backwards. Had to use reversed()
        matrix_row_values = [value.get() for value in reversed(
            self.matrix_frame.grid_slaves()) if value.get()]

        ranges_and_discounts = {str(range): (int(discount) / 100) for range, discount in zip(
            matrix_row_values[::2], matrix_row_values[1::2])}

        client_name = self.client_name_entry.get()
        client_info = {
            "full_rate": float(self.client_full_rate_entry.get()),
            "currency": self.client_currency_entry.get(),
            "matrix": ranges_and_discounts
        }

        self.save_client_to_json(client_name, client_info)

    def save_client_to_json(self, client_name: str, client_info) -> None:
        self.client_dict[client_name] = client_info
        client_data = {"clients": self.client_dict}

        try:
            with open("client-data.json", "w") as client_data_file:
                client_dict: Dict[Any] = json.dump(
                    client_data, client_data_file, indent=4)
        except json.decoder.JSONDecodeError:
            print("JSON empty")
            return None

        self.clear_matrix_rows()

    def clear_matrix_rows(self):
        pass


if __name__ == "__main__":
    transcalc_gui = TransCalcGui()
    transcalc_gui.root.mainloop()
