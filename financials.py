import pint

ureg = pint.UnitRegistry()

ureg.define('dollar = dimensionless')

dollar = ureg.Quantity(1, 'dollar')
dollar = 1

# Status Quo
per_mile_us_shipping_cost = 1.38 * dollar / (ureg.mile)
per_mile_fuel_cost = 0.54 * dollar / (ureg.mile)
per_mile_equipment_cost = 0.24 * dollar / (ureg.mile)
per_mile_driver_cost = 0.36 * dollar / (ureg.mile)
per_mile_maintenance_cost = 0.12 * dollar / (ureg.mile)
per_mile_insurance_cost = 0.05 * dollar / (ureg.mile)

# electric status quo
per_mile_electricity_cost = 0.45 * per_mile_fuel_cost
per_mile_electric_maintenance_cost = 0.04 * dollar / (ureg.mile)
per_mile_electric_energy_use = 600 * ureg.kWh / (500 * ureg.mile) # based on Tesla semi

# proposal
pgh_to_chi = 431 * ureg.miles

proportion_to_electric = 0.7
added_weight_factor = 1.3 # todo, fudge factor
depletion_factor = 0.8 # how much capacity it has after full cycles
battery_price_per_kwh = 1200 * dollar / (5.2 * ureg.kWh) # based on used Tesla battery prices
battery_price_per_kwh = (300 * dollar / (120 * ureg.amp * ureg.hour * 12.8 * ureg.volt)).to('1/kWh') # based on https://www.alibaba.com/product-detail/deep-cycle-long-life-lifepo4-batteries_62245071040.html?spm=a2700.7724857.normalList.93.25113891P874Zg
battery_price_per_kwh = (32 * dollar / (105 * ureg.amp * ureg.hour * 3.2 * ureg.volt)).to('1/kWh') # based on https://www.alibaba.com/product-detail/3-2V100Ah-lithium-iron-phosphate-battery_1600064520018.html?spm=a2700.7724857.videoBannerStyleB_top.9.25113891P874Zg
# battery_price_per_kwh = (27 * dollar / (90 * ureg.amp * ureg.hour * 3.2 * ureg.volt)).to('1/kWh') # based on https://www.alibaba.com/product-detail/New-graphene-lithium-iron-phosphate-battery_62174779869.html?spm=a2700.7724857.normalList.85.25113891P874Zg
battery_price_per_kwh = (13 * dollar / (10 * ureg.amp * ureg.hour * 2.4 * ureg.volt)).to('1/kWh') # https://www.alibaba.com/product-detail/LITHIUM-TITANATE-BATTERY-32145-2-4V_62467696954.html?spm=a2700.galleryofferlist.topad_creative.d_image.68121d683pILmp&fullFirstScreen=true
# battery_price_per_kwh = (37 * dollar / (50 * ureg.amp * ureg.hour * 3.2 * ureg.volt)).to('1/kWh') # https://www.alibaba.com/product-detail/Cylindrical-32700-battery-32650-lifepo4-3_62387635956.html?spm=a2700.galleryofferlist.normal_offer.d_title.66224c67RFquit

print("battery price per kwh", battery_price_per_kwh)
battery_capacity = proportion_to_electric * per_mile_electric_energy_use * pgh_to_chi * added_weight_factor / depletion_factor
battery_price = battery_price_per_kwh * battery_capacity

# operating costs
# single 53' trailer
sixth_wheel_per_mile_fuel_cost = (per_mile_fuel_cost * (1-proportion_to_electric) + \
                                    per_mile_electricity_cost * (proportion_to_electric)) * added_weight_factor
sixth_wheel_per_mile_maintenance_cost = (per_mile_maintenance_cost * (1-proportion_to_electric) + \
                                    per_mile_electric_maintenance_cost * (proportion_to_electric)) * added_weight_factor
sixth_wheel_per_mile_insurance_cost = 0.04 * dollar / (ureg.mile)

# PRICING
delta = (per_mile_fuel_cost + per_mile_maintenance_cost + per_mile_insurance_cost) - \
        (sixth_wheel_per_mile_fuel_cost + sixth_wheel_per_mile_maintenance_cost + sixth_wheel_per_mile_insurance_cost)
sixth_wheel_per_mile_rental_cost = 0.8 * delta

sixth_wheel_per_mile_cost = per_mile_us_shipping_cost - delta + \
                            + sixth_wheel_per_mile_rental_cost

overall_savings = (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost) / per_mile_us_shipping_cost * 100
driver_savings = (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost) / per_mile_driver_cost * 100
print("Overall percentage savings", overall_savings)
print("Potential driver wage increase", driver_savings)

sixth_wheel_capital_expense = battery_price * 1.3 # roughly based on Tesla
print("Cost of each sixth wheel", sixth_wheel_capital_expense)

sixth_wheel_untilization = 0.5 # proportion of day on road 
sixth_wheel_speed = 45 * ureg.mph
sixth_wheel_miles_per_year = (sixth_wheel_untilization * sixth_wheel_speed * ureg.year).to('mile')
sixth_wheel_annual_revenue_no_yard = (sixth_wheel_miles_per_year * sixth_wheel_per_mile_rental_cost).to('dimensionless')

print("annual revenue w/ no yard work", sixth_wheel_annual_revenue_no_yard)


# battery_lifespan = 6000 * pgh_to_chi #based on https://www.fortresspower.com/how-to-calculate-the-energy-cost-of-different-battery-chemistries/#
battery_lifespan = 2000 * pgh_to_chi #based on https://www.alibaba.com/product-detail/deep-cycle-long-life-lifepo4-batteries_62245071040.html?spm=a2700.7724857.normalList.93.25113891P874Zg
battery_lifespan = 3000 * pgh_to_chi #based on https://www.alibaba.com/product-detail/3-2V100Ah-lithium-iron-phosphate-battery_1600064520018.html?spm=a2700.7724857.videoBannerStyleB_top.9.25113891P874Zg
# battery_lifespan = 10000 * pgh_to_chi #based on https://www.alibaba.com/product-detail/New-graphene-lithium-iron-phosphate-battery_62174779869.html?spm=a2700.7724857.normalList.85.25113891P874Zg
battery_lifespan = 25000 * pgh_to_chi #based on https://www.alibaba.com/product-detail/LITHIUM-TITANATE-BATTERY-32145-2-4V_62467696954.html?spm=a2700.galleryofferlist.topad_creative.d_image.68121d683pILmp&fullFirstScreen=true
# battery_lifespan = 4000 * pgh_to_chi #based on https://www.alibaba.com/product-detail/Cylindrical-32700-battery-32650-lifepo4-3_62387635956.html?spm=a2700.galleryofferlist.normal_offer.d_title.66224c67RFquit
print("annual miles", sixth_wheel_miles_per_year)
print("battery life", ureg.year * battery_lifespan / sixth_wheel_miles_per_year)
print("lifetime value", sixth_wheel_per_mile_rental_cost * sixth_wheel_miles_per_year * (battery_lifespan / sixth_wheel_miles_per_year))

sixth_wheel_margins = 0.5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               # TODO: Very important and hard to know - what are the 
print("sixth wheel payback period", ureg.year * sixth_wheel_capital_expense / (sixth_wheel_annual_revenue_no_yard * sixth_wheel_margins))

pgh_to_chi_daily_trucks = 25e3
pgh_to_chi_tam_no_yard = 365 * pgh_to_chi_daily_trucks * pgh_to_chi * sixth_wheel_per_mile_rental_cost
print("PGH to CHI no yard TAM", pgh_to_chi_tam_no_yard)

# YARD PRICING
detention_time_per_trip = 4 * ureg.hours
percent_at_endpoints = 0.3
trips_per_year = pgh_to_chi_daily_trucks * 365 * percent_at_endpoints 
hourly_wages = 24.48 * dollar / ureg.hour
pgh_to_chi_tam_yard = detention_time_per_trip * hourly_wages * trips_per_year
# NOTE: making the sixth wheels autonomous yard jockeys will improve margins on this market
print("PGH to CHI yard TAM", pgh_to_chi_tam_yard)

# AUTONOMY PRICING
sixth_wheel_per_mile_driver_cost_autonomy = 0.01 * dollar / (ureg.mile)
sixth_wheel_per_mile_rental_cost_autonomy = 0.3 * dollar / (ureg.mile)
sixth_wheel_per_mile_cost_autonomy = per_mile_us_shipping_cost - (per_mile_fuel_cost + per_mile_maintenance_cost + per_mile_insurance_cost + per_mile_driver_cost) + \
                            + (sixth_wheel_per_mile_fuel_cost + sixth_wheel_per_mile_maintenance_cost + sixth_wheel_per_mile_insurance_cost + sixth_wheel_per_mile_driver_cost_autonomy) + \
                            + sixth_wheel_per_mile_rental_cost_autonomy


overall_savings = (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost_autonomy) / per_mile_us_shipping_cost * 100
print("Overall percentage savings, + autonomy", overall_savings)

sixth_wheel_untilization = 0.65 # proportion of day on road 
sixth_wheel_annual_revenue_no_yard_autonomy = (sixth_wheel_untilization * sixth_wheel_speed * ureg.year * sixth_wheel_per_mile_rental_cost_autonomy).to('dimensionless')
print("annual revenue w/ no yard work, autonomy", sixth_wheel_annual_revenue_no_yard_autonomy)

sixth_wheel_margins = 0.8
print("sixth wheel payback period, autonomy", ureg.year * sixth_wheel_capital_expense / (sixth_wheel_annual_revenue_no_yard_autonomy * sixth_wheel_margins))

pgh_to_chi_tam_no_yard = 365 * pgh_to_chi_daily_trucks * pgh_to_chi * sixth_wheel_per_mile_rental_cost_autonomy
print("PGH to CHI no yard TAM, + autonomy", pgh_to_chi_tam_no_yard)

lfp_density = (90 * ureg.amp * ureg.hour * 3.2 * ureg.volt) / (1.85 * ureg.kg) # https://www.alibaba.com/product-detail/New-graphene-lithium-iron-phosphate-battery_62174779869.html?spm=a2700.7724857.normalList.85.25113891P874Zg
lfp_battery_weight = battery_capacity / lfp_density
print("battery capacity", battery_capacity)
print("lfp weight", lfp_battery_weight.to('lb'))

# https://www.alibaba.com/product-detail/New-graphene-lithium-iron-phosphate-battery_62174779869.html?spm=a2700.7724857.normalList.85.25113891P874Zg
single_battery_volume = 30*226*125*(ureg.mm**3)
single_battery_price = 27 * dollar
num_batteries = battery_price / single_battery_price
total_battery_volume = num_batteries*single_battery_volume
sixth_wheel_length = (total_battery_volume / (102 * ureg.inch * 110 * ureg.inch)).to('feet')
print("number of batteries", num_batteries)
print("Min Length of battery pack", sixth_wheel_length)

# https://www.cheaptubes.com/resources/graphene-battery-users-guide/
# https://www.alibaba.com/product-detail/High-Energy-Graphene-Supercapacitor-Module-16V_1600080785165.html?spm=a2700.galleryofferlist.normal_offer.d_title.5839b775SsIW9T

supercap_capacitance = 100000 * ureg.farad
supercap_voltage = 2.7 * ureg.volt
energy_in_supercap = 0.5 * supercap_capacitance * supercap_voltage**2
print("energy in supercap", energy_in_supercap.to('kWh'))
print("number supercaps", (battery_capacity / energy_in_supercap).to('dimensionless'))