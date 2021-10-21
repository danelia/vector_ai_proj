from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .tasks import run_insert_task, run_update_task, run_delete_task
from project import celery_app


class ViewSetController(ModelViewSet):

    def __init__(self, model_name):
        self.model_name = model_name

    def create(self, request):
        data = self._requst_helper(request)
        if not data:
            return Response({'Message' : "Please send data"}, status=status.HTTP_400_BAD_REQUEST)

        task_id = run_insert_task.delay(self.model_name, data)
        
        return Response({'ID' : task_id.id}, status=status.HTTP_200_OK)

    def update(self, request, entry_id):
        data = self._requst_helper(request)
        if not data:
            return Response({'Message' : "Please send data"}, status=status.HTTP_400_BAD_REQUEST)

        task_id = run_update_task.delay(self.model_name, data, entry_id)

        return Response({'ID' : task_id.id}, status=status.HTTP_200_OK)

    def delete(self, request, entry_id):
        task_id = run_delete_task.delay(self.model_name, entry_id)

        return Response({'ID' : task_id.id}, status=status.HTTP_200_OK)
    
    def _requst_helper(self, request):
        data = request.data
        data.pop("id", None)

        return data

class ContinentViewSet(ViewSetController):
    def __init__(self):
        super().__init__("Continent")

class CountryViewSet(ViewSetController):
    def __init__(self):
        super().__init__("Country")

class CityViewSet(ViewSetController):
    def __init__(self):
        super().__init__("City")

@api_view(['GET'])
def check_task(request, task_id):
    st = celery_app.AsyncResult(task_id)

    if not st.ready():
        return Response({'Message' : 'No results for that task_id'}, status=status.HTTP_200_OK)
    
    res, ok, message = st.result
    resp = {'Message' : message}

    if res is not None:
        resp['ID'] = res

    return Response(resp, status=status.HTTP_200_OK if ok else status.HTTP_400_BAD_REQUEST)
