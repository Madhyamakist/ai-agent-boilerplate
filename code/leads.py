from flask import Flask, jsonify
from typing import List, Dict, Any
from psycopg.rows import dict_row
from db import sync_connection  # Assuming you already have this in your project
from http import HTTPStatus

def leads() -> List[Dict[str, Any]]:
    """
    Retrieve all stored chat info records.
    """
    try:
        with sync_connection.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT 
                    session_id,
                    COALESCE(contact_name, '') as name,
                    COALESCE(email, '') as email,
                    COALESCE(mobile, '') as mobile_number,
                    COALESCE(country, '') as country,
                    COALESCE(status, 'OPEN') as status,
                    COALESCE(remarks, '') as remarks
                FROM chat_info
                ORDER BY created_at DESC;
            """)
            records = cur.fetchall()

        return records, HTTPStatus.OK

    except Exception as e:
        print("Error fetching leads:", e)
        raise

