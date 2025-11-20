from fastapi import FastAPI
app=FastAPI()

@app.get("/")
def read_root():
    '''Simple Hello World endpoint'''
    return {"Hello": "World"}
#path parameter
@app.get("/items/{item_id}")
def get_item(item_id: int):
    '''Get item by ID'''
    return {"item_id": item_id}

#query parameter
@app.get("/search")
def search_items(query:str=None, limit:int=10):
    '''search items with optional query and limit'''
    return {"query": query, "limit": limit}