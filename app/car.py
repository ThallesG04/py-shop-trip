from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Car:
    # Representa o carro do cliente
    brand: str
    fuel_consumption: float

    def fuel_cost_for_distance(
            self,
            distance_km: float,
            fuel_price: float,
) -> float:
        liters_spent = distance_km * (self.fuel_consumption / 100.0)
        return liters_spent * fuel_price
    # Calcula gasto de combustível para percorrer uma distância
