from veryfi import Client

def processing_receipt(client_id, client_secret, username, api_key, file):
    veryfi_client = Client(client_id, client_secret, username, api_key)
    categories = ['Grocery', 'Food']
    response = veryfi_client.process_document(file, categories=categories)
    return response

def calculating_receipt(response):
    receipt_dict = {}

    receipt_dict['items'] = []

    for i in range(len(response['line_items'])):
        item = {
            'description': response['line_items'][i]['description'],
            'quantity': int(response['line_items'][i]['quantity']),
            'total': float(response['line_items'][i]['total'])
        }
        receipt_dict['items'].append(item)

    receipt_dict['subtotal'] = float(response['subtotal'])

    if len(response['tax_lines']) and float(response['tax']) != float(response['tax_lines'][0]['total']):
        receipt_dict['tax & other fees'] = float(response['tax']) + float(response['tax_lines'][0]['total'])
    else:
        receipt_dict['tax & other fees'] = float(response['tax'])

    if response['tip'] is not None:
        receipt_dict['tip'] = float(response['tip'])
    else:
        receipt_dict['tip'] = 0

    receipt_dict['total'] = float(response['total'])

    return receipt_dict

