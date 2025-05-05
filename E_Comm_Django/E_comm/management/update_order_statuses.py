# File: E_comm/management/commands/update_order_statuses.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from E_comm.models import Order  # Adjust the import path as needed for your project structure

class Command(BaseCommand):
    help = 'Updates order statuses based on time elapsed'

    def handle(self, *args, **options):
        # Get all active orders (orders that are not yet delivered)
        active_orders = Order.objects.exclude(status='DELIVERED')
        updated_count = 0
        
        for order in active_orders:
            # Store the old status
            old_status = order.status
            
            # Update the status (emails are sent internally in the update_status method)
            order.update_status()
            
            # If status changed, count it
            if old_status != order.status:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Order #{order.id}: Status updated from {old_status} to {order.status}'
                ))
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully updated {updated_count} orders'
        ))