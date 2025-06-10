import os
import time
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# 1. CONFIGURATION
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "Cultural_Heritage_Datasets")
OUTPUT_CSV = os.path.join(DATA_DIR, "combined_heritage_with_coords.csv")
UNWANTED_COLS = [f"Unnamed: {i}" for i in range(6, 10)]

# 2. READ & CONCAT ALL CSV FILES
all_dfs = []
for fname in os.listdir(DATA_DIR):
    if not fname.lower().endswith(".csv"):
        continue
    path = os.path.join(DATA_DIR, fname)
    try:
        df = pd.read_csv(path, encoding='utf-8').dropna(how='all')
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding='latin1').dropna(how='all')
    df["source_file"] = fname  # Keep track of origin
    all_dfs.append(df)

combined = pd.concat(all_dfs, ignore_index=True)

# 3. CLEAN & NORMALIZE COLUMNS
combined = (
    combined
    .drop(columns=[c for c in UNWANTED_COLS if c in combined.columns], errors='ignore')
    .assign(
        **{
            "Nature of heritage": combined.get(
                "Nature of heritage (open space ; monuments ; street etc.)"
            ).fillna(
                combined.get("Nature of heritage (open space, monuments, street etc.)", "")
            )
        }
    )
    .drop(columns=[
        "Nature of heritage (open space ; monuments ; street etc.)",
        "Nature of heritage (open space, monuments, street etc.)"
    ], errors='ignore')
)

# 4. SET UP GEOCODER
geolocator = Nominatim(user_agent="culture_explorer_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# 5. GEOCODE UNIQUE CITIES
cities = combined["City Name"].dropna().unique()
city_coords = {}
print(f"Geocoding {len(cities)} unique cities…")

for city in cities:
    try:
        loc = geocode(f"{city}, India")
        if loc:
            city_coords[city] = (loc.latitude, loc.longitude)
            print(f"  ✓ {city}: {loc.latitude:.5f}, {loc.longitude:.5f}")
        else:
            city_coords[city] = (None, None)
            print(f"  ✗ {city}: Not found")
    except Exception as e:
        city_coords[city] = (None, None)
        print(f"  ⚠ {city}: Error – {e}")
        time.sleep(1)

# 6. MAP COORDINATES BACK INTO DATAFRAME
combined["Latitude"] = combined["City Name"].map(lambda c: city_coords.get(c, (None, None))[0])
combined["Longitude"] = combined["City Name"].map(lambda c: city_coords.get(c, (None, None))[1])

# 7. WRITE FINAL OUTPUT
combined.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Done! File saved to: {OUTPUT_CSV}")