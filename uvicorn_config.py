import uvicorn
from typing import Dict, Any

# Development configuration
dev_config: Dict[str, Any] = {
    "app": "main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "reload_dirs": ["."],
    "workers": 1,
    "log_level": "debug",
    "access_log": True,
    "use_colors": True,
    "proxy_headers": True,
    "forwarded_allow_ips": "*"
}

# Production configuration
prod_config: Dict[str, Any] = {
    "app": "main:app",
    "host": "0.0.0.0",
    "port": 8000,
    "reload": False,
    "workers": 4,
    "log_level": "info",
    "access_log": True,
    "proxy_headers": True,
    "forwarded_allow_ips": "*"
}

def run_dev():
    """Run the application in development mode"""
    uvicorn.run(**dev_config)

def run_prod():
    """Run the application in production mode"""
    uvicorn.run(**prod_config)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        run_prod()
    else:
        run_dev() 