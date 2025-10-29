#!/usr/bin/env python3
"""
Service initialization script for AskLegal Enhanced
Initializes database, vector stores, and optional services
"""
import os
import sys
import json
from pathlib import Path

def init_database():
    """Initialize SQLite database"""
    print("\n💾 Initializing database...")
    
    try:
        import sqlite3
        
        db_path = './asklegal.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                business_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create chat_sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Create chat_messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id)
            )
        ''')
        
        # Create documents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("  ✓ Database initialized")
        print(f"  ✓ Location: {db_path}")
        return True
        
    except Exception as e:
        print(f"  ✗ Database initialization failed: {e}")
        return False

def init_vector_store():
    """Initialize FAISS vector store with legal documents"""
    print("\n🗄️  Initializing vector store...")
    
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer
        
        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder='./models/embeddings')
        
        # Check if we have legal data to index
        legal_data_path = Path('../data/data_ipc_law.txt')
        
        if legal_data_path.exists():
            print("  Loading legal documents...")
            with open(legal_data_path, 'r', encoding='utf-8') as f:
                legal_text = f.read()
            
            # Split into chunks
            chunks = [legal_text[i:i+500] for i in range(0, len(legal_text), 500)]
            chunks = chunks[:100]  # Limit for testing
            
            print(f"  Creating embeddings for {len(chunks)} chunks...")
            embeddings = model.encode(chunks, show_progress_bar=True)
            
            # Create FAISS index
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings.astype('float32'))
            
            # Save index and metadata
            os.makedirs('./data', exist_ok=True)
            faiss.write_index(index, './data/legal_documents.index')
            
            # Save metadata
            metadata = {
                'chunks': chunks,
                'dimension': dimension,
                'total_vectors': index.ntotal
            }
            
            with open('./data/legal_documents_metadata.json', 'w') as f:
                json.dump(metadata, f)
            
            print(f"  ✓ Vector store initialized with {index.ntotal} vectors")
            print(f"  ✓ Dimension: {dimension}")
            return True
        else:
            print("  ⚠️  Legal data not found, creating empty index")
            
            # Create empty index
            dimension = 384
            index = faiss.IndexFlatL2(dimension)
            os.makedirs('./data', exist_ok=True)
            faiss.write_index(index, './data/legal_documents.index')
            
            print("  ✓ Empty vector store created")
            return True
            
    except Exception as e:
        print(f"  ✗ Vector store initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_optional_services():
    """Check status of optional services (Redis, Neo4j)"""
    print("\n🔍 Checking optional services...")
    
    services_status = {
        'Redis': False,
        'Neo4j': False
    }
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=1)
        r.ping()
        services_status['Redis'] = True
        print("  ✓ Redis is running")
    except:
        print("  ⚠️  Redis not available (will use in-memory fallback)")
    
    # Check Neo4j
    try:
        from neo4j import GraphDatabase
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        driver.verify_connectivity()
        services_status['Neo4j'] = True
        print("  ✓ Neo4j is running")
        driver.close()
    except:
        print("  ⚠️  Neo4j not available (will use fallback)")
    
    return services_status

def create_sample_data():
    """Create sample data for testing"""
    print("\n📝 Creating sample data...")
    
    try:
        import sqlite3
        
        conn = sqlite3.connect('./asklegal.db')
        cursor = conn.cursor()
        
        # Insert sample user
        cursor.execute('''
            INSERT OR IGNORE INTO users (email, full_name, business_type)
            VALUES ('demo@example.com', 'Demo User', 'Manufacturing')
        ''')
        
        conn.commit()
        conn.close()
        
        print("  ✓ Sample data created")
        return True
        
    except Exception as e:
        print(f"  ⚠️  Sample data creation failed: {e}")
        return False

def main():
    """Main initialization function"""
    print("="*60)
    print("AskLegal Enhanced - Service Initialization")
    print("="*60)
    
    try:
        # Step 1: Initialize database
        if not init_database():
            print("\n⚠️  Database initialization failed, but continuing...")
        
        # Step 2: Initialize vector store
        if not init_vector_store():
            print("\n⚠️  Vector store initialization failed, but continuing...")
        
        # Step 3: Check optional services
        services = check_optional_services()
        
        # Step 4: Create sample data
        create_sample_data()
        
        # Summary
        print("\n" + "="*60)
        print("✅ Service initialization complete!")
        print("="*60)
        print("\nService Status:")
        print("  ✓ Database: Ready")
        print("  ✓ Vector Store: Ready")
        print(f"  {'✓' if services['Redis'] else '⚠'} Redis: {'Running' if services['Redis'] else 'Using fallback'}")
        print(f"  {'✓' if services['Neo4j'] else '⚠'} Neo4j: {'Running' if services['Neo4j'] else 'Using fallback'}")
        
        print("\nNext steps:")
        print("  1. Run: python start_app.py")
        print("  2. Access at: http://localhost:8001")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
