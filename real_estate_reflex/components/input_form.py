"""Input form component for the real estate loan calculator."""

import reflex as rx
from real_estate_reflex.real_estate_reflex import State

def input_form() -> rx.Component:
    """Input form for loan parameters."""
    return rx.card(
        rx.vstack(
            rx.heading("Loan Parameters", size="lg", mb="4"),
            rx.form_control(
                rx.form_label("Loan Amount ($)"),
                rx.number_input(
                    value=State.loan_amount,
                    on_change=State.set_loan_amount,
                    min_=1,
                    step=1000,
                    width="100%",
                ),
            ),
            rx.form_control(
                rx.form_label("Annual Interest Rate (%)"),
                rx.number_input(
                    value=State.annual_interest_rate,
                    on_change=State.set_annual_interest_rate,
                    min_=0,
                    max_=30,
                    step=0.1,
                    precision=2,
                    width="100%",
                ),
            ),
            rx.form_control(
                rx.form_label("Loan Term (Years)"),
                rx.number_input(
                    value=State.loan_term_years,
                    on_change=State.set_loan_term_years,
                    min_=1,
                    max_=50,
                    step=1,
                    width="100%",
                ),
            ),
            rx.button(
                "Calculate",
                on_click=State.calculate_loan,
                color_scheme="blue",
                width="100%",
                mt="4",
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )

def affordability_estimator() -> rx.Component:
    """Affordability estimator form."""
    return rx.card(
        rx.vstack(
            rx.heading("Affordability Estimator", size="lg", mb="4"),
            rx.text(
                "Enter your desired monthly payment to estimate how much you can afford to borrow."
            ),
            rx.form_control(
                rx.form_label("Desired Monthly Payment ($)"),
                rx.number_input(
                    value=State.desired_monthly_payment,
                    on_change=State.set_desired_monthly_payment,
                    min_=1,
                    step=100,
                    width="100%",
                ),
            ),
            rx.text(
                f"Estimated Affordable Loan Amount: ${State.affordable_loan_amount:,.2f}",
                font_weight="bold",
                mt="2",
            ) if State.affordable_loan_amount > 0 else rx.text(""),
            rx.button(
                "Calculate Affordable Amount",
                on_click=State.calculate_affordable_loan,
                color_scheme="green",
                width="100%",
                mt="4",
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        mt="6",
    )

def scenario_comparison() -> rx.Component:
    """Scenario comparison component."""
    return rx.card(
        rx.vstack(
            rx.heading("Loan Scenario Comparison", size="lg", mb="4"),
            rx.box(
                rx.hstack(
                    rx.vstack(
                        rx.heading("Scenario A", size="md"),
                        rx.form_control(
                            rx.form_label("Loan Amount ($)"),
                            rx.number_input(
                                value=State.scenario_a_loan_amount,
                                on_change=State.set_scenario_a_loan_amount,
                                min_=1,
                                step=1000,
                                width="100%",
                            ),
                        ),
                        rx.form_control(
                            rx.form_label("Interest Rate (%)"),
                            rx.number_input(
                                value=State.scenario_a_interest_rate,
                                on_change=State.set_scenario_a_interest_rate,
                                min_=0,
                                max_=30,
                                step=0.1,
                                precision=2,
                                width="100%",
                            ),
                        ),
                        rx.form_control(
                            rx.form_label("Term (Years)"),
                            rx.number_input(
                                value=State.scenario_a_term_years,
                                on_change=State.set_scenario_a_term_years,
                                min_=1,
                                max_=50,
                                step=1,
                                width="100%",
                            ),
                        ),
                        width="48%",
                    ),
                    rx.vstack(
                        rx.heading("Scenario B", size="md"),
                        rx.form_control(
                            rx.form_label("Loan Amount ($)"),
                            rx.number_input(
                                value=State.scenario_b_loan_amount,
                                on_change=State.set_scenario_b_loan_amount,
                                min_=1,
                                step=1000,
                                width="100%",
                            ),
                        ),
                        rx.form_control(
                            rx.form_label("Interest Rate (%)"),
                            rx.number_input(
                                value=State.scenario_b_interest_rate,
                                on_change=State.set_scenario_b_interest_rate,
                                min_=0,
                                max_=30,
                                step=0.1,
                                precision=2,
                                width="100%",
                            ),
                        ),
                        rx.form_control(
                            rx.form_label("Term (Years)"),
                            rx.number_input(
                                value=State.scenario_b_term_years,
                                on_change=State.set_scenario_b_term_years,
                                min_=1,
                                max_=50,
                                step=1,
                                width="100%",
                            ),
                        ),
                        width="48%",
                    ),
                    width="100%",
                    justify="space-between",
                ),
                width="100%",
            ),
            rx.button(
                "Compare Scenarios",
                on_click=State.compare_scenarios,
                color_scheme="purple",
                width="100%",
                mt="4",
            ),
            rx.cond(
                State.scenario_a_monthly > 0,
                rx.vstack(
                    rx.heading("Comparison Results", size="md", mt="4"),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Monthly Payment:"),
                            rx.text("Total Interest:"),
                            rx.text("Total Payment:"),
                            rx.text("Total Years:"),
                            align_items="flex-start",
                            width="30%",
                        ),
                        rx.vstack(
                            rx.text(f"${State.scenario_a_monthly:,.2f}"),
                            rx.text(f"${State.scenario_a_total_interest:,.2f}"),
                            rx.text(f"${State.scenario_a_monthly * State.scenario_a_term_years * 12:,.2f}"),
                            rx.text(f"{State.scenario_a_term_years} years"),
                            align_items="flex-end",
                            width="30%",
                        ),
                        rx.vstack(
                            rx.text(f"${State.scenario_b_monthly:,.2f}"),
                            rx.text(f"${State.scenario_b_total_interest:,.2f}"),
                            rx.text(f"${State.scenario_b_monthly * State.scenario_b_term_years * 12:,.2f}"),
                            rx.text(f"{State.scenario_b_term_years} years"),
                            align_items="flex-end",
                            width="30%",
                        ),
                        width="100%",
                        justify="space-between",
                    ),
                    width="100%",
                ),
                rx.text(""),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
        mt="6",
    )
