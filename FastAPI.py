from fastapi import FastAPI
import json
app = FastAPI()
@app.get("/data/")
def data():
    pass
@app.get('/summary/')
def summary():
    pass
@app.get('/visualization/')
def geraph():
    pass
@app.get('/corrolation/')
def cor():
    pass
@app.post('/preprocess/')
def preprocess(content:json):
    pass
@app.post('/patterns/')
def patterns(content:json):
    pass
@app.get('/insights/')
def insights():
    pass
@app.get('/limitations/')
def limit():
    pass
@app.get('/future research/')
def advice():
    pass
