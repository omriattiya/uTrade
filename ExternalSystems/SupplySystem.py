from ExternalSystems.ExternalSystemInterfaces.SupplyInterface import SupplyInterface
from datetime import datetime


class SupplySystem(SupplyInterface):
    def supply_a_purchase(self,username, purchase_id):
        return "A supply procedure of the Purchase:" + str(
            purchase_id) + " which bought at uTrade inc. for user: " + username + " was started on " + datetime.now().strftime(
            "%c") \
               + ", and APPROVED by the Supply System."



