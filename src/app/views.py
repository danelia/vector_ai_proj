from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import run_insert_task, run_update_task, run_delete_task
from .helpers import request_validator

@api_view(['POST'])
@request_validator(method_name='insert')
def insert(table_name, values):
    id_, ok, message = run_insert_task(table_name, values)

    if message is not None:
        return Response({'Message' : message}, status=status.HTTP_400_BAD_REQUEST)
    if not ok:
        # this will only happen if Values dict has wrong field names for selected table
        return Response({'Message' : 'Please make sure you send right Values'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'Message' : 'Operation succesful!', 'ID' : id_}, status=status.HTTP_200_OK)

@api_view(['POST'])
@request_validator(method_name='update')
def update(table_name, target_id, values):
    rows_n, ok, message = run_update_task(table_name, target_id, values)
    
    if message is not None:
        return Response({'Message' : message}, status=status.HTTP_400_BAD_REQUEST)
    if not ok:
        return Response({'Message' : 'Please make sure you send right Values'}, status=status.HTTP_400_BAD_REQUEST)
    if rows_n == 0:
        return Response({'Message' : 'No entry with that ID'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'Message' : 'Operation succesful!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@request_validator(method_name='delete')
def delete(table_name, target_id):
    rows_n = run_delete_task(table_name, target_id)
    
    if rows_n == 0:
        return Response({'Message' : 'No entry with that ID'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'Message' : 'Operation Succesfull!', 'Deleted_Rows' : rows_n}, status=status.HTTP_200_OK)
