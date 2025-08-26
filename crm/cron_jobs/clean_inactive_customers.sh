#!/bin/bash

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Execute Django command to delete inactive customers (no orders in the last year)
DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer
from django.db.models import Max

# Find customers with no orders in the last year
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.annotate(last_order=Max('order__created_at')).filter(last_order__lt=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
")

# Log the number of deleted customers with timestamp
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
