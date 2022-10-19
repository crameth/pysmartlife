import logging
import time

from tuyapy import TuyaApi
from pywebio import start_server
from pywebio.input import *
from pywebio.output import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

api = TuyaApi()

def main():
    auth = input_group("Authentication",[
        input('Username:', name='username'),
        input('Password:', name='password', type=PASSWORD),
        select('Country:', name='country', options=[65]),
    ])
    
    # if user hits submit here?
    s = time.time()
    try:
        with put_loading().style("margin:0 auto;"):
            api.init(auth['username'], auth['password'], auth['country'])
    except Exception as e:
        logging.error(e)
        exit()
    logging.info("--- Connect to API: %s seconds ---" % (time.time() - s))

    # retrieve device info
    s = time.time()
    try:
        with put_loading().style("margin:0 auto;"):
            devices = api.get_all_devices()
    except Exception as e:
        logging.error(e)
        exit()
    logging.info("--- Get all devices: %s seconds ---" % (time.time() - s))

    table_data = [
        [put_html('<h3>Device</h3>'), put_html('<h3>State</h3>'), put_html('<h3>Actions</h3>')],
    ]
    
    for d in devices:
        if d.dev_type == 'switch':
            row = []
            
            # device info
            s = time.time()
            device_info = []
            
            if d.icon is not None:
                device_info.append(put_image(src=d.icon, width='64px', height='64px'))
            else:
                device_info.append(put_text(''))

            device_string = f'<h5>{d.obj_name}</h5>'
            device_string = device_string + f'<h6>{d.obj_id} ({d.dev_type})</h6>'

            device_info.append(put_html(device_string))
            
            row.append(put_row(content=device_info, size='25% 75%'))
            logging.info("--- Device info: %s seconds ---" % (time.time() - s))
            
            # state info (to be polled using d.update())
            s = time.time()
            state_info = []
            actions = None
            
            if d.available():
                if d.state():
                    state_info = put_buttons([
                        dict(label='Available', value=None, color='success', disabled=True),
                        dict(label='On', value=None, color='success', disabled=True),
                    ], onclick=None)
                else:
                    state_info = put_buttons([
                        dict(label='Available', value=None, color='success', disabled=True),
                        dict(label='Off', value=None, color='danger', disabled=True),
                    ], onclick=None)
                
                device_controller = api.get_device_by_id(d.obj_id)
                actions = put_buttons([
                    dict(label='On', value=None, color='success'),
                    dict(label='Off', value=None, color='danger'),
                    dict(label='Update', value=None),
                ], onclick=[
                    device_controller.turn_on, 
                    device_controller.turn_off, 
                    device_controller.update
                ])
            else:
                state_info = put_button(label='Unavailable', color='danger', disabled=True, onclick=None)
                actions = put_text('')
            
            row.append(state_info)
            row.append(actions)
            logging.info("--- State/actions info: %s seconds ---" % (time.time() - s))
            
            table_data.append(row)
    
    s = time.time()
    put_table(table_data)
    logging.info("--- Render table: %s seconds ---" % (time.time() - s))

start_server(main, port=33333, debug=True)