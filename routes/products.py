from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags=["produtcts"],
                   responses={404: {"Message": "No encontrado"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def get_products():
    return products_list

@router.get("/{id}")
async def products(id: int):
    return products_list[id]
