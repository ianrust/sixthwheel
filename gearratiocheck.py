import pint
import math

ureg = pint.UnitRegistry()

gear_ratio = 4
electric_torque = 988 * ureg.N * ureg.m
wheel_radius = 21 * ureg.inch

vehicle_weight = (80e3 * ureg.pound).to("kg")

# assuuming a 60s 0-60
diesel_torque = (
    (0.0456 * 9.806 * ureg.m / (ureg.s ** 2)) * vehicle_weight * wheel_radius
).to("N*m")

total_torque = diesel_torque + electric_torque * gear_ratio

acceleration = total_torque / (wheel_radius * vehicle_weight)
print("0-60:", ((60 * ureg.mph) / acceleration).to("s"))

print("pull force", (acceleration * vehicle_weight).to("lbf"))

max_brake_force = 20000 * ureg.lbf
max_brake_deceleration = max_brake_force / vehicle_weight
print(max_brake_deceleration.to("m/s^2"))
brake_time = (60 * ureg.mph) / max_brake_deceleration
print(brake_time.to("s"))
print("stopping distance", (0.5 * max_brake_deceleration * (brake_time ** 2)).to("ft"))
