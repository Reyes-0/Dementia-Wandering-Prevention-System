from sinch import Client
from config import (
    sinch_key_id,
    sinch_key_secret,
    sinch_project_id,
    mobile_number_to_recieve_sms,
    mobile_number_to_send_sms_from,
    image_url_from_azure_blob_storage
)

def sms():
    sinch_client = Client(
        key_id = sinch_key_id,
        key_secret = sinch_key_secret,
        project_id = sinch_project_id
    )

    send_batch_response = sinch_client.sms.batches.send(
        body = "Elderly detected out of boundary.\
            Click here to see the image: f{image_url_from_azure_blob_storage}",
        to = [mobile_number_to_recieve_sms],
        from_ = mobile_number_to_send_sms_from,
        delivery_report="none"
    )

    print(send_batch_response)