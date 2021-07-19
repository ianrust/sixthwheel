import pint
import math

ureg = pint.UnitRegistry()

# battery params
cycle_life = 5000
battery_cost = 250 / ureg.kilowatt_hour
battery_specific_density = 140 * ureg.watt_hours / ureg.kg
depth_of_discharge = 0.6

# energy params
generation_price = 0.04 / ureg.kilowatt_hour
sale_price = 0.15 / ureg.kilowatt_hour

# electrical efficiencies
powertrain_efficiency = 0.96
charging_efficiency = 0.87

# movement losses
truck_mass = 80e3 * ureg.pound
avg_speed = 57.5 * ureg.mph
diesel_energy_density = 36e6 * ureg.joule / ureg.liter
diesel_steady_state = 7.5 * ureg.mile / ureg.gallon
diesel_wattage = 0.325 * diesel_energy_density / diesel_steady_state * avg_speed

print((diesel_energy_density / diesel_steady_state).to("kWh/mile"))
print(947 * ureg.kWh / (600 * ureg.mile * 0.73))

power_use_per_kg = (diesel_wattage / truck_mass).to("kW/kg") / (
    powertrain_efficiency * charging_efficiency
)
energy_use_per_kg_per_mile = (power_use_per_kg / avg_speed).to("kWh / (kg * mile)")
transport_cost_per_kWh_per_mile = (
    energy_use_per_kg_per_mile * sale_price / battery_specific_density
)

for miles in range(10, 500, 10):
    dollars_lost_in_transit_per_kwh = (
        miles * ureg.mile * transport_cost_per_kWh_per_mile
    )
    lifetime_value_per_kwh = (
        depth_of_discharge
        * cycle_life
        * (
            sale_price
            - generation_price / charging_efficiency
            - dollars_lost_in_transit_per_kwh
        )
    )
    roi = lifetime_value_per_kwh / battery_cost

    print(miles, " miles, roi: ", roi)