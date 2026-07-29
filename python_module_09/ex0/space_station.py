try:
    import sys
    from datetime import datetime
    from pydantic import BaseModel, Field, ValidationError
except ImportError as e:
    print(f"\nerror: {e}")
    print("Create venv: python -m venv env")
    print("Activate: source env/bin/activate")
    print("Install pydantic")
    print("And then: python space_station.py\n")
    sys.exit(1)


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    Name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


if __name__ == "__main__":
    try:
        user = SpaceStation(
            station_id="ISS001",
            Name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="Operational")

        print("Space Station Data Validation")
        print("=" * 40)
        print("Valid station created:")
        print(f"ID: {user.station_id}")
        print(f"Name: {user.Name}")
        print(f"Crew: {user.crew_size} poeple")
        print(f"Power: {user.power_level}%")
        print(f"Oxygen: {user.oxygen_level}")
        print(f"Status: {user.notes}\n")
        print("=" * 40)
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])

    try:
        user = SpaceStation(
            station_id="ISS001",
            Name="International Space Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes="Operational"
        )

        print(f"Crew: {user.crew_size} poeple")
        print(f"Power: {user.power_level}%")
        print(f"Oxygen: {user.oxygen_level}")
        print(f"Status: {user.notes}\n")
        print(f"ID: {user.station_id}")
        print(f"Name: {user.Name}")

    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            print(error["msg"])
