import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union


DATA_FILE = Path(__file__).with_name("data.json")


@dataclass
class Garment:
    name: str
    size: str
    water_impact: Optional[float] = None
    carbon_emissions: Optional[float] = None
    textile_waste: Optional[float] = None

    @classmethod
    def from_record(cls, record: dict) -> "Garment":
        if not isinstance(record, dict):
            raise ValueError("Each garment in data.json must be an object.")

        name = record.get("item")
        details = record.get("details")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Each garment must have a non-empty item name.")
        if not isinstance(details, dict):
            raise ValueError(f"Garment {name!r} must have a details object.")

        size = details.get("size")
        if not isinstance(size, str) or not size.strip():
            raise ValueError(f"Garment {name!r} must have a non-empty size.")

        return cls(
            name=name,
            size=size,
            water_impact=_optional_number(details.get("water"), "water"),
            carbon_emissions=_optional_number(details.get("carbon"), "carbon"),
            textile_waste=_optional_number(details.get("waste"), "waste"),
        )

    def to_record(self) -> dict:
        return {
            "item": self.name,
            "details": {
                "size": self.size,
                "water": self.water_impact,
                "carbon": self.carbon_emissions,
                "waste": self.textile_waste,
            },
        }


def _optional_number(value: object, field_name: str) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number or null in data.json.")
    if not math.isfinite(value):
        raise ValueError(f"{field_name} must be a finite number in data.json.")
    return value


def load_garments(
    file_path: Union[str, Path] = DATA_FILE,
) -> list[Garment]:
    with Path(file_path).open("r", encoding="utf-8") as data_file:
        records = json.load(data_file)

    if not isinstance(records, list):
        raise ValueError("data.json must contain a list of garments.")
    return [Garment.from_record(record) for record in records]


def save_garments(
    garments: list[Garment], file_path: Union[str, Path] = DATA_FILE
) -> None:
    records = [garment.to_record() for garment in garments]
    with Path(file_path).open("w", encoding="utf-8") as data_file:
        json.dump(records, data_file, indent=2, allow_nan=False)
        data_file.write("\n")
