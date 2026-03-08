#!/usr/bin/env python3
"""
Development Environment Verification Script
Checks if all required services are running and accessible.
"""

import sys
import time
import requests
import mysql.connector
import redis
from typing import Dict, List, Tuple


def check_service(name: str, check_func) -> Tuple[bool, str]:
    """Check if a service is running."""
    try:
        result = check_func()
        return True, result
    except Exception as e:
        return False, str(e)


def check_mysql() -> str:
    """Check MySQL connection."""
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='user',
        password='password',
        database='trialmatch'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    conn.close()
    return f"MySQL {version}"


def check_redis() -> str:
    """Check Redis connection."""
    r = redis.Redis(host='localhost', port=6379, db=0)
    info = r.info()
    return f"Redis {info['redis_version']}"


def check_localstack() -> str:
    """Check LocalStack health."""
    response = requests.get('http://localhost:4566/_localstack/health', timeout=5)
    if response.status_code == 200:
        health = response.json()
        services = [k for k, v in health.get('services', {}).items() if v == 'available']
        return f"LocalStack - {len(services)} services available: {', '.join(services[:5])}"
    return "LocalStack - Health check failed"


def check_opensearch() -> str:
    """Check OpenSearch cluster."""
    response = requests.get('http://localhost:9200/_cluster/health', timeout=5)
    if response.status_code == 200:
        health = response.json()
        return f"OpenSearch - {health['status']} ({health['number_of_nodes']} nodes)"
    return "OpenSearch - Health check failed"


def main():
    """Run all service checks."""
    print("🔍 Clinical Trial Matcher - Development Environment Verification")
    print("=" * 60)
    
    services = [
        ("MySQL Database", check_mysql),
        ("Redis Cache", check_redis),
        ("LocalStack (AWS)", check_localstack),
        ("OpenSearch", check_opensearch),
    ]
    
    results: List[Tuple[str, bool, str]] = []
    
    for name, check_func in services:
        print(f"Checking {name}...", end=" ")
        success, message = check_service(name, check_func)
        
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        results.append((name, success, message))
    
    print("\n" + "=" * 60)
    
    # Summary
    successful = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    if successful == total:
        print(f"🎉 All {total} services are running correctly!")
        print("\nYou can now start the backend and frontend servers:")
        print("  Backend:  cd backend && uvicorn src.main:app --reload")
        print("  Frontend: cd frontend && npm run dev")
    else:
        print(f"⚠️  {successful}/{total} services are running.")
        print("\nFailed services:")
        for name, success, message in results:
            if not success:
                print(f"  - {name}: {message}")
        
        print("\nTo fix issues:")
        print("  1. Make sure Docker is running: docker --version")
        print("  2. Start services: docker-compose up -d")
        print("  3. Check logs: docker-compose logs [service-name]")
        print("  4. Wait for services to be ready (may take 1-2 minutes)")
        
        sys.exit(1)


if __name__ == "__main__":
    main()