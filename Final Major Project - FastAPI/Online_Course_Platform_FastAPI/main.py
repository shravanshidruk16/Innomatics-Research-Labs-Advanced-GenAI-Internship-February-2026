from fastapi import FastAPI , Query , HTTPException
from models import EnrollRequest , NewCourse

app = FastAPI(title="LearnHub - An Online Course Platform",version="1.0")
"""
1. Routes are placed according the there nature : Static / Dynamic.
2. I gave numbers to each route inorder to cross check the Endpoints.
3. Since the question numbers or tasks are not in a particular order due to the nature of the endpoints but I tried to number them and completed all the endpoints mentioned !
4. Tested everything in SwaggerUI and aligned all Endpoints there clearly and perfectly .
"""

# Courses Data
courses = [
    {
        'id': 1,
        'title': "Data Science and Big Data Bootcamp",
        'instructor': "Krish Naik",
        'category': "Data Science",
        'level': "Intermediate",
        'price': 4999,
        'seats_left': 43
    },
    {
        'id': 2,
        'title': "Full Stack Web Development with MERN",
        'instructor': "Angela Yu",
        'category': "Web Dev",
        'level': "Beginner",
        'price': 599,
        'seats_left': 30
    },
    {
        'id': 3,
        'title': "UI/UX Design Masterclass",
        'instructor': "Daniel Scott",
        'category': "Design",
        'level': "Beginner",
        'price': 0,
        'seats_left': 25
    },
    {
        'id': 4,
        'title': "Advanced Kubernetes & DevOps",
        'instructor': "Bret Fisher",
        'category': "DevOps",
        'level': "Advanced",
        'price': 399,
        'seats_left': 15
    },
    {
        'id': 5,
        'title': "Machine Learning A-Z",
        'instructor': "Kirill Eremenko",
        'category': "Data Science",
        'level': "Intermediate",
        'price': 5499,
        'seats_left': 20
    },
    {
        'id': 6,
        'title': "React JS Complete Guide",
        'instructor': "Maximilian Schwarzmüller",
        'category': "Web Dev",
        'level': "Intermediate",
        'price': 4499,
        'seats_left': 35
    },
    {
        'id': 7,
        'title': "Graphic Design Bootcamp",
        'instructor': "Lindsay Marsh",
        'category': "Design",
        'level': "Beginner",
        'price': 0,
        'seats_left': 40
    },
    {
        'id': 8,
        'title': "Docker & CI/CD Pipeline",
        'instructor': "Stephen Grider",
        'category': "DevOps",
        'level': "Intermediate",
        'price': 299,
        'seats_left': 28
    },
    {
        'id': 9,
        'title': "Deep Learning with TensorFlow",
        'instructor': "Andrew Ng",
        'category': "Data Science",
        'level': "Advanced",
        'price': 6999,
        'seats_left': 12
    },
    {
        'id': 10,
        'title': "Next.js & Modern Web Apps",
        'instructor': "Colt Steele",
        'category': "Web Dev",
        'level': "Advanced",
        'price': 399,
        'seats_left': 18
    }
]

# Enrollment Data
enrollments = []
enrollment_counter = 1

# Wishlist Data
wishlist = []

# ---------------------- Beginner Level ----------------------

# 1. Home Route
@app.get('/')
def home():
    return {'message':'Welcome to LearnHub Online Courses'}

# 2. List All Courses
@app.get('/courses')
def list_courses():
    total_seats = sum([c['seats_left'] for c in courses])

    return {
        'courses':courses,
        'total':len(courses),
        'total_seats_available':total_seats
    }

# 3. Courses Summary / The dynamic route is defined at bottom
@app.get('/courses/summary')
def courses_summary():
    total_courses = len(courses)

    free_courses = len([c for c in courses if c['price'] == 0])

    # Most expensive course
    most_expensive_course = max(courses, key=lambda c: c['price']) if courses else None

    # Total seats
    total_seats = sum(c['seats_left'] for c in courses)

    # Count by category
    category_count = {}
    for c in courses:
        category = c['category']
        category_count[category] = category_count.get(category, 0) + 1

    return {
        "total_courses": total_courses,
        "free_courses": free_courses,
        "most_expensive_course": most_expensive_course,
        "total_seats": total_seats,
        "category_count": category_count
    }

# ---------------------- Hard Level ----------------------

# 16. Search
@app.get('/courses/search')
def search(keyword: str):
    result = [
        c for c in courses
        if keyword.lower() in c['title'].lower()
        or keyword.lower() in c['instructor'].lower()
        or keyword.lower() in c['category'].lower()
    ]
    return {"total": len(result), "data": result}


# 17. Sort
@app.get('/courses/sort')
def sort(sort_by:str="price",order:str="asc"):
    return sorted(courses,key=lambda x:x[sort_by],reverse=(order=="desc"))

# 18. Pagination
@app.get('/courses/page')
def page(page:int=1,limit:int=3):
    start = (page-1)*limit
    return courses[start:start+limit]


# 4. Get Enrollments
@app.get('/enrollments')
def get_enrollments():
    return {"total":len(enrollments),"data":enrollments}


# 19. Enrollment Search , Sort and Enrollment Pages
@app.get('/enrollments/search')
def search_enroll(name:str):
    return [e for e in enrollments if name.lower() in e['student'].lower()]

@app.get('/enrollments/sort')
def sort_enrollments(order: str = "asc"):
    
    sorted_data = sorted(
        enrollments,
        key=lambda x: x['final_fee'],
        reverse=True if order == "desc" else False
    )
    
    return {
        "order": order,
        "data": sorted_data
    }

@app.get('/enrollments/page')
def paginate_enrollments(page: int = 1, limit: int = 5):
    
    start = (page - 1) * limit
    end = start + limit

    paginated_data = enrollments[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": len(enrollments),
        "data": paginated_data
    }

# 20. Browse (All-in-One)
@app.get('/courses/browse')
def browse_courses(
    keyword: str = None,
    category: str = None,
    level: str = None,
    max_price: float = None,
    sort_by: str = "price",   # default sort field
    order: str = "asc",       # asc / desc
    page: int = 1,
    limit: int = 5
):
    
    result = courses.copy()

    # 1. Keyword Search
    if keyword:
        result = [
            c for c in result
            if keyword.lower() in c['title'].lower()
            or keyword.lower() in c['instructor'].lower()
        ]

    # 2. Category Filter
    if category:
        result = [
            c for c in result
            if c['category'].lower() == category.lower()
        ]

    # 3. Level Filter
    if level:
        result = [
            c for c in result
            if c['level'].lower() == level.lower()
        ]

    # 4. Price Filter
    if max_price is not None:
        result = [
            c for c in result
            if c['price'] <= max_price
        ]

    total_results = len(result)

    # 5. Sorting
    try:
        result = sorted(
            result,
            key=lambda x: x.get(sort_by, 0),
            reverse=True if order == "desc" else False
        )
    except Exception:
        return {"error": f"Invalid sort field: {sort_by}"}

    # 6. Pagination
    if page < 1 or limit < 1:
        return {"error": "Page and limit must be greater than 0"}

    start = (page - 1) * limit
    end = start + limit

    paginated_data = result[start:end]

    total_pages = (total_results + limit - 1) // limit

    # Final Response
    return {
        "filters": {
            "keyword": keyword,
            "category": category,
            "level": level,
            "max_price": max_price
        },
        "sorting": {
            "sort_by": sort_by,
            "order": order
        },
        "pagination": {
            "current_page": page,
            "limit": limit,
            "total_results": total_results,
            "total_pages": total_pages
        },
        "data": paginated_data
    }


# ---------------------- Filter ----------------------

# 5. Filter Courses
def filter_courses_logic(category=None, level=None, max_price=None, has_seats=None):
    result = courses

    if category is not None:
        result = [c for c in result if c['category'].lower()==category.lower()]

    if level is not None:
        result = [c for c in result if c['level'].lower()==level.lower()]

    if max_price is not None:
        result = [c for c in result if c['price']<=max_price]

    if has_seats is not None:
        result = [c for c in result if (c['seats_left']>0)==has_seats]

    return result

@app.get('/courses/filter')
def filter_courses(
    category:str=Query(default=None),
    level:str=Query(default=None),
    max_price:int=Query(default=None),
    has_seats:bool=Query(default=None)
):
    result = filter_courses_logic(category,level,max_price,has_seats)

    return {"total":len(result),"courses":result}

# ---------------------- Dynamic Route ----------------------

# 6. Get Course By ID
@app.get('/courses/{course_id}')
def get_course(course_id:int):
    for c in courses:
        if c['id']==course_id:
            return c
    raise HTTPException(status_code=404,detail="Course not found")

# ---------------------- Helper Functions ----------------------

# 7. Find Course
def find_course(course_id):
    for c in courses:
        if c['id']==course_id:
            return c
    return None

# 8. Calculate Fee
def calculate_enrollment_fee(price,seats_left,coupon_code):
    final = price

    if seats_left>5: # 10% discount
        final *= 0.9

    #Applied coupon code after the Early Bird Discount 

    if coupon_code:
        code = coupon_code.strip().upper()

        if code=="STUDENT20": # 20% discount
            final *= 0.8
        elif code=="FLAT500":
            final -= 500

    return max(0,int(final))

# ---------------------- Easy Level ----------------------

# 9. Enroll Course
@app.post('/enrollments')
def enroll(student:EnrollRequest):
    global enrollment_counter

    course = find_course(student.course_id)

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")

    if course['seats_left']<=0:
        raise HTTPException(status_code=400,detail="No seats available")

    base_price = course['price']

    early_discount = 0
    coupon_discount = 0

    # Early bird
    if course['seats_left'] > 5:
        early_discount = int(base_price * 0.1)

    price_after_early = base_price - early_discount

    # Coupon
    if student.coupon_code:
        code = student.coupon_code.strip().upper()

        if code == "STUDENT20":
            coupon_discount = int(price_after_early * 0.2)
        elif code == "FLAT500":
            coupon_discount = 500

    final_fee = max(0, price_after_early - coupon_discount)

    course['seats_left']-=1

    enrollment = {
        "enrollment_id":enrollment_counter,
        "student":student.student_name,
        "course":course['title'],
        "course_id":course['id'],
        "course_instructor":course['instructor'],
        "original_course_price":course['price'],
        "discounts": {
        "early_bird": early_discount,
        "coupon": coupon_discount
        },
        "final_fee":final_fee,
        "payment_method": student.payment_method,
        "gift":student.gift_enrollment,
        "recipient":student.recipient_name if student.gift_enrollment else None # here the models.py will work if name is missing and gift is true
    }

    enrollments.append(enrollment)
    enrollment_counter+=1

    return enrollment

# ---------------------- Medium Level ----------------------

# 10. Add Course
@app.post('/courses',status_code=201)
def add_course(course:NewCourse):

    for c in courses:
        if c['title'].lower()==course.title.lower():
            raise HTTPException(status_code=400,detail="Duplicate course")

    new_id = max([c['id'] for c in courses])+1
    new_course = {"id":new_id,**course.dict()}

    courses.append(new_course)
    return new_course

# 11. Update Course
@app.put('/courses/{course_id}')
def update_course(course_id:int,price:int=Query(None),seats:int=Query(None)):
    course = find_course(course_id)

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")

    if price is not None:
        course['price']=price

    if seats is not None:
        course['seats_left']=seats

    return course

# 12. Delete Course
@app.delete('/courses/{course_id}')
def delete_course(course_id:int):
    course = find_course(course_id)

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    
    for student in enrollments:
        if student['course_id']==course_id:
            return {'message':'Cannot Delete Course As Students are Enrolled !'}

    courses.remove(course)
    return {"message":"Deleted successfully"}

# ---------------------- Workflow ----------------------

# 13. Add to Wishlist
@app.post('/wishlist/add')
def add_wishlist(course_id:int):
    course = find_course(course_id)

    if not course:
        raise HTTPException(status_code=404,detail="Course not found")

    if course in wishlist:
        return {"message":"Already added , add a different one"}

    wishlist.append(course)
    return {"message":"Course Added in Wishlist , Happy Learning !"}

# 14. View Wishlist
@app.get('/wishlist')
def view_wishlist():
    tot_price_wishlist_items=sum(c['price'] for c in wishlist)
    return {"total":len(wishlist),"data":wishlist,'total_price_of_all_wishlisted_items':tot_price_wishlist_items}

# 15. Remove Wishlist
@app.delete('/wishlist/{course_id}')
def remove_wishlist(course_id:int):
    course = find_course(course_id)

    if course not in wishlist:
        raise HTTPException(status_code=404,detail="Not in wishlist")

    wishlist.remove(course)
    return {"message":"Course Removed Successfully!"}

