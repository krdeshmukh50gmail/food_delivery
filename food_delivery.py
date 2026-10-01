from abc import ABC, abstractmethod


class User(ABC):
    def __init__(self, name, phone):
        self._name = name
        self._phone = phone
        self._wallet_balance = 0

    @abstractmethod
    def notify(self, message):
        pass

    @abstractmethod
    def display_profile(self):
        pass

    def add_to_wallet(self, amount):
        if amount < 0:
            print("Wallet top-up rejected: amount cannot be negative.")
            return False

        self._wallet_balance += amount
        print(f"Wallet topped up by Rs. {amount:.2f}.")
        return True


class Customer(User):
    def __init__(self, name, phone, address):
        super().__init__(name, phone)
        self.address = address
        self.order_history = []

    def notify(self, message):
        print(f"[Customer Notification - {self._name}] {message}")

    def display_profile(self):
        print("\n--- Customer Profile ---")
        print(f"Name: {self._name}")
        print(f"Phone: {self._phone}")
        print(f"Wallet Balance: Rs. {self._wallet_balance:.2f}")
        print(f"Address: {self.address}")

    def place_order(self, restaurant, items):
        if not restaurant.is_open():
            raise ValueError("Restaurant is currently closed.")

        order = Order(items)
        self.order_history.append(order)
        return order


class DeliveryPartner(User):
    def __init__(self, name, phone, vehicle):
        super().__init__(name, phone)
        self.vehicle = vehicle
        self.is_available = True
        self.rating = 0.0

    def notify(self, message):
        print(f"[Delivery Partner Notification - {self._name}] {message}")

    def display_profile(self):
        print("\n--- Delivery Partner Profile ---")
        print(f"Name: {self._name}")
        print(f"Phone: {self._phone}")
        print(f"Vehicle: {self.vehicle}")
        print(f"Available: {'Yes' if self.is_available else 'No'}")
        print(f"Rating: {self.rating:.1f}")

    def accept_order(self, order):
        if not self.is_available:
            raise ValueError("Delivery partner is not available.")

        if order._status != "Placed":
            raise ValueError("Only a placed order can be accepted.")

        order.update_status("Accepted")
        self.is_available = False
        print(f"{self._name} accepted {order._order_id}.")

    def deliver(self, order, otp):
        if order._status != "Accepted":
            print("Delivery failed: order must be in Accepted status.")
            return False

        if not order.verify_otp(otp):
            print("Delivery failed: incorrect OTP.")
            return False

        order.update_status("Delivered")
        self.is_available = True
        print(f"{order._order_id} delivered successfully.")
        return True


class MenuItem:
    def __init__(self, name, price, is_veg):
        self.name = name
        self.price = price
        self.is_veg = bool(is_veg)


class Restaurant:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._menu = []

    def add_item(self, menu_item):
        self._menu.append(menu_item)

    def get_menu(self):
        return self._menu

    def is_open(self):
        return True


class Order:
    _next_order_number = 1
    VALID_STATUSES = {"Placed", "Accepted", "Delivered"}

    def __init__(self, items):
        self._order_id = f"ORD{Order._next_order_number}"
        Order._next_order_number += 1
        self._items = list(items)
        self._status = "Placed"
        self._otp = 1234

    def calculate_bill(self):
        subtotal = sum(item.price for item in self._items)
        gst = subtotal * 0.05
        packaging_fee = 20
        total = subtotal + gst + packaging_fee

        return {
            "subtotal": subtotal,
            "gst": gst,
            "packaging_fee": packaging_fee,
            "total": total,
        }

    def estimated_time(self):
        return 30

    def update_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            raise ValueError(
                f"Invalid status. Use one of: {', '.join(sorted(self.VALID_STATUSES))}"
            )

        current_status = self._status
        allowed_transitions = {
            "Placed": {"Accepted"},
            "Accepted": {"Delivered"},
            "Delivered": set(),
        }

        if new_status not in allowed_transitions[current_status]:
            raise ValueError(
                f"Invalid status transition: {current_status} -> {new_status}"
            )

        self._status = new_status

    def verify_otp(self, otp):
        return otp == self._otp
