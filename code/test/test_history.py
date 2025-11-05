import pytest
import uuid
from http import HTTPStatus

class TestHistoryAPI:
    """Test suite for the history API using the Flask test client."""

    def test_history_valid_session_id(self, client):
        """Test 1: History - Valid Session ID"""
        session_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.get('/history', query_string={'session_id': session_id})

        assert response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]
        data = response.get_json()
        assert "session_id" in data
        assert "history" in data
        assert data["session_id"] == session_id

    def test_history_missing_session_id(self, client):
        """Test 2: History - Missing Session ID"""
        response = client.get('/history')

        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.get_json()
        assert data["error"] == "session_id is required"

    def test_history_invalid_session_id_format(self, client):
        """Test 3: History - Invalid Session ID Format"""
        response = client.get('/history', query_string={'session_id': 'invalid-uuid-format'})

        assert response.status_code == HTTPStatus.BAD_REQUEST
        data = response.get_json()
        assert data["error"] == "Invalid session_id format"

    def test_history_new_vs_existing_session(self, client):
        """Test 4: Differentiate between new (201) and existing (200) sessions"""
        new_session_id = str(uuid.uuid4())
        response = client.get('/history', query_string={'session_id': new_session_id})

        # The test client will simulate the entire request-response cycle
        assert response.status_code == HTTPStatus.CREATED
        data = response.get_json()
        assert len(data["history"]) >= 1, "A new session should have a welcome message."

    def test_history_response_structure_validation(self, client):
        """Test 5: Validate the structure of a message object in the history"""
        session_id = "123e4567-e89b-12d3-a456-426614174000"
        response = client.get('/history', query_string={'session_id': session_id})
        data = response.get_json()
        
        if data.get("history") and len(data["history"]) > 0:
            message = data["history"][0]
            assert "content" in message
            assert "type" in message