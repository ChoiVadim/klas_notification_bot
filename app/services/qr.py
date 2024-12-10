import logging
import asyncio
from aiohttp import ClientSession
import xml.etree.ElementTree as ET
from base64 import encodebytes, b64encode

import qrcode
from Crypto.Cipher import AES


BASE_URL = "https://mobileid.kw.ac.kr"

# Add a session variable at module level
_session = None


async def get_session():
    global _session
    if _session is None:
        _session = ClientSession()
    return _session


def encode(msg: str):
    return b64encode(msg.encode(encoding="utf-8")).decode()


def encrypt(msg, secret):
    iv = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    cipher = AES.new(secret.encode(encoding="utf-8"), AES.MODE_CBC, iv)

    def fill_padding(msg):
        padding_sz = 16
        pad = lambda s: s + (padding_sz - len(s) % padding_sz) * chr(
            padding_sz - len(s) % padding_sz
        )
        return pad(msg).encode()

    return encodebytes(cipher.encrypt(fill_padding(msg))).decode().strip()


async def get_secret_key(real_id: str) -> str:
    url = f"{BASE_URL}/mobile/MA/xml_user_key.php"
    data = {"user_id": encode(real_id)}

    session = await get_session()
    async with session.post(url, data=data) as response:
        if response.status != 200:
            raise Exception(f"Failed to fetch secret key: {response.status}")

        response_data = await response.text()
        return parse_xml_response(response_data, "sec_key")


async def library_login(std_number: str, phone: str, password: str, secret: str) -> str:
    url = f"{BASE_URL}/mobile/MA/xml_login_and.php"
    encrypted_password = encrypt(password, secret)
    data = {
        "real_id": encode("0" + std_number),
        "rid": encode(std_number),
        "device_gb": "A",
        "tel_no": phone,
        "pass_wd": encrypted_password,
    }

    session = await get_session()
    async with session.post(url, data=data) as response:
        if response.status != 200:
            logging.error(f"Failed to get auth key: {response.status}")
            return None

        response_data = await response.text(encoding="iso-8859-1")
        auth_key = parse_xml_response(response_data, "auth_key")
        if not auth_key:
            logging.error(f"Failed to get auth key: {response_data}")
            return None

        return auth_key


async def get_qr_code(real_id: str, auth_key: str) -> dict:
    url = f"{BASE_URL}/mobile/MA/xml_userInfo_auth.php"
    data = {"real_id": encode(real_id), "auth_key": auth_key, "new_check": "Y"}

    async with ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status != 200:
                raise Exception(f"Failed to get QR code: {response.status}")

            response_data = await response.text(encoding="iso-8859-1")
            try:
                root = ET.fromstring(response_data)
                return {
                    "qr_code": (
                        root.find(".//qr_code").text
                        if root.find(".//qr_code") is not None
                        else None
                    ),
                    # "user_name": (
                    #     root.find(".//user_name").text
                    #     if root.find(".//user_name") is not None
                    #     else None
                    # ),
                    # "user_code": (
                    #     root.find(".//user_code").text
                    #     if root.find(".//user_code") is not None
                    #     else None
                    # ),
                    # "user_deptName": (
                    #     root.find(".//user_deptName").text
                    #     if root.find(".//user_deptName") is not None
                    #     else None
                    # ),
                }
            except ET.ParseError as e:
                print(f"Raw response: {response_data}")
                raise Exception(f"Failed to parse XML response: {e}")


def parse_xml_response(xml_string: str, tag: str) -> str:
    root = ET.fromstring(xml_string)
    for element in root.iter(tag):
        # Extract the text inside the CDATA section if present
        return element.text.strip() if element.text else None
    return None


async def generate_qr_code(qr_data: str, path: str):
    if "qr_code" not in qr_data or len(qr_data["qr_code"]) < 5:
        logging.error("Error: Invalid QR code data.")
        return

    qr_value = qr_data["qr_code"]

    # Optimized QR parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,  # Reduced box size
        border=4,  # Reduced border
    )

    qr.add_data(qr_value)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(path, format="PNG", optimize=True)  # Add optimization for PNG

    return path


async def get_qr(std_number: str, phone_number: str, password: str):
    real_id = "0" + std_number
    try:
        secret = await get_secret_key(real_id)
        auth_key = await library_login(std_number, phone_number, password, secret)
        qr_data = await get_qr_code(real_id, auth_key)
        qr_path = await generate_qr_code(qr_data, path="images/qr.png")
        return qr_path
    except Exception as e:
        logging.error(f"Error in get_qr: {e}")
        return None


async def main():
    std_number = ""
    phone = ""
    password = ""
    real_id = "0" + std_number

    try:
        secret = await get_secret_key(real_id)
        auth_key = await library_login(real_id, std_number, phone, password, secret)
        qr_data = await get_qr_code(real_id, auth_key)
        generate_qr_code(qr_data, path="qr.png")
    except Exception as e:
        logging.error(f"Error in main: {e}")


if __name__ == "__main__":
    asyncio.run(main())
