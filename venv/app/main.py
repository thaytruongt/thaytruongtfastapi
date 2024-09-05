from fastapi import FastAPI
from routers import user ,company,task,auth


app = FastAPI()

app.include_router(user.router)
app.include_router(company.router)
app.include_router(task.router)
app.include_router(auth.router)




@app.get("/", tags=["Task of User"])
async def health_check():
    return "APP Service FASTAPI is up and running!"