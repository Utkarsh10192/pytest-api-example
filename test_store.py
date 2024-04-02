from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_
import json 
import time
'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def generate_random_json():
    timestamp_ms = int(time.time() * 1000)
    name = "string"  
    type = "cat"     
    status = "available"  
    
    random_json = {
        "id": timestamp_ms,
        "name": name,
        "type": type,
        "status": status
    }
    
    return json.dumps(random_json)

def test_patch_order_by_id(generate_random_json):
    create_pet_endpoint = "/pets"
    create_response = api_helpers.post_api_data(create_pet_endpoint, json.loads(generate_random_json))
    assert create_response.status_code == 201
    order_id = store_order(create_response.json().get('id'))
    patch_endpoint = "/store/order/" + order_id
    data = {
          "status": "available"
    }
    response = api_helpers.patch_api_data(patch_endpoint, data)
    assert response.status_code == 200
    assert response.json().get("message") == 'Order and pet status updated successfully'
     
def store_order(pet_id):
    create_order_endpoint = "/store/order"
    params = {
        "pet_id": pet_id
    }
    response = api_helpers.post_api_data(create_order_endpoint, params)
    assert response.status_code == 201
    if response.status_code == 201:
        validate(response.json(), schemas.order)
    return response.json().get('id')

