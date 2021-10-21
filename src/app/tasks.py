from django.db.utils import InternalError

from .models import Continent, Country, City

from project import celery_app

# all tasks will return tuple of (ID, ok, Message)
# ok will be true or false depending on success of operation
# ID will be always None except succesful insert. If we get ID 
# from task it will mean insert was succesful.

@celery_app.task(bind=True)
def run_insert_task(self, model_name, data):  
    model = model_picker(model_name)

    try:
        curr_object = model(**data)
        curr_object.save()
    except InternalError as e:
        return None, False, str(e).split('\n')[0]
    except:
        return None, False, 'Please make sure you send right Values'
    
    return curr_object.id, True, 'Operation Succesful!'

@celery_app.task(bind=True)
def run_update_task(self, model_name, data, entry_id):
    model = model_picker(model_name)

    try:
        res = model.objects.filter(id=entry_id).update(**data)
    except InternalError as e:
        return None, False, str(e).split('\n')[0]
    except:
        return None, False, 'Please make sure you send right Values'

    if res == 0:
        return None, False, 'No entry with that ID'
    
    return None, True, 'Operation Succesful!'
    
@celery_app.task(bind=True)
def run_delete_task(self, model_name, entry_id):
    model = model_picker(model_name)

    res, _ = model.objects.filter(id=entry_id).delete()

    if res == 0:
        return None, False, 'No entry with that ID'

    return None, True, f'Success! Deleted {res} rows.'

def model_picker(table_name):
    if table_name == 'Continent':
        return Continent
    elif table_name == 'Country':
        return Country
    elif table_name == 'City':
        return City
