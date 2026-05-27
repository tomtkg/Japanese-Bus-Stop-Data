import csv
import json
import sys
import zipfile
from pathlib import Path
from typing import Any
from image import save_image
from prefecture import PREF_EN, PREF_JP, get_pref


def write_csv(name: str, header: list[str], rows: list[list[Any]]) -> None:
    with Path(name).open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def get_operators(properties: dict) -> list[str]:
    operators = properties["P11_002"]
    return [
        operator.strip() 
        for operator in str(operators).split("・") 
        if operator.strip()
    ]


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


def get_data(geojson_bytes: bytes) -> list[list[Any]]:
    data = []
    for feature in json.loads(geojson_bytes)["features"]:
        p = feature["properties"]
        data.append([p["P11_001"], get_operators(p), get_routes(p)])
    return data


def main() -> None:
    Path("data").mkdir(exist_ok=True)
    Path("images").mkdir(exist_ok=True)
    Path("prefectures").mkdir(exist_ok=True)
    
    stop_rows = []
    op_dict: dict[str, list[set]] = {}
    with zipfile.ZipFile(Path(sys.argv[1])) as outer_zip:
        for name in outer_zip.namelist():
            with zipfile.ZipFile(outer_zip.open(name)) as inner_zip:
                name = name.removesuffix("_GML.zip")
                code = int(name[-2:])
                
                data = get_data(inner_zip.read(f"{name}/{name}.geojson"))
                
                write_csv(
                    f"prefectures/{code:02d}_{PREF_EN[code]}.csv",
                    ["停留所名", "事業者名", "バス系統"],
                    [[v[0], "・".join(v[1]), ", ".join(v[2])] for v in data]
                )
                
                stop_rows.append([
                    code, PREF_JP[code], len(data),
                    len({v[0] for v in data}),
                    len({operator for v in data for operator in v[1]}),
                    len({route for v in data for route in v[2]})
                ])

                for stop, operators, routes in data:
                    for operator in operators:
                        if operator not in op_dict:
                            op_dict[operator] = [set(), set(), set()]
                        op_dict[operator][0].add(code)
                        op_dict[operator][1].update(routes)
                        op_dict[operator][2].add(stop)

    write_csv(
        "data/bus_stops_summary.csv",
        ["code", "都道府県名", "停留所数", "停留所数（マージ）", "事業者数", "バス系統数"],
        [["0", "単純合計"] + [sum(v[i] for v in stop_rows) for i in [2, 3, 4, 5]]]
        + stop_rows
    )
    write_csv(
        "data/bus_operators_summary.csv",
        ["都道府県名", "事業者名", "バス系統数", "停留所数"],
        [[get_pref(v[0]), op, len(v[1]), len(v[2])] for op, v in op_dict.items()]
    )
    names = ["bus_stops", "merged_bus_stops", "bus_operators", "bus_routes"]
    for i in range(4):
        save_image(names[i], [v[i+2] for v in stop_rows])


if __name__ == "__main__":
    main()
