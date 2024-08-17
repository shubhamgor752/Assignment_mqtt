from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient

class StatusCountView(APIView):
    def get(self, request):
        start_time_str = request.query_params.get('start')
        end_time_str = request.query_params.get('end')
        
        # Check if both parameters are provided and valid
        if start_time_str is None or end_time_str is None:
            return Response({"error": "Both 'start' and 'end' parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_time = float(start_time_str)
            end_time = float(end_time_str)
        except ValueError:
            return Response({"error": "Invalid 'start' or 'end' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client.mqtt_database
        collection = db.messages

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_time, "$lte": end_time}}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]

        results = list(collection.aggregate(pipeline))
        response = {str(result['_id']): result['count'] for result in results}
        
        return Response(response, status=status.HTTP_200_OK)
