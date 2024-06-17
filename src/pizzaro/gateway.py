import asyncio
import json
import logging
import threading


def send_command(command, socket):
    request = json.dumps({"command": command}).encode('utf-8')

    print('REQ: ', request)
    socket.sendall(request)

    response = socket.recv(1024)
    print('RESP: ', response)
    return response


async def wait_for_stepper_available(s):
    while True:
        resp = send_command('mmd wait_idle', s)
        if "MmdUnavailable" not in f'{resp}':
            print(resp)
            break
        await asyncio.sleep(0.1)


async def system_reset(s):
    send_command(f'mmd home', s)
    send_command(f'mmd pr_off', s)
    send_command(f'mmd pp_off', s)
    send_command(f'mmd belt_off', s)
    send_command(f'mmd dispenser0_off', s)
    send_command(f'mmd dispenser1_off', s)
    await wait_for_stepper_available(s)


async def wait_for_linear_bull_available(s):
    while True:
        resp = send_command('hpd wait_idle', s)
        if "HpdUnavailable" not in f'{resp}':
            print(resp)
            break
        await asyncio.sleep(1)


async def make_pie_base(s):
    send_command(f'hpd move_to 56800', s)
    await wait_for_linear_bull_available(s)
    # TODO(zephyr): report errors if the position isn't close to the target
    # send_command(f'hpd get_pos', s)
    await asyncio.sleep(7)
    send_command(f'hpd move_to 50000', s)
    await wait_for_linear_bull_available(s)
    await asyncio.sleep(0.5)
    send_command(f'hpd move_to 56800', s)
    await wait_for_linear_bull_available(s)
    await asyncio.sleep(7)
    # send_command(f'hpd move_to 50000', s)
    # await wait_for_linear_bull_available(s)
    # await asyncio.sleep(0.5)
    # send_command(f'hpd move_to 56800', s)
    # await wait_for_linear_bull_available(s)
    # await asyncio.sleep(7)

    send_command(f'hpd home', s)
    await wait_for_linear_bull_available(s)
    await asyncio.sleep(0.5)


async def add_ketchup(s):
    send_command(f'mmd pr_spd 100', s)
    await asyncio.sleep(0.2)
    send_command(f'mmd pr_spd 200', s)
    await asyncio.sleep(0.2)
    send_command(f'mmd pr_spd 300', s)
    await asyncio.sleep(0.2)
    send_command(f'mmd pr_spd 400', s)
    await asyncio.sleep(0.2)
    send_command(f'mmd pr_spd 500', s)
    await asyncio.sleep(0.2)
    send_command(f'mmd pr_spd 600', s)

    START_POS = 90
    CENTER_POS = 570
    CLOSE_TO_CENTER_POS = 520
    PP_ZERO_SPD = 180
    PP_MAX_SPD = 400
    STEPPER_SPD = 500
    for y in range(START_POS, CLOSE_TO_CENTER_POS, 30):
        x = - int(1.5 * (PP_ZERO_SPD + (PP_MAX_SPD - PP_ZERO_SPD) * (CENTER_POS - y) / (CENTER_POS - START_POS)))
        print(f"xfguo_ketchup() 5: x = {x}, y = {y}")
        send_command(f'mmd move_to {y}', s)
        await wait_for_stepper_available(s)
        send_command(f'mmd pp_spd {x}', s)
        await asyncio.sleep(0.7)
    send_command(f'mmd move_to 200', s)
    send_command(f'mmd pr_off', s)
    send_command(f'mmd pp_off', s)
    print("Done")


async def add_cheese(s):
    send_command(f'mmd home', s)
    send_command(f'mmd belt_off', s)
    send_command(f'mmd pr_off', s)
    await wait_for_stepper_available(s)

    def dispenser0_thread(s, speed, stop_dispenser0):
        while not stop_dispenser0.is_set():
            send_command(f'mmd dispenser0_spd {speed}', s)
            print(f"Current speed: {speed}")
            speed = -speed
            time.sleep(30)
        send_command(f'mmd dispenser0_off', s)

    # 创建停止事件
    stop_dispenser0 = threading.Event()
    
    # 创建并启动线程
    thread = threading.Thread(target=dispenser0_thread, args=(s, 600, stop_dispenser0,))
    thread.start()

    d1_spd = -300
    (onhold_secs, keep_secs) = (1, 4)
    print(d1_spd, onhold_secs, keep_secs)
    send_command(f'mmd dispenser1_spd {d1_spd}', s)
    for i in range(1):
        send_command(f'mmd move_to 100', s)
        send_command(f'mmd belt_spd 50', s)
        send_command(f'mmd pr_spd 70', s)
        await asyncio.sleep(onhold_secs)

        send_command(f'mmd move_to 130', s)
        send_command(f'mmd belt_spd 0', s)
        send_command(f'mmd pr_spd 100', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 200', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 300', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 400', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 500', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 600', s)
        await asyncio.sleep(0.2)
        send_command(f'mmd pr_spd 700', s)
        send_command(f'mmd belt_spd 100', s)
        await asyncio.sleep(2)

    MIN_POS = 100
    PRODUCT = (540 - MIN_POS) * 50 / 75
    for p in range(140, 460, 60):
        # d1_spd = -1000 if d1_spd <= -1000 else d1_spd - 80
        send_command(f'mmd dispenser1_spd {d1_spd}', s)
        r = 540 - p
        a = (p - MIN_POS) * 2 + 50
        # a = 700
        v_b = round(a * r / PRODUCT) // 10 * 10
        print(d1_spd, p, a, v_b)
        send_command(f'mmd move_to {p}', s)
        send_command(f'mmd belt_spd 150', s)
        send_command(f'mmd pr_spd 700', s)
        await wait_for_stepper_available(s)
        await asyncio.sleep(keep_secs * r / 540)

    send_command(f'mmd move_to 460', s)
    stop_dispenser0.set()
    send_command(f'mmd dispenser0_off', s)
    send_command(f'mmd dispenser1_off', s)
    await asyncio.sleep(5)
    await wait_for_stepper_available(s)

    send_command(f'mmd home', s)
    send_command(f'mmd belt_off', s)
    send_command(f'mmd pr_off', s)
    await wait_for_stepper_available(s)

    thread.join()

