"""
Inventory Management System

A simple system to manage stock inventory with functionality to add, remove,
and track items along with their quantities.
"""

import json
from datetime import datetime
from typing import Dict, List, Union, Optional


class InventorySystem:
    def __init__(self):
        """Initialize the inventory system with an empty stock."""
        self.stock_data: Dict[str, int] = {}


    def add_item(self, item: str = "default", qty: int = 0, logs: Optional[List[str]] = None) -> None:
        """
        Add an item to the inventory with the specified quantity.

        Args:
            item: Name of the item to add
            qty: Quantity to add (can be negative for removals)
            logs: Optional list to track operation logs
        """
        if not item or not isinstance(item, str) or not isinstance(qty, int):
            return

        if logs is None:
            logs = []

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        logs.append(f"{datetime.now()}: Added {qty} of {item}")


    def remove_item(self, item: str, qty: int) -> bool:
        """
        Remove a quantity of an item from inventory.

        Args:
            item: Name of the item to remove
            qty: Quantity to remove

        Returns:
            bool: True if removal was successful, False otherwise
        """
        try:
            if item in self.stock_data:
                self.stock_data[item] -= qty
                if self.stock_data[item] <= 0:
                    del self.stock_data[item]
                return True
            return False
        except KeyError:
            return False


    def get_qty(self, item: str) -> int:
        """
        Get the current quantity of an item.

        Args:
            item: Name of the item to check

        Returns:
            int: Current quantity of the item (0 if not found)
        """
        return self.stock_data.get(item, 0)


    def load_data(self, file: str = "inventory.json") -> bool:
        """
        Load inventory data from a JSON file.

        Args:
            file: Path to the JSON file

        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            with open(file, "r", encoding='utf-8') as f:
                self.stock_data = json.loads(f.read())
            return True
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            return False


    def save_data(self, file: str = "inventory.json") -> bool:
        """
        Save inventory data to a JSON file.

        Args:
            file: Path to save the JSON file

        Returns:
            bool: True if saving was successful, False otherwise
        """
        try:
            with open(file, "w", encoding='utf-8') as f:
                json.dump(self.stock_data, f, indent=4)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False


    def print_data(self) -> None:
        """Print a report of all items in inventory."""
        print("Items Report")
        for item, quantity in self.stock_data.items():
            print(f"{item} -> {quantity}")


    def check_low_items(self, threshold: int = 5) -> List[str]:
        """
        Check for items with quantity below the threshold.

        Args:
            threshold: Minimum quantity threshold

        Returns:
            List[str]: List of items below the threshold
        """
        return [item for item, qty in self.stock_data.items() if qty < threshold]


def main():
    """Main function to demonstrate the inventory system functionality."""
    inventory = InventorySystem()
    
    # Add some test items
    inventory.add_item("apple", 10)
    inventory.add_item("banana", 3)
    
    # Demonstrate removal
    inventory.remove_item("apple", 3)
    
    # Check quantities
    print(f"Apple stock: {inventory.get_qty('apple')}")
    print(f"Low items: {inventory.check_low_items()}")
    
    # Save and load demonstration
    inventory.save_data()
    inventory.load_data()
    inventory.print_data()


if __name__ == "__main__":
    main()