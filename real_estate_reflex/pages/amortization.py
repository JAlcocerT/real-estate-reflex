"""Amortization schedule page for the Real Estate Loan Calculator."""

import reflex as rx
from real_estate_reflex.components.results import amortization_table_component
from real_estate_reflex.real_estate_reflex import State

def amortization() -> rx.Component:
    """The amortization schedule page."""
    return rx.container(
        rx.vstack(
            # Header
            rx.box(
                rx.vstack(
                    rx.heading("Amortization Schedule", size="xl"),
                    rx.text(
                        "Detailed monthly breakdown of your loan payments.",
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
            rx.box(
                amortization_table_component(),
                width="100%",
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
