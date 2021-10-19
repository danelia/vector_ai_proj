from django.db.utils import InternalError

from .models import Continent, Country, City

# returns tupple of (id_, ok, message)
# if something goes with sql trigger we will get message
def run_insert_task(table_name, values):
    Model = model_picker(table_name)
    
    try:
        curr_object = Model(**values)
        curr_object.save()
    except InternalError as e:
        return None, False, str(e).split('\n')[0]
    except:
        return None, False, None
    
    return curr_object.id, curr_object.id is not None, None

def run_update_task(table_name, target_id, values):
    Model = model_picker(table_name)

    try:
        res = Model.objects.filter(id=target_id).update(**values)
    except InternalError as e:
        return None, False, str(e).split('\n')[0]
    except:
        return None, False, None
    
    return res, True, None
    

def run_delete_task(table_name, target_id):
    Model = model_picker(table_name)

    res, _ = Model.objects.filter(id=target_id).delete()

    return res

def model_picker(table_name):
    if table_name == 'Continent':
        return Continent
    elif table_name == 'Country':
        return Country
    elif table_name == 'City':
        return City
