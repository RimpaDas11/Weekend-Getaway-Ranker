
import pandas as pd
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def rank_destinations(source_city):
    df = pd.read_csv("travel_data.csv")
    source_df = df[df["source_city"].str.lower() == source_city.lower()]
    if source_df.empty:
        raise ValueError("Source city not found")

    lat1, lon1 = source_df.iloc[0][["lat","lon"]]
    source_df["distance"] = source_df.apply(
        lambda x: haversine(lat1, lon1, x["lat"], x["lon"]), axis=1
    )

    source_df["score"] = (
        (1 / source_df["distance"]) * 0.4 +
        source_df["rating"] * 0.3 +
        source_df["popularity"] * 0.3
    )

    return source_df.sort_values("score", ascending=False)[
        ["destination", "distance", "rating", "popularity", "score"]
    ]

if __name__ == "__main__":
    city = input("Enter Source City: ")
    result = rank_destinations(city)
    print(result)
