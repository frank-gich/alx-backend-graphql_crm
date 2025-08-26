from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import logging

# Set up logging for heartbeat
logging.basicConfig(filename='/tmp/crm_heartbeat_log.txt', level=logging.INFO, format='%(message)s')

# Set up logging for low stock updates
low_stock_logger = logging.getLogger('low_stock')
low_stock_handler = logging.FileHandler('/tmp/low_stock_updates_log.txt')
low_stock_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
low_stock_logger.addHandler(low_stock_handler)
low_stock_logger.setLevel(logging.INFO)

async def log_crm_heartbeat():
    # Log heartbeat message with timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    logging.info(f'{timestamp} CRM is alive')
    
    # Query GraphQL endpoint to verify responsiveness
    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql('''
            query {
                hello
            }
        ''')
        result = await client.execute_async(query)
        logging.info(f'{timestamp} GraphQL endpoint responded: {result.get("hello", "No response")}')
    except Exception as e:
        logging.error(f'{timestamp} GraphQL endpoint error: {str(e)}')

async def update_low_stock():
    try:
        # Set up GraphQL client
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the GraphQL mutation
        mutation = gql('''
            mutation {
                updateLowStockProducts {
                    products {
                        name
                        stock
                    }
                    message
                }
            }
        ''')

        # Execute the mutation
        result = await client.execute_async(mutation)
        
        # Log updated products
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for product in result['updateLowStockProducts']['products']:
            low_stock_logger.info(f"[{timestamp}] Updated product: {product['name']}, New stock: {product['stock']}")
        
        low_stock_logger.info(f"[{timestamp}] {result['updateLowStockProducts']['message']}")
        
    except Exception as e:
        low_stock_logger.error(f"[{timestamp}] Error updating low stock products: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(update_low_stock())
    
async def log_crm_heartbeat():
    # Log heartbeat message with timestamp in DD/MM/YYYY-HH:MM:SS format
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    logging.info(f'{timestamp} CRM is alive')
    
    # Query GraphQL endpoint to verify responsiveness
    try:
        transport = AIOHTTPTransport(url='http://localhost:8000/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql('''
            query {
                hello
            }
        ''')
        result = await client.execute_async(query)
        logging.info(f'{timestamp} GraphQL endpoint responded: {result.get("hello", "No response")}')
    except Exception as e:
        logging.error(f'{timestamp} GraphQL endpoint error: {str(e)}')

if __name__ == "__main__":
    import asyncio
    asyncio.run(log_crm_heartbeat())
