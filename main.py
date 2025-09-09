from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tarefas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, index=True)
    concluida = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class TarefaCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None

class TarefaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    concluida: Optional[bool] = None

class TarefaOut(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    concluida: bool
    class Config:
        orm_mode = True

app = FastAPI()

@app.post("/tarefas", response_model=TarefaOut)
def criar_tarefa(tarefa: TarefaCreate):
    db = SessionLocal()
    db_tarefa = Tarefa(titulo=tarefa.titulo, descricao=tarefa.descricao)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    db.close()
    return db_tarefa

@app.get("/tarefas", response_model=List[TarefaOut])
def listar_tarefas():
    db = SessionLocal()
    tarefas = db.query(Tarefa).all()
    db.close()
    return tarefas

@app.get("/tarefas/{tarefa_id}", response_model=TarefaOut)
def obter_tarefa(tarefa_id: int):
    db = SessionLocal()
    tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    db.close()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa

@app.put("/tarefas/{tarefa_id}", response_model=TarefaOut)
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaUpdate):
    db = SessionLocal()
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        db.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    if tarefa.titulo is not None:
        db_tarefa.titulo = tarefa.titulo
    if tarefa.descricao is not None:
        db_tarefa.descricao = tarefa.descricao
    if tarefa.concluida is not None:
        db_tarefa.concluida = tarefa.concluida
    db.commit()
    db.refresh(db_tarefa)
    db.close()
    return db_tarefa

@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    db = SessionLocal()
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        db.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db.delete(db_tarefa)
    db.commit()
    db.close()
    return {"ok": True}

@app.patch("/tarefas/{tarefa_id}/concluir", response_model=TarefaOut)
def marcar_concluida(tarefa_id: int):
    db = SessionLocal()
    db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if not db_tarefa:
        db.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    db_tarefa.concluida = True
    db.commit()
    db.refresh(db_tarefa)
    db.close()
    return db_tarefa
