import PySimpleGUI as sg
import model


def slider_element(name, default, ranger, step):
    return [
        sg.Text(name),
        sg.Slider(
            ranger,
            default,
            step,
            orientation="h",
            size=(100, 15),
            key=name,
        ),
    ]


layout = [
    slider_element("diesel per mile", 0.38, (0, 1.0), 0.001),
    slider_element("electric per kwh", 0.03, (0, 0.3), 0.001),
    slider_element("battery per kwh", 200, (1, 600), 1),
    slider_element("proportion electric", 0.7, (0, 1.0), 0.001),
    slider_element("take", 0.6, (0.01, 1.0), 0.001),
    slider_element("toll increase", 0.0, (0, 0.20), 0.001),
    slider_element("range", 150, (10, 800), 10),
    slider_element("battery cycle life", 4000, (0, 40000), 100),
    slider_element("depletion at end of life", 0.8, (0, 1.0), 0.001),
    slider_element("additional component cost", 30000, (0, 45000), 1000),
    slider_element(
        # maintenance + tires
        "annual operating cost",
        (0.3 * 15000 + 4000 * 2 / 16) * 1.25,
        (0, 25000),
        1000,
    ),
    slider_element("insurance multiple", 0.8, (0.0, 3.0), 0.01),
    [sg.Text("Payback period (years): "), sg.Text("100000", key="payback_period")],
    [sg.Text("Rate of return (%): "), sg.Text("100000", key="rate_of_return")],
    [
        sg.Text("Rate of return with carbon credit (%): "),
        sg.Text("100000", key="rate_of_return_credit"),
    ],
    [
        sg.Text("Battery lifespan (years): "),
        sg.Text("100000", key="years_until_battery_failure"),
    ],
    [sg.Text("6w weight (lbs): "), sg.Text("100000", key="weight")],
    [
        sg.Text("Single trip rental cost ($): "),
        sg.Text("100000", key="single_rental_cost"),
    ],
    [sg.Text("Fuel discount: "), sg.Text("100000", key="fuel_discount")],
    [sg.Text("Battery Capacity (kwh): "), sg.Text("100000", key="battery_capacity")],
    [sg.Text("Lifetime Value ($): "), sg.Text("100000", key="lifetime_value")],
    [
        sg.Text("Customer savings on trip ($): "),
        sg.Text("100000", key="customer_savings"),
    ],
    [sg.Text("Vehicle Cost ($): "), sg.Text("100000", key="vehicle_cost")],
    [sg.Text("Battery Cost ($): "), sg.Text("100000", key="battery_cost")],
    [sg.Text("Single Unit ARR ($): "), sg.Text("100000", key="arr")],
    [sg.Text("Per mile savings (%): "), sg.Text("100000", key="per_mile_savings")],
    [
        sg.Text("Per mile savings with solar (%): "),
        sg.Text("100000", key="per_mile_savings_solar"),
    ],
]

window = sg.Window("6W financial model", layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read(timeout=10)
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break

    result = model.run(values)

    window.Element("weight").update(result["6w weight"])
    window.Element("payback_period").update(result["payback period"])
    window.Element("years_until_battery_failure").update(
        result["years until battery failure"]
    )
    window.Element("rate_of_return").update(result["rate of return"])
    window.Element("rate_of_return_credit").update(
        result["rate of return with carbon credit"]
    )
    window.Element("single_rental_cost").update(result["single rental cost"])
    window.Element("fuel_discount").update(result["fuel discount"])
    window.Element("battery_capacity").update(result["battery capacity"])
    window.Element("lifetime_value").update(result["lifetime value"])
    window.Element("customer_savings").update(result["single rental savings"])
    window.Element("per_mile_savings").update(result["customer overall savings"])
    window.Element("per_mile_savings_solar").update(
        result["customer overall savings with solar"]
    )
    window.Element("vehicle_cost").update(result["single 6w cost"])
    window.Element("battery_cost").update(result["battery cost"])
    window.Element("arr").update(result["arr"])
window.close()