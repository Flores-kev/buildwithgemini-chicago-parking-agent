"""Seed script for initializing Firestore parking_records collection.

Project ID is explicitly hardcoded to prevent Agent Platform project number resolution issues.
"""

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-1a24275fdf4b"
COLLECTION_NAME = "parking_records"


def seed_firestore_records() -> None:
    """Seeds default parking records into Cloud Firestore."""
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    records = [
        {
            "id": "spot-1200-milwaukee",
            "address": "1200 N Milwaukee Ave, Chicago, IL 60622",
            "license_plate": "IL-WINDY312",
            "ward": 2,
            "section": "04",
            "status": "PARKED",
            "notes": "Near W Division St intersection. Check street sweeping schedule for Ward 2, Section 04.",
            "created_at": "2026-09-01T10:00:00Z",
        },
        {
            "id": "spot-2400-clark",
            "address": "2400 N Clark St, Chicago, IL 60614",
            "license_plate": "IL-CHI8890",
            "ward": 43,
            "section": "02",
            "status": "MOVED",
            "notes": "Winter Overnight Parking Ban arterial route. Relocated to side street.",
            "created_at": "2026-09-01T08:15:00Z",
        },
        {
            "id": "spot-800-michigan",
            "address": "800 N Michigan Ave, Chicago, IL 60611",
            "license_plate": "IL-WINDY312",
            "ward": 42,
            "section": "01",
            "status": "PARKED",
            "notes": "Magnificent Mile parking zone. Pre-warning alert set for 3 hours before enforcement.",
            "created_at": "2026-09-01T14:20:00Z",
        },
    ]

    for item in records:
        doc_id = item["id"]
        doc_ref = collection_ref.document(doc_id)
        doc_ref.set(item)
        print(f"Seeded Firestore document: {COLLECTION_NAME}/{doc_id}")

    print("Firestore seeding complete!")


if __name__ == "__main__":
    seed_firestore_records()
