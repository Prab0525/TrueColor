"""
API Testing Script
Use this to test the /analyze endpoint with a sample image
"""

import requests
import json
import sys

def test_analyze_endpoint(image_path: str, endpoint: str = "http://localhost:8000/analyze"):
    """
    Test the /analyze endpoint with an image
    
    Args:
        image_path: Path to test image
        endpoint: API endpoint URL
    """
    print(f"Testing {endpoint} with image: {image_path}")
    print("-" * 60)
    
    try:
        # Open and send image
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            response = requests.post(endpoint, files=files)
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print("\nResults:")
            print(json.dumps(result, indent=2))
            
            print("\n📊 Analysis Summary:")
            print(f"  Skin LAB: L={result['skinLAB'][0]:.1f}, A={result['skinLAB'][1]:.1f}, B={result['skinLAB'][2]:.1f}")
            print(f"  Undertone: {result['undertone']}")
            print(f"  Pantone Family: {result['pantone_family']}")
            print(f"\n💄 Recommended Shades:")
            print(f"  Fenty Beauty: {', '.join(result['fenty'])}")
            print(f"  NARS: {', '.join(result['nars'])}")
            print(f"  Too Faced: {', '.join(result['tooFaced'])}")
            
        else:
            print(f"❌ Error {response.status_code}")
            print(response.json())
            
    except FileNotFoundError:
        print(f"❌ Image file not found: {image_path}")
    except requests.exceptions.ConnectionError:
        print(f"❌ Could not connect to {endpoint}")
        print("Make sure the server is running (python run.py)")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_health_endpoint(endpoint: str = "http://localhost:8000/health"):
    """Test the health check endpoint"""
    print(f"Testing health endpoint: {endpoint}")
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            print("✅ Server is healthy")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        print("Make sure the server is running (python run.py)")


if __name__ == "__main__":
    # Test health endpoint first
    test_health_endpoint()
    
    print("\n" + "=" * 60 + "\n")
    
    # Test analyze endpoint
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        test_analyze_endpoint(image_path)
    else:
        print("Usage: python test_api.py <path_to_image>")
        print("\nExample:")
        print("  python test_api.py test_images/face1.jpg")
