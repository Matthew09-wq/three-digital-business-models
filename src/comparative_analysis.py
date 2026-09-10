"""
Three Digital Business Models, One Financial Lens
Comparative Financial Analysis
Author: Matthew Walker

Public portfolio version of the analytical engine supporting:
- FY2021-FY2025 common-period comparison
- Indexed revenue growth
- Operating margin trends
- Free cash flow margin trends
- Latest financial quality comparison
- Balance-sheet comparison

No proprietary raw datasets are included.

Financial figures are presented in US$ billions unless otherwise stated.
"""

from typing import Dict, List


# ============================================================
# COMPANY DATA
# ============================================================

YEARS = [2021, 2022, 2023, 2024, 2025]

HISTORICAL_DATA: Dict[str, Dict[str, List[float]]] = {
    "Microsoft": {
        "revenue": [168.09, 198.27, 211.92, 245.12, 281.72],
        "operating_margin": [41.59, 42.06, 41.77, 44.64, 45.62],
        "fcf_margin": [33.39, 32.86, 28.07, 30.22, 25.42],
    },
    "Adobe": {
        "revenue": [15.78, 17.61, 19.41, 21.50, 23.77],
        "operating_margin": [36.76, 34.64, 34.26, 31.35, 36.63],
        "fcf_margin": [43.60, 42.01, 35.77, 36.61, 41.45],
    },
    "Netflix": {
        "revenue": [29.70, 31.62, 33.72, 39.00, 45.18],
        "operating_margin": [20.86, 17.82, 20.62, 26.71, 29.49],
        "fcf_margin": [-0.44, 5.12, 20.54, 17.75, 20.94],
    },
}


LATEST_POSITION = {
    "Microsoft": {
        "revenue": 331.84,
        "revenue_growth": 17.79,
        "operating_margin": 46.78,
        "net_margin": 40.31,
        "free_cash_flow": 66.99,
        "fcf_margin": 20.19,
        "net_cash_debt": 36.55,
        "current_ratio": 1.23,
        "debt_to_equity": 0.09,
    },
    "Adobe": {
        "revenue": 25.20,
        "revenue_growth": 11.49,
        "operating_margin": 36.07,
        "net_margin": 28.69,
        "free_cash_flow": 10.28,
        "fcf_margin": 40.80,
        "net_cash_debt": 0.38,
        "current_ratio": 1.00,
        "debt_to_equity": 0.53,
    },
    "Netflix": {
        "revenue": 48.37,
        "revenue_growth": 16.02,
        "operating_margin": 29.68,
        "net_margin": 28.22,
        "free_cash_flow": 11.15,
        "fcf_margin": 23.06,
        "net_cash_debt": -5.40,
        "current_ratio": 1.19,
        "debt_to_equity": 0.54,
    },
}


# ============================================================
# ANALYTICAL FUNCTIONS
# ============================================================

def indexed_series(values: List[float]) -> List[float]:
    """
    Index a series to 100 in the first year.
    """
    base = values[0]

    return [
        value / base * 100
        for value in values
    ]


def percentage_point_change(values: List[float]) -> float:
    """
    Calculate the change between the first and final observation
    in percentage points.
    """
    return values[-1] - values[0]


def revenue_growth(start: float, end: float) -> float:
    """
    Calculate total revenue growth over the common period.
    """
    return (end / start - 1) * 100


def net_position_as_pct_revenue(
    net_cash_debt: float,
    revenue: float,
) -> float:
    """
    Express net cash / debt as a percentage of latest revenue.

    Positive = net cash.
    Negative = net debt.
    """
    return net_cash_debt / revenue * 100


# ============================================================
# COMMON-PERIOD ANALYSIS
# ============================================================

def build_common_period_summary():
    """
    Build FY2021-FY2025 like-for-like trend measures.
    """

    summary = {}

    for company, data in HISTORICAL_DATA.items():

        revenue_index = indexed_series(
            data["revenue"]
        )

        summary[company] = {
            "fy2025_revenue_index": revenue_index[-1],
            "total_revenue_growth_pct": revenue_growth(
                data["revenue"][0],
                data["revenue"][-1],
            ),
            "operating_margin_change_pp":
                percentage_point_change(
                    data["operating_margin"]
                ),
            "fcf_margin_change_pp":
                percentage_point_change(
                    data["fcf_margin"]
                ),
        }

    return summary


# ============================================================
# OUTPUT HELPERS
# ============================================================

def print_indexed_revenue():
    print("\nINDEXED REVENUE — FY2021 = 100")
    print("=" * 58)

    header = "Company".ljust(14)

    for year in YEARS:
        header += f"{year:>9}"

    print(header)

    for company, data in HISTORICAL_DATA.items():

        indexed = indexed_series(
            data["revenue"]
        )

        row = company.ljust(14)

        for value in indexed:
            row += f"{value:>9.1f}"

        print(row)


def print_margin_trends():
    print("\nOPERATING MARGIN — FY2021 TO FY2025")
    print("=" * 58)

    for company, data in HISTORICAL_DATA.items():

        values = " | ".join(
            f"{value:.1f}%"
            for value in data["operating_margin"]
        )

        print(f"{company:<10}: {values}")

    print("\nFREE CASH FLOW MARGIN — FY2021 TO FY2025")
    print("=" * 58)

    for company, data in HISTORICAL_DATA.items():

        values = " | ".join(
            f"{value:.1f}%"
            for value in data["fcf_margin"]
        )

        print(f"{company:<10}: {values}")


def print_common_period_summary():
    summary = build_common_period_summary()

    print("\nCOMMON-PERIOD SUMMARY — FY2021 TO FY2025")
    print("=" * 72)

    print(
        f"{'Company':<12}"
        f"{'Revenue Index':>15}"
        f"{'Op Margin Δ':>15}"
        f"{'FCF Margin Δ':>15}"
    )

    for company, metrics in summary.items():

        print(
            f"{company:<12}"
            f"{metrics['fy2025_revenue_index']:>15.1f}"
            f"{metrics['operating_margin_change_pp']:>14.1f}pp"
            f"{metrics['fcf_margin_change_pp']:>14.1f}pp"
        )


def print_latest_position():
    print("\nLATEST FINANCIAL POSITION")
    print("=" * 86)

    print(
        f"{'Company':<12}"
        f"{'Revenue':>12}"
        f"{'Growth':>10}"
        f"{'Op Margin':>12}"
        f"{'FCF Margin':>12}"
        f"{'Net Cash/(Debt)':>18}"
    )

    for company, metrics in LATEST_POSITION.items():

        print(
            f"{company:<12}"
            f"${metrics['revenue']:>10.1f}bn"
            f"{metrics['revenue_growth']:>9.1f}%"
            f"{metrics['operating_margin']:>11.1f}%"
            f"{metrics['fcf_margin']:>11.1f}%"
            f"${metrics['net_cash_debt']:>15.1f}bn"
        )


def print_balance_sheet_comparison():
    print("\nBALANCE-SHEET COMPARISON")
    print("=" * 72)

    print(
        f"{'Company':<12}"
        f"{'Net Cash/(Debt)':>18}"
        f"{'% Revenue':>12}"
        f"{'Current':>12}"
        f"{'Debt/Equity':>14}"
    )

    for company, metrics in LATEST_POSITION.items():

        net_pct = net_position_as_pct_revenue(
            metrics["net_cash_debt"],
            metrics["revenue"],
        )

        print(
            f"{company:<12}"
            f"${metrics['net_cash_debt']:>15.1f}bn"
            f"{net_pct:>11.1f}%"
            f"{metrics['current_ratio']:>12.2f}x"
            f"{metrics['debt_to_equity']:>13.2f}x"
        )


# ============================================================
# SANITY CHECKS
# ============================================================

def run_checks():
    """
    Confirm the public analytical outputs reproduce
    the headline figures used in the case study.
    """

    summary = build_common_period_summary()

    expected = {
        "Microsoft": {
            "index": 167.6,
            "op_change": 4.0,
            "fcf_change": -8.0,
        },
        "Adobe": {
            "index": 150.6,
            "op_change": -0.1,
            "fcf_change": -2.2,
        },
        "Netflix": {
            "index": 152.1,
            "op_change": 8.6,
            "fcf_change": 21.4,
        },
    }

    tolerance = 0.15

    for company, targets in expected.items():

        actual = summary[company]

        assert abs(
            actual["fy2025_revenue_index"]
            - targets["index"]
        ) < tolerance

        assert abs(
            actual["operating_margin_change_pp"]
            - targets["op_change"]
        ) < tolerance

        assert abs(
            actual["fcf_margin_change_pp"]
            - targets["fcf_change"]
        ) < tolerance

    print("\nModel checks: PASS")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print(
        "\nTHREE DIGITAL BUSINESS MODELS, "
        "ONE FINANCIAL LENS"
    )

    print(
        "Microsoft vs Adobe vs Netflix"
    )

    print_indexed_revenue()

    print_margin_trends()

    print_common_period_summary()

    print_latest_position()

    print_balance_sheet_comparison()

    run_checks()
