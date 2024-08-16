from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas
from database import SessionLocal, engine
from sqlalchemy.future import select

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD operations for Customers
@app.post("/customers/", response_model=schemas.CustomerInDB)
async def create_customer(
    customer: schemas.CustomerCreate, db: Session = Depends(get_db)
):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.get("/customers/{customer_id}", response_model=schemas.CustomerInDB)
async def read_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.execute(
        select(models.Customer).filter(models.Customer.id == customer_id)
    ).scalar_one_or_none()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@app.put("/customers/{customer_id}", response_model=schemas.CustomerInDB)
async def update_customer(
    customer_id: str, customer: schemas.CustomerCreate, db: Session = Depends(get_db)
):
    db_customer = db.execute(
        select(models.Customer).filter(models.Customer.id == customer_id)
    ).scalar_one_or_none()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    db_customer = db.execute(
        select(models.Customer).filter(models.Customer.id == customer_id)
    ).scalar_one_or_none()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}


# CRUD operations for Products
@app.post("/products/", response_model=schemas.ProductInDB)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/{product_id}", response_model=schemas.ProductInDB)
async def read_product(product_id: str, db: Session = Depends(get_db)):
    db_product = db.execute(
        select(models.Product).filter(models.Product.id == product_id)
    ).scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@app.put("/products/{product_id}", response_model=schemas.ProductInDB)
async def update_product(
    product_id: str, product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    db_product = db.execute(
        select(models.Product).filter(models.Product.id == product_id)
    ).scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(get_db)):
    db_product = db.execute(
        select(models.Product).filter(models.Product.id == product_id)
    ).scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


# CRUD operations for Orders
@app.post("/orders/", response_model=schemas.OrderInDB)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/{order_id}", response_model=schemas.OrderInDB)
async def read_order(order_id: str, db: Session = Depends(get_db)):
    db_order = db.execute(
        select(models.Order).filter(models.Order.id == order_id)
    ).scalar_one_or_none()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


@app.put("/orders/{order_id}", response_model=schemas.OrderInDB)
async def update_order(
    order_id: str, order: schemas.OrderUpdate, db: Session = Depends(get_db)
):
    db_order = db.execute(
        select(models.Order).filter(models.Order.id == order_id)
    ).scalar_one_or_none()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order.model_dump().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str, db: Session = Depends(get_db)):
    db_order = db.execute(
        select(models.Order).filter(models.Order.id == order_id)
    ).scalar_one_or_none()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}
