#!/usr/bin/env python3
"""
Local Development Startup Script
Starts the local agent creation server and opens the web interface
"""

import subprocess
import threading
import time
import webbrowser
import os
import sys

def start_local_server():
    """Start the local agent creation server"""
    print("🚀 Starting local agent creation server...")
    try:
        subprocess.run([sys.executable, "local_agent_server.py"], check=True)
    except KeyboardInterrupt:
        print("🛑 Local server stopped")
    except Exception as e:
        print(f"❌ Error starting local server: {e}")

def start_web_server():
    """Start the web development server"""
    print("🌐 Starting web development server...")
    try:
        os.chdir("clara-onboarding-website")
        subprocess.run(["python", "-m", "http.server", "3001"], check=True)
    except KeyboardInterrupt:
        print("🛑 Web server stopped")
    except Exception as e:
        print(f"❌ Error starting web server: {e}")

def main():
    """Main startup function"""
    print("🎯 Clara Agent Creation - Local Development Setup")
    print("=" * 60)
    
    # Check if required files exist
    if not os.path.exists("local_agent_server.py"):
        print("❌ local_agent_server.py not found!")
        return
    
    if not os.path.exists("clara-onboarding-website"):
        print("❌ clara-onboarding-website directory not found!")
        return
    
    print("📋 Starting services...")
    print("   • Local Agent Creation Server (port 8000)")
    print("   • Web Development Server (port 3001)")
    print("   • Opening browser to http://localhost:3001")
    print("\n⏹️  Press Ctrl+C to stop all services")
    print("=" * 60)
    
    try:
        # Start local agent server in background thread
        agent_server_thread = threading.Thread(target=start_local_server, daemon=True)
        agent_server_thread.start()
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Start web server in background thread
        web_server_thread = threading.Thread(target=start_web_server, daemon=True)
        web_server_thread.start()
        
        # Wait a moment for the web server to start
        time.sleep(2)
        
        # Open browser
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:3001")
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down all services...")
        print("✅ Development environment stopped")

if __name__ == "__main__":
    main()