import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(filename='/tmp/crm_report_log.txt', level=logging.INFO, format='%(message)s')

@shared_task
def generate_crm_report():
    try:
        # Set up GraphQL client
        transport = AIOHTTPTransport(url='http://localhost:8000/graphql')
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        # Define the GraphQL query
        query = gql('''
            query {
                customers {
                    totalCount
                }
                orders {
                    totalCount
                    edges {
                        node {
                            totalAmount
                        }
                    }
                }
            }
        ''')

        # Execute the query
        result = client.execute(query)
        
        # Calculate totals
        total_customers = result['customers']['totalCount']
        total_orders = result['orders']['totalCount']
        total_revenue = sum(edge['node']['totalAmount'] for edge in result['orders']['edges'])
        
        # Log the report
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f'{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue')
        
    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.error(f'{timestamp} - Error generating CRM report: {str(e)}')
