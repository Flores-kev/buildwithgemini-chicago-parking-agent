"""Firestore function tools for managing saved Chicago parking records.

Hardcodes PROJECT_ID as a string constant so it functions reliably on Agent Platform runtime.
"""

import datetime
from typing import Any
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-03-1a24275fdf4b"
COLLECTION_NAME = "parking_records"


def _get_firestore_client() -> firestore.Client:
    """Returns a Firestore Client bound to the explicit project ID string."""
    return firestore.Client(project=PROJECT_ID)


def save_parking_record(
    address: str,
    license_plate: str = "IL-CHICAGO",
    notes: str = "",
    ward: int = 1,
    section: str = "01",
) -> dict[str, Any]:
    """Saves a user's parked vehicle location into the Firestore parking_records collection.

    Args:
        address: The Chicago street address where the vehicle is parked (e.g. '1200 N Milwaukee Ave').
        license_plate: The vehicle license plate identifier.
        notes: Optional parking details or notes.
        ward: Chicago Ward number.
        section: Chicago Ward Section identifier.

    Returns:
        A dictionary containing the saved parking record details and doc ID.
    """
    db = _get_firestore_client()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    doc_id = f"spot-{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"

    record_data = {
        "id": doc_id,
        "address": address,
        "license_plate": license_plate,
        "ward": ward,
        "section": section,
        "status": "PARKED",
        "notes": notes,
        "created_at": now_iso,
    }

    db.collection(COLLECTION_NAME).document(doc_id).set(record_data)
    return {
        "status": "SUCCESS",
        "message": f"Successfully saved parking record for {address}",
        "record": record_data,
    }


def get_parking_records(limit: int = 5) -> list[dict[str, Any]]:
    """Retrieves saved parking records from the Firestore parking_records collection.

    Args:
        limit: Maximum number of recent parking records to fetch.

    Returns:
        A list of dictionary objects representing saved parking records.
    """
    db = _get_firestore_client()
    docs = db.collection(COLLECTION_NAME).limit(limit).stream()
    records = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        records.append(data)

    return records


def update_parking_record_status(
    record_id: str, status: str, notes: str = ""
) -> dict[str, Any]:
    """Updates the status (e.g., 'PARKED', 'RELOCATED', 'MOVED', 'WARNING_ISSUED') of a saved parking record in Firestore.

    Args:
        record_id: The document ID of the parking record (e.g. 'spot-1200-milwaukee').
        status: The new status string to apply.
        notes: Optional updated notes.

    Returns:
        A dictionary confirming the update operation.
    """
    db = _get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(record_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {
            "status": "ERROR",
            "message": f"Parking record with ID '{record_id}' not found.",
        }

    update_payload = {"status": status}
    if notes:
        update_payload["notes"] = notes

    doc_ref.update(update_payload)
    return {
        "status": "SUCCESS",
        "message": f"Updated status of record '{record_id}' to '{status}'",
        "record_id": record_id,
        "new_status": status,
    }
