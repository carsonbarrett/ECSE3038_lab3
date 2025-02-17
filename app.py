from fastapi import FastAPI, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from uuid import UUID, uuid4

app = FastAPI()

data = []

class tank(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    location: str
    lat: float
    long: float
    

class Tank_Update(BaseModel):
    location: str | None = None
    lat: float | None = None
    long: float | None = None

@app.get("/tank")
async def get_all_tank():
   return JSONResponse(content=jsonable_encoder(data))

@app.get("/tank/{id}")
async def get_all_tank_by_id(id: UUID):
    for tank in data:
        if tank.id == id:  
            return JSONResponse(content=jsonable_encoder(tank))
    return JSONResponse(status_code=404, content={"error error": "Check again nuh man"}) 

@app.post("/tank")
async def add_all_tank(tank_request: tank):
    data.append(tank_request)
    tank_json = jsonable_encoder(tank_request)

    return JSONResponse(status_code=201, content={"Successfully Created": True, "result": tank_json})

@app.patch("/tank/{id}")
async def update_all_tank(id: UUID, tank_update: Tank_Update):
         
         for i, tank in enumerate(data):
              if tank.id == id: 
                 tank_update_dict = tank_update.model_dump(exclude_unset=True)

                 try: 
                         updated_tank = tank.copy(update = tank_update_dict)
                         data[i] = tank.model_validate(updated_tank)
                         json_updated_tank = jsonable_encoder(updated_tank)

                         return JSONResponse(json_updated_tank, status_code=200)
                 except ValidationError:
                    raise HTTPException(status_code=400, detail="Ensure there's a location, lat and long before you try againi :)")
              raise HTTPException(status_code=404, detail="Just Try Again:)")   


@app.delete("/tank/{id}") 
async def delete_all_tank(id: UUID):
    for tank in data:
            if tank.id == id:
                data.remove(tank)
            return Response(status_code=204) 
    raise HTTPException(status_code=404, detail="look again nuh ute it nuh deh yah")
