from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(filename='/tmp/order_reminders_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Set up GraphQL client
transport = AIOHTTPTransport(url='http://localhost:8000/graphql')
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the GraphQL query
query = gql('''
    query {
        orders(orderDate_Gte: "%s") {
            id
            customer {
                email
            }
        }
    }
''' % (datetime.now() - timedelta(days=7)).isoformat())

async def send_reminders():
    try:
        # Execute the query
        result = await client.execute_async(query)
        
        # Log each order
        for order in result['orders']:
            logging.info(f"Order ID: {order['id']}, Customer Email: {order['customer']['email']}")
        
        print("Order reminders processed!")
    except Exception as e:
        logging.error(f"Error processing order reminders: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_reminders())