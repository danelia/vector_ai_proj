import functools as ft

def request_validator(method_name):
    def decorator(func):

        @ft.wraps(func)
        def wrapper(*args, **kwargs):
            req = args[0]

            res = {'table_name' : req.data.get('Name', None)}

            values = req.data.get('Values', None)
            target_id = req.data.get('ID', None)
    
            if res['table_name'] is None or res['table_name'] not in ['Continent', 'Country', 'City']:
                m = 'Please make sure Name parameter is one of these: Continent, Country, City'
                return Response({'Message' : m}, status=status.HTTP_400_BAD_REQUEST)
            else:
                if method_name == 'insert' or method_name == 'update':
                    if not values:
                        m = 'Please send Values'
                        return Response({'Message' : m}, status=status.HTTP_400_BAD_REQUEST)
        
                    values.pop('id', None)
                    res['values'] = values
                if method_name == 'update' or method_name == 'delete':
                    if target_id is None:
                        m = 'Please send ID'
                        return Response({'Message' : m}, status=status.HTTP_400_BAD_REQUEST)
                    
                    res['target_id'] = target_id
            return func(**res)
        return wrapper
    return decorator