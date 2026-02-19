from __future__ import annotations

from typing import Dict, List, Tuple

from .car import Car
from .customer import Customer
from .shop import Shop
from .utils import load_config, money_fmt, to_location


def shop_trip() -> None:
    """
    Required main function. Takes no arguments.

    - Loads config.json
    - Builds Shop/Customer/Car objects
    - For each customer prints trip cost to each shop
    - Chooses cheapest shop and performs purchase if possible
    """
    config = load_config("config.json")
    fuel_price: float = float(config["FUEL_PRICE"])

    shops: List[Shop] = []
    for raw_shop in config["shops"]:
        shops.append(
            Shop(
                name=str(raw_shop["name"]),
                location=to_location(raw_shop["location"]),
                products={
                    str(key): float(value)
                    for key, value in raw_shop["products"].items()
                },
            )
        )
    shops_tuple: Tuple[Shop, ...] = tuple(shops)

    customers: List[Customer] = []
    for raw_customer in config["customers"]:
        car_data = raw_customer["car"]
        car = Car(
            brand=str(car_data["brand"]),
            fuel_consumption=float(car_data["fuel_consumption"]),
        )

        customers.append(
            Customer(
                name=str(raw_customer["name"]),
                product_cart={
                    str(key): int(value)
                    for key, value in raw_customer["product_cart"].items()
                },
                location=to_location(raw_customer["location"]),
                money=float(raw_customer["money"]),
                car=car,
            )
        )

    for customer in customers:
        print(f"{customer.name} has {money_fmt(customer.money)} dollars")

        costs_by_shop: Dict[str, float] = {}
        for shop in shops_tuple:
            trip_cost = customer.trip_cost_to_shop(shop, fuel_price)
            if trip_cost is None:
                continue

            costs_by_shop[shop.name] = trip_cost
            print(
                f"{customer.name}'s trip to the {shop.name} costs "
                f"{money_fmt(trip_cost)}"
            )

        if not costs_by_shop:
            print(
                f"{customer.name} doesn't have enough money to make a purchase "
                "in any shop"
            )
            continue

        best_shop, best_cost = customer.choose_cheapest_shop(
            shops_tuple,
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
            f"{customer.name} now has {money_fmt(customer.money)} dollars\n"
        )
