import json
import os

inventory_file = 'inventory.json'


if not os.path.exists(inventory_file):
    with open(inventory_file, 'w') as f:
        json.dump([], f)  


history_stack = []


def load_inventory():
    with open(inventory_file, 'r') as f:
        return json.load(f)


def save_inventory(inventory):
    with open(inventory_file, 'w') as f:
        json.dump(inventory, f, indent=4)


def add_item():
    inventory = load_inventory()
    history_stack.append(inventory.copy())
    print("\n")
    print("** Adding an item will take approximately 1 to 2 minutes **")
    print("** Please make sure all data fields are correct, items can only be updated retroactively, not deleted **")
    print("\n")
    print("ADD ITEM:")
    name = input("Enter item name: ")
    sku = input("Enter item SKU (must be unique): ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    threshold = int(input("Enter low stock threshold: "))

    for item in inventory:
        if item['sku'] == sku:
            print("Error: SKU must be unique.")
            history_stack.pop()  
            return

    inventory.append({
        'name': name,
        'sku': sku,
        'quantity': quantity,
        'price': price,
        'low_stock_threshold': threshold
    })
    save_inventory(inventory)
    print("Item added successfully!")


def update_item():
    inventory = load_inventory()
    history_stack.append(inventory.copy())
    sku = input("Enter the SKU of the item to update: ")

    for item in inventory:
        if item['sku'] == sku:
            print("Updating item:", item)
            item['name'] = input("Enter new name (leave blank to keep current): ") or item['name']
            quantity = input("Enter new quantity (leave blank to keep current): ")
            item['quantity'] = int(quantity) if quantity else item['quantity']
            price = input("Enter new price (leave blank to keep current): ")
            item['price'] = float(price) if price else item['price']
            threshold = input("Enter new low stock threshold (leave blank to keep current): ")
            item['low_stock_threshold'] = int(threshold) if threshold else item['low_stock_threshold']
            save_inventory(inventory)
            print("Item updated successfully!")
            return
    print("Item not found.")
    history_stack.pop()  


def view_all_inventory():
    inventory = load_inventory()
    if inventory:
        print("All Inventory Items:")
        for item in inventory:
            print(f"Name: {item['name']}, SKU: {item['sku']}, Quantity: {item['quantity']}, Price: ${item['price']}, Low Stock Threshold: {item['low_stock_threshold']}")
    else:
        print("No items in inventory.")


def view_low_stock():
    inventory = load_inventory()
    low_stock_items = [item for item in inventory if item['quantity'] < item['low_stock_threshold']]
    if low_stock_items:
        print("Low Stock Items:")
        for item in low_stock_items:
            print(f"Name: {item['name']}, SKU: {item['sku']}, Quantity: {item['quantity']}")
    else:
        print("All items are sufficiently stocked.")


def view_not_low_stock():
    inventory = load_inventory()
    not_low_stock_items = [item for item in inventory if item['quantity'] >= item['low_stock_threshold']]
    if not_low_stock_items:
        print("Items Not Low in Stock:")
        for item in not_low_stock_items:
            print(f"Name: {item['name']}, SKU: {item['sku']}, Quantity: {item['quantity']}")
    else:
        print("No items meet the criteria for sufficient stock.")


def search_item():
    inventory = load_inventory()
    search_query = input("Enter SKU or part of the item name to search: ").lower()
    found_items = [item for item in inventory if search_query in item['sku'].lower() or search_query in item['name'].lower()]
    if found_items:
        print("Search Results:")
        for item in found_items:
            print(f"Name: {item['name']}, SKU: {item['sku']}, Quantity: {item['quantity']}, Price: ${item['price']}, Low Stock Threshold: {item['low_stock_threshold']}")
    else:
        print("No items found matching the search criteria.")


def undo_last_operation():
    if not history_stack:
        print("No actions to undo.")
        return
    confirm = input("Are you sure you want to undo the last operation? (y/n): ").strip().lower()
    if confirm == 'y':
        # Revert to the last saved state
        last_state = history_stack.pop()
        save_inventory(last_state)
        print("Undo successful! Inventory reverted to the previous state.")
    else:
        print("Undo canceled.")


def welcome_message():
    print("\n")
    print("Welcome to the Inventory Management System!")
    print("This tool helps store owners and administrators manage product inventory.")
    print("Features include adding items, updating quantities, checking low stock, viewing items, searching, and undoing recent actions.")
    print("Press 'b' during updates to go back to the previous state.")
    print("Let's get started!\n")


def view_inventory():
    inventory = load_inventory()
    if not inventory:
        print("No items in inventory.")
        return
    print("\nView Inventory - Filter Options")
    print("1. View All")
    print("2. View Low Stock Items Only")
    print("3. View Sufficently Stocked Items")
    filter_choice = input("Choose an option (1/2/3): ")
    if filter_choice == '2':
        items = [item for item in inventory if item['quantity'] < item['low_stock_threshold']]
        print("Low Stock Items:")
    elif filter_choice == '3':
        items = [item for item in inventory if item['quantity'] >= item['low_stock_threshold']]
        print("Sufficently Stocked Items:")
    else:
        items = inventory
        print("All Inventory Items:")
    if items:
        for item in items:
            print(f"Name: {item['name']}, SKU: {item['sku']}, Quantity: {item['quantity']}, Price: ${item['price']}, Low Stock Threshold: {item['low_stock_threshold']}")
    else:
        print("No items match the selected criteria.")


def main_menu():
    welcome_message()
    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. Update Item")
        print("3. View Inventory")
        print("4. Search Item")
        print("5. Undo Last Operation (Press 'b')")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            add_item()
        elif choice == '2':
            update_item()
        elif choice == '3':
            view_inventory()
        elif choice == '4':
            search_item()
        elif choice == '5' or choice.lower() == 'b':
            undo_last_operation()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main_menu()