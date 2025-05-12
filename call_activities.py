import os
from regex import D
import requests
import logging
import json
from uuid import UUID
import csv 
from datetime import datetime, timezone
from functools import lru_cache
import base64 # Import base64 module

# define a test customer ID 
customer_id_test: str = '87b38988-d31c-4e29-97ed-7c64433cd107'

# define a test attachment 
#test_attachment_path: str = '/Users/martinmashalov/Documents/ScannedInvoicesDemo/scanned_invoice_2.pdf'
test_attachment_path: str = '/Users/wb/Downloads/download.pdf'


class LoginEMS: 

    """This class is used to login to the EMS API"""
    
    def __init__(self): 
        # define constant API parameters
        self.EMS_BASE_URL: str = "https://www.ams360.com/ems"
        self.AUTHENTICATE_ENDPOINT: str = "/auth"
        self.EMS_KEY: str = "c1c00f1d-6363-4c56-94c6-64a491871354"
        self.AGENCY_NUMBER: str = "8880007-1"
        self.USER_NAME: str = "customai"
        self.PASSWORD: str = "Welcome2025"
        self.APP_LOGIN_ENDPOINT: str = "/auth/app/login"
        self.APP_ACCESS_KEY: str = "61450e86-3b30-4db8-b39b-dbaa67473350"

        self.HEADERS: dict = {
            "Content-Type": "application/json"
        }

    def authenticate(self): 
        """authentication to the EMS API"""
        auth_url = f"{self.EMS_BASE_URL}{self.AUTHENTICATE_ENDPOINT}"
        payload = {
            "appKey": str(UUID(self.EMS_KEY))
        }

        try:
            response = requests.post(auth_url, json=payload, headers=self.HEADERS)
            #print(f"Request URL: {auth_url}")
            #print(f"Request Headers: {self.HEADERS}")
            #print(f"Request Payload: {json.dumps(payload, indent=4)}")
            #print(f"Response Status Code: {response.status_code}")
            #print(f"Response Text: {response.text}")

            response.raise_for_status()
            data = response.json()
            print("Authentication Success:", json.dumps(data, indent=4))
            return data.get("loginKey")
        except requests.exceptions.RequestException as e:
            print("Authentication Error:", e)
            return None

    def login(self): 
        """login to the EMS API"""

        # get the login key from the authentication function 
        login_key = self.authenticate()

        # login to the EMS API
        login_url = f"{self.EMS_BASE_URL}{self.APP_LOGIN_ENDPOINT}"
        payload = {
            "agencyNo": self.AGENCY_NUMBER,
            "appAccessToAgencyKey": str(UUID(self.APP_ACCESS_KEY)),
            "loginKey": login_key
        }

        try:
            response = requests.post(login_url, json=payload, headers=self.HEADERS)
            #print(f"Request URL: {login_url}")
            #print(f"Request Headers: {self.HEADERS}")
            #print(f"Request Payload: {json.dumps(payload, indent=4)}")
            #print(f"Response Status Code: {response.status_code}")
            #print(f"Response Text: {response.text}")

            response.raise_for_status()
            data = response.json()
            print("Application Login Success:", json.dumps(data, indent=4))
            return data  # Contains tokens
        except requests.exceptions.RequestException as e:
            print("Application Login Error:", e)
            return None


class CallActivities(LoginEMS): 

    """This class is used to call the activities from the EMS API"""

    def __init__(self): 
        super().__init__()

        # get access tokens 
        login_data = self.login()
        if login_data:
             self.access_token = login_data.get("accessJwt")
        else:
             self.access_token = None
             print("Error: Failed to login, access token not set.")
    
    def append_attachment_to_activity(self, activity_id: str, comment: str, description: str, source_file_path: str): 
        """add an attachment to an activity"""

        # define the base url 
        base_url: str = f"{self.EMS_BASE_URL}/activity/attachment"

        # define the filename 
        filename: str = os.path.basename(source_file_path)

        # define the file content and encode it
        with open(source_file_path, "rb") as file:
            file_content = file.read()
        base64_encoded_data = base64.b64encode(file_content).decode('utf-8')

        # define the request body using the Base64 encoded string
        body: dict = {
            "ActivityId": str(activity_id),
            "Comment": comment,
            "Description": description,
            "SourceFileName": filename,
            "Data": base64_encoded_data, 
            'FileSizeInBytes': len(file_content), 
            'Compressed': True, 
        }

        # Prepare JSON payload explicitly to ensure proper escaping
        json_payload = json.dumps(body, ensure_ascii=True)

        # define the headers
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # Send JSON body directly; data field is now a Base64 string
        response = requests.post(base_url, json=body, headers=headers, timeout=10)
        result = response.json()
        return result
        
    def create_customer_activity(self, customer_id: str, comment: str, action_code: str): 
        """create a customer activity"""
        if not self.access_token:
            print("Error: Cannot create activity without access token.")
            return None

        # define the base url 
        base_url = f"{self.EMS_BASE_URL}/activity/customer"

        # define the request body 
        body: dict = {
            "customerId": customer_id,
            "comment": comment, 
            "action": action_code, 
            "timeStamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        }

        # define the headers 
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        # call the API 
        try:
            response = requests.post(base_url, json=body, headers=headers, timeout=10) # Increased timeout
            response.raise_for_status()  # Raise HTTPError for bad responses
            data = response.json()
            # Extract only the activityId from the response
            return data.get('activityId') 
        except requests.exceptions.Timeout:
             print(f"Error calling {base_url}: Request timed out.")
             return None
        except requests.exceptions.RequestException as e:
            print(f"Error calling {base_url}: {e}")
            if e.response is not None:
                 print(f"Response Status Code: {e.response.status_code}")
                 print(f"Response Text: {e.response.text}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
        
    def create_policy_actiivty(self, policy_id: str, comment: str, action_code: str): 
        """create a policy activity"""
        

        
        



        
call_activities = CallActivities()  

# Check if login was successful before proceeding
if call_activities.access_token:
    # create a customer activity 
    activity_id = call_activities.create_customer_activity(customer_id_test, "Test Comment", "NewProspect/Customer")
    print(f"Created Activity ID: {activity_id}")

    # append an attachment to the activity 
    if activity_id:
         attachment_response = call_activities.append_attachment_to_activity(activity_id, "Test Comment", "Test Description", test_attachment_path)
         print(f"Attachment Response: {attachment_response}")
    else:
         print("Skipping attachment: Failed to create activity.")
else:
    print("Skipping API calls: Login failed.")



