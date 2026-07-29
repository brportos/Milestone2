try:
    from enum import Enum
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from datetime import datetime
    import sys
except ImportError as e:
    print(f"\nError: {e}")
    print("Create venv: python -m venv env")
    print("Activate: source env/bin/activate")
    print("Install pydantic")
    print("And then: python alien_contact.py\n")
    sys.exit(1)


class RankEnum(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMemberModel(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: RankEnum
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMissionModel(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMemberModel] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def mission_validation_rules(self) -> "SpaceMissionModel":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if not any(
            member.rank in (RankEnum.CAPTAIN, RankEnum.COMMANDER)
            for member in self.crew
        ):
            raise ValueError("Must have at least one Commander or Captain")
        if (
            self.duration_days > 365 and sum(
                member.years_experience >= 5 for member in self.crew
                ) < len(self.crew)/2
        ):
            raise ValueError(
                "Long missions (> 365 days) need 50%"
                "experienced crew (5+ years)"
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


if __name__ == "__main__":
    try:
        space = SpaceMissionModel(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMemberModel(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=RankEnum.COMMANDER.value,
                    age=42,
                    specialization="Mission Command",
                    years_experience=20
                ),
                CrewMemberModel(
                    member_id="C002",
                    name="John Smith",
                    rank=RankEnum.LIEUTENANT.value,
                    age=34,
                    specialization="Navigation",
                    years_experience=10
                ),
                CrewMemberModel(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=RankEnum.OFFICER.value,
                    age=28,
                    specialization="Engineering",
                    years_experience=5
                ),
            ],
            mission_status="planet",
            budget_millions=2500.0
        )

        print("Space Mission Crew Validation")
        print("=" * 40)
        print("Valid mission created:")
        print(f"Mission: {space.mission_name}")
        print(f"ID: {space.mission_id}")
        print(f"Destination: {space.destination}")
        print(f"Duration: {space.duration_days} days")
        print(f"Budget: ${space.budget_millions}M")
        print(f"Crew size: {len(space.crew)}")
        print("Crew members:")
        for member in space.crew:
            print(
                f"- {member.name} ({member.rank.value})"
                f"- {member.specialization}"
                )

        print()
        print("=" * 40)

    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])

    try:
        space = SpaceMissionModel(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMemberModel(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=RankEnum.OFFICER.value,
                    age=42,
                    specialization="Mission Command",
                    years_experience=20
                ),
                CrewMemberModel(
                    member_id="C002",
                    name="John Smith",
                    rank=RankEnum.LIEUTENANT.value,
                    age=34,
                    specialization="Navigation",
                    years_experience=10
                ),
                CrewMemberModel(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=RankEnum.OFFICER.value,
                    age=28,
                    specialization="Engineering",
                    years_experience=5
                ),
            ],
            mission_status="planet",
            budget_millions=2500.0
        )

        for member in space.crew:
            print(f"- {member.name} ({member.rank}) - {member.specialization}")

        print(f"Mission: {space.mission_name}")
        print(f"ID: {space.mission_id}")
        print(f"Destination: {space.destination}")
        print(f"Duration: {space.duration_days} days")
        print(f"Budget: ${space.budget_millions}M")
        print(f"Crew size: {len(space.crew)}")

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"].replace("Value error,", "Mission"))
