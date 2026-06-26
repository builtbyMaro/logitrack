from classes import Package, Drone, DeliveryTruck, LogisticsHub

hub = LogisticsHub("Metro-East Hub")

package1 = Package("PKG01", 3.2, "10001")
package2 = Package("PKG02", 18.5, "10002")
package3 = Package("PKG03", 4.1, "10001")

drone1 = Drone("0001", 4.99, 100)
truck1 = DeliveryTruck("0001", 3000, "East Zone")

hub.add_vehicle(drone1)
hub.add_vehicle(truck1)

hub.accept_package(package1)
hub.accept_package(package2)
hub.accept_package(package3)

hub.dispatch_fleet()

print("=====ALL PACKAGES=====")
for value in hub._packages_inventory.values():
    print(value)
print("========================================")

print("---Drone Packages---")
for package in drone1._loaded_packages:
    print(package.package_id)
print("--------------------")

print("---Truck Packages---")
for package in truck1._loaded_packages:
    print(package.package_id)
