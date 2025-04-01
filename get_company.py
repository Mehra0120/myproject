import requests
from config.connection import connection
from flask import jsonify  

def get_companies_access(access_token):
    try:
        conn = connection()
        cursor = conn.cursor()

        SELECT_DATA = '''SELECT vc_microsoft_comp_id FROM makess.mst_company'''   
        cursor.execute(SELECT_DATA)
        resultData = cursor.fetchall()

        company_data = get_companies(access_token)

        if resultData:
            first_table_entry = resultData[0]  
            print(first_table_entry)

        matched_company = None
        for company in company_data["value"]:
            if company["id"] == first_table_entry[0]:  
                matched_company = company  
                break  

        cursor.close()
        conn.close()  

        if matched_company:
           # print("Matched Company Data:", matched_company["id"])
            return matched_company["id"]
        else:
        # print("No matching company found.")
         return jsonify({"message": "No matching company found"}), 404  
    
    except Exception as ex:
        print("EXCEPTION:", str(ex))
        return jsonify({"error": str(ex)}), 500  

        

def get_companies(access_token):
    if not access_token:
        print("No access token available.")
        return None

    api_url = "https://api.businesscentral.dynamics.com/v2.0/92aae17d-67c6-45f0-b4c6-8ca67df27519/Development/api/v1.0/companies"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        print("Company Data Retrieved Successfully.")

        return response.json()
    else:
        print("Error fetching companies:", response.status_code, response.text)
        return None
    

 