import pickle, requests
from time import time, sleep

def start(link,harga,model,payment):
    r = requests.Session()
    with open("julkar28","rb") as f:
        a = pickle.load(f)

    r.cookies.update(a)
    hdd = {
        "accept": "application/json",
        "accept-encoding": "gzip",
        "x-shopee-language": "id",
        "content-type": "application/json",
        "x-api-source": "rn",
        "if-none-match-": "*",
        "referer": "https://mall.shopee.co.id/",
        "user-agent": "Android app Shopee appver=27216 app_type=1",
        "x-csrftoken": a.get('csrftoken')
    }
    a = r.get("https://mall.shopee.co.id/api/v1/account_info/?need_cart=0&skip_address=0",headers=hdd)
    adrs_id = int(a.json()["default_address"]["id"])
    a = link.split("?")
    if len(a) == 2:
        a = a[0].split("/")
        shop_id = int(a[4])
        item_id = int(a[5])
    elif len(a) == 1:
        a = a[0].split(".")
        shop_id = int(a[3])
        item_id = int(a[4])
    a = r.get("https://mall.shopee.co.id/api/v2/item/get?itemid=" + str(item_id) + "&shopid=" + str(shop_id),headers=hdd).json()
    model_id = int(a["item"]["models"][model - 1]["modelid"])
    pay = [8003200, 8003001, 8001400][payment]
    harga_fs = harga * 100000

    i = "https://mall.shopee.co.id/api/v2/item/get?itemid=" + str(item_id) + "&shopid=" + str(shop_id)
    str_json = {"shop_orders":[{"shop_info":{"shop_id":shop_id},"item_infos":[{"item_id":item_id,"model_id":model_id,"quantity":1}]}]}

    a = r.get(i,headers=hdd).json()["item"]["upcoming_flash_sale"]
    if a != None:
        sleep(a["start_time"] - time() - 5)

    boo = True
    while boo:
        if r.get(i,headers=hdd).json()["item"]["price"] == harga_fs:
            ts = time()
            r.post("https://mall.shopee.co.id/api/v2/buy_now/validate_checkout",json=str_json,headers=hdd)
            a = r.post("https://mall.shopee.co.id/api/v2/checkout/place_order",data=r.post("https://mall.shopee.co.id/api/v2/checkout/get",json={"cart_type": 1,"client_id": 5,"device_info": {"buyer_payment_info": {"is_jko_app_installed": False},"device_fingerprint": "","device_id": "","tongdun_blackbox": ""},"dropshipping_info": {"enabled": False,"name": "","phone_number": ""},"order_update_info": {},"promotion_data": {"auto_apply_shop_voucher": True,"check_shop_voucher_entrances": True,"free_shipping_voucher_info": {"disabled_reason": None,"free_shipping_voucher_code": None,"free_shipping_voucher_id": None},"platform_voucher": [],"shop_voucher": [],"use_coins": False},"selected_payment_channel_data": {"channel_id": pay,"version": 2,"text_info": {}},"shipping_orders": [{"buyer_address_data": {"address_type": 0,"addressid": adrs_id,"error_status": "","tax_address": ""},"buyer_ic_number": "","logistics": {"recommended_channelids": None},"selected_preferred_delivery_instructions": {},"selected_preferred_delivery_time_option_id": 0,"selected_preferred_delivery_time_slot_id": None,"shipping_id": 1,"shoporder_indexes": [0],"sync": True}],"shoporders": [{"buyer_address_data": {"address_type": 0,"addressid": adrs_id,"error_status": "","tax_address": ""},"items": [{"itemid": item_id,"modelid": model_id,"quantity": 1}],"logistics": {"recommended_channelids": None},"selected_preferred_delivery_instructions": {},"selected_preferred_delivery_time_option_id": 0,"selected_preferred_delivery_time_slot_id": None,"shipping_id": 1,"shop": {"shopid": shop_id}}],"tax_info": {"tax_id": ""},"timestamp": round(time())},headers=hdd).content,headers=hdd)
            if a.status_code == 200:
                boo = False
     
                jul = time() - ts
                return f"Sukses, waktu eksekusi {jul} detik"
