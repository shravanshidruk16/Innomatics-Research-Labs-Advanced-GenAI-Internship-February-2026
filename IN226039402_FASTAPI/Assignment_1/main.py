from fastapi import FastAPI , Query
 
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

# ============================================================
# STATIC Endpoints
# Always define STATIC routes first and then the DYNAMIC ones
# ============================================================


# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}


# ── Endpoint 1 — Return all products ─────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}


# Question 3
# ── Endpoint 2 — Return only in-stock products ───────────────
@app.get('/products/instock')
def get_instock_products():
    final_result = []
    for product in products:
        if product['in_stock']==True:
            final_result.append(product)
    return {'in stock products':final_result,'count':len(final_result)}


# Question 6 - Bonus Question
# ── Endpoint 3 — Best deals and premium products ─────────────
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


# Question 4
# ── Endpoint 4 — Store summary ───────────────────────────────
@app.get('/store/summary')
def get_summary():
    
    total_products = 0 
    in_stock = 0
    out_of_stock = 0
    categories = []
    for product in products:
        total_products+=1
        if product['in_stock']==True:
            in_stock+=1
            if product['category'] not in categories:
                categories.append(product['category'])
        else:
            out_of_stock+=1
    return {"store_name":"Shidruk & Sons Market","total_products": total_products, "in_stock": in_stock, "out_of_stock": out_of_stock, "categories": categories}


# ── Endpoint 5 — Filter products using Query parameters ──────
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationary'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}



# ============================================================
# DYNAMIC Endpoints
# These contain PATH PARAMETERS
# ============================================================


# ── Endpoint 6 — Return one product by its ID ─────────────────
@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}


# Question 2
# ── Endpoint 7 — Get products by category ────────────────────
@app.get('/products/category/{category_name}')
def get_products_by_category(category_name:str):
    final_result = []
    for product in products:
        if product['category'] == category_name:
            final_result.append(product)
    if not final_result:
        return {"error": "No products found in this category"}
    return {'result':final_result,'count':len(final_result)}


# Question 5
# ── Endpoint 8 — Search product by name ──────────────────────
@app.get('/products/search/{keyword}')
def get_prod_by_name(keyword:str):
    for product in products:
        if product['name'].lower()==keyword.lower():
            return product
    return {"message": "No products matched your search"}