# vector_ai_proj

My initial thought process was to create three endpoints for inserting, updating and deleting and passing table name in post data (last version of readme). The idea was that, if we had to add new table, we would just have to pass it in data, since the operations would be same. But then I realized it would be much better architecture to implement crud for each table. So in final version we have three main endpoints ('/continent', '/country', '/city') with three methods each:

`POST /continent`

    {
        'name' : 'test_name',
        'population' : 100,
        'area' : 10.12
    }

`PUT /continent/<id>`

    {
        'name' : 'test_name',
        'population' : 100,
        'area' : 10.12
    }

`DELETE /continent/<id>`

(Same three methods for city and country)

We use celery for worker, rabbitmq for broker and redis for backend. So, for every request we have to start new task and we return that task_id in response. All the responses for above endpoints will be the same:

    {
        'ID' : "123e4567-e89b-12d3-a456-426614174000"
    }
    
And we have final endpoint for checking that task:

`GET /check_task/<task_id>`

We have three tasks in total (one for inserting, one for updating and one for deleting), described in src/app/tasks.py. Since we have one method for checking task results, all of our tasks return tuple of (ID, ok, message). All db operations are done in these tasks and db errors are handled here as well, that's why we return 'ok' as true or false, if operation succeds or not, 'message' is coresponding message for success or db error(Our triggers also raises exception. That exception is handled here as well and returns such message). And finally 'ID' will be present if and only if operation was to insert and it succeded.

I also included custom django command 'python manage.py make_triggers'. All it does is read our triggers.sql file and execute sql command. This is useful because we need our triggers for db validation and when building docker image we can run it after migrations are done and before running server(src/run_web.sh).