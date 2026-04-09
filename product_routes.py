from datetime import timedelta
from fastapi import HTTPException

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer


from models import User, Product
from database import SessionLocal
from schemas import ProductModel, ProductUpdateModel
from fastapi.encoders import jsonable_encoder

SECRET_KEY = "58597a77ef066bb037ecaa7bc0d6e30a5b1bc6203a6b7321f5883f5084192c7a"

access_security = JwtAccessBearer(
    secret_key=SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(hours=1)  # Token expires in 1 hour
)

refresh_security = JwtRefreshBearer(
    secret_key=SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(days=30)  # Refresh token expires in 30 days
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

product_router = APIRouter(
    prefix="/product",
)


@product_router.post("/create", status_code=status.HTTP_201_CREATED, response_model=ProductModel)
async def create_product(product: ProductModel, db: Session = Depends(get_db), credentials: JwtAuthorizationCredentials = Depends(access_security)):

    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_staff:
        new_product = Product(
            name=product.name,
            price=product.price,
        )
        db.add(new_product)
        db.commit()
        data = {
            "success": True,
            "message": "Product created",
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price,
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=403, detail="Forbidden, only admin can create products")


@product_router.get("/list", status_code=status.HTTP_200_OK)
async def list_products(db: Session = Depends(get_db), credentials: JwtAuthorizationCredentials = Depends(access_security)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        products = db.query(Product).all()
        return jsonable_encoder(products)
    else:
        raise HTTPException(status_code=403, detail="Forbidden, only admin can list products")



@product_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(id:int, db: Session = Depends(get_db), credentials: JwtAuthorizationCredentials = Depends(access_security)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return jsonable_encoder(product)
    else:
        raise HTTPException(status_code=403, detail="Forbidden, only admin can list products")


@product_router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_product_by_id(id: int, credentials: JwtAuthorizationCredentials = Depends(access_security), db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product)
        db.commit()
        return jsonable_encoder({"success": True, "message": "Product deleted"})
    else:
        raise HTTPException(status_code=403, detail="Forbidden, only admin can delete products")


@product_router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_product(id: int, update_data: ProductUpdateModel, credentials: JwtAuthorizationCredentials = Depends(access_security),
                         db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        data = {
            "success": True,
            "message": "Product updated",
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        return jsonable_encoder(data)
    else:
        raise HTTPException(status_code=403, detail="Forbidden, only admin can update products")
