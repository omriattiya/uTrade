from DatabaseLayer import HistoryAppointings


def get_history_apppoitings(shop_name):
    return HistoryAppointings.get_history_appointing_by_shop(shop_name)
