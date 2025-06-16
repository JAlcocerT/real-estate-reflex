"""Navigation component for the Real Estate Calculator app."""

import reflex as rx

def navbar() -> rx.Component:
    """Navigation bar for the Real Estate Calculator app."""
    return rx.box(
        rx.hstack(
            rx.link(
                rx.hstack(
                    rx.icon("house-fill"),
                    rx.text("Real Estate Calculator", font_weight="bold"),
                    spacing="2",
                ),
                href="/",
                _hover={"text_decoration": "none"},
            ),
            rx.spacer(),
            rx.hstack(
                rx.link(
                    "Home",
                    href="/",
                    padding="2",
                    border_radius="md",
                    _hover={"bg": "gray.100"},
                ),
                rx.link(
                    "Amortization",
                    href="/amortization",
                    padding="2",
                    border_radius="md",
                    _hover={"bg": "gray.100"},
                ),
                rx.link(
                    "Comparison",
                    href="/comparison",
                    padding="2",
                    border_radius="md",
                    _hover={"bg": "gray.100"},
                ),
                rx.color_mode.button(),
                spacing="4",
            ),
            width="100%",
        ),
        padding_x="4",
        padding_y="3",
        position="sticky",
        top="0",
        z_index="999",
        bg="rgba(255, 255, 255, 0.8)",
        backdrop_filter="blur(10px)",
        border_bottom="1px solid",
        border_color="gray.200",
    )
