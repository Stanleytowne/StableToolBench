import requests
import json
import os

url = 'http://0.0.0.0:8080/virtual'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

# Test cases extracted from StableToolBench data examples
test_cases = [
    {
        "name": "Test 1: TTSKraken - List Languages (Original)",
        "data": {
            "category": "Artificial_Intelligence_Machine_Learning",
            "tool_name": "TTSKraken",
            "api_name": "List Languages",
            "tool_input": '{}',
            "strip": "truncate",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 2: Transfermarkt Search - Search for player",
        "data": {
            "category": "Sports",
            "tool_name": "theclique",
            "api_name": "transfermarkt_search_for_theclique",
            "tool_input": json.dumps({"name": "Lionel Messi"}),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 3: Transfermarkt Details - Get player details",
        "data": {
            "category": "Sports",
            "tool_name": "theclique",
            "api_name": "transfermarkt_details_for_theclique",
            "tool_input": json.dumps({
                "type_s": "players",
                "other": "",
                "id_talent": "",
                "part_slug": "lionel-messi"
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 4: Kick.com API - Get channel clips",
        "data": {
            "category": "Video, Images",
            "tool_name": "kick_com_api_kick_api",
            "api_name": "get_channel_clips_for_kick_com_api_kick_api",
            "tool_input": json.dumps({
                "cursor": "",
                "channel_name": "gmhikaru"
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 5: Kick.com API - Get channel details",
        "data": {
            "category": "Video, Images",
            "tool_name": "kick_com_api_kick_api",
            "api_name": "get_channel_details_for_kick_com_api_kick_api",
            "tool_input": json.dumps({
                "channel_name": "gmhikaru"
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 6: Keyword Analysis - Popular sites for query",
        "data": {
            "category": "Search",
            "tool_name": "keyword_analysis",
            "api_name": "popularsitesforquery_for_keyword_analysis",
            "tool_input": json.dumps({
                "q": "birthday party ideas"
            }),
            "strip": "",
            "toolbench_key": ""
        }
    },
    {
        "name": "Test 7: Keyword Analysis - Query keywords",
        "data": {
            "category": "Search",
            "tool_name": "keyword_analysis",
            "api_name": "querykeywords_for_keyword_analysis",
            "tool_input": json.dumps({
                "q": "birthday party ideas"
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
