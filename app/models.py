from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Integer, String, DateTime, BigInteger, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id_role: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False)

    employees: Mapped[List["Employee"]] = relationship("Employee", back_populates="role")


class Employee(Base):
    __tablename__ = "employees"

    id_employee: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(500), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    id_role: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id_role", ondelete="RESTRICT"), nullable=False)

    role: Mapped["Role"] = relationship("Role", back_populates="employees")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="employee", foreign_keys="Request.id_employee")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="employee")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="employee")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="employee")


class SubjectType(Base):
    __tablename__ = "subject_types"

    id_subject_type: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_type_name: Mapped[str] = mapped_column(String(50), nullable=False)

    clients: Mapped[List["Client"]] = relationship("Client", back_populates="subject_type")


class Client(Base):
    __tablename__ = "clients"

    id_client: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(12), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    id_subject_type: Mapped[int] = mapped_column(Integer, ForeignKey("subject_types.id_subject_type", ondelete="RESTRICT"), nullable=False)

    subject_type: Mapped["SubjectType"] = relationship("SubjectType", back_populates="clients")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="client")


class Locality(Base):
    __tablename__ = "localities"

    id_locality: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    locality_name: Mapped[str] = mapped_column(String(200), nullable=False)

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="locality")


class Address(Base):
    __tablename__ = "addresses"

    id_address: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column(String(500), nullable=False)
    house: Mapped[str] = mapped_column(String(500), nullable=False)
    apartment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    id_locality: Mapped[int] = mapped_column(Integer, ForeignKey("localities.id_locality", ondelete="RESTRICT"), nullable=False)

    locality: Mapped["Locality"] = relationship("Locality", back_populates="addresses")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="address")


class Status(Base):
    __tablename__ = "statuses"

    id_status: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    requests: Mapped[List["Request"]] = relationship("Request", back_populates="status")


class Request(Base):
    __tablename__ = "requests"

    id_request: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_client: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id_client", ondelete="RESTRICT"), nullable=False)
    id_employee: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id_employee", ondelete="RESTRICT"), nullable=False)
    id_address: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id_address", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    id_status: Mapped[int] = mapped_column(Integer, ForeignKey("statuses.id_status", ondelete="RESTRICT"), nullable=False)
    appointment_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    client: Mapped["Client"] = relationship("Client", back_populates="requests")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="requests", foreign_keys=[id_employee])
    address: Mapped["Address"] = relationship("Address", back_populates="requests")
    status: Mapped["Status"] = relationship("Status", back_populates="requests")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="request", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="request", cascade="all, delete-orphan")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="request", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "appointments"

    id_appointment: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_request: Mapped[int] = mapped_column(Integer, ForeignKey("requests.id_request", ondelete="CASCADE"), nullable=False)
    id_employee: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id_employee", ondelete="RESTRICT"), nullable=False)
    start_date_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    request: Mapped["Request"] = relationship("Request", back_populates="appointments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="appointments")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="appointment", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="appointment")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="appointment")


class Attachment(Base):
    __tablename__ = "attachments"

    id_attachment: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_appointment: Mapped[int] = mapped_column(Integer, ForeignKey("appointments.id_appointment", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    uploaded_by: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("employees.id_employee", ondelete="RESTRICT"), nullable=True)

    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="attachments")
    employee: Mapped[Optional["Employee"]] = relationship("Employee", foreign_keys=[uploaded_by])


class Comment(Base):
    __tablename__ = "comments"

    id_comment: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    id_request: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("requests.id_request", ondelete="CASCADE"), nullable=True)
    id_appointment: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("appointments.id_appointment", ondelete="RESTRICT"), nullable=True)
    id_employee: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id_employee", ondelete="RESTRICT"), nullable=False)

    request: Mapped[Optional["Request"]] = relationship("Request", back_populates="comments")
    appointment: Mapped[Optional["Appointment"]] = relationship("Appointment", back_populates="comments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="comments")


class ChangeType(Base):
    __tablename__ = "change_types"

    id_change_type: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    change_type_name: Mapped[str] = mapped_column(String(100), nullable=False)

    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="change_type")


class HistoryLog(Base):
    __tablename__ = "history_logs"

    id_history: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    field_name: Mapped[str] = mapped_column(String(50), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    id_request: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("requests.id_request", ondelete="CASCADE"), nullable=True)
    id_appointment: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("appointments.id_appointment", ondelete="RESTRICT"), nullable=True)
    id_employee: Mapped[int] = mapped_column(Integer, ForeignKey("employees.id_employee", ondelete="RESTRICT"), nullable=False)
    id_change_type: Mapped[int] = mapped_column(Integer, ForeignKey("change_types.id_change_type", ondelete="RESTRICT"), nullable=False)

    request: Mapped[Optional["Request"]] = relationship("Request", back_populates="history_logs")
    appointment: Mapped[Optional["Appointment"]] = relationship("Appointment", back_populates="history_logs")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="history_logs")
    change_type: Mapped["ChangeType"] = relationship("ChangeType", back_populates="history_logs")
