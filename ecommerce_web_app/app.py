from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load data
df = pd.read_csv("merged_ecommerce_data.csv")

@app.route("/", methods=["GET"])
def index():
    search = request.args.get("search")
    platform = request.args.get("platform")

    data = df.copy()

    # Search filter
    if search:
        data = data[data["product_name"].str.contains(search, case=False, na=False)]

    # Platform filter
    if platform and platform != "All":
        data = data[data["platform"] == platform]

    platforms = ["All"] + sorted(df["platform"].dropna().unique().tolist())

    return render_template(
        "index.html",
        tables=data.head(100).to_dict(orient="records"),
        platforms=platforms
    )

if __name__ == "__main__":
    app.run(debug=True)
