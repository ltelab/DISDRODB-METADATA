import os
import disdrodb
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd


STRING_FIELDS = {
    "data_source",
    "campaign_name",
    "station_name",
    "sensor_name",
    "sensor_long_name",
    "time_coverage_start",
    "time_coverage_end",
    "deployment_status",
    "location",
    "country",
    "continent",
    "title",
    "project_name",
    "institution",
    "contact",
    "authors",
    "references",
    "documentation",
    "website",
    "license",
    "doi",
    "disdrodb_data_url",
}

NUMERIC_FIELDS = {"latitude", "longitude", "altitude"}
FIELDS = {*STRING_FIELDS, *NUMERIC_FIELDS}


def generate_web_map_json(
    df: pd.DataFrame,
    stations_json_path: str | Path,
    filter_options_json_path: str | Path,
    max_duration: int | float = 25,
) -> None:
    missing = [col for col in FIELDS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df = df[df["latitude"].notna() & df["longitude"].notna()]
    df = df[df["altitude"].notna()]
    df = df[(df["latitude"] >= -90) & (df["latitude"] <= 90)]
    df = df[(df["longitude"] >= -180) & (df["longitude"] <= 180)]

    df[list(STRING_FIELDS)] = (
        df[list(STRING_FIELDS)]
        .astype("string")
        .apply(lambda c: c.str.strip())
        .fillna("")
    )
    df[list(NUMERIC_FIELDS)] = (
        df[list(NUMERIC_FIELDS)]
        .apply(pd.to_numeric, errors="coerce")
        .where(lambda x: x.notna(), None)
    )
    df["altitude"] = df["altitude"].round(0).astype(int)

    df["id"] = df["data_source"] + "/" + df["campaign_name"] + "/" + df["station_name"]

    base_url = "https://github.com/ltelab/DISDRODB-METADATA/blob/main/DISDRODB/METADATA"
    df["github_url"] = (
        base_url
        + "/"
        + df["data_source"]
        + "/"
        + df["campaign_name"]
        + "/"
        + "metadata"
        + "/"
        + df["station_name"]
        + ".yml"
    )

    df = df.sort_values(["data_source", "campaign_name", "station_name"]).reset_index(drop=True)
    df = df[[*FIELDS, "id", "github_url"]]

    list_stations_dict = [row.to_dict() for _, row in df.iterrows()]

    stations_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(list_stations_dict),
        "stations": list_stations_dict,
    }

    # exclude "" values from filter lists
    def uniq_nonempty(series: pd.Series) -> list[str]:
        return sorted({v for v in series.tolist() if isinstance(v, str) and v != ""})

    filter_options_payload = {
        "sensor_names": uniq_nonempty(df["sensor_name"]),
        "data_sources": uniq_nonempty(df["data_source"]),
        "campaign_names": uniq_nonempty(df["campaign_name"]),
        "countries": uniq_nonempty(df["country"]),
        "continents": uniq_nonempty(df["continent"]),
        "deployment_statuses": uniq_nonempty(df["deployment_status"]),
        "max_duration": max_duration,
    }

    stations_json_path = Path(stations_json_path)
    filter_options_json_path = Path(filter_options_json_path)

    stations_json_path.parent.mkdir(parents=True, exist_ok=True)
    filter_options_json_path.parent.mkdir(parents=True, exist_ok=True)

    with stations_json_path.open("w", encoding="utf-8") as f:
        json.dump(stations_payload, f, ensure_ascii=False, separators=(",", ":"))

    with filter_options_json_path.open("w", encoding="utf-8") as f:
        json.dump(filter_options_payload, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    df = disdrodb.read_metadata_archive()

    # default local output: public/data
    output_dir = Path(os.environ.get("OUTPUT_DIR", "public/data"))

    generate_web_map_json(
        df=df,
        stations_json_path=output_dir / "stations.json",
        filter_options_json_path=output_dir / "filter-options.json",
        max_duration=25,
    )
