from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Allow our React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, you would lock this down
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    conn = sqlite3.connect('space_data.db')
    conn.row_factory = sqlite3.Row # This lets us access columns by name
    return conn

@app.get("/api/launches")
def get_launches():
    """Returns total launch counts and success rates grouped by agency."""
    conn = get_db_connection()
    # A classic SQL aggregation query (Recruiters love this)
    query = """
        SELECT 
            agency, 
            COUNT(*) as total_launches,
            SUM(CASE WHEN is_success = 1 THEN 1 ELSE 0 END) as successful_launches
        FROM launches
        GROUP BY agency
        ORDER BY total_launches DESC
    """
    launches = conn.execute(query).fetchall()
    conn.close()
    
    # Convert SQL rows to JSON dictionaries
    return [dict(row) for row in launches]

@app.get("/api/timeline")
def get_timeline():
    """Returns launch volume grouped by year and agency."""
    conn = get_db_connection()
    query = """
        SELECT year, agency, COUNT(*) as launches
        FROM launches
        GROUP BY year, agency
        ORDER BY year ASC
    """
    timeline = conn.execute(query).fetchall()
    conn.close()
    
    return [dict(row) for row in timeline]

