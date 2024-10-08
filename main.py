import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import stripe

stripe.api_key = "sk_test_51PyBXd08ctt1MXZ67wyqrIj6jP56aFdGaTkyxi44X8YN51FLIde6ZnrXfPxo4IYl47QfK6rRhp3Eef9qQOKfHYum00mIkt5DF9"

def main():
    app = tk.Tk()
    app.title("Silk Road")
    app.geometry("800x600")
    app.configure(bg="#3498db") 
    return app

app = main()

products = [
    {"Name": "Water Bottle", "price": 999, "img": "water_bottle.png"},
    {"Name": "MacBook", "price": 69999, "img": "macbook.png"},
    {"Name": "Headphones", "price": 15000, "img": "headphones.png"},
    {"Name": "Smartphone", "price": 100000, "img": "smartphone.png"},
    {"Name": "Camera", "price": 90000, "img": "camera.png"},
    {"Name": "Smartwatch", "price":45000, "img": "smartwatch.png"},
    {"Name": "Backpack", "price": 2000, "img": "backpack.png"},
    {"Name": "Tablet", "price": 40000, "img": "tablet.png"},
]

cart = []

def addToCart(product):
    cart.append(product)
    messagebox.showinfo("Cart", f"{product['Name']} added to cart!")

def displayProducts(app, productFrame):
    for idx, product in enumerate(products):
        # Load an image for the product
        img = Image.open(product["img"])
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        labelImage = tk.Label(productFrame, image=photo, bg="#3498db")
        labelImage.image = photo  # Prevent garbage collection
        labelImage.grid(row=idx, column=0, padx=10, pady=10)

        label = tk.Label(productFrame, text=f"{product['Name']} - ₹{product['price']}",
                         font=("Arial", 12), bg="#3498db", fg="white")
        label.grid(row=idx, column=1, padx=10, pady=10)

        button = tk.Button(productFrame, text="Add to Cart", command=lambda p=product: addToCart(p),
                           padx=10, pady=5, bg="#2ecc71", fg="white", font=("Helvetica", 12, "bold"))
        button.grid(row=idx, column=2, padx=10, pady=10)

def viewCart():
    cartWindow = tk.Toplevel(app)
    cartWindow.title("Your Cart")
    cartWindow.geometry("400x300")
    cartWindow.configure(bg="#ecf0f1")

    header = tk.Label(cartWindow, text="Product - Price", font=("Arial", 12, "bold"), bg="#ecf0f1")
    header.grid(row=0, column=0, padx=10, pady=10)

    for idx, item in enumerate(cart):
        itemLabel = tk.Label(cartWindow, text=f"{item['Name']} - ₹{item['price']}", bg="#ecf0f1")
        itemLabel.grid(row=idx + 1, column=0, padx=10, pady=5)

    checkoutButton = ttk.Button(cartWindow, text="Checkout", command=processPayment)
    checkoutButton.grid(row=len(cart) + 1, column=0, pady=10)

def processPayment():
    try:
        totalAmount = sum(item['price'] for item in cart) * 100  # in paise
        stripe.PaymentIntent.create(
            amount=totalAmount,
            currency='inr',
            payment_method_types=['card']
        )
        showSuccessPopup()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def showSuccessPopup():
    popup = tk.Toplevel(app)
    popup.title("Payment Successful")
    popup.geometry("300x150")
    label = tk.Label(popup, text="Your payment was successful!", font=("Arial", 12))
    label.pack(pady=20)
    okButton = tk.Button(popup, text="OK", command=popup.destroy)
    okButton.pack(pady=10)

def setupMenu(app):
    menu = tk.Menu(app)
    app.config(menu=menu)
    fileMenu = tk.Menu(menu)
    menu.add_cascade(label="Exit?", menu=fileMenu)
    fileMenu.add_command(label="Yes", command=app.quit)

    helpMenu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=helpMenu)
    helpMenu.add_command(label="About", command=lambda: messagebox.showinfo("About", "This is an eCommerce app\n\nAuthor: Aarnav"))

def setupStatusBar(app):
    status = tk.Label(app, text="Welcome to Silk Road!", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status.pack(side=tk.TOP, fill=tk.X)

def showLoading():
    loading = tk.Toplevel(app)
    loading.title("Processing Payment")
    loading.geometry("300x100")
    label = tk.Label(loading, text="Processing, please wait...")
    label.pack(pady=20)

    app.after(2000, loading.destroy)

productFrame = tk.Frame(app, bg="#3498db")
productFrame.pack(side=tk.LEFT, padx=20)

cartButton = tk.Button(app, text="View Cart", command=viewCart, padx=10, pady=5, bg="#2980b9", fg="#fff", font=("Arial", 12, "bold"))
cartButton.pack(side=tk.RIGHT, padx=20)

displayProducts(app, productFrame)
setupMenu(app)
setupStatusBar(app)
app.mainloop()
