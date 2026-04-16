from datetime import datetime
from typing import Optional, List
from sqlalchemy import Integer, String, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Role(Base):
    __tablename__ = "Roles"

    id_role: Mapped[int] = mapped_column("IdRole", Integer, primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column("RoleName", String(50), nullable=False)

    employees: Mapped[List["Employee"]] = relationship("Employee", back_populates="role")


class Employee(Base):
    __tablename__ = "Employees"

    id_employee: Mapped[int] = mapped_column("IdEmployee", Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column("Login", String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column("Password", String(500), nullable=False)
    first_name: Mapped[str] = mapped_column("FirstName", String(50), nullable=False)
    last_name: Mapped[str] = mapped_column("LastName", String(50), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column("Phone", String(12), nullable=True)
    id_role: Mapped[int] = mapped_column("IdRole", Integer, ForeignKey("Roles.IdRole", ondelete="RESTRICT"), nullable=False)

    role: Mapped["Role"] = relationship("Role", back_populates="employees")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="employee", foreign_keys="Request.id_employee")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="employee")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="employee")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="employee")


class SubjectType(Base):
    __tablename__ = "SubjectTypes"

    id_subject_type: Mapped[int] = mapped_column("IdSubjectType", Integer, primary_key=True, autoincrement=True)
    subject_type_name: Mapped[str] = mapped_column("SubjectTypeName", String(50), nullable=False)

    clients: Mapped[List["Client"]] = relationship("Client", back_populates="subject_type")


class Client(Base):
    __tablename__ = "Clients"

    id_client: Mapped[int] = mapped_column("IdClient", Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column("FirstName", String(150), nullable=False)
    last_name: Mapped[str] = mapped_column("LastName", String(150), nullable=False)
    phone: Mapped[str] = mapped_column("Phone", String(12), nullable=False)
    email: Mapped[Optional[str]] = mapped_column("Email", String(100), nullable=True)
    id_subject_type: Mapped[Optional[int]] = mapped_column("IdSubjectType", Integer, ForeignKey("SubjectTypes.IdSubjectType", ondelete="RESTRICT"), nullable=True)

    subject_type: Mapped[Optional["SubjectType"]] = relationship("SubjectType", back_populates="clients")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="client")


class Locality(Base):
    __tablename__ = "Localities"

    id_locality: Mapped[int] = mapped_column("IdLocality", Integer, primary_key=True, autoincrement=True)
    locality_name: Mapped[str] = mapped_column("LocalityName", String(200), nullable=False)

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="locality")


class Address(Base):
    __tablename__ = "Addresses"

    id_address: Mapped[int] = mapped_column("IdAddress", Integer, primary_key=True, autoincrement=True)
    street: Mapped[str] = mapped_column("Street", String(500), nullable=False)
    house: Mapped[str] = mapped_column("House", String(500), nullable=False)
    apartment: Mapped[Optional[str]] = mapped_column("Apartment", String(50), nullable=True)
    id_locality: Mapped[int] = mapped_column("IdLocality", Integer, ForeignKey("Localities.IdLocality", ondelete="RESTRICT"), nullable=False)

    locality: Mapped["Locality"] = relationship("Locality", back_populates="addresses")
    requests: Mapped[List["Request"]] = relationship("Request", back_populates="address")


class Status(Base):
    __tablename__ = "Statuses"

    id_status: Mapped[int] = mapped_column("IdStatus", Integer, primary_key=True, autoincrement=True)
    status_name: Mapped[str] = mapped_column("StatusName", String(50), nullable=False, unique=True)

    requests: Mapped[List["Request"]] = relationship("Request", back_populates="status")


class Request(Base):
    __tablename__ = "Requests"

    id_request: Mapped[int] = mapped_column("IdRequest", Integer, primary_key=True, autoincrement=True)
    id_client: Mapped[int] = mapped_column("IdClient", Integer, ForeignKey("Clients.IdClient", ondelete="RESTRICT"), nullable=False)
    id_employee: Mapped[int] = mapped_column("IdEmployee", Integer, ForeignKey("Employees.IdEmployee", ondelete="RESTRICT"), nullable=False)
    id_address: Mapped[int] = mapped_column("IdAddress", Integer, ForeignKey("Addresses.IdAddress", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DateTime, nullable=False)
    id_status: Mapped[int] = mapped_column("IdStatus", Integer, ForeignKey("Statuses.IdStatus", ondelete="RESTRICT"), nullable=False)
    appointment_date: Mapped[Optional[datetime]] = mapped_column("AppointmentDate", DateTime, nullable=True)

    client: Mapped["Client"] = relationship("Client", back_populates="requests")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="requests", foreign_keys=[id_employee])
    address: Mapped["Address"] = relationship("Address", back_populates="requests")
    status: Mapped["Status"] = relationship("Status", back_populates="requests")
    appointments: Mapped[List["Appointment"]] = relationship("Appointment", back_populates="request", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="request", cascade="all, delete-orphan")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="request", cascade="all, delete-orphan")


class Appointment(Base):
    __tablename__ = "Appointments"

    id_appointment: Mapped[int] = mapped_column("IdAppointment", Integer, primary_key=True, autoincrement=True)
    id_request: Mapped[int] = mapped_column("IdRequest", Integer, ForeignKey("Requests.IdRequest", ondelete="CASCADE"), nullable=False)
    id_employee: Mapped[int] = mapped_column("IdEmployee", Integer, ForeignKey("Employees.IdEmployee", ondelete="RESTRICT"), nullable=False)
    start_date_time: Mapped[datetime] = mapped_column("StartDateTime", DateTime, nullable=False)
    end_date_time: Mapped[Optional[datetime]] = mapped_column("EndDateTime", DateTime, nullable=True)

    request: Mapped["Request"] = relationship("Request", back_populates="appointments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="appointments")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="appointment", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="appointment")
    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="appointment")


class Attachment(Base):
    __tablename__ = "Attachments"

    id_attachment: Mapped[int] = mapped_column("IdAttachment", Integer, primary_key=True, autoincrement=True)
    id_appointment: Mapped[int] = mapped_column("IdAppointment", Integer, ForeignKey("Appointments.IdAppointment", ondelete="CASCADE"), nullable=False)
    file_name: Mapped[str] = mapped_column("FileName", String(255), nullable=False)
    file_path: Mapped[str] = mapped_column("FilePath", String(500), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column("FileSize", BigInteger, nullable=True)
    content_type: Mapped[Optional[str]] = mapped_column("ContentType", String(100), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column("UploadedAt", DateTime, nullable=False, default=datetime.now)
    uploaded_by: Mapped[Optional[int]] = mapped_column("UploadedBy", Integer, ForeignKey("Employees.IdEmployee", ondelete="RESTRICT"), nullable=True)

    appointment: Mapped["Appointment"] = relationship("Appointment", back_populates="attachments")
    employee: Mapped[Optional["Employee"]] = relationship("Employee", foreign_keys=[uploaded_by])


class Comment(Base):
    __tablename__ = "Comments"

    id_comment: Mapped[int] = mapped_column("IdComment", Integer, primary_key=True, autoincrement=True)
    comment_text: Mapped[str] = mapped_column("CommentText", String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column("CreatedAt", DateTime, nullable=False)
    id_request: Mapped[Optional[int]] = mapped_column("IdRequest", Integer, ForeignKey("Requests.IdRequest", ondelete="CASCADE"), nullable=True)
    id_appointment: Mapped[Optional[int]] = mapped_column("IdAppointment", Integer, ForeignKey("Appointments.IdAppointment", ondelete="RESTRICT"), nullable=True)
    id_employee: Mapped[int] = mapped_column("IdEmployee", Integer, ForeignKey("Employees.IdEmployee", ondelete="RESTRICT"), nullable=False)

    request: Mapped[Optional["Request"]] = relationship("Request", back_populates="comments")
    appointment: Mapped[Optional["Appointment"]] = relationship("Appointment", back_populates="comments")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="comments")


class ChangeType(Base):
    __tablename__ = "ChangeTypes"

    id_change_type: Mapped[int] = mapped_column("IdChangeType", Integer, primary_key=True, autoincrement=True)
    change_type_name: Mapped[str] = mapped_column("ChangeTypeName", String(100), nullable=False)

    history_logs: Mapped[List["HistoryLog"]] = relationship("HistoryLog", back_populates="change_type")


class HistoryLog(Base):
    __tablename__ = "HistoryLogs"

    id_history: Mapped[int] = mapped_column("IdHistory", Integer, primary_key=True, autoincrement=True)
    field_name: Mapped[str] = mapped_column("FieldName", String(50), nullable=False)
    old_value: Mapped[Optional[str]] = mapped_column("OldValue", String(500), nullable=True)
    new_value: Mapped[Optional[str]] = mapped_column("NewValue", String(500), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column("CreatedAt", DateTime, nullable=True, default=datetime.now)
    id_request: Mapped[Optional[int]] = mapped_column("IdRequest", Integer, ForeignKey("Requests.IdRequest", ondelete="CASCADE"), nullable=True)
    id_appointment: Mapped[Optional[int]] = mapped_column("IdAppointment", Integer, ForeignKey("Appointments.IdAppointment", ondelete="RESTRICT"), nullable=True)
    id_employee: Mapped[int] = mapped_column("IdEmployee", Integer, ForeignKey("Employees.IdEmployee", ondelete="RESTRICT"), nullable=False)
    id_change_type: Mapped[int] = mapped_column("IdChangeType", Integer, ForeignKey("ChangeTypes.IdChangeType", ondelete="RESTRICT"), nullable=False)

    request: Mapped[Optional["Request"]] = relationship("Request", back_populates="history_logs")
    appointment: Mapped[Optional["Appointment"]] = relationship("Appointment", back_populates="history_logs")
    employee: Mapped["Employee"] = relationship("Employee", back_populates="history_logs")
    change_type: Mapped["ChangeType"] = relationship("ChangeType", back_populates="history_logs")
