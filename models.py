from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from cmpMgmtServices import app

db = SQLAlchemy(app)

class Campaign(db.Model):
    __tablename__ = "campaign"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_name = db.Column('campaign_name', db.Unicode)
    strategy_number = db.Column('strategy_number', db.Integer)
    marketing_channel = db.Column('marketing_channel', db.Unicode)
    campaign_drop_dt = db.Column('campaign_drop_dt', db.Date, default=datetime.utcnow)
    campaign_effective_dt = db.Column('campaign_effective_dt', db.Date, default=datetime.utcnow)
    eligible_population_type = db.Column('eligible_population_type', db.Unicode)
    line_of_business = db.Column('line_of_business', db.Unicode)
    # privacy_suppression_ind = db.Column('privacy_suppression_ind', db.BOOLEAN)
    output_table_name = db.Column('output_table_name', db.Unicode)
    input_file_url = db.Column('input_file_url', db.Unicode)
    input_file_type = db.Column('input_file_type', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)
    filters = db.relationship('Filters', backref="parent", lazy='dynamic')
    sorts = db.relationship('Sorts', backref="parent", lazy='dynamic')
    dedups = db.relationship('Dedups', backref="parent", lazy='dynamic')
    minus = db.relationship('Minus', backref="parent", lazy='dynamic')
    classifies = db.relationship('Classifies', backref="parent", lazy='dynamic')
    distributes = db.relationship('Distributes', backref="parent", lazy='dynamic')

class Filters(db.Model):
    __tablename__ = "filters"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    filter_column = db.Column('filter_column', db.Unicode)
    filter_operator = db.Column('filter_operator', db.Unicode)
    filter_value = db.Column('filter_value', db.Unicode)
    input_table_name = db.Column('input_table_name', db.Unicode)
    output_table_name = db.Column('output_table_name', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)

class Sorts(db.Model):
    __tablename__ = "sorts"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    sort_keys = db.Column('sort_keys', db.Unicode)
    order = db.Column('order', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)


class Dedups(db.Model):
    __tablename__ = "dedups"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    unique_fields = db.Column('unique_fields', db.Unicode)
    dedup_fields = db.Column('dedup_fields', db.Unicode)
    dedup_function = db.Column('dedup_function', db.Unicode)
    description = db.Column('description', db.Unicode)
    input_table_name = db.Column('input_table_name', db.Unicode)
    output_table_name = db.Column('output_table_name', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('created_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('created_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)


class Minus(db.Model):
    __tablename__ = "minus"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    s3input_table = db.Column('s3input_table', db.Unicode)
    readfile_seq = db.Column('readfile_seq', db.Integer)
    minus_seq = db.Column('minus_seq', db.Integer)
    input_table_name = db.Column('input_table_minus', db.Unicode)
    read_table_output = db.Column('read_table_output', db.Unicode)
    output_table_name = db.Column('output_table_minus', db.Unicode)
    inserted_dt = db.Column('created_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('created_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)



class Classifies(db.Model):
    __tablename__ = "classifies"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    input_table_name = db.Column('input_table_name', db.Unicode)
    output_table_name = db.Column('output_table_name', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)
    classify_rules = db.relationship('Classify_rules', backref="parent", lazy='dynamic')


class Classify_rules(db.Model):
    __tablename__ = "classify_rules"
    id = db.Column('id', db.Integer, primary_key=True)
    classify_id = db.Column(db.Integer, db.ForeignKey('classifies.id'))
    vendor_cell_value = db.Column('vendor_cell_value', db.Unicode)
    vendor_cell_description = db.Column('vendor_cell_description', db.Unicode)
    classify_rule_order = db.Column('classify_rule_order', db.Integer)
    expressions = db.Column('expressions', db.Unicode)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)


class Distributes(db.Model):
    __tablename__ = "distributes"
    id = db.Column('id', db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'))
    input_table_name = db.Column('input_table_name', db.Unicode)
    output_table_name = db.Column('output_table_name', db.Unicode)
    rule_seq = db.Column('rule_seq', db.Integer)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)
    distribute_rules = db.relationship('Distribute_rules', backref="parent", lazy='dynamic')

class Distribute_rules(db.Model):
    __tablename__ = "distribute_rules"
    id = db.Column('id', db.Integer, primary_key=True)
    distribute_id = db.Column(db.Integer, db.ForeignKey('distributes.id'))
    distribute_rule_order = db.Column('distribute_rule_order', db.Integer)
    expressions = db.Column('expressions', db.Unicode)
    test_cell_weight = db.Column('test_cell_weight', db.Float)
    controlled_cell_weight = db.Column('controlled_cell_weight', db.Float)
    inserted_dt = db.Column('inserted_dt', db.Date, default=datetime.utcnow)
    inserted_by = db.Column('inserted_by', db.Unicode)
    updated_dt = db.Column('updated_dt', db.Date, default=datetime.utcnow)
    updated_by = db.Column('updated_by', db.Unicode)
