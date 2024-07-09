from fastapi import FastAPI
from StatisticalAnalysis import *
from fastapi.responses import HTMLResponse
app = FastAPI()


@app.get("/api/data/", response_class=HTMLResponse)
def data():
    # return {'info: ': housing.describe(),
    #         'Data: ': dict(housing.iloc[:5,:5])}
    # تبدیل دیتافریم به HTML
    html_table = housing.iloc[:5,:].to_html(index=False)
    html_describe = housing.describe().to_html()
    # قالب HTML برای نمایش جدول
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DataFrame Table</title>
        <style>
            table {{
                width: 50%;
                margin: 25px auto;
                border-collapse: collapse;
                text-align: left;
            }}
            th, td {{
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>DataFrame Table</h1>
        {html_table}
        <h2>Describe Table</h2>
        {html_describe}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get('/api/summary/')
def summary():
    pass

@app.get('/api/visualization/')
def graph():
    pass

@app.get('/api/correlation/')
def cor():
    pass

@app.post('/api/preprocess/')
def preprocess(content: dict):
    pass

@app.post('/api/patterns/')
def patterns(content: dict):
    pass

@app.get('/api/insights/')
def insights():
    pass



