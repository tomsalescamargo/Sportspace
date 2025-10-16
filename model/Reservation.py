from datetime import datetime
from utils.enums import ReservationStatus

class Reservation:
    def __init__(self, client_id: int, court_id: int, date_time: datetime, status: ReservationStatus):
        self.client_id = client_id
        self.court_id = court_id
        self.date_time = date_time
        self.status = status
        self.__payments = []
        self.__extra_services = []

    @property
    def client_id(self) -> int:
        return self.__client_id

    @client_id.setter
    def client_id(self, client_id: int):
        self.__client_id = client_id

    @property
    def court_id(self) -> int:
        return self.__court_id

    @court_id.setter
    def court_id(self, court_id: int):
        self.__court_id = court_id

    @property
    def date_time(self) -> datetime:
        return self.__date_time

    @date_time.setter
    def date_time(self, date_time: datetime):
        self.__date_time = date_time

    @property
    def status(self) -> ReservationStatus:
        return self.__status

    @status.setter
    def status(self, status: ReservationStatus):
        self.__status = status

    @property
    def payments(self) -> list:
        return self.__payments

    @property
    def extra_services(self) -> list:
        return self.__extra_services

