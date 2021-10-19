# vector_ai_proj

### Part 1

We will use PostgreSQL for our database. We will have three tables: Continent, Country and City. Our validation check for population and area will be handled by triggers (src/triggers.sql) and errors we will handled in python.

I implemented three apis for inserting (/insert), updating (/update) and deleting (/delete). 

`POST /insert`

    {
        'Name' : 'Continent',
        'Values' : {
            'name' : 'test_name',
            'population' : 100,
            'area' : 10.12
        }
    }

##### Response
    {
        "Message": "Operation succesful!",
        "ID": 8
    }
    
`POST /update`

    {
    	"Name" : "Continent",
    	"ID" : 30,
    	"Values": {
    		"name" : "jaba",
    		"population" :10,
    		"area" : 1
    	}
    }
    
##### Response
    {
        "Message": "Operation succesful!"
    }
    
`POST /delete`

    {
    	"Name" : "Continent",
    	"ID" : 30
    }

##### Response
    
    {
        "Message": "Operation Succesfull!",
        "Deleted_Rows": 8
    }

In all previous examples 'Name' should be one of : 'Continent', 'Country', 'City' and the 'Values' dictionary keys are:

    'Continent' : ['name', 'population', 'area']
    'Country' : ['name', 'population', 'area', 'n_hospitals', 'n_national_parks', 'continent_ id']
    'City' : ['name', 'population', 'area', 'n_roads', 'n_trees', 'country_id']
    
In case of inserting we are waiting for all the keys described above, in case of updating only the fields present will be updated.

For parsing and validating request payload we will use decorator implemented in src/app/helpers.py. If something is missing we will return response with such message.

After validating payload we will do any SQL related task in src/app/tasks.py and handle all errors here as well. Several things may happen: 

Value keys might be wrong - in this case we return message 'Please make sure you send right Values'.
SQL validation check may trigger - in this case we get error message defined by us in triggers.sql and return it.
In case of deleting and updating ID may not exists - we return 'No entry with that ID' message.
