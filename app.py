from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from environs import Env

from src.controllers import user

env = Env()
env.read_env()
# reading the string value for the boolean typeS
debug_mode = env('DEBUG_MODE') == 'true'

app = Flask(__name__)

CORS(app, max_age=600, supports_credentials=True)
# cors = CORS(app)
api = Api(app)

# User Endpoints

api.add_resource(user.Register, '/register')
api.add_resource(user.Login, '/login')
api.add_resource(user.Protected, '/protected')

# # Business Endpoints
# # region
# api.add_resource(orders.BusinessUserPaymentData, '/biz/orders/data')
# # endregion

# # Order Endpoints
# # region
# api.add_resource(orders.OrderHistory, '/orders/data')

# # endregion

# # Agent Enpoints
# # region
# api.add_resource(agent.AgentsInfo,
#                  '/agents')
# api.add_resource(agent.AgentsInfoDownload,
#                  '/agents/download')
# api.add_resource(agent.AgentOrderCashInfo,
#                  '/agent/<agent_id>/collection_history')
# api.add_resource(agent.AgentOrderCashInfoDownload,
#                  '/agent/<agent_id>/collection_history_download')
# api.add_resource(agent.CashCollectionTotalInfo,
#                  '/agents/collection_history_download')
# api.add_resource(agent.AgentRoutingModal,
#                  '/agent/<agent_id>/routemap')


# endregion
@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


# Name is only set to main when file is explicitly run (not on imports):
if __name__ == '__main__':
    # TODO debug mode if staging, not in production
    print('Dev Mode - ', debug_mode)
    # print(type(debug_mode))
    app.run(port=5000, debug=debug_mode, host="0.0.0.0")
