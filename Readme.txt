- Language used inp roject : python fastapi ;
- for database , im using mysql since im most familiar with it asnd it has already been installed on my pc you can use any
other database you just need to change the database.pyfile
- To run this , i will assume you have python and sql installed on your pc.
+ set up : install all necessary package -- pip install fastapi uvicorn sqlmodel pymysql passlib[bcrypt] pyjwt python-dotenv --
( open terminal of your project and past the pip install there )
+ after that just paste -- fastapi dev main.py -- and the program should run now / you can use docker to run it faster without setting up ( step 6 )
+ all end point i used require authentication jwt so you must get token before testing ( just do the following steps )

1.Login to get a JWT:
curl -X POST http://localhost:8000/api/login \
 -H "Content-Type: application/json" \
 -d '{"email":"admin@gmail.com","password":"admin123"}' --- default generated one

2.Copy access_token from the response and use it in all requests:
Authorization: Bearer <access_token>

3.Create Course (201 Created)
curl -X POST http://localhost:8000/api/courses/
 -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
 -d '{"title":"FastAPI for Beginners","description":"Intro to FastAPI","difficulty":"Beginner"}'

4.List Courses (200 OK) ( this will get all course )
curl -X GET http://localhost:8000/api/courses/ \
 -H "Authorization: Bearer <TOKEN>"

4.5. For any one wants to have a pagination just use
curl -X GET http://localhost:8000/api/courses/page?limit={number}&offset={number} \
-- replace the number based on your preference
+ limit = how many items per page.
+ offset = where to start in the dataset.
 -H "Authorization: Bearer <TOKEN>"

5.curl -X POST http://localhost:8000/api/enrollments \
 -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
 -d '{"studentEmail":"student1@gmail.com","courseId":1}'

 curl -X GET http://localhost:8000/api/students/student1@gmail.com/enrollments \
 -H "Authorization: Bearer <TOKEN>"

6.Containerir : use docker ( make sure you have docker desktop and have it turned on )
git clone https://github.com/thai4356/API_Testing
cd FastAPIProject

# Build and start
docker compose up --build

# Open API docs
# http://localhost:8000/docs

# Stop (keep containers)
docker compose stop

# Remove containers, keep volumes
docker compose down

# Remove everything (containers + volumes)
docker compose down -v

then use http://localhost:8000/docs there you should use all the things ( i prefer use postman since it is easier and more user friendly