from fastapi import FastAPI, Query, HTTPException
from typing import List

app = FastAPI(title="Assignment 5", version="1.0")

# ---------------------------------------------------
# DATA
# ---------------------------------------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
]

orders = []
"""
In every file I have defined static routes above dynamic to avoid failure in Swagger UI , also gave proper visible comments in the same format as I did it earlier
"""
# ---------------------------------------------------
# STATIC ROUTES
# ---------------------------------------------------

@app.get("/")
def home():
    return {"message": "Assignment 5 API Running"}


@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# ---------------------------------------------------
# Q1 — SEARCH PRODUCTS
# ---------------------------------------------------

@app.get("/products/search")
def search_products(keyword: str = Query(...)):

    results = [p for p in products if keyword.lower() in p["name"].lower()]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }


# ---------------------------------------------------
# Q2 — SORT PRODUCTS
# ---------------------------------------------------

@app.get("/products/sort")
def sort_products(
    sort_by: str = Query("price"),
    order: str = Query("asc")
):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = (order == "desc")

    sorted_list = sorted(products, key=lambda p: p[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_list
    }


# ---------------------------------------------------
# Q3 — PAGINATION
# ---------------------------------------------------

@app.get("/products/page")
def paginate_products(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):

    start = (page - 1) * limit
    end = start + limit

    total = len(products)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "products": products[start:end]
    }


# ===================================================
# NEW ROUTES (ABOVE DYNAMIC)
# ===================================================

# ---------------------------------------------------
# Q4 — SEARCH ORDERS
# ---------------------------------------------------

@app.get("/orders/search")
def search_orders(customer_name: str = Query(...)):

    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }


# ---------------------------------------------------
# Q5 — SORT BY CATEGORY + PRICE
# ---------------------------------------------------

@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "products": result,
        "total": len(result)
    }


# ---------------------------------------------------
# Q6 — COMBINED (SEARCH + SORT + PAGINATION)
# ---------------------------------------------------

@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20)
):

    result = products

    # 1. SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # 2. SORT
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    # 3. PAGINATION
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }


# ---------------------------------------------------
# BONUS — PAGINATE ORDERS
# ---------------------------------------------------

@app.get("/orders/page")
def paginate_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(3, ge=1, le=20)
):

    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start:start + limit]
    }


# ---------------------------------------------------
# DYNAMIC ROUTE (LAST)
# ---------------------------------------------------

@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return {"product": p}

    return {"error": "Product not found"}


# ---------------------------------------------------
# OPTIONAL — CREATE ORDERS (for testing Q4 + Bonus)
# ---------------------------------------------------

@app.post("/orders")
def create_order(customer_name: str, product_id: int):

    for p in products:
        if p["id"] == product_id:

            order = {
                "order_id": len(orders) + 1,
                "customer_name": customer_name,
                "product": p["name"],
                "price": p["price"]
            }

            orders.append(order)

            return {"message": "Order created", "order": order}

    raise HTTPException(status_code=404, detail="Product not found")