from django.http import HttpResponse
from django.template import loader

from DomainLayer import ShoppingPolicyLogic


def getShopShoppingPolicies(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        shop_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_shop(shop_name)
        html = ""
        for policy in shop_policies:
            is_none = ""
            selectors = {}
            if policy.restriction is 'N':
                is_none = "disabled"
            selectors['N'] = ""
            selectors['UT'] = ""
            selectors['AL'] = ""
            selectors['E'] = ""
            selectors[policy.restriction] = 'selected="selected"'

            html += loader.render_to_string('components/shopping_shop_policy.html', context={
                'id': policy.policy_id,
                'selector_value': policy.restriction,
                'quantity': policy.quantity,
                'is_none': is_none,
                'N_S': selectors.get('N'),
                'UT_S': selectors.get('UT'),
                'AL_S': selectors.get('AL'),
                'E_S': selectors.get('E'),
            })

        return HttpResponse(html)


def getShopShoppingPolicyConditions(request):
    if request.method == 'GET':
        shop_name = request.GET.get('shop_name')
        policy_id = request.GET.get('policy_id')
        shop_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_shop(shop_name)
        for SP in shop_policies:
            if SP.policy_id == int(policy_id):
                return HttpResponse(SP.conditions.replace("'", "''"))
        return HttpResponse("FAILED: Can't find that policy")


def getItemShoppingPolicyConditions(request):
    if request.method == 'GET':
        policy_id = request.GET.get('policy_id')
        item_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_items()
        for SP in item_policies:
            if SP.policy_id == int(policy_id):
                return HttpResponse(SP.conditions.replace("'", "''"))
        return HttpResponse("FAILED: Can't find that policy")


def getCategoryShoppingPolicyConditions(request):
    if request.method == 'GET':
        policy_id = request.GET.get('policy_id')
        category_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_category()
        for CP in category_policies:
            if CP.policy_id == int(policy_id):
                return HttpResponse(CP.conditions.replace("'", "''"))
        return HttpResponse("FAILED: Can't find that policy")


def getGlobalShoppingPolicyConditions(request):
    if request.method == 'GET':
        policy_id = request.GET.get('policy_id')
        global_policies = ShoppingPolicyLogic.get_all_shopping_policy_on_identity()
        for GP in global_policies:
            if GP.policy_id == int(policy_id):
                return HttpResponse(GP.conditions.replace("'", "''"))
        return HttpResponse("FAILED: Can't find that policy")
