from ExternalSystems.ExternalSystemInterfaces.SupplyInterface import SupplyInterface


class ProxySupplySystem(SupplyInterface):
    def supply_a_purchase(self, username, purchase_id):
        return False
