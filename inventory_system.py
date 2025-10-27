"""
A simple inventory system to add, remove, get, load, print and check
low items in an inventory.
"""
import json
from datetime import datetime
import ast

# global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """Adds an item to the inventory."""
    if logs is None:
        logs = []
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(item, qty):
    """Removes a specified quantity of an item from the inventory."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Item '{item}' does not exist in inventory.")


def get_qty(item):
    """Gets the current quantity of a specific item."""
    return stock_data.get(item, 0)  # Use .get() for safety


def load_data(file="inventory.json"):
    """Loads inventory data from a JSON file."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            return data
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. \
        Starting with empty inventory.")
        return {}


def save_data(file="inventory.json"):
    """Saves the current inventory data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data, indent=4))


def print_data():
    """Prints a report of all items and their quantities."""
    print("Items Report")
    print("-" * 20)
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")
    print("-" * 20)


def check_low_items(threshold=5):
    """Returns a list of items below the specified threshold."""
    result = []
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """Main function to run the inventory system operations."""
    global stock_data
    stock_data = load_data()

    add_item("apple", 10)
    add_item("banana", 5)
    try:
        # invalid types, will now fail gracefully
        add_item(123, "ten")
    except TypeError as e:
        print(f"Error adding item: {e}")

    remove_item("apple", 3)
    remove_item("orange", 1)  # Will print "item does not exist"
    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()

    # Demonstrate loading the saved data
    stock_data = load_data()
    print("\nData after saving and reloading:")
    print_data()

    # Original code was dangerous; fixed by using ast.literal_eval()
    ast.literal_eval("['safe', 'list']")
    print("ast.literal_eval used successfully.")


if __name__ == "__main__":
    main()