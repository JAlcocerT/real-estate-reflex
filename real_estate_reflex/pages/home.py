"""Home page for the Real Estate Loan Calculator."""

import reflex as rx
from real_estate_reflex.components.input_form import input_form, affordability_estimator
from real_estate_reflex.components.results import (
    summary_card,
    interest_principal_pie_chart,
    principal_interest_line_chart,
    remaining_balance_chart
)
from real_estate_reflex.real_estate_reflex import State

def home() -> rx.Component:
    """The main page of the real estate loan calculator."""
    return rx.container(
        rx.vstack(
            # Header
            rx.box(
                rx.vstack(
                    rx.heading("Real Estate Loan Calculator", size="xl"),
                    rx.text(
                        "Calculate mortgage payments, view amortization schedules, and visualize loan details.",
                        color="gray.500",
                        font_size="lg",
                    ),
                    align_items="center",
                    spacing="2",
                    py="6",
                ),
                width="100%",
                text_align="center",
            ),
            
            # Main content
            rx.flex(
                rx.box(
                    rx.vstack(
                        input_form(),
                        affordability_estimator(),
                        width="100%",
                    ),
                    width=["100%", "100%", "30%", "30%"],
                    mr=["0", "0", "4", "4"],
                ),
                rx.box(
                    rx.vstack(
                        summary_card(),
                        rx.flex(
                            interest_principal_pie_chart(),
                            remaining_balance_chart(),
                            direction=["column", "column", "row", "row"],
                            width="100%",
                            spacing="4",
                            mt="4",
                        ),
                        principal_interest_line_chart(),
                        width="100%",
                        spacing="4",
                    ),
                    width=["100%", "100%", "70%", "70%"],
                ),
                direction=["column", "column", "row", "row"],
                width="100%",
                spacing="4",
            ),
            
            # Footer
            rx.box(
                rx.text(
                    f"© {rx.datetime.now().year} Real Estate Loan Calculator. Built with Reflex.",
                    color="gray.500",
                    text_align="center",
                ),
                py="4",
                mt="10",
                width="100%",
            ),
            width="100%",
            max_width="1200px",
            px="4",
        ),
        py="4",
    )
