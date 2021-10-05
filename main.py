import csv
import time

import asyncio
from arsenic import get_session, browsers, services

class_name_to_search = "zenroomspageperks-rating-info-total-value"
service = services.Geckodriver(binary="geckodriver.exe")
browser = browsers.Firefox()


def write_data_to_file(tag, hotel_code, for_start_time):
    try:
        value = tag.get_text()
        result_text = hotel_code + "; " + value.text + "\n"
    except:
        result_text = hotel_code + "; " + "null\n"

    with open("code_with_rating_async.txt", "a", encoding='utf-8') as file:
        file.write(result_text)

    print(f"loading {hotel_code} got {(time.time() - for_start_time)} seconds")


async def proceed_hotel_code(url, hotel_code, for_start_time, session):
    await session.get(url)
    try:
        tag = await session.wait_for_element(10, class_name_to_search)
        write_data_to_file(session.get_page_source(), hotel_code, for_start_time)
    except:
        write_data_to_file(session.get_page_source(), hotel_code, for_start_time)


async def looper():
    start_time = time.time()

    with open("maps_collection_async.csv", 'r', encoding="utf-8-sig") as fd:
        hotel_code_rows = csv.reader(fd)
        async with get_session(service, browser) as session:
            for hotel_code_row in hotel_code_rows:
                for_start_time = time.time()
                hotel_code_bytes = hotel_code_row[0].encode()
                hotel_code = hotel_code_bytes.decode()
                url = "https://ostrovok.ru/rooms/" + hotel_code
                await proceed_hotel_code(url, hotel_code, for_start_time, session)

    print(f"loading {hotel_code} got {(time.time() - start_time)} seconds")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(looper())


if __name__ == "__main__":
    main()
