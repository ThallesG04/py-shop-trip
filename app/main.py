from __future__ import annotations

from typing import Dict, List, Tuple

from .car import Car
from .customer import Customer
from .shop import Shop
from .utils import load_config, money_fmt, money_trim, to_location


def shop_trip() -> None:
    """Run shop trip simulation."""
    config = load_config("config.json")
    fuel_price: float = float(config["FUEL_PRICE"])

    shops_list: List[Shop] = []
    for raw_shop in config["shops"]:
        products = {
            str(key): float(value)
            for key, value in raw_shop["products"].items()
        }
        shops_list.append(
            Shop(
                name=str(raw_shop["name"]),
                location=to_location(raw_shop["location"]),
                products=products,
            )
        )

    shops: Tuple[Shop, ...] = tuple(shops_list)

    customers: List[Customer] = []
    for raw_customer in config["customers"]:
        car_data = raw_customer["car"]
        car = Car(
            brand=str(car_data["brand"]),
            fuel_consumption=float(car_data["fuel_consumption"]),
        )

        cart = {
            str(key): int(value)
            for key, value in raw_customer["product_cart"].items()
        }

        customers.append(
            Customer(
                name=str(raw_customer["name"]),
                product_cart=cart,
                location=to_location(raw_customer["location"]),
                money=float(raw_customer["money"]),
                car=car,
            )
        )

    for customer in customers:
        print(
            f"{customer.name} has "
            f"{money_trim(customer.money)} dollars"
        )

        costs: Dict[str, float] = {}

        for shop in shops:
            trip_cost = customer.trip_cost_to_shop(shop, fuel_price)
            if trip_cost is None:
                continue

            costs[shop.name] = trip_cost
            print(
                f"{customer.name}'s trip to the {shop.name} costs "
                f"{money_fmt(trip_cost)}"
            )

        if not costs:
            print(
                f"{customer.name} doesn't have enough money to make a purchase "
                "in any shop"
            )
            continue

        best_shop, best_cost = customer.choose_cheapest_shop(
            shops,
            fuel_price,
        )

        if best_shop is None or best_cost is None:
            print(
                f"{customer.name} doesn't have enough money to make a purchase "
                "in any shop"
            )
            continue

        if customer.money < best_cost:
            print(
                f"{customer.name} doesn't have enough money to make a purchase "
                "in any shop"
            )
            continue

        print(f"{customer.name} rides to {best_shop.name}")
        customer.perform_purchase_trip(best_shop, best_cost)
        print(f"{customer.name} rides home")
        print(
            f"{customer.name} now has "
            f"{money_fmt(customer.money)} dollars\n"
        )
