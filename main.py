from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Arayüz bağlantısı için CORS izni
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELLER
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    table_id: int
    items: List[OrderItem]

# VERİLER
products_db = {
    1: {"name": "Hamburger", "price": 120.0},
    2: {"name": "Patates Kızartması", "price": 45.0},
    3: {"name": "Kola", "price": 30.0}
}
orders_db = []

# --- ENDPOINTLER ---

@app.get("/")
def home():
    return {"mesaj": "Sistem Aktif"}

# 1. Siparişleri Listeleme (MUTFAK İÇİN) - Burası 405 hatasını çözen yer!
@app.get("/orders")
def get_orders():
    return orders_db

# 2. Sipariş Verme (MÜŞTERİ İÇİN)
@app.post("/orders")
async def create_order(order_data: OrderCreate):
    new_order = {
        "id": len(orders_db) + 1,
        "table_id": order_data.table_id,
        "items": order_data.items,
        "status": "Hazırlanıyor"
    }
    orders_db.append(new_order)
    return new_order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)