import requests
import json

url = 'http://10.153.48.58:8080/virtual'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Test cases extracted from toolllama_G123_dfs_eval.json with successful API responses
test_cases = [
    {
        "name": "Test 1: Tokopedia - Get sorting methods (successful response)",
        "data": {
            "category": "eCommerce",
            "tool_name": "tokopedia_super_api",
            "api_name": "sortproductsmaster_for_tokopedia_super_api",
            "tool_input": json.dumps({}),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 2: Qvantana - Ultimate Oscillator for BTCUSDT",
        "data": {
            "category": "Financial",
            "tool_name": "qvantana",
            "api_name": "ultimateoscillator_for_qvantana",
            "tool_input": json.dumps({
                "exchange": "binance",
                "interval": "1d",
                "market": "spot",
                "symbol": "btcusdt",
                "backtracks": 30
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 3: Qvantana - Typical Price for BTCUSDT",
        "data": {
            "category": "Financial",
            "tool_name": "qvantana",
            "api_name": "typical_price_for_qvantana",
            "tool_input": json.dumps({
                "exchange": "binance",
                "market": "spot",
                "symbol": "btcusdt",
                "interval": "1d",
                "backtracks": 30
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 4: Qvantana - Trix indicator for BTCUSDT",
        "data": {
            "category": "Financial",
            "tool_name": "qvantana",
            "api_name": "trix_for_qvantana",
            "tool_input": json.dumps({
                "exchange": "binance",
                "market": "spot",
                "symbol": "btcusdt",
                "interval": "1d",
                "backtracks": 30
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 5: Twelve Data - MAXINDEX for AAPL",
        "data": {
            "category": "Financial",
            "tool_name": "twelve_data",
            "api_name": "maxindex_for_twelve_data",
            "tool_input": json.dumps({
                "interval": "1day",
                "symbol": "AAPL",
                "series_type": "close",
                "outputsize": 100
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 6: Twelve Data - MINMAX for AAPL",
        "data": {
            "category": "Financial",
            "tool_name": "twelve_data",
            "api_name": "minmax_for_twelve_data",
            "tool_input": json.dumps({
                "interval": "1day",
                "symbol": "AAPL",
                "series_type": "close",
                "outputsize": 100
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 7: Twelve Data - TEMA for AAPL",
        "data": {
            "category": "Financial",
            "tool_name": "twelve_data",
            "api_name": "tema_for_twelve_data",
            "tool_input": json.dumps({
                "interval": "1day",
                "symbol": "AAPL",
                "series_type": "close",
                "outputsize": 100,
                "time_period": 14
            }),
            "strip": "",
            "toolbench_key": ""
        }
    }
]

def run_test(test_case):
    """Run a single test case"""
    print(f"\n{'='*80}")
    print(f"{test_case['name']}")
    print(f"{'='*80}")
    print(f"Request data: {json.dumps(test_case['data'], indent=2)}")
    print(f"\nSending request...")
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(test_case['data']), timeout=60)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting API Server Tests")
    print(f"Server URL: {url}")
    
    results = []
    for test_case in test_cases:
        success = run_test(test_case)
        results.append((test_case['name'], success))
    
    # Print summary
    print(f"\n{'='*80}")
    print("Test Summary")
    print(f"{'='*80}")
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")
