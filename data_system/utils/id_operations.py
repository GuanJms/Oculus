# Import the uuid library which is used for generating unique identifiers
import uuid


def generate_unique_uuid() -> str:
    # Generate a random UUID (Universally Unique Identifier)
    unique_id = uuid.uuid4()
    return str(unique_id)

# Uncomment the line below to test the function
# print(generate_unique_uuid())
