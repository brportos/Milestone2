try:
    import sys
    from pydantic import BaseModel, Field, ValidationError, model_validator
    from enum import Enum
    from datetime import datetime
except ImportError as e:
    print(f"\nError: {e}")
    print("Create venv: python -m venv env")
    print("Activate: source env/bin/activate")
    print("Install pydantic")
    print("And then: python alien_contact.py\n")
    sys.exit(1)


class ContactTypeEnum(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class ContactType(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactTypeEnum
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def custom_validation_rules(self) -> "ContactType":
        if not self.contact_id.startswith('AC'):
            raise ValueError("Contact ID must start with 'AC'")
        if (
            self.contact_type == ContactTypeEnum.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactTypeEnum.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


if __name__ == "__main__":
    try:
        contact = ContactType(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactTypeEnum.RADIO.value,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )

        print("Alien Contact Log Validation")
        print("=" * 40)
        print("Valid contact report:")
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Witnesses: {contact.witness_count}")
        print(f"Message: '{contact.message_received}'\n")
        print("=" * 40)

    except ValidationError as e:
        for err in e.errors():
            print(err["msg"])

    try:
        contacts = ContactType(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactTypeEnum.TELEPATHIC.value,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=1,
            message_received="Greetings from Zeta Reticuli",
        )
        print(f"Witnesses: {contacts.witness_count}")
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Message: '{contact.message_received}'\n")

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"].replace("Value error,", "").strip())
