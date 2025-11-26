"""
Test script to diagnose FastAPI application loading issues.
Run this to identify what's preventing Swagger UI from loading.
"""

import sys
import traceback

def test_basic_imports():
    """Test if basic imports work."""
    print("Step 1: Testing basic imports...")
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        print("  ✓ All basic packages imported successfully")
        return True
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False


def test_app_creation():
    """Test if FastAPI app can be created."""
    print("\nStep 2: Testing FastAPI app creation...")
    try:
        from fastapi import FastAPI
        app = FastAPI()
        print("  ✓ FastAPI app created successfully")
        return True
    except Exception as e:
        print(f"  ✗ App creation error: {e}")
        traceback.print_exc()
        return False


def test_database_models():
    """Test if database models load correctly."""
    print("\nStep 3: Testing database models...")
    try:
        from app.models.user import User
        from app.models.post import Post
        from app.models.comment import Comment
        print("  ✓ All models loaded successfully")
        return True
    except Exception as e:
        print(f"  ✗ Model loading error: {e}")
        traceback.print_exc()
        return False


def test_schemas():
    """Test if Pydantic schemas load correctly."""
    print("\nStep 4: Testing Pydantic schemas...")
    try:
        from app.schemas.user import UserCreate, UserOut
        from app.schemas.post import PostCreate, PostOut
        from app.schemas.comment import CommentCreate, CommentOut
        print("  ✓ All schemas loaded successfully")
        return True
    except Exception as e:
        print(f"  ✗ Schema loading error: {e}")
        traceback.print_exc()
        return False


def test_routers():
    """Test if routers load correctly."""
    print("\nStep 5: Testing routers...")
    try:
        from app.routers import users, posts, comments
        print("  ✓ All routers loaded successfully")
        return True
    except Exception as e:
        print(f"  ✗ Router loading error: {e}")
        traceback.print_exc()
        return False


def test_main_app():
    """Test if main app loads correctly."""
    print("\nStep 6: Testing main application...")
    try:
        from app.main import app
        print("  ✓ Main application loaded successfully")
        print(f"  ✓ App title: {app.title}")
        print(f"  ✓ Docs URL: {app.docs_url}")
        return True
    except Exception as e:
        print(f"  ✗ Main app loading error: {e}")
        traceback.print_exc()
        return False


def test_openapi_schema():
    """Test if OpenAPI schema can be generated."""
    print("\nStep 7: Testing OpenAPI schema generation...")
    try:
        from app.main import app
        schema = app.openapi()
        if schema and 'paths' in schema:
            print(f"  ✓ OpenAPI schema generated successfully")
            print(f"  ✓ Found {len(schema['paths'])} endpoints")
            return True
        else:
            print("  ✗ OpenAPI schema is empty or invalid")
            return False
    except Exception as e:
        print(f"  ✗ Schema generation error: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("FastAPI Application Loading Diagnostic")
    print("="*60)
    
    tests = [
        test_basic_imports,
        test_app_creation,
        test_database_models,
        test_schemas,
        test_routers,
        test_main_app,
        test_openapi_schema
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        if not result:
            print("\n" + "="*60)
            print("TEST FAILED - Stopping here")
            print("="*60)
            break
    
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\nAll tests passed! The app should work.")
        print("Try starting with: uvicorn app.main:app --reload")
    else:
        print("\nSome tests failed. Fix the errors above before starting the server.")


if __name__ == "__main__":
    main()