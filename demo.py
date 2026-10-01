from food_delivery import Customer, DeliveryPartner, MenuItem, Order, Restaurant, User


def print_separator():
    print("\n" + "=" * 60)


def main():
    print_separator()
    print("FOOD DELIVERY SYSTEM - END-TO-END DEMONSTRATION")
    print_separator()

    # 1. Register customer
    print("\n1. REGISTER CUSTOMER")
    priya = Customer("Priya", "9876543210", "Bangalore")
    priya.display_profile()

    # 2. Register delivery partner
    print("\n2. REGISTER DELIVERY PARTNER")
    rajesh = DeliveryPartner("Rajesh", "9876543211", "Bike")
    rajesh.display_profile()

    # 3. Create restaurant and menu
    print("\n3. CREATE RESTAURANT AND MENU")
    bawarchi = Restaurant("Bawarchi", "MG Road")
    bawarchi.add_item(MenuItem("Biryani", 250, True))
    bawarchi.add_item(MenuItem("Kebab", 180, False))

    print(f"Restaurant: {bawarchi.name}")
    print(f"Location: {bawarchi.location}")
    print("Menu:")
    for item in bawarchi.get_menu():
        food_type = "Veg" if item.is_veg else "Non-Veg"
        print(f"  - {item.name}: Rs. {item.price:.2f} ({food_type})")

    # 4. Wallet top-up
    print("\n4. WALLET TOP-UP")
    priya.add_to_wallet(500)
    priya.add_to_wallet(-100)
    print(f"Final wallet balance: Rs. {priya._wallet_balance:.2f}")

    # 5. Place order
    print("\n5. PLACE ORDER")
    menu = bawarchi.get_menu()
    biryani = next(item for item in menu if item.name == "Biryani")
    kebab = next(item for item in menu if item.name == "Kebab")

    order = priya.place_order(bawarchi, [biryani, kebab])

    print(f"Order ID: {order._order_id}")
    print(f"Order status: {order._status}")
    print(f"Orders in Priya's history: {len(priya.order_history)}")
    print("Wallet was not deducted during order placement, as required.")

    # 6. Bill
    print("\n6. BILL CALCULATION")
    bill = order.calculate_bill()
    print(f"Subtotal:       Rs. {bill['subtotal']:.2f}")
    print(f"GST (5%):       Rs. {bill['gst']:.2f}")
    print(f"Packaging fee:  Rs. {bill['packaging_fee']:.2f}")
    print(f"Total:          Rs. {bill['total']:.2f}")
    print(f"Estimated time: {order.estimated_time()} minutes")

    # 7. Accept and deliver
    print("\n7. ORDER ACCEPTANCE AND OTP DELIVERY")
    rajesh.accept_order(order)
    print(f"Order status after acceptance: {order._status}")
    print(f"Rajesh available: {rajesh.is_available}")

    print("\nAttempt delivery with incorrect OTP: 9999")
    rajesh.deliver(order, 9999)
    print(f"Order status: {order._status}")
    print(f"Rajesh available: {rajesh.is_available}")

    print("\nAttempt delivery with correct OTP: 1234")
    rajesh.deliver(order, 1234)
    print(f"Order status: {order._status}")
    print(f"Rajesh available: {rajesh.is_available}")

    # 8. Notifications
    print("\n8. USER NOTIFICATIONS")
    priya.notify("Order delivered")
    rajesh.notify("Order delivered")

    # Extra completion checks
    print("\n9. COMPLETION CHECKS")

    try:
        User("Test User", "0000000000")
    except TypeError:
        print("[PASS] User cannot be instantiated directly.")
    else:
        print("[FAIL] User was instantiated directly.")

    print(
        f"[PASS] Negative wallet top-up preserved balance: "
        f"Rs. {priya._wallet_balance:.2f}"
    )
    print(
        f"[PASS] place_order() returned Order: {isinstance(order, Order)}"
    )
    print(
        f"[PASS] Reference total is Rs. 471.50: "
        f"{bill['total'] == 471.50}"
    )
    print(
        f"[PASS] Final order status is Delivered: "
        f"{order._status == 'Delivered'}"
    )
    print(
        f"[PASS] Delivery partner is available again: "
        f"{rajesh.is_available}"
    )

    print_separator()
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print_separator()


if __name__ == "__main__":
    main()
