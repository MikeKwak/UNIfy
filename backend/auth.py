"""
JWT Authentication module for AWS Cognito integration
"""

import jwt
import requests
import json
import os
from functools import wraps
from flask import request, jsonify
from typing import Dict, Any, Optional

# AWS Cognito configuration
AWS_REGION = os.environ.get('COGNITO_REGION', 'us-east-1')
AWS_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID', '')
AWS_USER_POOL_CLIENT_ID = os.environ.get('COGNITO_USER_POOL_CLIENT_ID', '')

# Cache for JWKS (JSON Web Key Set)
_jwks_cache = None
_jwks_cache_timestamp = 0
JWKS_CACHE_DURATION = 3600  # 1 hour in seconds

def get_jwks() -> Dict[str, Any]:
    """
    Fetch and cache the JWKS from AWS Cognito.
    """
    global _jwks_cache, _jwks_cache_timestamp
    import time
    
    current_time = time.time()
    
    # Return cached JWKS if still valid
    if _jwks_cache and (current_time - _jwks_cache_timestamp) < JWKS_CACHE_DURATION:
        return _jwks_cache
    
    try:
        jwks_url = f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{AWS_USER_POOL_ID}/.well-known/jwks.json"
        response = requests.get(jwks_url, timeout=10)
        response.raise_for_status()
        
        _jwks_cache = response.json()
        _jwks_cache_timestamp = current_time
        
        return _jwks_cache
    except Exception as e:
        print(f"Error fetching JWKS: {e}")
        return {}

def get_public_key(token: str) -> Optional[str]:
    """
    Get the public key for verifying the JWT token.
    """
    try:
        # Decode the header to get the key ID
        header = jwt.get_unverified_header(token)
        kid = header.get('kid')
        
        if not kid:
            return None
        
        # Get JWKS
        jwks = get_jwks()
        keys = jwks.get('keys', [])
        
        # Find the key with matching kid
        for key in keys:
            if key.get('kid') == kid:
                # Convert JWK to PEM format
                from jwt.algorithms import RSAAlgorithm
                return RSAAlgorithm.from_jwk(json.dumps(key))
        
        return None
    except Exception as e:
        print(f"Error getting public key: {e}")
        return None

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode the JWT token.
    """
    try:
        # Get the public key
        public_key = get_public_key(token)
        if not public_key:
            return None
        
        # Verify and decode the token
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=AWS_USER_POOL_CLIENT_ID,
            issuer=f"https://cognito-idp.{AWS_REGION}.amazonaws.com/{AWS_USER_POOL_ID}"
        )
        
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None

def require_auth(f):
    """
    Decorator to require authentication for Flask routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip auth for health check and test endpoints
        if request.endpoint in ['health_check', 'test_recommendations']:
            return f(*args, **kwargs)
        
        # TEMPORARY: Skip auth for recommendations endpoint during development
        if request.endpoint == 'get_university_recommendations':
            print("TEMPORARILY SKIPPING AUTH FOR RECOMMENDATIONS ENDPOINT")
            # Add a mock user for development
            request.user = {
                'user_id': 'dev-user-123',
                'email': 'dev@example.com',
                'username': 'devuser',
                'groups': []
            }
            return f(*args, **kwargs)
        
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        print(f"Authorization header: {auth_header}")
        print(f"All headers: {dict(request.headers)}")
        
        if not auth_header:
            print("No Authorization header found")
            return jsonify({
                "success": False,
                "error": {
                    "code": "MISSING_AUTH",
                    "message": "Authorization header is required"
                }
            }), 401
        
        # Extract the token
        try:
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                raise ValueError("Invalid authorization scheme")
        except ValueError:
            return jsonify({
                "success": False,
                "error": {
                    "code": "INVALID_AUTH_SCHEME",
                    "message": "Authorization header must be 'Bearer <token>'"
                }
            }), 401
        
        # Verify the token
        print(f"Verifying token: {token[:50]}...")
        payload = verify_token(token)
        print(f"Token verification result: {payload}")
        
        if not payload:
            print("Token verification failed")
            return jsonify({
                "success": False,
                "error": {
                    "code": "INVALID_TOKEN",
                    "message": "Invalid or expired token"
                }
            }), 401
        
        # Add user info to the request context
        request.user = {
            'user_id': payload.get('sub'),
            'email': payload.get('email'),
            'username': payload.get('cognito:username'),
            'groups': payload.get('cognito:groups', [])
        }
        
        return f(*args, **kwargs)
    
    return decorated_function

def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Get the current authenticated user from the request context.
    """
    return getattr(request, 'user', None)
