import os
import sys
import json
from datetime import datetime
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings

# 
# from pyrfc import Connection

class OverwriteStorage(FileSystemStorage):
    """Custom storage class to overwrite files with the same name."""

    def get_available_name(self, name, max_length=None):
        """Overwrite the file if it exists."""
        if self.exists(name):
            self.delete(name)
        return name

class FileUploadManager:
    """Class to handle file upload, edit, delete, and logging."""

    def __init__(self, file_name_custom=None, allowed_extensions=None, max_file_size=None, log_mode=1):
        self.file_name_custom = file_name_custom or ''
        self.allowed_extensions = allowed_extensions or ['.png', '.jpg', '.jpeg', '.pdf']
        self.max_file_size = max_file_size or 5 * 1024 * 1024  # Default to 5 MB
        self.log_file = os.path.join(settings.MEDIA_ROOT, 'upload_logs.txt')
        self.log_mode = log_mode  # Enable or disable logging

    def _generate_file_path(self, directory, file_name, extension, use_suffix=True):
        """Generate the desired file path with an optional suffix."""
        suffix = f"{self.file_name_custom}" if use_suffix else ""
        return os.path.join(directory, f"{file_name.strip()}{suffix}{extension}")

    def _validate_file(self, file):
        """Validate file extensions and size."""
        file_name, extension = os.path.splitext(file.name)
        if extension.lower() not in self.allowed_extensions:
            raise ValueError(f"File extension '{extension}' is not allowed.")
        if file.size > self.max_file_size:
            raise ValueError(f"File size exceeds the allowed limit of {self.max_file_size / (1024 * 1024)} MB.")

    def _delete_file(self, file_path):
        """Helper function to delete a file and log the action."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.log_action("DELETE", os.path.basename(file_path), "success", "File deleted successfully.")
            else:
                self.log_action("DELETE", os.path.basename(file_path), "error", "File not found.")
        except Exception as e:
            self.log_action("DELETE", os.path.basename(file_path), "error", str(e))
            raise

    def log_action(self, action_type, file_name=None, status='success', message=''):
        """Log actions performed during file handling."""
        if self.log_mode:  # Check if logging is enabled
            with open(self.log_file, 'a') as log:
                log.write(
                    f"{datetime.now()} | {action_type} | File: {file_name or 'N/A'} | Status: {status} | Message: {message}\n"
                )

    def _save_file(self, upload_file_current, uploaded_file_path):
        """Save file to the specified path in chunks."""
        with open(uploaded_file_path, 'wb') as f:
            for chunk in upload_file_current.chunks():
                f.write(chunk)

    def handle_upload(self, upload_file_current, upload_file_temp, list_path, mode):
        """Handle file upload for different modes (SAVE, EDIT, DELETE)."""
        result = {
            'status': False,
            'filename': '',
            'message': 'Unknown error',
            'uploaded_file_path': None
        }
        try:
            # Create directory if not exists
            upload_directory = os.path.join(settings.MEDIA_ROOT, *list_path)
            os.makedirs(upload_directory, exist_ok=True)

            # Determine file paths
            uploaded_file_path = None
            if mode == 1:  # SAVE
                self._validate_file(upload_file_current)
                file_name, extension = os.path.splitext(upload_file_current.name)
                uploaded_file_path = self._generate_file_path(upload_directory, file_name, extension)
                with open(uploaded_file_path, 'wb') as f:
                    for chunk in upload_file_current.chunks():
                        f.write(chunk)
                result['filename'] = f"{file_name.strip()}{self.file_name_custom}{extension}"
                result['uploaded_file_path'] = uploaded_file_path

            elif mode == 2:  # EDIT
                self._validate_file(upload_file_current)
                # Delete temp file if it exists
                if upload_file_temp:
                    if isinstance(upload_file_temp, str):  # Case where it's a string path
                        file_path_temp = self._generate_file_path(
                            upload_directory, upload_file_temp, '', use_suffix=False
                        )
                    self._delete_file(file_path_temp)

                # Save new file
                file_name, extension = os.path.splitext(upload_file_current.name)
                uploaded_file_path = self._generate_file_path(upload_directory, file_name, extension)
                with open(uploaded_file_path, 'wb') as f:
                    for chunk in upload_file_current.chunks():
                        f.write(chunk)
                result['filename'] = f"{file_name.strip()}{self.file_name_custom}{extension}"
                result['uploaded_file_path'] = uploaded_file_path

            elif mode == 3:  # DELETE
                if upload_file_temp:
                    if isinstance(upload_file_temp, str):  # Case where it's a string path
                        file_path_temp = self._generate_file_path(
                            upload_directory, upload_file_temp, '', use_suffix=False
                        )
                    self._delete_file(file_path_temp)
            else:
                result['message'] = 'Invalid mode specified'
                return result

            # Success response
            result['status'] = True
            result['message'] = 'Operation completed successfully'

        except Exception as e:
            error_line = sys.exc_info()[-1].tb_lineno
            error_message = f"Line {error_line}: {str(e)}"
            self.log_action("ERROR", status="error", message=error_message)
            result['message'] = error_message

        return result




def generate_datetime_string(time, mode='upload'):
    """Generate a custom timestamp string."""
    return time.strftime('_%Y%m%d_%H%M%S')


class ErrorLogger:
    """Class to log errors with timestamps."""
    
    def __init__(self, log_file='error_logs.txt'):
        # Define the log folder and the log file path
        self.log_folder = 'log'
        self.log_file = os.path.join(self.log_folder, log_file)
        
        # Ensure the log folder exists
        self._create_log_folder()

    def _create_log_folder(self):
        """Create the log folder if it doesn't exist."""
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)  # Create the 'log' folder if it doesn't exist

    def log_error(self, error_message, error_time=None):
        """Log error messages with timestamp."""
        error_time = error_time or datetime.now()
        log_entry = f"{error_time} - {error_message}\n"
        
        # Write the log entry to the file inside the 'log' folder
        with open(self.log_file, 'a') as log:
            log.write(log_entry)
            
            


class FileDirectoryManager:
    """Class to manage file operations in a directory."""

    def __init__(self, base_path=None):
        self.base_path = base_path or settings.MEDIA_ROOT

    def list_files_in_directory(self, list_path):
        try:
            directory_path = os.path.join(self.base_path, *list_path)
            if not os.path.exists(directory_path):
                raise FileNotFoundError(f"Directory {directory_path} does not exist.")
            
            files = [
                f for f in os.listdir(directory_path)
                if os.path.isfile(os.path.join(directory_path, f))
            ]
            return {"status": True, "files": files, "message": "Files listed successfully"}
        
        except Exception as e:
            return {"status": False, "files": [], "message": str(e)}

    def missing_files(self, list_path, check_files):
        try:
            result = self.list_files_in_directory(list_path)
            if not result["status"]:
                return result  # Return error if directory listing failed

            existing_files = result["files"]
            missing_files = [f for f in check_files if f not in existing_files]
            return {
                "status": True,
                "missing_files": missing_files,
                "message": "Missing files checked successfully"
            }
        
        except Exception as e:
            return {"status": False, "missing_files": [], "message": str(e)}

    def all_files_exist(self, list_path, check_files):
        try:
            result = self.list_files_in_directory(list_path)
            if not result["status"]:
                return result  # Return error if directory listing failed

            existing_files = result["files"]
            all_exist = all(f in existing_files for f in check_files)
            return {
                "status": all_exist,
                "message": "All files exist" if all_exist else "Some files are missing"
            }
        
        except Exception as e:
            return {"status": False, "message": str(e)}

    def delete_file(self, list_path, file_name):
        try:
            directory_path = os.path.join(self.base_path, *list_path)
            file_path = os.path.join(directory_path, file_name)

            if not os.path.exists(file_path):
                return {"status": False, "message": f"File {file_name} does not exist."}
            
            os.remove(file_path)
            return {"status": True, "message": f"File {file_name} deleted successfully."}
        
        except Exception as e:
            return {"status": False, "message": str(e)}

    def add_file(self, list_path, file_name, file_content):
        try:
            directory_path = os.path.join(self.base_path, *list_path)
            os.makedirs(directory_path, exist_ok=True)
            
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, 'w') as file:
                file.write(file_content)

            return {"status": True, "message": f"File {file_name} created successfully."}
        
        except Exception as e:
            return {"status": False, "message": str(e)}


def connect_bapi(ntype=''):
    if(ntype=='N-1'):
        conn = Connection(user='sapconnect', passwd='lotus900', ashost= settings.IP_SAP_TEST, sysnr='00', client='100')
    elif (ntype=='PROD'):
        conn = Connection(user='sapconnect', passwd='lotus900', ashost= '192.168.0.7', sysnr='00', client='100')
    elif (ntype=='DEV'):
        conn = Connection(user='powfrfc', passwd='Mis1711!', ashost= '192.168.2.7', sysnr='00', client='302')
    else:
        conn = Connection(user='sapconnect', passwd='lotus900', ashost= settings.IP_SAP, sysnr='00', client='100')
    return conn