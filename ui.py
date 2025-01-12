from tkinter import *
from tkinter import messagebox
from btc_agent import fetch_and_store_btc_price

window = Tk()
window.title("Welcome to your personal btc ai agent")
window.geometry('800x600')
window.resizable(False, False)
window.iconbitmap('btc.ico')
window.configure(bg='black', padx=54, pady=54)

def update_price_label():
    try:
        price = fetch_and_store_btc_price()
        print(f"Debug - Received price: {price}")  # Debug print
        
        if price is not None:  # Check for None specifically
            lbl_btc_price.configure(text=f"Current BTC Price: {price}")
        else:
            lbl_btc_price.configure(text="Unable to fetch price")
    except Exception as e:
        print(f"Debug - Error: {str(e)}")  # Debug print
        lbl_btc_price.configure(text=f"Error: {str(e)}")
        messagebox.showerror("Error", str(e))

# Labels
lbl = Label(window, text="Welcome to your personal $BTC AI agent", 
            font=("Arial Bold", 20), bg='black', fg='white', pady=16, padx=16)
lbl.grid(column=0, row=0, columnspan=2, pady=16, padx=16)

lbl_btc_price = Label(window, text="Loading Bitcoin price...", font=("Arial Bold", 16), bg='black', fg='white', pady=16, padx=16)
lbl_btc_price.grid(column=0, row=1, pady=16, padx=16)

# Buttons
btn_get_bt_price = Button(window, text="Get BTC Price", font=("Arial Bold", 16), bg='black', fg='black', pady=16, padx=16, command=update_price_label)
btn_get_bt_price.grid(column=1, row=1, pady=16, padx=16)

# Initial price update
update_price_label()

window.mainloop()
