from datetime import timedelta
from fastapi import HTTPException, Body

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer


from models import User, Order, Product
from database import SessionLocal
from schemas import OrderModel, OrderUpdateModel, OrderStatusModel
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

order_router = APIRouter(
    prefix="/order",
)


def fetch_order(id: int, db: Session):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def get_order_instance(id: int, db: Session = Depends(get_db)):
    return fetch_order(id, db)




@order_router.get("/")
async def welcome_page(credentials: JwtAuthorizationCredentials = Depends(access_security)):

    return {'message': 'Welcome to Order API!'}


@order_router.post("/make", status_code=status.HTTP_201_CREATED,)
async def make_order(order: OrderModel, credentials: JwtAuthorizationCredentials = Depends(access_security), db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_product = db.query(Product).filter_by(id=order.product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_order = Order(
        quantity=order.quantity,
        product_id=order.product_id,
        user_id=db_user.id,
    )
    db.add(new_order)
    db.commit()

    response = {
        "success": True,
        "message": "Order created",
        "id": new_order.id,
        "user_id": new_order.user_id,
        "product_id": new_order.product_id,
        "quantity": new_order.quantity,
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "price": db_product.price,
        },
        "total_price": db_product.price * new_order.quantity
    }
    return jsonable_encoder(response)


@order_router.get("/list", status_code=status.HTTP_200_OK,) #listing all orders
async def list_orders(credentials: JwtAuthorizationCredentials = Depends(access_security), db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_staff:
        orders = db.query(Order).filter_by(user_id=db_user.id).all()
        return jsonable_encoder(orders)
    else:
        HTTPException(status_code=403, detail="User not authorized")


@order_router.get("/{id}")
async def get_order_by_id(id: int, credentials: JwtAuthorizationCredentials = Depends(access_security), db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.is_staff:
        order = db.query(Order).filter(Order.id==id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        return {
            "success": True,
            "message": "Order found",
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "product": {
                "id": order.product_id,
                "name": order.product.name,
                "price": order.product.price,
            }
        }
    else:
        HTTPException(status_code=403, detail="User not authorized")



@order_router.get("/user/orders", status_code=status.HTTP_200_OK,)
async def get_user_orders(credentials: JwtAuthorizationCredentials = Depends(access_security), db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        orders = db.query(Order).filter_by(user_id=db_user.id).all()

        return jsonable_encoder(orders)
    else:
        HTTPException(status_code=403, detail="User not authorized")



@order_router.get("/user/order/{id}", status_code=status.HTTP_200_OK,)
async def get_user_order_by_id(id: int, credentials: JwtAuthorizationCredentials = Depends(access_security),
                               db: Session = Depends(get_db)):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        order = db.query(Order).filter(Order.id==id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {
            "success": True,
            "message": "Order found",
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "product": {
                "id": order.product_id,
                "name": order.product.name,
                "price": order.product.price,
            }
        }
    else:
        HTTPException(status_code=403, detail="User not authorized")



@order_router.put("/{id}/update", status_code=status.HTTP_200_OK)
async def update_order_by_id(
    id: int,
    update_data: OrderUpdateModel = Body(...),
    credentials: JwtAuthorizationCredentials = Depends(access_security),
    db: Session = Depends(get_db)
):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    order_to_update = db.query(Order).filter(Order.id == id).first()
    if not order_to_update:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_to_update.user_id != db_user.id:
        raise HTTPException(status_code=403, detail="You cannot update other user's orders")

    if update_data.quantity is not None:
        order_to_update.quantity = update_data.quantity

    if update_data.product_id is not None:
        order_to_update.product_id = update_data.product_id

    db.commit()
    db.refresh(order_to_update)

    return jsonable_encoder({
        "success": True,
        "message": "Order updated",
        "id": order_to_update.id,
        "user_id": order_to_update.user_id,
        "product_id": order_to_update.product_id,
        "quantity": order_to_update.quantity,
        "order_status": order_to_update.order_statuses,
        "product": {
            "id": order_to_update.product_id,
            "name": order_to_update.product.name,
            "price": order_to_update.product.price,
            "quantity": order_to_update.quantity
        }
    })



@order_router.patch("/{id}/update-status", status_code=status.HTTP_200_OK)
async def update_order_by_id(
        id: int,
        order: OrderStatusModel,
        credentials: JwtAuthorizationCredentials = Depends(access_security),
        db: Session = Depends(get_db)

):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.is_staff:
        order_to_update = db.query(Order).filter(Order.id==id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order_to_update.order_statuses = order.order_status
        db.commit()
        db.refresh(order_to_update)
        return jsonable_encoder({
            "success": True,
            "message": "Order updated",
            "id": order_to_update.id,
            "user_id": order_to_update.user_id,
            "product_id": order_to_update.product_id,
            "quantity": order_to_update.quantity,
            "order_status": order_to_update.order_statuses,
            "product": {
                "id": order_to_update.product_id,
                "name": order_to_update.product.name,
                "price": order_to_update.product.price,
                "quantity": order_to_update.quantity
            }
        })


@order_router.delete("/{id}/delete", status_code=status.HTTP_200_OK)
async def delete_order_by_id(
        id: int,
        credentials: JwtAuthorizationCredentials = Depends(access_security),
        db: Session = Depends(get_db)
):
    current_username = credentials.subject["username"]
    db_user = db.query(User).filter_by(username=current_username).first()
    order_to_delete = db.query(Order).filter(Order.id==id).first()
    if not order_to_delete:
        raise HTTPException(status_code=404, detail="Order not found")

    if order_to_delete.user_id != db_user.id:
        raise HTTPException(status_code=403, detail="You cannot delete other user's orders")

    if order_to_delete.order_statuses != "Pending":
        raise HTTPException(status_code=403, detail="You can only delete an order while it is still pending")

    db.delete(order_to_delete)
    db.commit()
    return jsonable_encoder({
        "success": True,
        "message": "Order deleted",
        "id": order_to_delete.id,
        "user_id": order_to_delete.user_id,
    })








