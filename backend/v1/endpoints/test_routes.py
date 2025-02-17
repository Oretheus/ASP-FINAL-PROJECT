import firebase_admin
from firebase_admin import firestore, exceptions
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/firebase-test")
async def firebase_test():
    """
    Test Firebase connection.
    """
    try:
        db = firestore.client()
        test_doc = db.collection("test_collection").document("test_doc").get()
        if test_doc.exists:
            return {"status": "connected", "message": "Firebase connected successfully", "sample_data": test_doc.to_dict()}
        else:
            return {"status": "connected", "message": "Firebase connected, but document not found"}
    except exceptions.FirebaseError as e:
        raise HTTPException(status_code=500, detail=f"Firebase error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"General error: {str(e)}")
