from datetime import datetime

from ExternalSystems.ExternalSystemInterfaces.SupplyInterface import SupplyInterface


class SupplySystem(SupplyInterface):
    def supply_a_purchase(self, username, purchase_id):
        if username[0:5] == 'guest':
            return "A supply procedure of the purchase which bought at uTrade inc. for guest was started on " + datetime.now().strftime(
                "%c") \
                   + ", and APPROVED by the Supply System."
        else:
            return "A supply procedure of the Purchase:" + str(
                purchase_id) + " which bought at uTrade inc. for user: " + username + " was started on " + datetime.now().strftime(
                "%c") \
                   + ", and APPROVED by the Supply System."
