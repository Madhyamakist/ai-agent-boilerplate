from db import sync_connection


def delete_chat_info(session_id: str) -> bool:
    '''
    delete a row in chat_info  table.

    '''
    try:
        with sync_connection.cursor() as cur:
            cur.execute(
                "DELETE FROM chat_info WHERE session_id = %s RETURNING session_id;", 
                (session_id,)
                )
            deleted_row = cur.fetchone()
            sync_connection.commit()
            return bool(deleted_row)
    except Exception as e:
        sync_connection.rollback()
        print(f"[DATABASE ERROR] Failed to delete lead {session_id}: {e}")
        raise
