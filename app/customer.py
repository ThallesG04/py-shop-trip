from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from .car import Car
from .shop import Shop
from.utils import Location, euclidean_distance_km


@dataclass
class Customer:
    name: str
    product_cart: Dict[str, int]
    location: Location
    money: float
    car: Car
    # Representa um cliente

    def trip_cost_to_shop(
            self,
            shop: Shop,
            fuel_price: float
) -> Optional[float]:
        if not shop.can_fulfill_cart(self.product_cart):
            return None

        distance_one_way = euclidean_distance_km(
            self.location,
            shop.location
        )
        fuel_one_way = self.car.fuel_cost_for_distance(
            distance_one_way,
            fuel_price
        )

        product_cost = shop.cart_cost(self.product_cart)

        total = (2.0 * fuel_one_way) + product_cost
        return total
    # Calcula o custo total, ir a loja, comprar e voltar

    def choose_cheapest_shop(
            self,
            shops: Tuple[Shop, ...],
            fuel_price: float
) -> Tuple[Optional[Shop], Optional[float]]:
        best_shop: Optional[Shop] = None
        best_cost: Optional[float] = None

        for shop in shops:
            cost = self.trip_cost_to_shop(shop, fuel_price)
            if cost is None:
                continue

            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_shop = shop

        return best_shop, best_cost
    # Avalia todas as lojas e retorna a mais barata e o custo total

    def perform_purchase_trip(
            self,
            shop: Shop,
            total_cost: float
) -> None:
        home_location = self.location
        self.location = shop.location

        shop.print_receipt(self.name, self.product_cart)
        self.money -= total_cost

        self.location = home_location
        # Executa a viagem: vai até a loja, imprime recibo,
        # volta pra casa,e atualiza o dinheiro do cliente.
