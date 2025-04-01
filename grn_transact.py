import requests
from config.connection import connection
from flask import jsonify  
#test1
def push_grn_transactions(auth_token, company_id):
    try: 
        print("Auth Token:", auth_token)
        print("Company ID:", company_id)

        conn = connection()
        cursor = conn.cursor()        

        SELECT_DATA = ''' 
        SELECT Request_ID, GRN_Transaction_No, BC_Master_Type, Transaction_Type, BC_Master_Code, 
               Transaction_Date, Payment_Method_Code, Location_Code, Short_Cut_Dimension_1_Code, 
               POS_Created_By_User, POS_Approved_By_User, Item_No, Quantity, Direct_Unit_Cost, 
               Lot_No, Expiry_Date
        FROM GRN_Transactions 
        WHERE ROWNUM = 1
        '''                         
       
        cursor.execute(SELECT_DATA)
        resultData = cursor.fetchone() 

        if resultData:
            payload = {
                "requestID": resultData[0],
                "grnTransactionNo": resultData[1],
                "bcMasterType": resultData[2],
                "transactionType": resultData[3],
                "bcMasterCode": resultData[4],
                "transactionDate": resultData[5].strftime('%Y-%m-%d') if resultData[5] else None,
                "paymentMethodCode": resultData[6],
                "shortcutDimension1Code": resultData[8],
                "posCreatedByUser": resultData[9],
                "posApprovedByUser": resultData[10],
                "posTransactionLine": [{
                    "itemNo": resultData[11],
                    "quantity": resultData[12],
                    "unitAmount": resultData[13],
                    "lotNo": resultData[14],
                    "expiryDate": resultData[15].strftime('%Y-%m-%d') if resultData[15] else None,
                    "locationCode": resultData[7]
                }]
            }

            api_url = f"https://api.businesscentral.dynamics.com/v2.0/92aae17d-67c6-45f0-b4c6-8ca67df27519/Development/api/ccare/posInterface/v1.0/companies({company_id})/posTransactions?$expand=posTransactionLine"

            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Content-Type": "application/json"
            }

            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 201:
                response_data = response.json()
                print(response_data)
                
                if response_data.get("processedInBC") == "Success":
                    try:
                        update_query = '''
                        UPDATE GRN_Transactions 
                        SET ch_pushed_status = 'Y' 
                        WHERE Request_ID = :1
                        '''
                        cursor.execute(update_query, (resultData[0],))
                        conn.commit()
                        print(f"Database updated for transaction {resultData[1]}: ch_pushed_status = 'Y'")
                    except Exception as db_ex:
                        print(f"Database update failed for transaction {resultData[1]}: {str(db_ex)}")
                
                print(f"Transaction {resultData[1]} successfully pushed to API.")
            else:
                print(f"Failed to push transaction {resultData[1]}. Status Code: {response.status_code}, Response: {response.text}")
        
        cursor.close()
        conn.close()

    except Exception as ex:
        print("EXCEPTION:", str(ex)) 
        return None
