class Customer:
    """Represents the app's user, tracking name and past purchase history."""

    def __init__(self, name: str):
        self.name = name
        self.purchase_history: list[Transaction] = []

    def add_transaction(self, transaction: Transaction):
        self.purchase_history.append(transaction)


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


class Transaction:
    """Represents a single purchase: the selected items and their total cost."""

    def __init__(self, selected_items: list[FoodItem] = None):
        self.selected_items = selected_items if selected_items is not None else []

    def compute_total(self) -> float:
        return round(sum(item.price for item in self.selected_items), 2)


if __name__ == "__main__":
    burger = FoodItem("Spicy Burger", 7.99, "Entrees", 4.5)
    soda = FoodItem("Large Soda", 2.50, "Drinks", 3.8)

    menu = Menu()
    menu.add_item(burger)
    menu.add_item(soda)
    assert menu.filter_by_category("Drinks") == [soda]

    order = Transaction([burger, soda])
    assert order.compute_total() == 10.49

    customer = Customer("Alex")
    customer.add_transaction(order)
    assert customer.purchase_history == [order]

    print("All smoke tests passed.")
