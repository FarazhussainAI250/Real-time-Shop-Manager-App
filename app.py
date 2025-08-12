import streamlit as st
from datetime import datetime
import uuid

# ------------------ Models ------------------
class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity):
        self.stock += quantity


class Customer:
    def __init__(self, customer_id, name, phone):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.cart = []

    def add_to_cart(self, product):
        self.cart.append(product)


class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.products = customer.cart
        self.total = sum(p.price for p in self.products)

    def get_receipt_text(self, store_name):
        receipt = f"Store: {store_name}\n"
        receipt += f"Customer: {self.customer.name} | Phone: {self.customer.phone}\n"
        receipt += f"Order ID: {self.order_id}\n\n"
        receipt += "Items:\n"
        for item in self.products:
            receipt += f"- {item.name}: Rs. {item.price}\n"
        receipt += f"\nTotal: Rs. {self.total}"
        return receipt
    


st.markdown("""
<style>
/* Background Image */
.stApp {
    background-image: url("https://t3.ftcdn.net/jpg/02/41/43/18/360_F_241431868_8DFQpCcmpEPVG0UvopdztOAd4a6Rqsoo.jpg");
    background-size: cover;
    background-position: right;
    background-repeat: no-repeat;
}

/* Top-right Header */
#top-header {
    position: fixed;
    top: 80px;  /* 👈 Yahi line hai jo update karni thi */
    right: 20px;
    background-color: rgba(0,0,0,0.5);
    padding: 14px 18px;
    border-radius: 8px;
    color: white;
    font-size: 18px;
    font-weight: bold;
    z-index: 90;
}

/* Bottom-left Footer */
#bottom-footer {
    position: fixed;
    bottom: 10px;
    left:300px;
    background-color: rgba(0,0,0,0.5);
    padding: 6px 14px;
    border-radius: 6px;
    color: white;
    font-size: 14px;
    z-index: 100;
}
</style>

<div id="top-header">Respected Sir Shahzaib & Sir Ali Hamza</div>
<div id="bottom-footer">Developed by Faraz Hussain</div>
""", unsafe_allow_html=True)


# ------------------ In-Memory Data ------------------
if "products" not in st.session_state:
    st.session_state.products = []
if "current_customer" not in st.session_state:
    st.session_state.current_customer = None
if "order_receipt" not in st.session_state:
    st.session_state.order_receipt = ""

# ------------------ Sidebar (Left Layout) ------------------
st.sidebar.header("Jani Mart - Shop Control")

st.sidebar.subheader("Add Product")
product_name = st.sidebar.text_input("Product Name")
product_price = st.sidebar.number_input("Price", min_value=1)
product_stock = st.sidebar.number_input("Stock Quantity", min_value=1)

if st.sidebar.button("Add Product"):
    product = Product(str(uuid.uuid4()), product_name, product_price, product_stock)
    st.session_state.products.append(product)
    st.success(f"{product.name} added to inventory")

# ------------------ Main Area ------------------


st.markdown("""
<h1 style='color:black; font-size: 50px; font-weight: bold;'>
    🛒 Jani Mart - Real-time Shop Manager
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style='color: black; font-size: 20px; font-weight: bold;'>
    Customer Info
</h2>
""", unsafe_allow_html=True)
cust_name = st.text_input("Customer Name")
cust_phone = st.text_input("Phone Number")
cust_id = st.text_input("Customer ID")
if st.button("Start Shopping"):
    if cust_name and cust_phone:
        new_cust = Customer(str(uuid.uuid4()), cust_name, cust_phone)
        st.session_state.current_customer = new_cust
        st.success("Customer added. You can now add products to cart.")
    else:
        st.warning("Please enter both name and phone.")

if st.session_state.current_customer:
    st.subheader("Add to Cart")
    product_options = [f"{p.name} (Rs. {p.price}, Stock: {p.stock})" for p in st.session_state.products if p.stock > 0]
    selected_product = st.selectbox("Select Product", options=product_options)

    if st.button("Add to Cart"):
        selected_index = product_options.index(selected_product)
        selected_item = st.session_state.products[selected_index]
        if selected_item.stock > 0:
            selected_item.update_stock(-1)
            st.session_state.current_customer.add_to_cart(selected_item)
            st.success(f"{selected_item.name} added to cart. Remaining stock: {selected_item.stock}")
        else:
            st.warning("Out of stock")

    # ------------------ Show Cart ------------------
    if st.session_state.current_customer.cart:
        st.subheader("🛒 Current Cart")
        for p in st.session_state.current_customer.cart:
            st.write(f"{p.name} - Rs. {p.price}")

        if st.button("Generate Total Bill & Receipt"):
            order = Order(str(uuid.uuid4())[:8], st.session_state.current_customer)
            receipt_text = order.get_receipt_text("Jani Mart")
            st.session_state.order_receipt = receipt_text

    if st.session_state.order_receipt:
        st.subheader("🧾 Receipt")
        st.text(st.session_state.order_receipt)
        st.download_button("Download Receipt", st.session_state.order_receipt, file_name="receipt.txt")







