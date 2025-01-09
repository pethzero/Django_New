from django.db import models, transaction
from myapp.models import *
import sys

class Process:
    def __init__(self):
        self.result = {}
        self.status = True  # ใช้ Boolean เพื่อความง่าย
        self.message = ''
        self.savepoint = None  # เก็บ savepoint

    def DBcreate(self, param, name, engine):
        """
        Dynamically create a database object with manual control for commit and rollback.
        """
        try:
            # Fetch model dynamically
            db_name = globals().get(name)
            if not db_name:
                raise ValueError(f"Invalid model name: {name}")

            # Start transaction and create savepoint
            with transaction.atomic(using=engine):
                self.savepoint = transaction.savepoint(using=engine)

                # Save object to database
                obj_db = db_name.objects.using(engine).create(**param)

                self.message = "Object created successfully"
                self.result = {
                    'status': self.status,
                    'message': self.message,
                    'obj_db': obj_db
                }
        except Exception as e:
            # Handle exceptions and set status to False
            print(f"{sys.exc_info()[-1].tb_lineno} : {str(e)}")
            self.status = False
            self.result = {
                'status': self.status,
                'message': f"Error: {str(e)}",
                'obj_db': None
            }

        return self.result

    def commit(self, engine):
        """Commit the transaction."""
        if self.savepoint:
            transaction.savepoint_commit(self.savepoint, using=engine)
            print("Transaction committed")
        else:
            print("No savepoint found to commit")

    def rollback(self, engine):
        """Rollback the transaction."""
        if self.savepoint:
            transaction.savepoint_rollback(self.savepoint, using=engine)
            print("Transaction rolled back")
        else:
            print("No savepoint found to rollback")
