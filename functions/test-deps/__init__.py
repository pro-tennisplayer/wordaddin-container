import azure.functions as func
import json
import sys

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Test function to check dependencies and diagnose issues"""
    try:
        # Test basic imports
        test_results = {
            'status': 'testing',
            'python_version': sys.version,
            'imports': {},
            'database_test': {}
        }
        
        # Test psycopg2 import
        try:
            import psycopg2
            test_results['imports']['psycopg2'] = 'SUCCESS'
            test_results['imports']['psycopg2_version'] = psycopg2.__version__
        except ImportError as e:
            test_results['imports']['psycopg2'] = f'FAILED: {str(e)}'
        
        # Test other imports
        try:
            import uuid
            test_results['imports']['uuid'] = 'SUCCESS'
        except ImportError as e:
            test_results['imports']['uuid'] = f'FAILED: {str(e)}'
            
        try:
            from datetime import datetime
            test_results['imports']['datetime'] = 'SUCCESS'
        except ImportError as e:
            test_results['imports']['datetime'] = f'FAILED: {str(e)}'
        
        # Test database connection
        try:
            import psycopg2
            conn = psycopg2.connect(
                host="apex-psql-toebb934.postgres.database.azure.com",
                database="apexdb",
                user="psqladmin",
                password="ApexSecurePass123!",
                port="5432"
            )
            test_results['database_test']['connection'] = 'SUCCESS'
            conn.close()
        except Exception as e:
            test_results['database_test']['connection'] = f'FAILED: {str(e)}'
        
        return func.HttpResponse(
            json.dumps(test_results, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'error': str(e),
                'traceback': str(sys.exc_info())
            }),
            status_code=500,
            mimetype="application/json"
        )
