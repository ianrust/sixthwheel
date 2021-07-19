import pint
import math

ureg = pint.UnitRegistry()

# LFP
battery_specific_density = 140 * ureg.watt_hours / ureg.kg
battery_volumetric_density = 325 * ureg.watt_hours / ureg.liter

# LTO
# battery_specific_density = 80 * ureg.watt_hours / ureg.kg
# battery_volumetric_density = 177 * ureg.watt_hours / ureg.liter


# cylinder packing ratio
battery_density_packed = 0.9069 * battery_volumetric_density / battery_specific_density
print(battery_density_packed.to("kg/m^3"))

# battery geometry
length = 19 * ureg.inch
inner_radius = 7 * ureg.inch
outer_radius = 18 * ureg.inch
tire_radius = 22 * ureg.inch

# additional mass geometry
add_density = 8050 * ureg.kg / (ureg.meter ** 3)
add_thickness = 0.25 * ureg.inch

battery_moment_of_inertia = (
    0.5
    * math.pi
    * length
    * battery_density_packed
    * (outer_radius ** 4 - inner_radius ** 4)
)

additional_moment_of_inertia = (
    0.5
    * math.pi
    * length
    * add_density
    * ((outer_radius + add_thickness) ** 4 - (outer_radius) ** 4)
)

battery_mass = (
    math.pi * length * battery_density_packed * (outer_radius ** 2 - inner_radius ** 2)
)

additional_mass = (
    math.pi
    * length
    * add_density
    * ((outer_radius + add_thickness) ** 2 - outer_radius ** 2)
)

num_wheels = 8
final_speed = 60 * ureg.mph

wheel_torque = 1000 * (ureg.newton * ureg.meter) / (num_wheels)
truck_mass = 80e3 * ureg.pound

# normal truck force
normal_truck_force = truck_mass * final_speed / (60 * ureg.second)

linear_acceleration = (
    wheel_torque * num_wheels / tire_radius + normal_truck_force
) / truck_mass

on_time = (final_speed / linear_acceleration).to("s")
print("0-60 w/ diesel", on_time)

print((battery_mass + additional_mass).to("kg"))
print((battery_mass * battery_specific_density).to("kWh"))
print((battery_mass * battery_specific_density).to("kWh") * num_wheels)
print(wheel_torque)

battery_acceleration = wheel_torque / (
    battery_moment_of_inertia + additional_moment_of_inertia
)

rads = battery_acceleration * on_time
rpm = (rads / (2 * math.pi)).to("1/minute")

truck_energy = (0.5 * truck_mass * (final_speed ** 2)).to("kWh")

print("rpm", rpm)
print(
    "energy of flywheel",
    (0.5 * (battery_moment_of_inertia + additional_moment_of_inertia) * (rads ** 2)).to(
        "kWh"
    ),
)
print(
    "flywheel / diesel %",
    (wheel_torque * num_wheels / tire_radius / normal_truck_force).to("dimensionless")
    * 100,
)

diesel_energy_density = 36e6 * ureg.joule / ureg.liter
diesel_steady_state = 7.5 * ureg.mile / ureg.gallon

diesel_wattage = 0.325 * diesel_energy_density / diesel_steady_state * final_speed
print("diesel_wattage", diesel_wattage.to("kW"))

turn_radius = 100 * ureg.meter

print(
    "roll torque",
    (
        num_wheels
        * (battery_moment_of_inertia + additional_moment_of_inertia)
        * rads
        * (final_speed / turn_radius)
    ).to("N*m"),
)

print(
    "bad roll torque",
    (truck_mass * (final_speed ** 2) / turn_radius * 5 * ureg.feet).to("N*m"),
)
