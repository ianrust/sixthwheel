import pint
import math

ureg = pint.UnitRegistry()

# solar_power_per_area = (1e9 * ureg.watt_hour / ureg.year / ureg.acre).to("kW/m^2")

charger_power = 150 * ureg.kilowatt
utilization = 0.51
build_multiple = 1.1

# print((utilization * build_multiple * charger_power / solar_power_per_area))
# print(
#     (
#         utilization
#         * build_multiple
#         * charger_power
#         / (ureg.kilowatt / (100 * ureg.foot ** 2))
#     ).to("m^2")
# )
solar_area = (
    utilization * build_multiple * charger_power / (15 * ureg.watt / (ureg.foot ** 2))
).to("m^2")
solar_linear = math.sqrt(solar_area / (ureg.meter ** 2)) * ureg.meter
print(solar_area)
print(solar_linear.to("ft"))

install_cost = 1 / ureg.watt
charger_installation_cost = charger_power * install_cost * utilization * build_multiple
charge_time = 60 * ureg.minute
battery_cost = 200 / ureg.kilowatt_hour
depth_of_discharge = 0.6
charging_efficiency = 0.87
battery_storage_cost = (
    battery_cost
    * charge_time
    * charger_power
    / (depth_of_discharge * charging_efficiency)
)
print("attery size", (battery_storage_cost / battery_cost).to("kWh"))
charger_cost = 50e3
other_costs = battery_storage_cost / 2
print("other costs", other_costs.to("dimensionless"))
# land use
land_cost_per_acre = 10e3 / ureg.acre
land_cost = land_cost_per_acre * solar_area
total_cost = (
    charger_installation_cost
    + battery_storage_cost
    + charger_cost
    + other_costs
    + land_cost
)
cycles_per_day = (24 * ureg.hour / (charge_time / utilization)).to("dimensionless")

revenue_per_kwh = 0.04 / ureg.kilowatt_hour
revenue_per_year = (revenue_per_kwh * charger_power * utilization).to("1/year")
operating_margins = 0.9

print(total_cost.to("dimensionless"))
print(revenue_per_year)
print(total_cost / (operating_margins * revenue_per_year))
print(
    "lifetime_battery cycles",
    cycles_per_day
    * 365
    * total_cost
    / (operating_margins * revenue_per_year)
    / ureg.year,
)
