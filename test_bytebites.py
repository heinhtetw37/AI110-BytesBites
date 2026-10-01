import unittest

from models import Customer, FoodItem, Menu, Transaction


class TestMenuAndTransaction(unittest.TestCase):
    def setUp(self):
        self.burger = FoodItem("Spicy Burger", 7.99, "Entrees", 4.5)
        self.soda = FoodItem("Large Soda", 2.50, "Drinks", 3.8)
        self.salad = FoodItem("Garden Salad", 5.49, "Entrees", 4.2)
        self.fries = FoodItem("Curly Fries", 3.25, "Sides", 4.8)

        self.menu = Menu()
        for item in (self.burger, self.soda, self.salad, self.fries):
            self.menu.add_item(item)

    def test_filter_by_category(self):
        self.assertEqual(self.menu.filter_by_category("Entrees"), [self.burger, self.salad])
        self.assertEqual(self.menu.filter_by_category("Drinks"), [self.soda])
        self.assertEqual(self.menu.filter_by_category("Desserts"), [])

    def test_filter_by_price_range(self):
        for min_price, max_price, expected in [
            (3.25, 5.49, [self.salad, self.fries]),  # inclusive boundaries
            (2.50, 2.50, [self.soda]),  # single exact match
            (100.00, 200.00, []),  # no matches
        ]:
            with self.subTest(min_price=min_price, max_price=max_price):
                self.assertEqual(self.menu.filter_by_price_range(min_price, max_price), expected)

    def test_sort_by_price(self):
        ascending = self.menu.sort_by_price()
        self.assertEqual(ascending, [self.soda, self.fries, self.salad, self.burger])

        descending = self.menu.sort_by_price(ascending=False)
        self.assertEqual(descending, [self.burger, self.salad, self.fries, self.soda])

    def test_sort_by_popularity(self):
        descending = self.menu.sort_by_popularity()
        self.assertEqual(descending, [self.fries, self.burger, self.salad, self.soda])

        ascending = self.menu.sort_by_popularity(descending=False)
        self.assertEqual(ascending, [self.soda, self.salad, self.burger, self.fries])

    def test_sort_on_empty_menu(self):
        empty_menu = Menu()
        self.assertEqual(empty_menu.sort_by_price(), [])
        self.assertEqual(empty_menu.sort_by_popularity(), [])

    def test_get_all_items_returns_copy(self):
        items = self.menu.get_all_items()
        items.append(FoodItem("Hacked Item", 0.01, "Hacks", 0.0))

        self.assertEqual(len(self.menu.get_all_items()), 4)

    def test_calculate_total_with_multiple_items(self):
        burger = FoodItem("Burger", 10.00, "Entrees", 4.5)
        soda = FoodItem("Soda", 5.00, "Drinks", 3.8)

        order = Transaction([burger, soda])

        self.assertEqual(order.compute_total(), 15.00)

    def test_order_total_is_zero_when_empty(self):
        order = Transaction()

        self.assertEqual(order.compute_total(), 0.0)
        self.assertEqual(order.get_item_count(), 0)

    def test_order_total_is_zero_after_removing_all_items(self):
        order = Transaction([self.burger, self.soda])

        order.remove_item(self.burger)
        order.remove_item(self.soda)

        self.assertEqual(order.compute_total(), 0.0)
        self.assertEqual(order.get_item_count(), 0)

    def test_compute_total_with_float_rounding(self):
        item_a = FoodItem("Item A", 0.10, "Misc", 1.0)
        item_b = FoodItem("Item B", 0.20, "Misc", 1.0)

        order = Transaction([item_a, item_b])

        self.assertEqual(order.compute_total(), 0.30)

    def test_remove_item_not_in_transaction_raises(self):
        order = Transaction([self.burger])

        with self.assertRaises(ValueError):
            order.remove_item(self.soda)

    def test_get_item_count_tracks_add_and_remove(self):
        order = Transaction([self.burger, self.soda])
        self.assertEqual(order.get_item_count(), 2)

        order.add_item(self.salad)
        self.assertEqual(order.get_item_count(), 3)

        order.remove_item(self.burger)
        self.assertEqual(order.get_item_count(), 2)


class TestCustomer(unittest.TestCase):
    def test_purchase_history_preserves_order(self):
        customer = Customer("Alex")
        first_order = Transaction([FoodItem("Burger", 10.00, "Entrees", 4.5)])
        second_order = Transaction([FoodItem("Fries", 3.00, "Sides", 4.0)])

        customer.add_purchase(first_order)
        customer.add_purchase(second_order)

        self.assertEqual(customer.get_purchase_history(), [first_order, second_order])

    def test_get_purchase_history_returns_copy(self):
        customer = Customer("Alex")
        order = Transaction([FoodItem("Burger", 10.00, "Entrees", 4.5)])
        customer.add_purchase(order)

        history = customer.get_purchase_history()
        history.append(Transaction())

        self.assertEqual(len(customer.get_purchase_history()), 1)


if __name__ == "__main__":
    unittest.main()
