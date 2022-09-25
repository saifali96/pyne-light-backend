
from datetime import datetime
import json
from typing import List


from app.analytics.schemas import CompanyFeatures, CompanyUserFeaturesCount


class AnalyticsService:
    def __init__(self):
        ...

    async def get_product_company_analytics(self):
        with open('analytics_data.json') as json_file:
            comp_analytics = json.load(json_file)

        with open('hs_company_data.json') as json_file:
            hs_comp_analytics = json.load(json_file)

        result = []
        
        for event in comp_analytics:

            company_idx = next((i for i, company in enumerate(result) if company["companyName"] == str(event["company_id"])), None)
            if company_idx is None:
                result.append({"companyName": str(event["company_id"]), "features": [{"featureName": event["event_name"], "featureUsedCount": 1}]})
                continue
            
            feature_idx = next((i for i, feature in enumerate(result[company_idx]["features"]) if feature["featureName"] == event["event_name"]), None)
            if feature_idx is None:
                result[company_idx]["features"].append({"featureName": event["event_name"], "featureUsedCount": 1})
                continue
            
            result[company_idx]["features"][feature_idx]["featureUsedCount"] += 1

        for comp in result:
            hs_company_idx = next((i for i, company in enumerate(hs_comp_analytics) if company["properties"]["company_id"] == str(comp["companyName"])), None)
            if hs_company_idx is None:
                comp["hsCompany"] = None
                continue

            comp["hsCompany"] = hs_comp_analytics[hs_company_idx]
            
        return result

    async def get_product_user_analytics(self, from_ts: datetime = None):
        with open('analytics_data.json') as json_file:
            comp_analytics = json.load(json_file)
        
        with open('hs_company_data.json') as json_file:
            hs_comp_analytics = json.load(json_file)

        with open('hs_contact_data.json') as json_file:
            hs_cont_analytics = json.load(json_file)

        result = []
        if from_ts:
            from_ts = from_ts.replace(tzinfo=None)
        
        for event in comp_analytics:

            if not from_ts:
                company_idx = next((i for i, company in enumerate(result) if company["companyName"] == str(event["company_id"])), None)
                if company_idx is None:
                    result.append({"companyName": str(event["company_id"]), "users": [{"userName": str(event["user_id"]), "features": [{"featureName": event["event_name"], "featureUsedCount": 1}]}]})
                    continue
                
                user_idx = next((i for i, user in enumerate(result[company_idx]["users"]) if user["userName"] == str(event["user_id"])), None)
                if user_idx is None:
                    result[company_idx]["users"].append({"userName": str(event["user_id"]), "features": [{"featureName": event["event_name"], "featureUsedCount": 1}]})
                    continue
                
                feature_idx = next((i for i, feature in enumerate(result[company_idx]["users"][user_idx]["features"]) if feature["featureName"] == event["event_name"]), None)
                if feature_idx is None:
                    result[company_idx]["users"][user_idx]["features"].append({"featureName": event["event_name"], "featureUsedCount": 1})
                    continue
                
                result[company_idx]["users"][user_idx]["features"][feature_idx]["featureUsedCount"] += 1
            elif datetime.strptime(event["timestamp"], "%m/%d/%Y, %H:%M:%S") >= from_ts:
                company_idx = next((i for i, company in enumerate(result) if company["companyName"] == str(event["company_id"])), None)
                if company_idx is None:
                    result.append({"companyName": str(event["company_id"]), "users": [{"userName": str(event["user_id"]), "features": [{"featureName": event["event_name"], "featureUsedCount": 1}]}]})
                    continue
                
                user_idx = next((i for i, user in enumerate(result[company_idx]["users"]) if user["userName"] == str(event["user_id"])), None)
                if user_idx is None:
                    result[company_idx]["users"].append({"userName": str(event["user_id"]), "features": [{"featureName": event["event_name"], "featureUsedCount": 1}]})
                    continue
                
                feature_idx = next((i for i, feature in enumerate(result[company_idx]["users"][user_idx]["features"]) if feature["featureName"] == event["event_name"]), None)
                if feature_idx is None:
                    result[company_idx]["users"][user_idx]["features"].append({"featureName": event["event_name"], "featureUsedCount": 1})
                    continue
                
                result[company_idx]["users"][user_idx]["features"][feature_idx]["featureUsedCount"] += 1
            else:
                continue

        for comp in result:
            hs_company_idx = next((i for i, company in enumerate(hs_comp_analytics) if company["properties"]["company_id"] == str(comp["companyName"])), None)
            if hs_company_idx is None:
                comp["hsCompany"] = None
            else:
                comp["hsCompany"] = hs_comp_analytics[hs_company_idx]    

            for user in comp["users"]:
                hs_contact_idx = next((i for i, hs_user in enumerate(hs_cont_analytics) if hs_user["properties"]["user_id"] == str(user["userName"])), None)
                if hs_contact_idx is None:
                    user["hsContact"] = None
                    continue

                user["hsContact"] = hs_cont_analytics[hs_contact_idx]    
        
        return result


    async def get_company_list(self) -> List[CompanyFeatures]:
        resp: List[CompanyFeatures] = await self.get_product_company_analytics()

        return resp

    async def get_company_user_list(self) -> List[CompanyUserFeaturesCount]:
        resp: CompanyUserFeaturesCount = await self.get_product_user_analytics()

        return resp

    async def get_company_user_from_list(self, from_ts: datetime = None) -> List[CompanyUserFeaturesCount]:
        resp: CompanyUserFeaturesCount = await self.get_product_user_analytics(from_ts)

        return resp

