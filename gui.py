import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from api import fetch_exchange_rates
from converter import get_exchange_rate, convert_currency
from tkinter import PhotoImage
import os

def convert_currency_gui():
    def update_exchange_rate():
        try:
            base_currency = base_currency_combo.get().upper()
            target_currency = target_currency_combo.get().upper()

            if base_currency and target_currency:
                rates = fetch_exchange_rates(base_currency)
                exchange_rate = get_exchange_rate(target_currency, rates)
                exchange_rate_label.config(text=f"1 {base_currency} = {exchange_rate:.2f} {target_currency}")

                # Update converted amount dynamically
                amount = float(base_amount_entry.get()) if base_amount_entry.get() else 0
                converted_amount = convert_currency(amount, exchange_rate) if amount != 0 else 0
                target_amount_entry.configure(state="normal")
                target_amount_entry.delete(0, END)
                target_amount_entry.insert(0, f"{converted_amount:.2f}" if converted_amount != 0 else "0")
                target_amount_entry.configure(state="readonly")
            else:
                exchange_rate_label.config(text="Select both currencies to see the exchange rate.")
        except Exception as e:
            exchange_rate_label.config(text=f"Error: {e}")
            target_amount_entry.configure(state="normal")
            target_amount_entry.delete(0, END)
            target_amount_entry.insert(0, "0")
            target_amount_entry.configure(state="readonly")

    def swap_currencies():
        base_currency = base_currency_combo.get()
        target_currency = target_currency_combo.get()
        base_currency_combo.set(target_currency)
        target_currency_combo.set(base_currency)
        update_exchange_rate()
    
    root = ttk.Window(themename="litera")
    '''
    # Grid debug
    
    def add_grid_debug(root):
        for row in range(3):  # Adjust range based on your layout
            for col in range(3):  # Adjust range based on your layout
                frame = ttk.Frame(root, borderwidth=1, relief="solid")
                frame.grid(row=row, column=col, sticky="nsew")
    add_grid_debug(root)
    '''
    root.title("Currency Converter")

    # Center the window on the screen
    window_width = 500
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int((screen_height - window_height) / 2)
    position_right = int((screen_width - window_width) / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # Set app icon
    # Get the absolute path to the directory where the script is located
    script_dir = os.path.abspath(os.path.dirname(__file__))

    # Combine the directory path with the icon file name
    icon_path = os.path.join(script_dir, "assets/icon.png")
    try:
        root.iconphoto(False, ttk.PhotoImage(file=icon_path))
    except Exception as e:
        print(f"Failed to set icon: {e}")

    # Configure the grid system
    root.columnconfigure((0,1,2), weight=1)
    # Fetch list of currencies for the comboboxes
    try:
        sample_rates = fetch_exchange_rates("USD")  # Use USD to get a sample list of currencies
        currency_list = sorted(sample_rates["rates"].keys())
    except Exception as e:
        currency_list = []
        print(f"Error fetching currency list: {e}")

    # Exchange Rate Label
    exchange_rate_label = ttk.Label(root, text="", font=("Arial", 12))
    exchange_rate_label.grid(row=0, column=1, columnspan=1, pady=10)

    # Base Currency Row in Frame
    base_frame = ttk.Frame(root)
    base_frame.grid(row=1, column=1, sticky="nsew")
    root.rowconfigure(3, weight=1)
    root.columnconfigure(1, weight=1)  # Ensures the column stretches
    base_frame.columnconfigure(0, weight=1)
    base_frame.columnconfigure(1, weight=1)

    base_amount_entry = ttk.Entry(base_frame, width=15)
    base_amount_entry.insert(0, "0")
    base_amount_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    base_amount_entry.bind("<KeyRelease>", lambda e: update_exchange_rate())

    base_currency_combo = ttk.Combobox(base_frame, values=currency_list, width=5)
    base_currency_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    base_currency_combo.set("USD")  # Default value
    base_currency_combo.bind("<<ComboboxSelected>>", lambda e: update_exchange_rate())

    # Target Currency Row in Frame
    target_frame = ttk.Frame(root)
    target_frame.grid(row=2, column=1, sticky="nsew")
    root.rowconfigure(3, weight=1)
    target_frame.columnconfigure(0, weight=1)
    target_frame.columnconfigure(1, weight=1)

    target_amount_entry = ttk.Entry(target_frame, width=15)
    target_amount_entry.insert(0, "0")
    target_amount_entry.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    target_amount_entry.configure(state="readonly")

    target_currency_combo = ttk.Combobox(target_frame, values=currency_list, width=5)
    target_currency_combo.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    target_currency_combo.set("EUR")  # Default value
    target_currency_combo.bind("<<ComboboxSelected>>", lambda e: update_exchange_rate())


    # Swap Button
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "swap_btn.png")
    swap_image = PhotoImage(file=image_path).subsample(20, 15)
    from tkinter import Button

    # Swap Button
    swap_button = Button(root, image=swap_image, command=swap_currencies, bd=0, highlightthickness=0)
    swap_button.grid(row=1, column=2, rowspan=2, padx=5, pady=5, sticky="w")




    update_exchange_rate()  # Initialize exchange rate display

    root.mainloop()