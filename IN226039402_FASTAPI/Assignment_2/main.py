from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="E-commerce API", description="A simple API to manage products in an online store.", version="1.0")

# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse','price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationary',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationary',  'in_stock': True },
    {'id': 5 ,'name': 'Laptop Stand', 'price':1299,'category':'Electronics','in_stock':True},
    {'id': 6 , 'name': 'Mechanical Keyboard', 'price':2499,'category':'Electronics','in_stock':True},
    {'id': 7 , 'name': 'Webcam', 'price':1899 , 'category': 'Electronics', 'in_stock':False}
]

feedback = []
orders = []

# ============================================================
# STATIC Endpoints
# ============================================================

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}


@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}


# ── Endpoint — Return only in-stock products ─────────────────
@app.get('/products/instock')
def get_instock_products():
    final_result = []
    for product in products:
        if product['in_stock'] == True:
            final_result.append(product)

    return {'in stock products': final_result, 'count': len(final_result)}


# ── Endpoint — Best deals and premium products ───────────────
@app.get('/products/deals')
def get_deals():

    lowest_price = min(product['price'] for product in products)
    highest_price = max(product['price'] for product in products)

    best_deal = [p for p in products if p['price'] == lowest_price]
    premium_pick = [p for p in products if p['price'] == highest_price]

    return {
        "best deals": best_deal,
        "premium products": premium_pick
    }


# ── Endpoint — Store summary ─────────────────────────────────
@app.get('/store/summary')
def get_summary():

    total_products = 0
    in_stock = 0
    out_of_stock = 0
    categories = []

    for product in products:

        total_products += 1

        if product['in_stock'] == True:
            in_stock += 1

        else:
            out_of_stock += 1

        if product['category'] not in categories:
            categories.append(product['category'])

    return {
        "store_name": "Shidruk & Sons Market",
        "total_products": total_products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "categories": categories
    }


# ============================================================
# Q1 — FILTER PRODUCTS (Added min_price)
# ============================================================

@app.get('/products/filter')
def filter_products(
    category: str = Query(None, description='Electronics or Stationary'),
    max_price: int = Query(None, description='Maximum price'),
    min_price: int = Query(None, description='Minimum price'),
    in_stock: bool = Query(None, description='True = in stock only')
):

    result = products

    if category:
        result = [p for p in result if p['category'] == category]

    if max_price:
        result = [p for p in result if p['price'] <= max_price]

    if min_price:
        result = [p for p in result if p['price'] >= min_price]

    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]

    return {
        "filtered_products": result,
        "count": len(result)
    }

# ============================================================
# Q4 — PRODUCT SUMMARY DASHBOARD
# ============================================================

@app.get("/products/summary")
def product_summary():

    in_stock = [p for p in products if p["in_stock"]]

    out_stock = [p for p in products if not p["in_stock"]]

    expensive = max(products, key=lambda p: p["price"])

    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": categories
    }


# ============================================================
# DYNAMIC Endpoints
# ============================================================

@app.get('/products/{product_id}')
def get_product(product_id: int):

    for product in products:
        if product['id'] == product_id:
            return {'product': product}

    return {'error': 'Product not found'}


# ── Get products by category ─────────────────────────────────
@app.get('/products/category/{category_name}')
def get_products_by_category(category_name: str):

    final_result = []

    for product in products:
        if product['category'] == category_name:
            final_result.append(product)

    if not final_result:
        return {"error": "No products found in this category"}

    return {'result': final_result, 'count': len(final_result)}


# ── Search product by name ───────────────────────────────────
@app.get('/products/search/{keyword}')
def get_prod_by_name(keyword: str):

    for product in products:
        if product['name'].lower() == keyword.lower():
            return product

    return {"message": "No products matched your search"}


# ============================================================
# Q2 — GET ONLY PRICE OF PRODUCT
# ============================================================

@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):

    for product in products:

        if product["id"] == product_id:

            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}


# ============================================================
# Q3 — CUSTOMER FEEDBACK (Pydantic + POST)
# ============================================================

class CustomerFeedback(BaseModel):

    customer_name: str = Field(..., min_length=2, max_length=100)

    product_id: int = Field(..., gt=0)

    rating: int = Field(..., ge=1, le=5)

    comment: Optional[str] = Field(None, max_length=300)


@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):

    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }





# ============================================================
# Q5 — BULK ORDER SYSTEM
# ============================================================

class OrderItem(BaseModel):

    product_id: int = Field(..., gt=0)

    quantity: int = Field(..., gt=0, le=50)


class BulkOrder(BaseModel):

    company_name: str = Field(..., min_length=2)

    contact_email: str = Field(..., min_length=5)

    items: List[OrderItem] = Field(..., min_items=1)


@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):

    confirmed = []

    failed = []

    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:

            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })

        elif not product["in_stock"]:

            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })

        else:

            subtotal = product["price"] * item.quantity

            grand_total += subtotal

            confirmed.append({
                "product": product["name"],
                "qty": item.quantity,
                "subtotal": subtotal
            })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }

# ── Orders storage ─────────────────────────
orders = []


# ── POST /orders  (order starts as pending) ─────────────────
@app.post("/orders")
def place_order(product_id: int, quantity: int):

    for product in products:

        if product["id"] == product_id:

            if not product["in_stock"]:
                return {"error": "Product is out of stock"}

            order_id = len(orders) + 1

            new_order = {
                "order_id": order_id,
                "product_id": product_id,
                "product_name": product["name"],
                "quantity": quantity,
                "total_price": product["price"] * quantity,
                "status": "pending"   # important change
            }

            orders.append(new_order)

            return {
                "message": "Order placed successfully",
                "order": new_order
            }

    return {"error": "Product not found"}


# ── GET /orders/{order_id} ─────────────────
@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:

        if order["order_id"] == order_id:
            return {"order": order}

    return {"error": "Order not found"}


# ── PATCH /orders/{order_id}/confirm ─────────────────
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:

        if order["order_id"] == order_id:

            order["status"] = "confirmed"

            return {
                "message": "Order confirmed",
                "order": order
            }

    return {"error": "Order not found"}