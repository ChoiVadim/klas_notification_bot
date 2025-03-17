import os
import json
import logging
import asyncio
import datetime
from typing import Optional, Dict, List

import aiohttp
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import base64


class KwangwoonUniversityApi:
    def __init__(self) -> None:
        self.ua: UserAgent = UserAgent()
        self.current_dir: str = os.path.dirname(os.path.abspath(__file__))
        self.headers: dict = {
            "Content-Type": "application/json",
            "User-Agent": self.ua.random,
        }
        self.cookies: dict = {}
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _cookies_is_valid(self) -> bool:
        if not self.cookies:
            logging.error("No cookies found. Please log in first.")
            return False
        return True

    def set_cookies(self, cookies: dict):
        self.cookies = cookies

    async def login_with_cookies(self, cookies: dict) -> bool:
        self.set_cookies(cookies)
        login_form_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginForm.do"

        async with self.session.get(login_form_url, cookies=self.cookies) as response:
            if str(response.url) != login_form_url:
                logging.info(f"Log in with cookies. Status code: {response.status}")
                return True
        return False

    def _encryptor(self, public_key: str, data: str) -> Optional[str]:
        pem = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----"

        public_key = RSA.importKey(pem)

        # Jsencrypt uses PKCS1_v1_5
        cipher = PKCS1_v1_5.new(public_key)

        encoded = base64.b64encode(
            cipher.encrypt(data.encode()),
        ).decode()

        return encoded

    async def login(self, login_id: str, login_pwd: str) -> Optional[Dict]:
        login_form_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginForm.do"
        public_key_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginSecurity.do"
        login_url = "https://klas.kw.ac.kr/usr/cmn/login/LoginConfirm.do"

        async with self.session.get(
            login_form_url, cookies=self.cookies
        ) as login_form_response:
            if str(login_form_response.url) != login_form_url:
                logging.info(
                    f"Log in with cookies. Status code: {login_form_response.status}"
                )
                return 1

        async with self.session.get(public_key_url) as public_key_response:
            public_key_json = await public_key_response.json()
            public_key_str = public_key_json["publicKey"]

        login_data = {"loginId": login_id, "loginPwd": login_pwd, "storeIdYn": "Y"}
        login_json = json.dumps(login_data)

        try:
            encrypted_login = self._encryptor(public_key_str, login_json)
            if not encrypted_login:
                logging.error("Encryption failed")
                return None

            login_body = {
                "loginToken": encrypted_login,
                "redirectUrl": "/std/cmn/frame/Frame.do",
                "redirectTabUrl": "",
            }

            async with self.session.post(
                login_url,
                json=login_body,
                headers=self.headers,
                cookies=self.cookies,
            ) as login_response:
                if login_response.status == 200:
                    response_data = await login_response.json()
                    if response_data.get("errorCount", 0) == 0:
                        logging.debug("Login successful.")
                        self.cookies = {
                            cookie.key: cookie.value
                            for cookie in self.session.cookie_jar
                        }
                        return self.cookies
                    elif (
                        response_data.get("fieldErrors")[0].get("message")
                        == "비밀번호 실패 5회 초과로 인하여 계정이 잠겼습니다.\n비밀번호 찾기를 이용해주세요."
                    ):
                        logging.error(
                            "Login failed. Enter wrong password 5 times. Please reset password."
                        )
                        return None
                    else:
                        logging.error(
                            "Failed to parse response. Login failed. Wrong password or ID"
                        )
                        return None
                else:
                    logging.error("Failed to communicate with server.")
                    logging.error(f"Status code: {login_response.status}")
                    return None

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    async def get_subjects(self) -> Optional[Dict]:
        if not self._cookies_is_valid():
            return None

        url = "https://klas.kw.ac.kr/std/cmn/frame/YearhakgiAtnlcSbjectList.do"

        async with self.session.post(
            url=url, headers=self.headers, cookies=self.cookies, json={}
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                logging.debug("Data about subjects retrieved successfully.")
                return response_data[0]
            else:
                logging.error(
                    f"Failed to retrieve data. Status code: {response.status}"
                )
                return None

    async def _make_lecture_request(
        self, url: str, subject_id: str, year: str
    ) -> Optional[Dict]:
        if not self._cookies_is_valid():
            return None

        requests_body = {
            "selectSubj": subject_id,
            "selectYearhakgi": year,
            "selectChangeYn": "Y",
        }

        async with self.session.post(
            url=url, json=requests_body, headers=self.headers, cookies=self.cookies
        ) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def _get_lectures(self, subject_id: str, year: str) -> Optional[Dict]:
        lectures_url = (
            "https://klas.kw.ac.kr/std/lis/evltn/SelectOnlineCntntsStdList.do"
        )
        return await self._make_lecture_request(lectures_url, subject_id, year)

    async def _get_homeworks(self, subject_id: str, year: str) -> Optional[Dict]:
        homeworks_url = "https://klas.kw.ac.kr/std/lis/evltn/TaskStdList.do"
        return await self._make_lecture_request(homeworks_url, subject_id, year)

    async def _get_team_projects(self, subject_id: str, year: str) -> Optional[Dict]:
        team_projects_url = "https://klas.kw.ac.kr/std/lis/evltn/PrjctStdList.do"
        return await self._make_lecture_request(team_projects_url, subject_id, year)

    async def _get_quizzes(self, subject_id: str, year: str) -> Optional[Dict]:
        quizzes_url = "https://klas.kw.ac.kr/std/lis/evltn/AnytmQuizStdList.do"
        return await self._make_lecture_request(quizzes_url, subject_id, year)

    def _get_not_done_lectures_info(self, lectures: list[dict]) -> list[dict]:
        not_done_lectures = []
        today_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for lecture in lectures:
            if (
                lecture.get("prog") is not None
                and lecture.get("prog") < 100
                and lecture.get("startDate") < today_date
                and lecture.get("endDate") > today_date
            ):
                not_done_lectures.append(
                    {
                        "title": lecture.get("sbjt"),
                        "progress": lecture.get("prog"),
                        "expire_date": lecture.get("endDate"),
                        "left_time": self._get_left_time(
                            lecture.get("endDate"), "%Y-%m-%d %H:%M"
                        ),
                    }
                )
        return not_done_lectures

    def _get_not_done_homeworks_info(self, homeworks: list[dict]) -> list[dict]:
        not_done_homeworks = []
        today_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for homework in homeworks:
            if (
                homework.get("submityn") == "N"
                and homework.get("startdate") < today_date
                and homework.get("expiredate") > today_date
            ):
                not_done_homeworks.append(
                    {
                        "title": homework.get("title"),
                        "expire_date": homework.get("expiredate"),
                        "left_time": self._get_left_time(
                            homework.get("expiredate"), "%Y-%m-%d %H:%M:%S"
                        ),
                    }
                )
        return not_done_homeworks

    def _get_not_done_team_projects_info(self, team_projects: list[dict]) -> list[dict]:
        not_done_team_projects = []
        today_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        for team_project in team_projects:
            if (
                team_project.get("submityn") != "Y"
                and team_project.get("startdate") < today_date
                and team_project.get("expiredate") > today_date
            ):
                not_done_team_projects.append(
                    {
                        "title": team_project.get("title"),
                        "expire_date": team_project.get("expiredate"),
                        "left_time": self._get_left_time(
                            team_project.get("expiredate"),
                            "%Y-%m-%dT%H:%M:%S.%f%z",
                            True,
                        ),
                    }
                )
        return not_done_team_projects

    def _get_not_done_quizzes_info(self, quizzes: list[dict]) -> list[dict]:
        not_done_quizzes = []
        today_date = datetime.datetime.now().strftime("%Y%m%d%H%M")
        for quiz in quizzes:
            if (
                quiz.get("issubmit") == "N"
                and quiz.get("sdate") < today_date
                and quiz.get("edate") > today_date
            ):
                not_done_quizzes.append(
                    {
                        "title": quiz.get("papernm"),
                        "expire_date": quiz.get("edt"),
                        "left_time": self._get_left_time(
                            quiz.get("edt"), "%Y-%m-%d %H:%M"
                        ),
                    }
                )
        return not_done_quizzes

    def _get_left_time(self, expire_date, date_format, remove_timezone=False):
        expire_date_time = datetime.datetime.strptime(expire_date, date_format)
        if remove_timezone:
            expire_date_time = expire_date_time.replace(tzinfo=None)
        now_time = datetime.datetime.now()
        return expire_date_time - now_time

    async def get_todo_list(self) -> Optional[List[Dict]]:
        if not self._cookies_is_valid():
            return None

        subjects = await self.get_subjects()
        if not subjects:
            return None

        todo_list = [
            {"id": subject.get("value"), "name": subject.get("name"), "todo": {}}
            for subject in subjects.get("subjList")
        ]

        try:
            subject_semester = subjects.get("value")

            # Use asyncio.gather to fetch all data concurrently
            for todo in todo_list:
                year = subject_semester
                subject_id = todo.get("id")

                lectures, homeworks, team_projects, quizzes = await asyncio.gather(
                    self._get_lectures(subject_id, year),
                    self._get_homeworks(subject_id, year),
                    self._get_team_projects(subject_id, year),
                    self._get_quizzes(subject_id, year),
                )

                todo["todo"] = {
                    "lectures": self._get_not_done_lectures_info(lectures),
                    "homeworks": self._get_not_done_homeworks_info(homeworks),
                    "team_projects": self._get_not_done_team_projects_info(
                        team_projects
                    ),
                    "quizzes": self._get_not_done_quizzes_info(quizzes),
                }

            return todo_list

        except Exception as e:
            logging.error(f"An error occurred while getting todo list: {e}")
            return None

    async def _make_student_info_request(self, url: str) -> Optional[Dict]:
        if not self._cookies_is_valid():
            return None

        headers = {
            "Content-Type": "application/json",
            "User-Agent": self.ua.random,
        }

        async with self.session.post(
            url=url, json={}, headers=headers, cookies=self.cookies
        ) as response:
            if response.status == 200:
                return await response.json()
            return None

    async def _get_major_credits(self, major):
        if "전자정보공학대학" in major:
            return {
                "total_credits": 133,
                "major_credits": 60,
                "elective_credits": 30,
            }
        elif "소프트웨어학" in major:
            return {
                "total_credits": 133,
                "major_credits": 60,
                "elective_credits": 30,
            }
        elif "공과대학" in major:
            if "건축학" in major:
                return {
                    "total_credits": 163,
                    "major_credits": 120,
                    "elective_credits": 55,
                }
            else:
                return {
                    "total_credits": 133,
                    "major_credits": 60,
                    "elective_credits": 30,
                }
        elif "자연과학대학" in major:
            return {
                "total_credits": 133,
                "major_credits": 60,
                "elective_credits": 30,
            }
        elif "인문사회과학대학" in major:
            return {
                "total_credits": 130,
                "general_credits": 51,
                "major_credits": 45,
                "elective_credits": 34,
            }
        elif "정책법학대학" in major:
            return {
                "total_credits": 130,
                "general_credits": 45,
                "major_credits": 36,
                "elective_credits": 49,
            }
        elif "경영대학" in major:
            if "국제통상학부" in major:
                return {
                    "total_credits": 133,
                    "general_credits": 57,
                    "major_credits": 45,
                    "elective_credits": 31,
                }
            else:
                return {
                    "total_credits": 130,
                    "general_credits": 54,
                    "major_credits": 45,
                    "elective_credits": 31,
                }
        else:
            return {
                "total_credits": 0,
                "general_credits": 0,
                "major_credits": 0,
                "elective_credits": 0,
            }

    async def get_student_info(self) -> Optional[Dict]:
        if not self._cookies_is_valid():
            return None

        student_info = await self._make_student_info_request(
            "https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreHakjukInfo.do",
        )
        
        if not student_info:
            logging.error("Failed to retrieve student info")
            return None
            
        grades = await self._make_student_info_request(
            "https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreSungjukTot.do",
        )
        
        if not grades:
            logging.error("Failed to retrieve grades")
            return None

        grades_for_each_semester = await self._make_student_info_request(
            "https://klas.kw.ac.kr/std/cps/inqire/AtnlcScreSungjukInfo.do",
        )
        
        if not grades_for_each_semester:
            logging.error("Failed to retrieve grades for each semester")
            return None

        semester = 0
        for semester_info in grades_for_each_semester:
            if semester_info.get("hakgiOrder") == "계절학기(동계)":
                continue
            semester += 1

        grade = student_info.get("grade", "N/A")
        student_id = student_info.get("hakbun", "N/A")
        major = student_info.get("hakgwa", "N/A")
        student_name = student_info.get("kname", "N/A")
        student_credits = grades.get("chidukHakjum", 0)
        elective_credits = grades.get("cultureChidukHakjum", 0)
        major_credits = grades.get("majorChidukHakjum", 0)
        average_score = grades.get("jaechulScoresum", "N/A")

        if major and "소프트웨어" in major:
            total_credits = 133
            total_major_credits = 60
            total_elective_credits = 30

            try:
                credits_ratio = round((student_credits / total_credits) * 100, 2)
                major_credits_ratio = round((major_credits / total_major_credits) * 100, 2)

                credits_for_each_semester = round(
                    (total_credits - student_credits) / max(1, (4 * 2 - semester + 1)), 2
                )
                major_credits_for_each_semester = round(
                    (total_major_credits - major_credits) / max(1, (4 * 2 - semester + 1)), 2
                )
            except (ZeroDivisionError, TypeError):
                credits_ratio = "N/A"
                major_credits_ratio = "N/A"
                credits_for_each_semester = "N/A"
                major_credits_for_each_semester = "N/A"
        else:
            total_credits = "N/A"
            total_major_credits = "N/A"
            total_elective_credits = "N/A"
            credits_ratio = "N/A"
            major_credits_ratio = "N/A"
            credits_for_each_semester = "N/A"
            major_credits_for_each_semester = "N/A"

        return {
            "uid": student_id,
            "name": student_name,
            "major": major,
            "grade": grade,
            "semester": semester,
            "credits": {
                "total": student_credits,
                "required": total_credits,
                "ratio": credits_ratio,
            },
            "major_credits": {
                "total": major_credits,
                "required": total_major_credits,
                "ratio": major_credits_ratio,
            },
            "elective_credits": {
                "total": elective_credits,
                "required": total_elective_credits,
            },
            "average_score": average_score,
            "credits_for_each_semester": credits_for_each_semester,
            "major_credits_for_each_semester": major_credits_for_each_semester,
        }

    async def get_student_photo_url(self) -> Optional[str]:
        if not self._cookies_is_valid():
            return None
        body = {
            "selectedGrcode": "",
            "selectedYearhakgi": "",
            "selectedSubj": "",
        }
        try:
            async with self.session.post(
                "https://klas.kw.ac.kr/std/sys/optrn/MyNumberQrStdPage.do",
                cookies=self.cookies,
                headers=self.headers,
                json=body,
            ) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    # Update the selector based on the actual HTML structure
                    img_tag = soup.select_one(".col-sm-5.text-center p.p-10 img")
                    if not img_tag:
                        # Try alternative selector
                        img_tag = soup.select_one("img[alt='faceofperson']")
                    if img_tag and img_tag.has_attr('src'):
                        return img_tag.get("src")
                    logging.warning("Could not find student photo image tag")
        except Exception as e:
            logging.error(f"Failed to retrieve student photo URL: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def main():
        async with KwangwoonUniversityApi() as student:
            username = input("Enter your ID: ")
            password = input("Enter your password: ")
            await student.login(username, password)
            todo_list = await student.get_todo_list()
            student_info = await student.get_student_info()
            student_photo_url = await student.get_student_photo_url()
            print(student_photo_url)
            print(student_info)
            # print(todo_list)

    asyncio.run(main())
