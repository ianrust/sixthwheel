import pint

ureg = pint.UnitRegistry()
# ureg.define('dollar = dimensionless')
# dollar = ureg.Quantity(1, 'dollar')
dollar = 1


def run(values):
    # Status Quo (Diesel)
    # source: https://www.thetruckersreport.com/infographics/cost-of-trucking/
    # alternate source: https://www.freightwaves.com/news/understanding-total-operating-cost-per-mile#:~:text=Typically%2C%20gross%20fuel%20expense%20averages%20between%20%240.40%2D%240.55%20per%20mile.
    per_mile_us_shipping_cost = 1.38 * dollar / (ureg.mile)
    per_mile_fuel_cost = values["diesel per mile"] * dollar / (ureg.mile)
    per_mile_equipment_cost = 0.24 * dollar / (ureg.mile)
    per_mile_driver_cost = 0.55 * dollar / (ureg.mile)
    per_mile_maintenance_cost = 0.12 * dollar / (ureg.mile)
    per_mile_insurance_cost = 0.05 * dollar / (ureg.mile)

    # source: https://apps.dana.com/commercial-vehicles/tco/
    per_mile_electric_maintenance_cost = 0.5 * per_mile_maintenance_cost

    # based on Tesla semi
    # source: https://electrek.co/2018/05/02/tesla-semi-production-version-range-increase-elon-musk/
    # alt source: https://lynceans.org/wp-content/uploads/2020/04/Tesla-Semi-converted.pdf
    # Important note - this says a Tesla semi will have ~20% lower operating costs,
    # Tesla range optimism is 27% https://www.caranddriver.com/features/a33824052/adjustment-factor-tesla-uses-for-big-epa-range-numbers/
    per_mile_electric_energy_use = 947 * ureg.kWh / (600 * ureg.mile * 0.73)
    print(per_mile_electric_energy_use)
    # Status Quo (Electric)

    # source: https://apps.dana.com/commercial-vehicles/tco/
    # alt source: https://avt.inl.gov/sites/default/files/pdf/fsev/costs.pdf]
    # PPA
    # https://pv-magazine-usa.com/2020/02/04/utility-scale-solar-ppa-pricing-down-4-7-in-2019-with-13-6-gw-of-corporate-deals-signed/#:~:text=Utility%2Dscale%20solar%20power%20purchase,kWh%2C%20according%20to%20LevelTen%20Energy.
    # + transmission costs
    # https://spectrum.ieee.org/energywise/energy/policy/how-to-predict-a-utilitys-transmission-and-distribution-costs-count-customers-served
    per_mile_electricity_cost = (
        values["electric per kwh"]
        * per_mile_electric_energy_use
        * dollar
        / (ureg.kilowatt_hour)
    )

    intended_range = values["range"] * ureg.miles

    # Best battery for application: Lithium Iron Phosphate
    # source: https://batteryuniversity.com/learn/article/types_of_lithium_ion
    # High cycles
    # Cheap
    # Good low temp performance
    # Safe (not nearly as suscpetible to thermal runaway as compared to Cobalt-based cathodes in Tesla Semi)

    # source: https://www.alibaba.com/product-detail/Graphene-lithium-iron-phosphate-battery-3_1600131559793.html
    # battery_price_per_kwh = (63 * dollar / (272 * ureg.amp * ureg.hour * 3.2 * ureg.volt)).to('1/kWh')
    # this price is more realistic
    # proterra batteries
    battery_price_per_kwh = (
        values["battery per kwh"] * dollar / ureg.kilowatt_hour
    ).to("1/kWh")
    battery_lifespan = values["battery cycle life"] * intended_range
    depletion_factor = values[
        "depletion at end of life"
    ]  # how much capacity it has after full cycles
    # battery_specific_density = (
    #     0.9 * (220 * ureg.amp * ureg.hour * 3.2 * ureg.volt) / (5.4 * ureg.kg)
    # )
    # proterra batteries
    battery_specific_density = 170 * ureg.watt_hours / ureg.kg
    # lfp_vol_density = (272 * ureg.amp * ureg.hour * 3.2 * ureg.volt) / (
    #     205 * ureg.mm * 72 * ureg.mm * 175 * ureg.mm
    # )
    lfp_vol_density = 325 * ureg.watt_hours / ureg.liter
    single_battery_price = 27 * dollar

    # How much work (proportionally) the electric motors will do (1 means 0% diesel, 0 means 100% diesel)
    proportion_to_electric = values["proportion electric"]

    # How much of the cost savings we claim as revenue, the rest passed on to the rest of the market
    # (carriers, owner/operators, etc)
    prop_take = values["take"]

    # How much more the tolls will cost by adding a 1-axle vehicle to the train
    # source: https://www.ohioturnpike.org/docs/default-source/annual-report-files/cafr-2019-final.pdf?sfvrsn=d361ebc4_2
    # when >3 trailers, ie classified as a road train (A type, ie fifth wheel to fifth wheel, 53' trailers)
    # per_mile_toll_increase = 0.07 * dollar / ureg.mile
    # when no increase in trailers, ie classified as a road train (B type, ie tow hitch to fifth wheel, twin 28' trailer LTL market)
    # we hope to generally negotiate additional weight fees to the state/tollway to 75% their stated price. Plus, most roads don't have tolls
    per_mile_toll_increase = values["toll increase"] * dollar / ureg.mile

    # avg speed when on road
    # https://ops.fhwa.dot.gov/freight/freight_analysis/nat_freight_stats/docs/10factsfigures/table3_8.htm
    sixth_wheel_speed = 57.5 * ureg.mph

    # proportion of day on road
    # https://en.wikipedia.org/wiki/Lithium_iron_phosphate_battery
    sixth_wheel_utilization = (
        intended_range
        / sixth_wheel_speed
        / (intended_range / sixth_wheel_speed + 1 * ureg.hour)  # 1C
        * 18
        / 24
    )

    print("utils", sixth_wheel_utilization)

    # cost of components (as a proportion of battery cost), roughly based on Tesla
    additional_component_cost = values["additional component cost"]

    # iteratively get capacity, since more battery weight means need for more capacity
    added_weight = 10000 * ureg.pound

    # How weight impacts fuel https://www.internationaltrucks.com/en/blog/fuel-economy-weight
    # 0.5% increase per 1000lbs
    percentage_fuel_per_pound = (0.5 / 100) / (1000 * ureg.pound)
    resultant_weight = added_weight * 0.9
    # weight of components  (structure, power electronics, motors, etc)
    additional_component_weight = 2500 * ureg.pound

    # https://ops.fhwa.dot.gov/freight/freight_analysis/nat_freight_stats/docs/10factsfigures/table3_3.htm
    # https://www.freightpros.com/blog/less-than-truckload/
    # https://www.terrybryant.com/how-much-does-semi-truck-weigh#:~:text=Semi%2Dtractors%20weigh%20up%20to,haul%20up%20to%2034%2C000%20pounds.
    base_truck_weight = 70000 * ureg.pound
    percent_under_base_weight = 0.8

    while abs(added_weight - resultant_weight) > 1 * ureg.pound:
        added_weight = resultant_weight
        battery_capacity = (
            proportion_to_electric
            * per_mile_electric_energy_use
            * intended_range
            * (1 + percentage_fuel_per_pound * added_weight)
            / depletion_factor
        )
        battery_price = battery_price_per_kwh * battery_capacity

        battery_weight = battery_capacity / battery_specific_density

        resultant_weight = battery_weight + additional_component_weight

    added_weight = resultant_weight

    print("battery", battery_weight.to("pound"))
    print("total", added_weight.to("pound"))

    added_weight_factor = 1 + percentage_fuel_per_pound * added_weight
    num_batteries = battery_price / single_battery_price

    # operating costs, averaged as a funtion of the proportion converted to electricity
    sixth_wheel_per_mile_fuel_cost = (
        per_mile_fuel_cost * (1 - proportion_to_electric)
        + per_mile_electricity_cost * (proportion_to_electric)
    ) * added_weight_factor
    sixth_wheel_per_mile_maintenance_cost = (
        per_mile_maintenance_cost * (1 - proportion_to_electric)
        + per_mile_electric_maintenance_cost * (proportion_to_electric)
    ) * added_weight_factor
    # Assume this is slightly lower because of ADAS features like ABS, ACC, anti-skid
    sixth_wheel_per_mile_insurance_cost = (
        values["insurance multiple"] * per_mile_insurance_cost
    )

    # PRICING
    delta = (
        -per_mile_toll_increase
        + (per_mile_fuel_cost + per_mile_maintenance_cost + per_mile_insurance_cost)
        - (
            sixth_wheel_per_mile_fuel_cost
            + sixth_wheel_per_mile_maintenance_cost
            + sixth_wheel_per_mile_insurance_cost
        )
    )
    sixth_wheel_per_mile_rental_cost = prop_take * delta

    # Total cost savings
    sixth_wheel_per_mile_cost_no_cut = per_mile_us_shipping_cost - delta

    overall_savings_no_cut = (
        (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost_no_cut)
        / per_mile_us_shipping_cost
        * 100
    )
    driver_savings_no_cut = (
        (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost_no_cut)
        / per_mile_driver_cost
        * 100
    )

    sixth_wheel_per_mile_cost = (
        per_mile_us_shipping_cost - delta + sixth_wheel_per_mile_rental_cost
    )

    overall_savings = (
        (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost)
        / per_mile_us_shipping_cost
        * 100
    )
    overall_savings_with_solar = (
        (
            per_mile_us_shipping_cost
            - sixth_wheel_per_mile_cost
            + per_mile_electricity_cost
        )
        / per_mile_us_shipping_cost
        * 100
    )
    driver_savings = (
        (per_mile_us_shipping_cost - sixth_wheel_per_mile_cost)
        / per_mile_driver_cost
        * 100
    )

    #  Capital analysis
    sixth_wheel_capital_expense = battery_price + additional_component_cost
    sixth_wheel_miles_per_year = (
        sixth_wheel_utilization * sixth_wheel_speed * ureg.year
    ).to("mile")
    sixth_wheel_annual_revenue = (
        sixth_wheel_miles_per_year * sixth_wheel_per_mile_rental_cost
    ).to("dimensionless")
    other_annual_operating_cost = values["annual operating cost"]

    sixth_wheel_margins = (
        sixth_wheel_annual_revenue - (other_annual_operating_cost)
    ) / sixth_wheel_annual_revenue

    battery_years = battery_lifespan / sixth_wheel_miles_per_year

    lifetime_value = battery_years * sixth_wheel_annual_revenue

    rate_of_return = 100 * (
        (
            (lifetime_value * sixth_wheel_margins + 0.7 * additional_component_cost)
            / sixth_wheel_capital_expense
        )
        ** (1 / battery_years)
        - 1
    )

    payback_period = (
        ureg.year
        * (sixth_wheel_capital_expense - 0.7 * additional_component_cost)
        / (sixth_wheel_annual_revenue * sixth_wheel_margins)
    )

    single_rental_cost = sixth_wheel_per_mile_rental_cost * intended_range
    diesel_mpg = 7 * ureg.mile / ureg.gallon

    fuel_discount = (
        100
        * (1 - (sixth_wheel_per_mile_fuel_cost / per_mile_fuel_cost))
        * (1 - prop_take)
    )

    return {
        "utilization": sixth_wheel_utilization,
        "6w weight": added_weight.to("pound"),
        "battery compartment length": (
            (battery_capacity / lfp_vol_density) / (110 * ureg.inch * 100 * ureg.inch)
        ).to("feet"),
        "battery compartment volume": ((battery_capacity / lfp_vol_density)).to(
            "meter^3"
        ),
        "battery capacity": battery_capacity,
        "battery cost": battery_price,
        "added weight factor": added_weight_factor,
        "6w per mile rental cost": sixth_wheel_per_mile_rental_cost,
        "potential overall savings": overall_savings_no_cut,
        "potential driver savings": driver_savings_no_cut,
        "customer overall savings": overall_savings,
        "customer overall savings with solar": overall_savings_with_solar,
        "customer driver savings": driver_savings,
        "single 6w cost": sixth_wheel_capital_expense,
        "years until battery failure": battery_years,
        "lifetime value": lifetime_value,
        "rate of return": rate_of_return,
        "payback period": payback_period,
        "single rental cost": single_rental_cost,
        "single rental savings": delta * (1 - prop_take) * intended_range,
        "fuel discount": fuel_discount,
        "arr": sixth_wheel_annual_revenue,
        "electric power use": (
            proportion_to_electric * per_mile_electric_energy_use * sixth_wheel_speed
        ).to("kilowatt"),
    }
