from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from .utils import Location, money_fmt


@dataclass(frozen=True)
class Shop:
    name: str
    location: Location
    products: Dict[str, float]
    # Representa uma loja

    def can_fulfill_cart(
            self,
            cart: Dict[str, int],
    ) -> bool:
        return all(
            product in self.products for product in cart
        )
    # Verifica se a loja vende todos os produtos do carrinho

    def cart_cost(
            self,
            cart: Dict[str, int],
    ) -> float:
        total = 0.0
        for product , qty in cart.items():
            unit_price = float(self.products[product])
            total += qty * unit_price
        return total
    # Calcula o custo total dos produtos do carrinho na loja

    def print_receipt(
            self,
            customer_name: str,
            cart: Dict[str, int],
    ) -> None:
        now_str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        print("\nDate:", now_str)
        print(f"Thanks, {customer_name}, for your purchase!")
        print("You have bought:")

        total = 0.0
        for product, qty in cart.items():
            unit_price = float(self.products[product])
            item_total = qty * unit_price
            total += item_total

            plural = product + "s"
            print(
                f"{qty} {plural} for {money_fmt(item_total)} dollars"
            )

        print(f"Total cost is {money_fmt(total)} dollars.")
        print("See you again!\n")
        # Imprime o recibo com data/hora atual

