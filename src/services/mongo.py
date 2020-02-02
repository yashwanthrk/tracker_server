import pymongo
from src.config.mongo import mongo_conf

# try:
#     client = pymongo.MongoClient(mongo_conf['endPoint'],
#                                 #  username=mongo_conf['username'],
#                                 #  password=mongo_conf['password'],
#                                 #  authSource=mongo_conf['authSource']
#                                  )
#     db = client[mongo_conf['db']]
#     print('connected to client')
# except pymongo.errors.ConnectionFailure:
#     print('Error connecting to db')

# print(db)


class OrdersModel:

    def get_business_payments_history(self, user_ids, start_ts=None, end_ts=None):

        match_stage = {
            'orderStatus': {
                '$in': ['DROPCOMPLETED', 'RETURNED']
            },
            'userID': {
                '$in': user_ids
            }
        }
        if start_ts or end_ts:
            match_stage['createdTimestamp'] = {}
            if start_ts:
                match_stage['createdTimestamp']['$gte'] = start_ts
            if end_ts:
                match_stage['createdTimestamp']['$lte'] = end_ts

        pipeline = [{
            '$match': match_stage
        },
            {
            '$lookup': {
                'from': 'users',
                'localField': 'userID',
                'foreignField': 'userID',
                'as': 'userData'
            }
        },
            {
            '$lookup': {
                'from': 'agents',
                'localField': 'agentID',
                'foreignField': 'agentID',
                'as': 'agentData'
            }
        },
            {
            '$unwind': {
                'path': '$userData'
            }
        },
            {
            '$unwind': {
                'path': '$agentData'
            }
        },
            {
            '$project': {
                '_id': 0,
                'userInfo': '$userData.user_info',
                'auditLog': '$audit_log',
                'senderName': '$sender.name',
                'senderNumber': '$sender.mobileNumber',
                'receiverName': '$receiver.name',
                'receiverNumber': '$receiver.mobileNumber',
                'pickAddress': '$pickLocation.address',
                'dropAddress': '$dropLocation.address',
                'orderID': 1,
                'orderStatus': 1,
                'orderType': 1,
                'urgencyType': '$ship.type',
                'distance': 1,
                'createdTimestamp': 1,
                'requestedTimestamp': 1,
                'collectionAmount': '$payments.collections.amount',
                'deliveryChargesBase':
                '$payments.deliveryCharges.baseDeliveryCharges',
                'deliveryChargesTotal': {
                    '$cond': {
                        'if': {
                            '$eq': [
                                '$payments.paymentStatus.deliveryChargesPaidToTP',
                                True
                            ]
                        },
                        'then': 0,
                        'else': '$payments.deliveryCharges.totalDeliveryCharges'
                    }
                },
                'collectionCharges': '$payments.collections.charges',
                'agentInfo': '$agentData.agent_info'
            }
        }]

        return list(db.orders.aggregate(pipeline))

    def get_agent_order_history(self, agent_id, start_ts=None, end_ts=None):
        match_stage = {
            'agentID': agent_id
        }
        if start_ts or end_ts:
            match_stage['createdTimestamp'] = {}
            if start_ts:
                match_stage['createdTimestamp']['$gte'] = start_ts
            if end_ts:
                match_stage['createdTimestamp']['$lte'] = end_ts

        pipeline = [{
            '$match': match_stage
        }, {
            '$project': {
                '_id': 0
            }
        }]
        return list(db.orders.aggregate(pipeline))

    def get_total_order_history(self, start_ts=None, end_ts=None):
        match_stage = {}
        if start_ts or end_ts:
            match_stage['createdTimestamp'] = {}
        if start_ts:
            match_stage['createdTimestamp']['$gte'] = start_ts
        if end_ts:
            match_stage['createdTimestamp']['$lte'] = end_ts
        pipeline = [{
            '$match': match_stage
        },
            {
            '$lookup': {
                'from': 'users',
                'localField': 'userID',
                'foreignField': 'userID',
                'as': 'userData'
            }
        },
            {
            '$lookup': {
                'from': 'agents',
                'localField': 'agentID',
                'foreignField': 'agentID',
                'as': 'agentData'
            }
        },
            {
            '$unwind': {
                'path': '$userData',
                "preserveNullAndEmptyArrays": True
            }
        },
            {
            '$unwind': {
                'path': '$agentData',
                "preserveNullAndEmptyArrays": True
            }
        },
            {
            '$project': {
                '_id': 0,
                'userInfo': '$userData.user_info',
                'auditLog': '$audit_log',
                'senderName': '$sender.name',
                'senderNumber': '$sender.mobileNumber',
                'receiverName': '$receiver.name',
                'receiverNumber': '$receiver.mobileNumber',
                'pickAddress': '$pickLocation.address',
                'dropAddress': '$dropLocation.address',
                'orderID': 1,
                'orderStatus': 1,
                'orderType': 1,
                'urgencyType': '$ship.type',
                'distance': 1,
                'createdTimestamp': 1,
                'requestedTimestamp': 1,
                'collectionAmount': '$payments.collections.amount',
                'deliveryChargesBase':
                '$payments.deliveryCharges.baseDeliveryCharges',
                'deliveryChargesTotal': {
                    '$cond': {
                        'if': {
                            '$eq': [
                                '$payments.paymentStatus.deliveryChargesPaidToTP',
                                True
                            ]
                        },
                        'then': 0,
                        'else': '$payments.deliveryCharges.totalDeliveryCharges'
                    }
                },
                'collectionCharges': '$payments.collections.charges',
                'agentInfo': '$agentData.agent_info',
                'cancellationReason' : 1
            }
        }]
        # return []
        return list(db.orders.aggregate(pipeline))


class BusinessGroupsModel():
    def get_business_via_code(self, code):
        business_user_data = db.business_groups.find_one({'code': code})
        return business_user_data


class AgentCashCollectionsModel():
    def get_cash_collected_for_orders(self, agent_id=None, start_ts=None, end_ts=None):
        match_stage = {}
        if agent_id:
            match_stage['agentID'] = agent_id
        if start_ts or end_ts:
            match_stage['timestamp'] = {}
            if start_ts:
                match_stage['timestamp']['$gte'] = start_ts
            if end_ts:
                match_stage['timestamp']['$lte'] = end_ts
        pipeline = [{
            '$match': match_stage
        }, {
            '$project': {
                'combinedOrderIDs': {
                    '$concatArrays': [
                        '$deliveryOrders', '$collectionOrders'
                    ]
                },
                'deliveryOrders': 1,
                'collectionOrders': 1,
                'timestamp': 1
            }
        }, {
            '$lookup': {
                'from': 'orders',
                'localField': 'combinedOrderIDs',
                'foreignField': 'orderID',
                'as': 'orders'
            }
        }, {
            '$unwind': {
                'path': '$orders'
            }
        }, {'$lookup': {
            'from': 'users',
            'localField': 'orders.userID',
            'foreignField': 'userID',
            'as': 'userInfo'
        }
        }, {
            '$unwind': {
                'path': '$userInfo'
            }
        },  {
            '$lookup': {
                'from': 'agents',
                'localField': 'orders.agentID',
                'foreignField': 'agentID',
                'as': 'agentInfo'
            }
        }, {
            '$unwind': {
                'path': '$agentInfo'
            }
        }, {
            '$project': {
                '_id': 0,
                'timestamp': 1,
                'orderID': '$orders.orderID',
                'deliveryOrders': 1,
                'collectionOrders': 1,
                'agentName': '$agentInfo.agent_info.name',
                # 'totalAmounts': '$orders.payments.totalAmounts',
                'userName': '$userInfo.user_info.name',
                'agentNumber': '$agentInfo.agent_info.phone',
                'deliveryCharge': {
                    '$cond': {
                            'if': {
                                '$in': [
                                    '$orders.orderID', '$deliveryOrders'
                                ]
                            },
                        'then': '$orders.payments.totalAmounts.deliveryCharges',
                        'else': 0
                    }
                },
                'collectionCharge': {
                    '$cond': {
                        'if': {
                            '$in': [
                                '$orders.orderID', '$collectionOrders'
                            ]
                        },
                        'then': '$orders.payments.totalAmounts.collections',
                        'else': 0
                    }
                }
            }
        }]
        return list(db.agent_cash_collections.aggregate(pipeline))


class AgentModel():
    def get_agent_info_by_id(self, agentID):
        return db.agents.find_one({"agentID": agentID})

    def get_agent_list(self, start_ts=None, end_ts=None):

        match_stage = {}
        if start_ts or end_ts:
            match_stage['agent_info.created_date'] = {}
            if start_ts:
                match_stage['agent_info.created_date']['$gte'] = start_ts
            if end_ts:
                match_stage['agent_info.created_date']['$lte'] = end_ts

        pipeline = [{
            '$match': match_stage
        },  {
            '$lookup': {
                'from': 'users',
                'localField': 'agent_info.accountVerifiedBy',
                'foreignField': 'userID',
                'as': 'admin'
            }
        }, {
            '$unwind': {
                'path': '$admin',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$project': {
                '_id': 0,
                'agent_info': 1,
                'admin': '$admin.user_info'
            }
        }]
        return list(db.agents.aggregate(pipeline))


class AgentTrackingModel():

    def get_agent_routes_by_id(self, agent_id, start_ts, end_ts):
        match_stage = {
            'agentID': agent_id,
            '$or': [
                {'onDuty':  {'$exists': True}},
                {'currentLocation': {'$exists': True}}
            ]
        }
        if start_ts or end_ts:
            match_stage['timestamp'] = {}
            if start_ts:
                match_stage['timestamp']['$gte'] = start_ts
            if end_ts:
                match_stage['timestamp']['$lte'] = end_ts

        pipeline = [{
            "$match": match_stage
        },  {
            "$sort": {"timestamp": 1}
        }, {
            "$project": {
                "_id": 0,
                "coordinates": "$currentLocation.coordinates",
                "onDuty": 1
            }
        }]

        return list(db.agent_tracking.aggregate(pipeline))
