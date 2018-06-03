from ExternalSystems.ExternalSystemInterfaces.SupplyInterface import SupplyInterface


class ProxySupplySystem(SupplyInterface):
    def supply_a_purchase(username, purchase_id):
        return "A supply procedure of the Purchase:" + str(purchase_id) + " which bought at uTrade inc. for user: " + username + " was started on " + datetime.now().strftime("%c")\
               + ", and APPROVED by the Supply System."
