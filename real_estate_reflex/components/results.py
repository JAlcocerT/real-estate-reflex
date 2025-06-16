"""Results component for the real estate loan calculator."""

import reflex as rx
import plotly.express as px
import plotly.graph_objects as go
from real_estate_reflex.real_estate_reflex import State

def format_currency(value: float) -> str:
    """Format a value as currency."""
    return f"${value:,.2f}"

def summary_card() -> rx.Component:
    """Summary card showing loan calculation results."""
    return rx.card(
        rx.vstack(
            rx.heading("Loan Summary", size="lg", mb="4"),
            rx.cond(
                State.monthly_payment > 0,
                rx.vstack(
                    rx.hstack(
                        rx.text("Monthly Payment:", font_weight="bold"),
                        rx.spacer(),
                        rx.text(format_currency(State.monthly_payment)),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Total Principal:", font_weight="bold"),
                        rx.spacer(),
                        rx.text(format_currency(State.loan_amount)),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Total Interest:", font_weight="bold"),
                        rx.spacer(),
                        rx.text(format_currency(State.total_interest)),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Total Payment:", font_weight="bold"),
                        rx.spacer(),
                        rx.text(format_currency(State.total_payment)),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.text("Loan Term:", font_weight="bold"),
                        rx.spacer(),
                        rx.text(f"{State.loan_term_years} years ({State.loan_term_years * 12} months)"),
                        width="100%",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.text("Enter loan details and click Calculate to see summary."),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )

def interest_principal_pie_chart() -> rx.Component:
    """Pie chart showing interest to principal ratio."""
    return rx.card(
        rx.vstack(
            rx.heading("Interest to Principal Ratio", size="md", mb="4"),
            rx.cond(
                State.total_interest > 0,
                rx.plotly(
                    go.Figure(
                        data=[
                            go.Pie(
                                labels=["Principal", "Interest"],
                                values=[State.loan_amount, State.total_interest],
                                hole=0.4,
                                marker=dict(colors=["#3182CE", "#E53E3E"]),
                            )
                        ],
                        layout=dict(
                            height=300,
                            margin=dict(l=20, r=20, t=30, b=20),
                        ),
                    ),
                ),
                rx.text("No data to display yet."),
            ),
            width="100%",
        ),
        width="100%",
    )

def principal_interest_line_chart() -> rx.Component:
    """Line chart showing principal vs interest payments over time."""
    return rx.card(
        rx.vstack(
            rx.heading("Principal vs Interest Over Time", size="md", mb="4"),
            rx.cond(
                len(State.amortization_table) > 0,
                rx.cond(
                    # Only show for loans with reasonable terms (avoid performance issues)
                    State.loan_term_years <= 30,
                    rx.vstack(
                        rx.plotly(
                            lambda: go.Figure(
                                data=[
                                    go.Scatter(
                                        x=[item["month"] for item in State.amortization_table],
                                        y=[item["principal"] for item in State.amortization_table],
                                        mode="lines",
                                        name="Principal",
                                        line=dict(color="#3182CE", width=2),
                                    ),
                                    go.Scatter(
                                        x=[item["month"] for item in State.amortization_table],
                                        y=[item["interest"] for item in State.amortization_table],
                                        mode="lines",
                                        name="Interest",
                                        line=dict(color="#E53E3E", width=2),
                                    ),
                                ],
                                layout=dict(
                                    height=400,
                                    margin=dict(l=50, r=20, t=30, b=50),
                                    xaxis_title="Month",
                                    yaxis_title="Amount ($)",
                                ),
                            )
                        ),
                        rx.text(
                            "This chart shows how your monthly payment is split between principal and interest over time. "
                            "As the loan progresses, more of your payment goes toward principal and less toward interest.",
                            font_size="sm",
                            color="gray.600",
                            mt="2",
                        ),
                        width="100%",
                    ),
                    rx.text("Chart not displayed for loan terms over 30 years to improve performance."),
                ),
                rx.text("No data to display yet."),
            ),
            width="100%",
        ),
        width="100%",
    )

def remaining_balance_chart() -> rx.Component:
    """Line chart showing remaining balance over time."""
    return rx.card(
        rx.vstack(
            rx.heading("Remaining Balance Over Time", size="md", mb="4"),
            rx.cond(
                len(State.amortization_table) > 0,
                rx.cond(
                    # Only show for loans with reasonable terms (avoid performance issues)
                    State.loan_term_years <= 30,
                    rx.vstack(
                        rx.plotly(
                            lambda: go.Figure(
                                data=[
                                    go.Scatter(
                                        x=[item["month"] for item in State.amortization_table],
                                        y=[item["ending_balance"] for item in State.amortization_table],
                                        mode="lines",
                                        name="Remaining Balance",
                                        line=dict(color="#805AD5", width=2),
                                        fill="tozeroy",
                                    ),
                                ],
                                layout=dict(
                                    height=400,
                                    margin=dict(l=50, r=20, t=30, b=50),
                                    xaxis_title="Month",
                                    yaxis_title="Remaining Balance ($)",
                                ),
                            )
                        ),
                        rx.text(
                            "This chart shows how your loan balance decreases over the term of the loan.",
                            font_size="sm",
                            color="gray.600",
                            mt="2",
                        ),
                        width="100%",
                    ),
                    rx.text("Chart not displayed for loan terms over 30 years to improve performance."),
                ),
                rx.text("No data to display yet."),
            ),
            width="100%",
        ),
        width="100%",
    )

def amortization_table_component() -> rx.Component:
    """Amortization table showing monthly payment breakdown."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Amortization Schedule", size="lg"),
                rx.spacer(),
                rx.cond(
                    len(State.amortization_table) > 0,
                    rx.button(
                        "Download CSV",
                        on_click=rx.download(
                            url=f"/download/amortization_table.csv",
                            filename="amortization_table.csv",
                        ),
                        size="sm",
                    ),
                    rx.text(""),
                ),
                width="100%",
            ),
            rx.cond(
                len(State.amortization_table) > 0,
                rx.data_table(
                    data=State.amortization_table,
                    columns=[
                        {"header": "Month", "accessor": "month"},
                        {"header": "Starting Balance", "accessor": "starting_balance", "cell": lambda row: format_currency(row["starting_balance"])},
                        {"header": "Payment", "accessor": "payment", "cell": lambda row: format_currency(row["payment"])},
                        {"header": "Principal", "accessor": "principal", "cell": lambda row: format_currency(row["principal"])},
                        {"header": "Interest", "accessor": "interest", "cell": lambda row: format_currency(row["interest"])},
                        {"header": "Ending Balance", "accessor": "ending_balance", "cell": lambda row: format_currency(row["ending_balance"])},
                    ],
                    pagination=True,
                    search=True,
                    sort=True,
                    selection_mode="single",
                    highlight_on_hover=True,
                    page_size=10,
                ),
                rx.text("Calculate loan to see amortization schedule."),
            ),
            spacing="4",
            width="100%",
        ),
        width="100%",
    )
