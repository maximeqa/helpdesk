"""
Production server for Render deployment using Waitress
"""
import os
from waitress import serve
from app import create_app

def main():
    app = create_app()
    app.config['DEBUG'] = False
    
    port = int(os.environ.get('PORT', 10000))
    
    print(f"Starting server on port {port}")
    print(f"Environment: {os.environ.get('RENDER_SERVICE_NAME', 'local')}")
    
    serve(
        app,
        host='0.0.0.0',
        port=port,
        threads=6, 
        connection_limit=1000,
        cleanup_interval=30,
        channel_timeout=120,
        send_bytes=18000,
        recv_bytes=65536,
        max_request_header_size=262144,
        max_request_body_size=1073741824, #1GB
    )

if __name__ == '__main__':
    main()