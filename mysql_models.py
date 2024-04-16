# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Appointment(models.Model):
    recno = models.AutoField(db_column='RECNO', primary_key=True)  # Field name made lowercase.
    created = models.DateTimeField(db_column='CREATED', blank=True, null=True)  # Field name made lowercase.
    lastupd = models.DateTimeField(db_column='LASTUPD', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=2, blank=True, null=True)  # Field name made lowercase.
    cust = models.IntegerField(db_column='CUST', blank=True, null=True)  # Field name made lowercase.
    docno = models.CharField(db_column='DOCNO', max_length=15, blank=True, null=True)  # Field name made lowercase.
    custname = models.CharField(db_column='CUSTNAME', max_length=250, blank=True, null=True)  # Field name made lowercase.
    cont = models.IntegerField(db_column='CONT', blank=True, null=True)  # Field name made lowercase.
    contname = models.CharField(db_column='CONTNAME', max_length=250, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=200, blank=True, null=True)  # Field name made lowercase.
    addr = models.CharField(db_column='ADDR', max_length=200, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='LOCATION', max_length=3, blank=True, null=True)  # Field name made lowercase.
    subject = models.CharField(db_column='SUBJECT', max_length=150, blank=True, null=True)  # Field name made lowercase.
    detail = models.CharField(db_column='DETAIL', max_length=500, blank=True, null=True)  # Field name made lowercase.
    ref = models.CharField(db_column='REF', max_length=500, blank=True, null=True)  # Field name made lowercase.
    priority = models.CharField(db_column='PRIORITY', max_length=2, blank=True, null=True)  # Field name made lowercase.
    timed = models.IntegerField(db_column='TIMED', blank=True, null=True)  # Field name made lowercase.
    timeh = models.IntegerField(db_column='TIMEH', blank=True, null=True)  # Field name made lowercase.
    timem = models.IntegerField(db_column='TIMEM', blank=True, null=True)  # Field name made lowercase.
    startd = models.DateField(db_column='STARTD', blank=True, null=True)  # Field name made lowercase.
    warnd = models.DateField(db_column='WARND', blank=True, null=True)  # Field name made lowercase.
    pricecost = models.DecimalField(db_column='PRICECOST', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pricepwithdraw = models.DecimalField(db_column='PRICEPWITHDRAW', max_digits=18, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    owner = models.IntegerField(db_column='OWNER', blank=True, null=True)  # Field name made lowercase.
    ownername = models.CharField(db_column='OWNERNAME', max_length=120, blank=True, null=True)  # Field name made lowercase.
    remark = models.CharField(db_column='REMARK', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'appointment'


class Bom(models.Model):
    bomid = models.IntegerField(db_column='BOMID', primary_key=True)  # Field name made lowercase.
    parentproductid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ParentProductID', blank=True, null=True)  # Field name made lowercase.
    componentproductid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ComponentProductID', related_name='bom_componentproductid_set', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(db_column='Level', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bom'


class Bomproc(models.Model):
    parentproductid = models.OneToOneField('Product', models.DO_NOTHING, db_column='ParentProductID', primary_key=True)  # Field name made lowercase. The composite primary key (ParentProductID, ComponentProductID) found, that is not supported. The first column is selected.
    componentproductid = models.ForeignKey('Product', models.DO_NOTHING, db_column='ComponentProductID', related_name='bomproc_componentproductid_set')  # Field name made lowercase.
    level = models.IntegerField(db_column='Level', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bomproc'
        unique_together = (('parentproductid', 'componentproductid'),)


class Empl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    code = models.CharField(db_column='CODE', unique=True, max_length=16, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'empl'


class Employees(models.Model):
    name = models.CharField(max_length=100)
    score = models.FloatField()
    grade = models.CharField(max_length=1, db_collation='latin1_swedish_ci')

    class Meta:
        managed = False
        db_table = 'employees'


class Product(models.Model):
    productid = models.IntegerField(db_column='ProductID', primary_key=True)  # Field name made lowercase.
    productname = models.CharField(db_column='ProductName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'product'


class Student(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=1, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    fileblob = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Students(models.Model):
    idc = models.CharField(max_length=13, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    detail = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    tier = models.CharField(max_length=1, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'


class T1(models.Model):
    a = models.IntegerField(unique=True, blank=True, null=True)
    b = models.IntegerField(unique=True, blank=True, null=True)
    c = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't1'


class TblCounter(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_datesave = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_counter'
