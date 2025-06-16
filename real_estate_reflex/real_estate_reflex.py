"""Real Estate Loan Calculator built with Reflex."""

import reflex as rx
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from typing import List, Dict, Any

from rxconfig import config


class State(rx.State):
    """The app state for the real estate loan calculator."""
    
    # Input variables
    loan_amount: float = 250000.0
    annual_interest_rate: float = 5.0
    loan_term_years: int = 30
    desired_monthly_payment: float = 0.0
    
    # Calculation results
    monthly_payment: float = 0.0
    total_interest: float = 0.0
    total_payment: float = 0.0
    amortization_table: List[Dict[str, Any]] = []
    
    # For scenario comparison
    show_comparison: bool = False
    scenario_a_loan_amount: float = 250000.0
    scenario_a_interest_rate: float = 5.0
    scenario_a_term_years: int = 30
    scenario_b_loan_amount: float = 250000.0
    scenario_b_interest_rate: float = 5.5
    scenario_b_term_years: int = 15
    scenario_a_monthly: float = 0.0
    scenario_a_total_interest: float = 0.0
    scenario_b_monthly: float = 0.0
    scenario_b_total_interest: float = 0.0
    
    # Affordability estimator result
    affordable_loan_amount: float = 0.0
    
    def calculate_monthly_payment(self, principal: float, annual_rate: float, years: int) -> float:
        """Calculate the monthly payment for a loan."""
        if annual_rate == 0:
            return principal / (years * 12)
            
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        return monthly_payment
    
    def calculate_loan(self):
        """Calculate loan details and generate amortization table."""
        self.monthly_payment = self.calculate_monthly_payment(
            self.loan_amount, self.annual_interest_rate, self.loan_term_years
        )
        
        # Generate amortization table
        monthly_rate = self.annual_interest_rate / 100 / 12
        amortization_data = []
        remaining_balance = self.loan_amount
        total_interest = 0
        
        for month in range(1, self.loan_term_years * 12 + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = self.monthly_payment - interest_payment
            total_interest += interest_payment
            remaining_balance -= principal_payment
            
            # Handle final payment rounding issues
            if month == self.loan_term_years * 12:
                principal_payment += remaining_balance
                remaining_balance = 0
            
            amortization_data.append({
                "month": month,
                "starting_balance": round(remaining_balance + principal_payment, 2),
                "payment": round(self.monthly_payment, 2),
                "principal": round(principal_payment, 2),
                "interest": round(interest_payment, 2),
                "ending_balance": round(remaining_balance, 2)
            })
        
        self.amortization_table = amortization_data
        self.total_interest = round(total_interest, 2)
        self.total_payment = round(self.loan_amount + total_interest, 2)
    
    def calculate_affordable_loan(self):
        """Calculate the affordable loan amount based on desired monthly payment."""
        if self.desired_monthly_payment <= 0:
            self.affordable_loan_amount = 0
            return
            
        monthly_rate = self.annual_interest_rate / 100 / 12
        num_payments = self.loan_term_years * 12
        
        if monthly_rate == 0:
            self.affordable_loan_amount = self.desired_monthly_payment * num_payments
            return
            
        # Formula for loan amount based on payment
        self.affordable_loan_amount = self.desired_monthly_payment * ((1 - (1 + monthly_rate) ** -num_payments) / monthly_rate)
        self.affordable_loan_amount = round(self.affordable_loan_amount, 2)
    
    def compare_scenarios(self):
        """Compare two different loan scenarios."""
        self.scenario_a_monthly = self.calculate_monthly_payment(
            self.scenario_a_loan_amount, self.scenario_a_interest_rate, self.scenario_a_term_years
        )
        
        self.scenario_b_monthly = self.calculate_monthly_payment(
            self.scenario_b_loan_amount, self.scenario_b_interest_rate, self.scenario_b_term_years
        )
        
        # Calculate total interest for each scenario
        scenario_a_total = self.scenario_a_monthly * self.scenario_a_term_years * 12
        scenario_a_interest = scenario_a_total - self.scenario_a_loan_amount
        self.scenario_a_total_interest = round(scenario_a_interest, 2)
        
        scenario_b_total = self.scenario_b_monthly * self.scenario_b_term_years * 12
        scenario_b_interest = scenario_b_total - self.scenario_b_loan_amount
        self.scenario_b_total_interest = round(scenario_b_interest, 2)
    
    def generate_principal_interest_chart_data(self):
        """Generate data for the principal vs interest chart."""
        data = []
        for month, row in enumerate(self.amortization_table):
            data.append({
                "month": month + 1,
                "principal": row["principal"],
                "interest": row["interest"]
            })
        return data
    
    def generate_balance_chart_data(self):
        """Generate data for the remaining balance chart."""
        return [{
            "month": row["month"],
            "balance": row["ending_balance"]
        } for row in self.amortization_table]
    
    # Event handlers for toggling comparison view and CSV download
    def toggle_comparison(self):
        """Toggle the loan comparison view."""
        self.show_comparison = not self.show_comparison
        
    def download_csv(self):
        """Convert amortization table to CSV and provide download."""
        if not self.amortization_table:
            return
            
        # Create a DataFrame from the amortization table
        df = pd.DataFrame(self.amortization_table)
        csv_string = df.to_csv(index=False)
        
        # Return CSV file for download
        return rx.download(csv_string, filename="amortization_schedule.csv")


# Create an instance of the app.
# This must be called to instantiate the app.
app = rx.App() 
