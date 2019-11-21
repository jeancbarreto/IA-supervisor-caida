
import platform
import asyncio
import logging

from bleak import BleakClient


async def run(address, loop, debug=True):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))
        data = []

        for service in client.services:
            log.info("[Service] {0}: {1}".format(service.uuid, service.description))
            if(service.description == "Hear Rate"): #Hear Rate, Generic Attribute Profile, Generic Access Profile, Vendor specific
                for char in service.characteristics:
                    if "read" in char.properties:
                        value = await client.read_gatt_char(char.uuid)
                        data.append(value)
                    
                    for descriptor in char.descriptors:
                        value = await client.read_gatt_descriptor(descriptor.handle)
                        print(value)

            

        print(data)
        for datoHeart in data:
            print("[Valor de ritmo cardiaco]: {0}".format(datoHeart))
            # for info in datoHeart:
            #     print("[Valor de ritmo cardiaco]: {0}".format(info))


if __name__ == "__main__":
    address = "C5:1A:2D:89:ED:42"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))