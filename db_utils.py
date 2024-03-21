from pymongo import MongoClient

client = MongoClient("mongodb://waqqly-server:dEzgSmTavFMIYqjkwr5OWtPXM6gBqVvuNCAd1JSge0cV105qPIRfNTpuQXzNxTR2HslxSDPEznVmACDbF5zwcQ==@waqqly-server.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@waqqly-server@")
DB_NAME = "waqqly_db"
# Create database if it doesn't exist
db = client[DB_NAME]
if DB_NAME not in client.list_database_names():
    # Create a database with 400 RU throughput that can be shared across
    # the DB's collections
    db.command({"customAction": "CreateDatabase", "offerThroughput": 400})
    print("Created db '{}' with shared throughput.\n".format(DB_NAME))
else:
    print("Using database: '{}'.\n".format(DB_NAME))


# # Get server information
# for k, v in client.server_info().items():
#     print("Key: {} , Value: {}".format(k, v))
#
# # Get server status of admin database
# print("Server status {}".format(client.admin.command("serverStatus")))
#
# # List databases
# databases = client.list_database_names()
# print("Databases: {}".format(databases))
# db = client.waqqly_db
#
# users = db.users

# print(users)
#
# user = {
#     "username": "johndoe",
#     "email": "johndoe@example.com",
#     "hashed_password": "$2b$12$9ReDGIZpDGaOwNdwmjuHReQbqlzEetYjCg532NHISYr/1hDWrClq2",
#     "type": "admin",
# }
#
# result = users.insert_one(user).inserted_id
# print("Upserted document with _id {}\n".format(result))
