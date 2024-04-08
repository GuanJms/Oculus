import asyncio
import datetime
import time

from colorama import init
from colorama import Fore, Back, Style


class GEN_ID:
    _id = 0

    @classmethod
    def GET_ID(cls):
        cls._id += 1
        return cls._id

async def main():
    #
    # print(Back.GREEN + Fore.BLACK + "Starting synchronous work.", flush=True)
    #
    # start_time = datetime.datetime.now()
    #
    # synchronous_work()
    # synchronous_work()
    #
    # end_time = datetime.datetime.now() - start_time
    #
    # print(
    #     Back.GREEN
    #     + Fore.BLACK
    #     + f"Ending synchronous work. Total time: {end_time.total_seconds(): .2} sec.",
    #     flush=True,
    # )
    #
    # print(Back.MAGENTA + Fore.BLACK + "Starting awaiting async functions.", flush=True)
    #
    # start_time = datetime.datetime.now()
    #
    # await async_work(Back.LIGHTYELLOW_EX + Fore.BLACK)
    # await async_work(Back.LIGHTRED_EX + Fore.BLACK)
    #
    # end_time = datetime.datetime.now() - start_time
    #
    # print(
    #     Back.MAGENTA
    #     + Fore.BLACK
    #     + f"Ending awaiting async functions. Total time: {end_time.total_seconds(): .2} sec.",
    #     flush=True,
    # )
    #
    # print(Back.LIGHTBLUE_EX + Fore.BLACK + "Starting running async.", flush=True)
    #
    # start_time = datetime.datetime.now()
    #
    # tasks = [
    #     async_work(Back.LIGHTYELLOW_EX + Fore.BLACK),
    #     async_work(Back.LIGHTRED_EX + Fore.BLACK),
    # ]
    #
    # await asyncio.gather(*tasks)
    #
    # end_time = datetime.datetime.now() - start_time
    #
    # print(
    #     Back.LIGHTBLUE_EX
    #     + Fore.BLACK
    #     + f"Ending running async. Total time: {end_time.total_seconds(): .2} sec.",
    #     flush=True,
    # )
    #
    #
    # start_time = datetime.datetime.now()
    #
    # tasks = [
    #     synchronous_work_in_async_function(),
    #     synchronous_work_in_async_function(),
    # ]
    #
    # await asyncio.gather(*tasks)

    # end_time = datetime.datetime.now() - start_time
    #
    # print(
    #     Back.LIGHTBLUE_EX
    #     + Fore.BLACK
    #     + f"Ending running async. Total time: {end_time.total_seconds(): .2} sec.",
    #     flush=True,
    # )

    # print(Style.RESET_ALL)

    # print()

    start_time = datetime.datetime.now()

    tasks = [
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID(), f=f_test(f_test(f_test(f_test(f_test(f_test(f_test(f_test(f_test()))))))))),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID(), f=f_test()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
        f_test(_id=GEN_ID.GET_ID()),
    ]

    await asyncio.gather(*tasks)

    end_time = datetime.datetime.now() - start_time

    print(
        Back.LIGHTBLUE_EX
        + Fore.BLACK
        + f"Ending running async. Total time: {end_time.total_seconds(): .2} sec.",
        flush=True,
    )


async def f_test(f=None, _id=None):
    i = 0
    print(Back.CYAN + Fore.BLACK + f"Start.{i}_{_id}.")

    while f:
        values = await asyncio.gather(f)
        i = values[0]
        f = None
    print(Back.CYAN + Fore.BLACK + f"Pretending to wait.{i}_{_id}.")
    await asyncio.sleep(0.1)
    return i + 1


def synchronous_work():
    print(Back.CYAN + Fore.BLACK + "Pretending to wait.")
    time.sleep(2)


async def async_work(colour: str = Fore.BLACK):
    print(colour + "Pretending to wait async.")
    await asyncio.sleep(2)


async def synchronous_work_in_async_function():
    print(Back.CYAN + Fore.BLACK + "Pretending to wait.")
    time.sleep(2)


if __name__ == "__main__":
    init()
    asyncio.run(main())
