import json
from fastapi import FastAPI, HTTPException, Body, Depends
from model import UserSchema, UserLoginSchema
from auth_handler import signJWT
from auth_bearer import JWTBearer

with open("menu.json", "r") as read_file:
    data = json.load(read_file)
app = FastAPI()

users = []

@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    users.append(user)
    return signJWT(user.username)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.username == data.username and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.username)
    return {
        "error": "Usename/Password salah!"
    }

@app.get('/')
def root():
    return {'Menu':'Item'}

@app.get('/menu')
async def read_all_menu():
    return data

@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def read_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item tidak ditemukan'
    )

@app.post('/menu', dependencies=[Depends(JWTBearer())])
async def post_menu(name:str):
    id=1
    if(len(data['menu'])>0):
        id=data['menu'][len(data['menu'])-1]['id']+1
    new_data={'id':id,'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    with open("menu.json", "w") as write_file:
        json.dump(data,write_file,indent=4)
    write_file.close()

    return (new_data)
    raise HTTPException(
        status_code=404, detail=f'Internal Server Error'
    )

@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def update_menu(item_id: int, name:str):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name']=name
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()
            return{"message":"Data berhasil diperbarui"}
    raise HTTPException(
        status_code=404, detail=f'Item tidak ditemukan'
    )

@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())])
async def delete_menu(item_id: int):
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file:
                json.dump(data,write_file,indent=4)
            write_file.close()

            return{"message":"Data berhasil dihapus"}
    raise HTTPException(
        status_code=404, detail=f'Item tidak ditemukan'
    )