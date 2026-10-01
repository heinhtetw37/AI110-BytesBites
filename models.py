class Customer:
    """Represents the app's user, tracking name and past purchase history."""

    def __init__(self, name: str):
        self.name = name
        self.purchase_history: list[Transaction] = []

    def add_purchase(self, transaction: Transaction):
        self.purchase_history.append(transaction)

    def get_purchase_history(self) -> list[Transaction]:
        return list(self.purchase_history)


class FoodItem:
    """Represents an individual product offered for sale."""

    def __init__(self, name: str, price: float, category: str, popularity_rating: float):
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def __repr__(self):
        return f"FoodItem({self.name!r}, {self.price}, {self.category!r}, {self.popularity_rating})"


class Menu:
    """Manages the full collection of available FoodItems."""

    def __init__(self):
        self.items: list[FoodItem] = []

    def add_item(self, item: FoodItem):
        self.items.append(item)

    def filter_by_category(self, category: str) -> list[FoodItem]:
        return [item for item in self.items if item.category == category]

    def filter_by_price_range(self, min_price: float, max_price: float) -> list[FoodItem]:
        # Returns items priced within [min_price, max_price], inclusive.
        return [item for item in self.items if min_price <= item.price <= max_price]

    def sort_by_price(self, ascending: bool = True) -> list[FoodItem]:
        # Returns items ordered by price; cheapest first when ascending=True.
        return sorted(self.items, key=lambda item: item.price, reverse=not ascending)

    def sort_by_popularity(self, descending: bool = True) -> list[FoodItem]:
        # Returns items ordered by popularity_rating; most popular first when descending=True.
        return sorted(self.items, key=lambda item: item.popularity_rating, reverse=descending)

    def get_all_items(self) -> list[FoodItem]:
        # Returns every item currently in the menu, unfiltered and unsorted.
        return list(self.items)


class Transaction:
    """Represents a single purchase: the selected items and their total cost."""

    def __init__(self, selected_items: list[FoodItem] | None = None):
        self.selected_items = list(selected_items) if selected_items is not None else []

    def compute_total(self) -> float:
        return round(sum(item.price for item in self.selected_items), 2)

    def add_item(self, item: FoodItem):
        # Adds a single item to this transaction's selected items.
        self.selected_items.append(item)

    def remove_item(self, item: FoodItem):
        # Removes a single item from this transaction's selected items.
        self.selected_items.remove(item)

    def get_item_count(self) -> int:
        # Returns how many items are selected in this transaction.
        return len(self.selected_items)

    def __repr__(self):
        return f"Transaction({self.selected_items!r})"


if __name__ == "__main__":
    # --- Create a small sample menu ---
    burger = FoodItem("Spicy Burger", 7.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.8)
    salad = FoodItem("Garden Salad", 5.49, "Entrees", 4.2)
    fries = FoodItem("Curly Fries", 3.25, "Sides", 4.8)

    menu = Menu()
    for item in (burger, soda, salad, fries):
        menu.add_item(item)

    print("All menu items:", menu.get_all_items())
    print("Entrees only:", menu.filter_by_category("Entrees"))
    print("Items $3-$6:", menu.filter_by_price_range(3.00, 6.00))
    print("Sorted by price (asc):", menu.sort_by_price())
    print("Sorted by popularity (desc):", menu.sort_by_popularity())

    assert menu.filter_by_category("Drinks") == [soda]
    assert menu.filter_by_price_range(3.00, 6.00) == [salad, fries]
    assert menu.sort_by_price()[0] is soda
    assert menu.sort_by_popularity()[0] is fries

    # --- Build and inspect a transaction ---
    order = Transaction([burger, soda])
    print("Order item count:", order.get_item_count())
    print("Order total:", order.compute_total())

    order.add_item(salad)
    print("After adding salad, item count:", order.get_item_count())
    print("New total:", order.compute_total())

    order.remove_item(soda)
    print("After removing soda, item count:", order.get_item_count())
    print("Final total:", order.compute_total())

    assert order.get_item_count() == 2
    assert order.compute_total() == 13.48

    # --- Attach the order to a customer ---
    customer = Customer("Alex")
    customer.add_purchase(order)

    second_order = Transaction([fries])
    customer.add_purchase(second_order)

    print("Customer purchase history:", customer.get_purchase_history())
    assert customer.get_purchase_history() == [order, second_order]

    print("All smoke tests passed.")
