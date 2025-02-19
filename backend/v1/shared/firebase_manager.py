import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app, exceptions
import asyncio
import logging

class FirebaseClient:
    _instance = None

    @staticmethod
    def get_instance():
        if FirebaseClient._instance is None:
            cred_path = "/etc/secrets/FIREBASE_CREDENTIALS.json"
            if not cred_path or not os.path.exists(cred_path):
                raise FileNotFoundError(
                    f"Missing Firebase credentials file at {cred_path}."
                )
            # Initialize Firebase client
            cred = credentials.Certificate(cred_path)
            initialize_app(cred)
            FirebaseClient._instance = firestore.client()
        
        return FirebaseClient._instance

    @staticmethod
    def test_connection():
        """
        Test Firebase connection by retrieving a document from a test collection.
        """
        try:
            db = FirebaseClient.get_instance()
            test_doc = db.collection("test_collection").document("test_doc").get()
            if test_doc.exists:
                logging.info("Firebase connection test successful.")
                return {"status": "connected", "message": "Firebase connection successful", "sample_data": test_doc.to_dict()}
            else:
                logging.warning("Firebase connection successful, but test document not found.")
                return {"status": "connected", "message": "Firebase connection successful, but document not found"}
        except exceptions.FirebaseError as e:
            logging.error(f"Firebase connection error: {e}")
            return {"status": "error", "message": f"Firebase error: {e}"}
        except Exception as e:
            logging.error(f"General connection error: {e}")
            return {"status": "error", "message": f"General error: {e}"}

class FirebaseManager:
    def __init__(self):
        self.db = FirebaseClient.get_instance() # Initialize Client

    def test_firebase_connection(self) -> dict:
        """
        Test Firebase connection using the FirebaseClient's test_connection method.
        """
        return FirebaseClient.test_connection()

    # --------------------
    # CRUD Functions
    # --------------------
    def store_data(self, collection: str, document_id: str, data: dict) -> dict:
        """
        Store or update a document.
        """
        try:
            self.db.collection(collection).document(document_id).set(data)
            return {"message": "Data successfully stored", "document_id": document_id}
        except Exception as e:
            return {"error": str(e)}

    def get_data(self, collection: str, document_id: str) -> dict:
        """
        Retrieve a document with error handling and timeout.
        """
        try:
            doc = self.db.collection(collection).document(document_id).get()
            if doc.exists:
                return doc.to_dict()
            else:
                return {"error": "Document not found"}
        except FirebaseError as e:
            return {"error": f"Firebase error: {str(e)}"}
        except Exception as e:
            return {"error": f"General error: {str(e)}"}

    async def async_get_data(self, collection: str, document_id: str) -> dict:
        """
        Retrieve a document asynchronously from Firebase.
        """
        try:
            loop = asyncio.get_event_loop()
            doc = await loop.run_in_executor(None, 
                lambda: self.db.collection(collection).document(document_id).get()
            )
            if doc.exists:
                return doc.to_dict()
            else:
                return {"error": "Document not found"}
        except exceptions.FirebaseError as e:
            return {"error": f"Firebase error: {str(e)}"}
        except Exception as e:
            return {"error": f"General error: {str(e)}"}

    # --------------------
    # User Functions
    # --------------------
    def get_user_data(self, collection: str, email: str) -> Optional[dict]:
        """
        Fetch a user by email.
        """
        user_docs = self.db.collection(collection).where(field_path="email", op_string="==", value=email).stream()
        if not user_docs:
            return None

        # Process the first document
        for doc in user_docs:
            user_data = doc.to_dict()
            return {
                "user_id": doc.id,
                "email": user_data["email"],
                "password_hash": user_data["password_hash"],
                "role": user_data["role"]
            }

        return None

    # ---------------------
    # Search Functions
    # --------------------
    def store_user_search(self, user_id: str, query: str, location: str, job_ids: list, next_page_token: str) -> dict:
        """
        Log user's search in the 'user_searches' collection.
        """
        search_id = str(uuid.uuid4())
        search_data = {
            "search_id": search_id,
            "user_id": user_id,
            "query": query,
            "location": location,
            "search_date": datetime.now(timezone.utc),
            "job_ids": job_ids,
            "next_page_token": next_page_token,
        }
        self.store_data("user_searches", search_id, search_data)
        return search_id

    # --------------------
    # Job Functions
    # --------------------
    def store_job(self, job_id: str, job_data: dict) -> dict:
        """
        Store a job in the 'jobs' collection.
        """
        return self.store_data("jobs", job_id, job_data)

    def fetch_job(self, job_id: str) -> dict:
        """
        Fetch a specific job by ID.
        """
        return self.get_data("jobs", job_id)

    def fetch_jobs_for_search(self, job_ids: list) -> list:
        """
        Fetch jobs based on a list of job IDs.
        """
        jobs = []
        for job_id in job_ids:
            job = self.fetch_job(job_id)
            if "error" not in job:
                jobs.append(job)
        return jobs

    # --------------------
    # Application Functions
    # --------------------
    def save_application(self, user_id: str, job_id:str) -> dict:
        """Save application."""
        return {"message": "Application saved successfully", "application_id": application_id}
    
    def update_application_status(self, application_id: str, new_status: str, comments: str) -> dict:
        """Update an application status"""
        return {"message": f"Application status updated to {new_status}"}

    def get_application_status(self, application_id: str) -> dict:
        """Get an application details"""
        return application_doc

    def get_user_applications(self, user_id: str) -> list:
        """Get all applications submitted by a user"""
        return user_applications