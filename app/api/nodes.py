router = APIRouter(prefix="/nodes", tags=["nodes"], dependencies=[Depends(parse_token)])

@router.post("/register", response_model=NodeOut, status_code=201)
async def register(node: NodeIn):
    node_id = str(uuid.uuid4())
    await pool.execute(
        """INSERT INTO nodes(id,ip,country,wg_port,ss_port,vless_port)
           VALUES(?,?,?,?,?,?)""",
        (node_id, node.ip, node.country, node.wg_port, node.ss_port, node.vless_port)
    ); await pool.commit()
    return {**node.dict(), "id": node_id, "load": 0}

@router.post("/{node_id}/heartbeat")
async def heartbeat(node_id: str, load: int):
    cur = await pool.execute("UPDATE nodes SET load=? WHERE id=?", (load, node_id))
    await pool.commit()
    if cur.rowcount == 0:
        raise HTTPException(404)

@router.post("/{node_id}/usage")
async def push_usage(node_id: str, user_id: str, up: int, down: int):
    await pool.execute(
        """INSERT INTO usage(user_id,node_id,date,bytes_up,bytes_down)
           VALUES (?,?,date('now'),?,?)
           ON CONFLICT(user_id,node_id,date) DO UPDATE
           SET bytes_up  = bytes_up  + excluded.bytes_up,
               bytes_down= bytes_down+ excluded.bytes_down
        """, (user_id, node_id, up, down))
    await pool.commit()