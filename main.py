import csv
import json
import sys
import zipfile
from pathlib import Path
from prefectures import PREF_EN, PREF_JP


def get_routes(properties: dict) -> list[str]:
    routes = []
    for i in range(1, 100):
        v = properties.get(f"P11_003_{i:02d}")
        if not v:
            break
        routes.extend(
            route.strip() 
            for route in str(v).split(",") 
            if route.strip()
        )
    return routes


def write_csv(name: str, geojson_bytes: bytes) -> None:
    rows = [["停留所名", "事業者名", "バス系統"]]
    for feature in json.loads(geojson_bytes)["features"]:
        properties = feature["properties"]
        rows.append([
            properties["P11_001"],
            properties["P11_002"],
            ", ".join(get_routes(properties))
        ])
    with Path(name).open('w', newline='', encoding='utf-8-sig') as f:
        csv.writer(f).writerows(rows)

def main() -> None:
    Path("data").mkdir(exist_ok=True)
    with zipfile.ZipFile(Path(sys.argv[1])) as outer_zip:
        for name in outer_zip.namelist():
            with zipfile.ZipFile(outer_zip.open(name)) as inner_zip:
                name = name.removesuffix("_GML.zip")
                code = int(name[-2:])
                
                write_csv(
                    f"data/{code:02d}_{PREF_EN[code]}.csv",
                    inner_zip.read(f"{name}/{name}.geojson")
                )


if __name__ == "__main__":
    main()
