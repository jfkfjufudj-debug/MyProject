"""
===================================================================
Video Extractor Server - Professional Authentication & Security
===================================================================
Author: Professional Development Team
Version: 1.0.0
Description: Advanced API authentication and security middleware
"""

import time
import hashlib
from typing import Dict, Optional, List
from collections import defaultdict, deque
from fastapi import HTTPException, Security, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger

from config.settings import settings

class SecurityManager:
    """
    Professional security manager with rate limiting and API key validation
    """
    
    def __init__(self):
        """Initialize security manager"""
        self.api_keys = self._load_api_keys()
        self.rate_limiter = RateLimiter()
        self.blocked_ips = set()
        self.suspicious_activities = defaultdict(list)
        
        # Security settings
        self.max_requests_per_minute = settings.MAX_REQUESTS_PER_MINUTE
        self.max_failed_attempts = 5
        self.block_duration = 3600  # 1 hour in seconds
        
        logger.info("Security manager initialized")
    
    def _load_api_keys(self) -> Dict[str, Dict]:
        """Load and validate API keys"""
        # In production, load from secure database or encrypted file
        # For now, using settings-based approach
        api_keys = {
            settings.API_KEY: {
                'name': 'default_key',
                'permissions': ['extract', 'download'],
                'rate_limit': settings.MAX_REQUESTS_PER_MINUTE,
                'created_at': time.time(),
                'last_used': None,
                'usage_count': 0
            }
        }
        
        # Add additional API keys if configured
        # This can be extended to support multiple keys
        return api_keys
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate API key and return key info"""
        if not api_key:
            return None
        
        key_info = self.api_keys.get(api_key)
        if key_info:
            # Update usage statistics
            key_info['last_used'] = time.time()
            key_info['usage_count'] += 1
            logger.debug(f"API key validated: {key_info['name']}")
            return key_info
        
        logger.warning(f"Invalid API key attempted: {api_key[:10]}...")
        return None
    
    def check_permissions(self, key_info: Dict, required_permission: str) -> bool:
        """Check if API key has required permissions"""
        return required_permission in key_info.get('permissions', [])
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Check if IP address is blocked"""
        return ip_address in self.blocked_ips
    
    def block_ip(self, ip_address: str, reason: str = "Security violation"):
        """Block IP address"""
        self.blocked_ips.add(ip_address)
        logger.warning(f"IP blocked: {ip_address} - Reason: {reason}")
        
        # Schedule unblock (in production, use proper task scheduler)
        # For now, we'll rely on periodic cleanup
    
    def record_suspicious_activity(self, ip_address: str, activity: str):
        """Record suspicious activity"""
        current_time = time.time()
        self.suspicious_activities[ip_address].append({
            'activity': activity,
            'timestamp': current_time
        })
        
        # Clean old activities (older than 1 hour)
        self.suspicious_activities[ip_address] = [
            act for act in self.suspicious_activities[ip_address]
            if current_time - act['timestamp'] < 3600
        ]
        
        # Check if IP should be blocked
        recent_activities = len(self.suspicious_activities[ip_address])
        if recent_activities >= self.max_failed_attempts:
            self.block_ip(ip_address, f"Too many suspicious activities: {recent_activities}")
    
    def cleanup_blocked_ips(self):
        """Clean up expired IP blocks (call periodically)"""
        # In production, implement proper expiration tracking
        # For now, this is a placeholder
        pass

class RateLimiter:
    """
    Professional rate limiter with sliding window algorithm
    """
    
    def __init__(self):
        """Initialize rate limiter"""
        self.requests = defaultdict(deque)
        self.window_size = 60  # 1 minute window
    
    def is_allowed(self, identifier: str, limit: int) -> bool:
        """Check if request is allowed under rate limit"""
        current_time = time.time()
        
        # Clean old requests outside the window
        while (self.requests[identifier] and 
               current_time - self.requests[identifier][0] > self.window_size):
            self.requests[identifier].popleft()
        
        # Check if under limit
        if len(self.requests[identifier]) < limit:
            self.requests[identifier].append(current_time)
            return True
        
        return False
    
    def get_remaining_requests(self, identifier: str, limit: int) -> int:
        """Get remaining requests for identifier"""
        current_time = time.time()
        
        # Clean old requests
        while (self.requests[identifier] and 
               current_time - self.requests[identifier][0] > self.window_size):
            self.requests[identifier].popleft()
        
        return max(0, limit - len(self.requests[identifier]))
    
    def get_reset_time(self, identifier: str) -> float:
        """Get time when rate limit resets"""
        if not self.requests[identifier]:
            return time.time()
        
        return self.requests[identifier][0] + self.window_size

class APIKeyValidator:
    """
    FastAPI dependency for API key validation
    """
    
    def __init__(self, required_permission: str = None):
        self.required_permission = required_permission
        self.security = HTTPBearer(auto_error=False)
    
    async def __call__(
        self, 
        request: Request,
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer(auto_error=False))
    ) -> Dict:
        """Validate API key from request"""
        
        # Get client IP
        client_ip = self._get_client_ip(request)
        
        # Check if IP is blocked
        if security_manager.is_ip_blocked(client_ip):
            logger.warning(f"Blocked IP attempted access: {client_ip}")
            raise HTTPException(
                status_code=403,
                detail="Access denied: IP address is blocked"
            )
        
        # Extract API key
        api_key = None
        
        # Try Authorization header first
        if credentials:
            api_key = credentials.credentials
        
        # Try query parameter as fallback
        if not api_key:
            api_key = request.query_params.get('api_key')
        
        # Try custom header
        if not api_key:
            api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            security_manager.record_suspicious_activity(client_ip, "Missing API key")
            raise HTTPException(
                status_code=401,
                detail="API key required"
            )
        
        # Validate API key
        key_info = security_manager.validate_api_key(api_key)
        if not key_info:
            security_manager.record_suspicious_activity(client_ip, "Invalid API key")
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        
        # Check permissions
        if self.required_permission:
            if not security_manager.check_permissions(key_info, self.required_permission):
                security_manager.record_suspicious_activity(
                    client_ip, 
                    f"Insufficient permissions: {self.required_permission}"
                )
                raise HTTPException(
                    status_code=403,
                    detail=f"Insufficient permissions: {self.required_permission} required"
                )
        
        # Check rate limit
        rate_limit = key_info.get('rate_limit', settings.MAX_REQUESTS_PER_MINUTE)
        if not security_manager.rate_limiter.is_allowed(api_key, rate_limit):
            logger.warning(f"Rate limit exceeded for API key: {key_info['name']}")
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={
                    "X-RateLimit-Limit": str(rate_limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(int(security_manager.rate_limiter.get_reset_time(api_key)))
                }
            )
        
        # Add rate limit headers to response (will be handled by middleware)
        remaining = security_manager.rate_limiter.get_remaining_requests(api_key, rate_limit)
        reset_time = security_manager.rate_limiter.get_reset_time(api_key)
        
        return {
            'api_key_info': key_info,
            'client_ip': client_ip,
            'rate_limit_headers': {
                "X-RateLimit-Limit": str(rate_limit),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(int(reset_time))
            }
        }
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request"""
        # Check for forwarded headers (proxy/load balancer)
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            # Take the first IP in the chain
            return forwarded_for.split(',')[0].strip()
        
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        # Fallback to direct connection IP
        return request.client.host if request.client else "unknown"

# Security middleware for additional protection
async def security_middleware(request: Request, call_next):
    """Security middleware for additional request validation"""
    
    # Add security headers to response
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    # Add rate limit headers if available
    if hasattr(request.state, 'rate_limit_headers'):
        for header, value in request.state.rate_limit_headers.items():
            response.headers[header] = value
    
    return response

# Global instances
security_manager = SecurityManager()

# Dependency factories
def require_api_key():
    """Require valid API key"""
    return APIKeyValidator()

def require_extract_permission():
    """Require API key with extract permission"""
    return APIKeyValidator(required_permission='extract')

def require_download_permission():
    """Require API key with download permission"""
    return APIKeyValidator(required_permission='download')

# Utility functions
def get_api_key_info(auth_data: Dict = Depends(require_api_key())) -> Dict:
    """Get API key information from auth data"""
    return auth_data['api_key_info']

def get_client_ip(auth_data: Dict = Depends(require_api_key())) -> str:
    """Get client IP from auth data"""
    return auth_data['client_ip']
