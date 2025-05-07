from firebase_admin import credentials, storage
import firebase_admin
import uuid
import datetime

class CloudStorage:
    _storage = None
    _app = None
    _cred = None

    def __new__(cls):
        if cls._storage == None:
            cls._initialize(cls)
            cls._storage = super(CloudStorage, cls).__new__(cls)
        return cls._storage
    
    def _initialize(self):
        self._storage_url = {"storageBucket": "bananatrends.firebasestorage.app"}
        self._cred = credentials.Certificate("bananatrends-firebase-adminsdk-fbsvc-14e3aa89f7.json")
        self._app = firebase_admin.initialize_app(self._cred, self._storage_url, name = "storage")

    def UploadFile(self, file_content, file_name, file_type="pdf"):
        """
        Saves a file to Google Storage. Only works from PDF.

        Args:
            file_content (pdf): The pdf-file. 
        Returns:
            download_url (json): Link to download the saved file in storage.
        """

        bucket = storage.bucket(app = self._app)

        blob = bucket.blob(file_name)
        blob.upload_from_filename(f"{file_name}.pdf", content_type='application/pdf')
        download_url = blob.generate_signed_url(expiration=datetime.timedelta(days=7))

        return {"download_url": download_url}