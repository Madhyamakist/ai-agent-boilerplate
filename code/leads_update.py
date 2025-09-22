from db import sync_connection

def update_lead(session_id: str, status: str = None, remarks: str = None):

    """
    Update lead in mock DB
    Returns: (updated_lead_dict, error_message, http_code)
    """
    try:
        sync_connection.rollback()
        
        with sync_connection.cursor() as cur:
            insert_query = """
            INSERT INTO chat_info (
                session_id,
                status, 
                remarks
            ) VALUES (%s, %s, %s)
            ON CONFLICT (session_id) 
            DO UPDATE SET 
                status = CASE 
                    WHEN EXCLUDED.status IS NOT NULL THEN EXCLUDED.status 
                    ELSE chat_info.status 
                END,
                remarks = CASE 
                    WHEN EXCLUDED.remarks IS NOT NULL THEN EXCLUDED.remarks 
                    ELSE chat_info.remarks 
                END
            """
            
            cur.execute(insert_query, (
                session_id,
                status,
                remarks
            ))

            sync_connection.commit()            
            
            # Log what was updated
            updates = []
            if status: updates.append(f"status='{status}'")
            if remarks: updates.append(f"remarks='{remarks}'")
            
            print(f"[DATABASE] Info updated for session {session_id}: {', '.join(updates) if updates else 'no new info'}")
    
    except Exception as e:
        sync_connection.rollback()
        print(f"[DATABASE ERROR] Failed to update lead for {session_id}: {str(e)}")
        raise
