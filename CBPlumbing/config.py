import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
        
    

class QueryConfig(object):
    JOB_STATUS_LIST = ['Open', 'In Progress', 'Complete']
    INVOICE_STATUS_LIST = ['Open', 'Issued', 'Paid']
    CUSTOMER_STATUS_LIST = ['Active', 'Inactive']
    JOB_TYPE_LIST = ['Service', 'Warranty', 'Install', 'Repair', 'Other']
    JOB_PRIORITY_LIST = ['Low', 'Medium', 'High']
    
    