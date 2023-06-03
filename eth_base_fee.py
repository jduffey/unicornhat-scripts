#!/usr/bin/env python

import time
import traceback
import requests
import unicornhathd
from digits import digits

url = 'http://192.168.0.10:8545'
headers = {'content-type': 'application/json'}


def get_block_number():
    payload = {
        "method": "eth_blockNumber",
        "params": [],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(url, json=payload, headers=headers).json()
    return int(response['result'], 16)


def get_block_by_number(block_number):
    payload = {
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "jsonrpc": "2.0",
        "id": 1,
    }
    response = requests.post(url, json=payload, headers=headers).json()
    return response['result']


def get_base_fee_for_block(block_number):
    return int(get_block_by_number(block_number)['baseFeePerGas'], 16)


def display_digit(digit, offset_x):
    pattern = digits[str(digit)]

    for y in range(5):
        for x in range(3):
            if pattern[y][x]:
                unicornhathd.set_pixel(x + offset_x, 15 - y, 255, 255, 255)  # white


def display_block_number(block_number):
    # Convert block_number to a 32-bit binary number
    binary_str = format(block_number, '032b')

    # Split binary string into two 16-bit parts
    binary_parts = [binary_str[16:], binary_str[:16]]

    for y in range(2):
        for x in range(16):
            if binary_parts[y][x] == '1':
                unicornhathd.set_pixel(x, y, 255, 255, 255)  # white
            else:
                unicornhathd.set_pixel(x, y, 0, 0, 0)  # off


green = (0, 255, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)


def set_bar_chart_pixels(my_list):
    most_recent_bar_y_vals = []
    for x in range(len(my_list)):
        strength = min(10, int(my_list[x]) // 10)
        for y in range(10):
            if y == 0:
                r = 0
                g = 0
                b = 255
            elif y <= 3:
                r = 0
                g = int((y/3) * 255)
                b = 255 - int((y/3) * 255)
            else:
                r = 255
                g = 255 - int(((y-4)/3) * 255)
                b = 0

            if y < strength:
                if x == 0:
                    most_recent_bar_y_vals.append((r, g, b))
                unicornhathd.set_pixel(x, y, r, g, b)

    for _ in range(4):
        for i in range(len(most_recent_bar_y_vals)):
            unicornhathd.set_pixel(0, i, *black)
        unicornhathd.show()
        time.sleep(0.25)
        for i, color in enumerate(most_recent_bar_y_vals):
            unicornhathd.set_pixel(0, i, *color)
        unicornhathd.show()
        time.sleep(0.25)


unicornhathd.rotation(0)
unicornhathd.brightness(0.5)


def get_most_recent_base_fees(block_number):
    return [get_base_fee_for_block(block_number - i) for i in range(16)]


# h/t https://m.minecraft.novaskin.me/skin/4942713520/Fire
def display_fireball():
    fireball = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 3, 0, 3, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 3, 2, 2, 2, 3, 3, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 3, 2, 2, 2, 2, 3, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 2, 2, 2, 1, 2, 2, 2, 2, 3, 0, 0],
        [0, 0, 3, 3, 2, 2, 2, 1, 1, 2, 2, 2, 2, 3, 0, 0],
        [0, 0, 3, 3, 2, 2, 1, 1, 1, 1, 2, 2, 2, 3, 3, 0],
        [0, 0, 3, 3, 2, 2, 1, 1, 1, 1, 2, 2, 2, 3, 3, 0],
        [0, 0, 0, 3, 2, 2, 1, 1, 1, 1, 2, 2, 3, 3, 3, 0],
        [0, 0, 0, 3, 3, 2, 2, 1, 1, 1, 2, 2, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 2, 1, 1, 2, 2, 3, 0, 0, 0, 0]
    ]

    colors = {
        0: (0, 0, 0),      # Black (off)
        1: (255, 255, 255),  # Yellow
        2: (255, 165, 0),  # Orange
        3: (255, 0, 0)     # Red
    }

    for y in range(16):
        for x in range(16):
            unicornhathd.set_pixel(x, 15 - y, *colors[fireball[y][x]])

    unicornhathd.show()


display_fireball()


green = (0, 255, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)


def display_countdown_timer():
    countdown_pixel_args = [
        {
            0: green,
            1: green,
            2: green,
            3: green,
            4: green,
        },
        {
            0: black
        },
        {
            1: black
        },
        {
            2: black,
            3: yellow,
            4: yellow,
        },
        {
            3: black,
            4: red,
        },
    ]

    countdown_indicator_x_pos = 0
    countdown_indicator_y_max = 15
    for countdown_position in countdown_pixel_args:
        for y_offset, color in countdown_position.items():
            y_pos = countdown_indicator_y_max - y_offset
            unicornhathd.set_pixel(countdown_indicator_x_pos, y_pos, *color)
        unicornhathd.show()
        time.sleep(1)


try:
    print('Initializing base fee values...')

    current_block_number = get_block_number()
    print(f'Current block number: {current_block_number}')

    most_recent_base_fees = get_most_recent_base_fees(current_block_number)
    print(f'Most recent base fees: {most_recent_base_fees}')

    base_fees_dec = [x / 10**9 for x in most_recent_base_fees]
    print(f'Base fees as dec: {base_fees_dec}')

    prev_block_number = None
    prev_time = time.time()
    while True:
        block_number = get_block_number()
        print(f'\nBlock number: {block_number}')

        current_time = time.time()
        print(f'Current time: {current_time}')

        elapsed_time = current_time - prev_time
        prev_time = current_time
        print(f'Elapsed time between updates: {elapsed_time}')

        # if we don't have a new block number (e.g. the proposer missed the slot)
        if block_number == prev_block_number:
            print('⚠️  No new block! ⚠️')
            for i in range(5):
                unicornhathd.set_pixel(0, 11 + i, 255, 0, 255)
            unicornhathd.show()
            time.sleep(7)
            display_countdown_timer()
            continue

        if prev_block_number is not None and block_number != prev_block_number + 1:
            print('⚠️  BLOCK SKIPPED DUE TO MISTIMING OF UPDATES ⚠️')

        prev_block_number = block_number

        base_fee = get_base_fee_for_block(block_number)
        # base_fee = 2345 * 10**9  # <- for testing digit display
        print(f'Base fee: {base_fee}')

        base_fee_decimal = base_fee / 10**9
        print(f'Base fee decimal: {base_fee_decimal}')

        base_fees_dec = [base_fee_decimal] + base_fees_dec[:15]
        # base_fees_dec = [10 * i for i in range(16)]  # <- for testing the color scale
        print(f'Base fees list: {base_fees_dec}')

        base_fee_str = str(base_fee_decimal).split('.')[0]
        print(f'Base fee string: {base_fee_str}')

        unicornhathd.clear()

        if len(base_fee_str) > 4:
            print("!!  Base fee too high for display  !!")
            # TODO: we probably need to clear out the area allocated for digits if this happens
        else:
            for i in range(len(base_fee_str)):
                display_digit(int(base_fee_str[i]), 13 - (len(base_fee_str) - 1 - i) * 4)

        set_bar_chart_pixels(base_fees_dec)
        unicornhathd.show()

        time.sleep(5)

        display_countdown_timer()

        # "erase" the remaining pixel of the countdown timer so that if on the next loop
        # there is not yet a new block, then the digits and chart can remain pending a new block
        unicornhathd.set_pixel(0, 11, *black)
        unicornhathd.show()

except KeyboardInterrupt:
    # unicornhathd.off()
    pass

except Exception:
    traceback.print_exc()
    unicornhathd.clear()
    unicornhathd.set_pixel(0, 15, *red); unicornhathd.set_pixel(4, 15, *red)
    unicornhathd.set_pixel(1, 14, *red); unicornhathd.set_pixel(3, 14, *red)
    unicornhathd.set_pixel(2, 13, *red)
    unicornhathd.set_pixel(1, 12, *red); unicornhathd.set_pixel(3, 12, *red)
    unicornhathd.set_pixel(0, 11, *red); unicornhathd.set_pixel(4, 11, *red)
    unicornhathd.show()