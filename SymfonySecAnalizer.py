import requests
from requests.exceptions import RequestException
# m10sec@proton.me
# URL de la aplicación Symfony a analizar
target_url = "http://example.com"  # Cambia esta URL al sitio objetivo

# Lista de pruebas para detectar problemas comunes en Symfony, incluyendo profiler y archivos confidenciales
tests = {
    "exposed_env_file": "/.env",
    "exposed_config": "/config.php",
    "exposed_vendor": "/vendor/autoload.php",
    "error_log": "/error_log",
    "console_route": "/_profiler",
    "app_dev": "/app_dev.php",
    "profiler_debug": "/app_dev.php/_profiler",  # Acceso directo al profiler en modo debug
    "phpinfo": "/app_dev.php/_profiler/phpinfo",  # Página de phpinfo en profiler
    "file_open": "/app_dev.php/_profiler/open?file=app/config/parameters.yml",  # Intento de acceso a archivo sensible
}

# Función para obtener la versión de Symfony mediante los headers
def get_symfony_version(response_headers):
    version = response_headers.get("X-Symfony-Version", None)
    if version:
        print(f"Symfony Version Detected: {version}")
        return version
    else:
        print("No Symfony version detected in headers.")
        return None

# Función para realizar las pruebas
def run_tests(url, test_paths):
    results = {}
    for test, path in test_paths.items():
        test_url = f"{url.rstrip('/')}{path}"
        try:
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                print(f"[+] {test} found at {test_url}")
                results[test] = test_url
            else:
                print(f"[-] {test} not found at {test_url}")
        except RequestException as e:
            print(f"[!] Error testing {test_url}: {e}")
    return results

# Ejecución del POC
try:
    response = requests.get(target_url, timeout=5)
    if response.status_code == 200:
        print("Target is reachable.")
        version = get_symfony_version(response.headers)
        results = run_tests(target_url, tests)
        print("\nTest Results:")
        for test, url in results.items():
            print(f"{test}: {url}")
    else:
        print("Failed to reach the target.")
except RequestException as e:
    print(f"Failed to connect to target: {e}")