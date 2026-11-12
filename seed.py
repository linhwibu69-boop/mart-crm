"""Explicit opt-in seed; all customers and purchases are test data."""
import os
from sqlalchemy import select
from app.database import Base, engine, SessionLocal
from app.models import User, Customer, Product
from app.security import hash_password
from app.services.purchases import PurchaseService
from app.schemas import PurchaseDTO

def seed():
    ap=os.getenv('MART_ADMIN_PASSWORD');cp=os.getenv('MART_CASHIER_PASSWORD')
    if not ap or not cp or min(len(ap),len(cp))<12:raise SystemExit('Set MART_ADMIN_PASSWORD and MART_CASHIER_PASSWORD, each at least 12 characters')
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.scalar(select(User.id).limit(1)):
            print('Existing database preserved. No seed added.');return
        admin=User(username='admin',password_hash=hash_password(ap),role='admin')
        db.add_all([admin,User(username='cashier',password_hash=hash_password(cp),role='cashier')])
        for i in range(1,9):db.add(Customer(name=f'Khách kiểm thử {i:02d}',phone=f'09000000{i:02d}',email=f'khach{i:02d}@example.com',address='Dữ liệu kiểm thử',consent=False))
        for sku,name,cat,price,stock in [('GAO-05','Gạo thơm túi 5 kg','Lương thực',165000,120),('SUA-01','Sữa tươi hộp 1 lít','Đồ uống',38000,240),('DAU-01','Dầu ăn chai 1 lít','Gia vị',52000,100),('BANH-01','Bánh quy hộp 300 g','Bánh kẹo',68000,80),('NUOC-01','Nước khoáng thùng 24 chai','Đồ uống',96000,70),('GIAT-01','Nước giặt túi 3 lít','Gia dụng',145000,60),('CAFE-01','Cà phê rang xay 500 g','Đồ uống',125000,8),('MI-01','Mì gói thùng 30 gói','Lương thực',110000,90)]:db.add(Product(sku=sku,name=name,category=cat,price=price,stock=stock))
        db.commit()
        for idx,(cid,pid,qty,redeem) in enumerate([(1,1,20,0),(2,1,35,0),(3,6,4,0),(4,2,12,0),(5,5,3,0),(6,8,5,0),(7,4,2,0),(1,6,3,20)]):PurchaseService(db).create(PurchaseDTO(customer_id=cid,items=[{'product_id':pid,'quantity':qty}],redeem_points=redeem,request_key=f'seed-order-{idx:03d}'),admin)
    print('Seed complete: 8 test customers, 8 products, 8 actual purchase records.')
if __name__=='__main__':seed()
