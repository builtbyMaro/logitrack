"""
The classes module contains\n
Package: models a package object, has package_id, weight, destination_zip, status, update_status().\n
Vehicle: models vehicle objects, has vehicle_id, max_weight_capacity, _loaded_packages, get_current_weight(), load_packages().\n
DeliveryTruck: models a truck of type Vehicle, adds route_zone.\n
Drone: models a drone of type Vehicle, adds battery_percentage and extends load_package().\n
LogisticsHub: models a logistics management, has hub_name, _packages_inventory, _fleet, add_vehicle(), accept_package(), dispatch_fleet().\n
"""

class Package:
    def __init__(
        self,
        package_id: str,
        weight: float,
        destination_zip: str,
        status: str = "Hub Warehouse",
    ):
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")

        self.package_id: str = package_id
        self.weight: float = weight
        self.destination_zip: str = destination_zip
        self.status: str = status
        self.shipping_cost: float = self._calculate_cost()

    def __str__(self):
        return (
            f"Package ID: {self.package_id}, "
            f"Shipping cost: {self.shipping_cost}, "
            f"Status: {self.status}"
        )

    def _calculate_cost(self) -> float:
        """Calculates package's shipping cost.\n Formula: 5 + 1.5 * package weight"""
        return 5 + (1.5 * self.weight)

    def update_status(self, new_status: str) -> bool:
        """Updates package's status.\n only accepts 3 arguments "Hub Warehouse" | "In Transit" | "Delivered", will fail otherwise."""
        valid_status = {
            "Hub Warehouse",
            "In Transit",
            "Delivered",
        }

        if new_status in valid_status:
            self.status = new_status
            return True

        return False


class Vehicle:
    def __init__(self, vehicle_id: str, max_weight_capacity: float):
        self.vehicle_id: str = vehicle_id
        self.max_weight_capacity: float = max_weight_capacity
        self._loaded_packages: list[Package] = []

    def get_current_weight(self) -> float:
        """Returns the total weight of all the vehicle's packages."""
        return sum([package.weight for package in self._loaded_packages])

    def load_package(self, package: Package) -> bool:
        """Tries to load package to vehicle.\n Load will only fail if vehicle has reached max_weight_capacity"""
        if (package.weight + self.get_current_weight()) > self.max_weight_capacity:
            return False
        else:
            self._loaded_packages.append(package)
            package.update_status("In Transit")
            return True


class DeliveryTruck(Vehicle):
    def __init__(
        self,
        vehicle_id: str,
        max_weight_capacity: float,
        route_zone: str,
    ):
        super().__init__(vehicle_id, max_weight_capacity)
        self.route_zone: str = route_zone


class Drone(Vehicle):
    def __init__(
        self,
        vehicle_id: str,
        max_weight_capacity: float,
        battery_percentage: int,
    ):
        super().__init__(vehicle_id, max_weight_capacity)
        self.battery_percentage: int = battery_percentage

    def load_package(self, package: Package) -> bool:
        """Tries to load a package to drone.\n Load will fail if package weight equals or is greater than 5."""
        if package.weight >= 5:
            return False
        return super().load_package(package)


class LogisticsHub:
    def __init__(self, hub_name: str):
        self.hub_name: str = hub_name
        self._packages_inventory: dict[str, Package] = {}
        self._fleet: list[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        """Adds vehicle to hub's fleet"""
        self._fleet.append(vehicle)
        return True

    def accept_package(self, package: Package) -> bool:
        """Adds package to hub's package inventory."""
        self._packages_inventory[package.package_id] = package
        return True

    def dispatch_fleet(self) -> None:
        """Loads hub's packages based on weight to available hub vehichles."""
        for package in self._packages_inventory.values():
            loaded = False
            for vehicle in self._fleet:
                if isinstance(vehicle, Drone):
                    if vehicle.load_package(package):
                        loaded = True
                        break
            
            if not loaded:
                for vehicle in self._fleet:
                    if isinstance(vehicle, DeliveryTruck):
                        if vehicle.load_package(package):
                            loaded =True
                            break

