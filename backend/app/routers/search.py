"""
Search router: hybrid search with FTS5 and embeddings.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import get_current_admin
from backend.app.models.schemas import SearchRequest, SearchResponse
from backend.app.services.search import build_fts_index, hybrid_search

router = APIRouter(prefix="/api/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search_records(data: SearchRequest, db: Session = Depends(get_db)):
    """Search records using hybrid (FTS5 + embeddings) search."""
    if not data.query or not data.query.strip():
        return SearchResponse(query="", results=[], total=0, search_method="none")

    results, method = hybrid_search(
        query=data.query.strip(),
        db=db,
        category=data.category,
        state=data.state,
        record_type=data.record_type,
        top_k=data.limit,
    )

    return SearchResponse(
        query=data.query,
        results=results,
        total=len(results),
        search_method=method,
    )


@router.post("/reindex")
def reindex_search(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    """Admin: rebuild the FTS5 search index."""
    count = build_fts_index(db)
    return {"message": f"FTS5 index rebuilt successfully with {count} chunks"}
