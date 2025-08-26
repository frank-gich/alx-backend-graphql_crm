from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='/tmp/crm_heartbeat_log.txt', level=logging.INFO, format='%(message)s')

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
