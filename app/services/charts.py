import pandas as pd


def generate_chart_data(rows):

    df = pd.DataFrame(rows)

    return {

        "lineChart": (
            df[[
                "year",
                "endBalance",
                "rmd",
                "tax",
                "growth"
            ]]
            .to_dict("records")
        ),

        "summary": {
            "maxBalance": float(df["endBalance"].max()),
            "minBalance": float(df["endBalance"].min()),
            "totalRmd": float(df["rmd"].sum()),
            "totalTax": float(df["tax"].sum())
        }
    }