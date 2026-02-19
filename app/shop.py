from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import Dict

from .utils import Location, money_fmt


@dataclass(frozen=True)
class Shop:
    """Shop with a location and a price list for products."""

    name: str
    location: Location
    products: Dict[str, float]

    def can_fulfill_cart(self, cart: Dict[str, int]) -> bool:
        """Return True if the shop has all products from cart."""
        return all(product_name in self.products for product_name in cart)

    def cart_cost(self, cart: Dict[str, int]) -> float:
        """Calculate total cost of the cart in this shop (assumes all products exist)."""
        total_cost = 0.0
        for product_name, quantity in cart.items():
            unit_price = float(self.products[product_name])
            total_cost += quantity * unit_price
        return total_cost

    def print_receipt(self, customer_name: str, cart: Dict[str, int]) -> None:
        """Print purchase receipt using current datetime."""
        now_value = datetime.datetime.now()
        now_str = now_value.strftime("%m/%d/%Y %H:%M:%S")

        print("\nDate:", now_str)
        print(f"Thanks, {customer_name}, for your purchase!")
        print("You have bought:")

        total_cost = 0.0
        for product_name, quantity in cart.items():
            unit_price = float(self.products[product_name])
            item_total = quantity * unit_price
            total_cost += item_total

            plural_name = f"{product_name}s"
            print(
                f"{quantity} {plural_name} for {money_fmt(item_total)} dollars"
            )

        print(f"Total cost is {money_fmt(total_cost)} dollars")
        print("See you again!\n")
