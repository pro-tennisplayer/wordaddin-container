import azure.functions as func
import json
import subprocess
import sys
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Install dependencies at runtime"""
    try:
        result = {
            'status': 'installing_dependencies',
            'python_path': sys.executable,
            'pip_path': None,
            'install_attempt': {}
        }
        
        # Try to find pip
        try:
            import pip
            result['pip_path'] = pip.__file__
        except ImportError:
            result['pip_path'] = 'pip not found'
        
        # Try to install psycopg2
        try:
            # Use subprocess to install package
            install_result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', 'psycopg2-binary==2.9.9'
            ], capture_output=True, text=True, timeout=60)
            
            result['install_attempt']['return_code'] = install_result.returncode
            result['install_attempt']['stdout'] = install_result.stdout
            result['install_attempt']['stderr'] = install_result.stderr
            
            if install_result.returncode == 0:
                result['install_attempt']['status'] = 'SUCCESS'
                
                # Try to import after installation
                try:
                    import psycopg2
                    result['install_attempt']['import_test'] = 'SUCCESS'
                    result['install_attempt']['version'] = psycopg2.__version__
                except ImportError as e:
                    result['install_attempt']['import_test'] = f'FAILED: {str(e)}'
            else:
                result['install_attempt']['status'] = 'FAILED'
                
        except Exception as e:
            result['install_attempt']['error'] = str(e)
        
        return func.HttpResponse(
            json.dumps(result, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                'status': 'error',
                'error': str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
