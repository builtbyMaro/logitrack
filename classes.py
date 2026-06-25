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

    def _calculate_cost(self) -> float:
        return 5 + (1.5 * self.weight)

    def update_status(self, new_status: str) -> bool:
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
        self.loaded_packages: list[Package] = []

    def get_current_weight(self) -> float:
        return sum([package.weight for package in self.loaded_packages])

    def load_package(self, package: Package) -> bool:
        if (package.weight + self.get_current_weight()) > self.max_weight_capacity:
            return False
        else:
            self.loaded_packages.append(package)
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
        if package.weight >= 5:
            return False
        return super().load_package(package)


class LogisticsHub:
    def __init__(self, hub_name: str):
        self.hub_name: str = hub_name
        self.packages_inventory: dict[str, Package] = {}
        self.fleet: list[Vehicle] = []

    def add_vehicle(self, vehicle: Vehicle) -> bool:
        self.fleet.append(vehicle)
        return True

    def accept_package(self, package: Package) -> bool:
        self.packages_inventory[package.package_id] = package
        return True

    def dispatch_fleet(self) -> None:
        for package in self.packages_inventory.values():
            if package.weight < 5:
                for vehicle in self.fleet:
                    if isinstance(vehicle, Drone):
                        if vehicle.load_package(package):
                            break
            else:
                for vehicle in self.fleet:
                    if isinstance(vehicle, DeliveryTruck):
                        if vehicle.load_package(package):
                            break

