from app.schemas.base import BaseSchema


class SubjectTypeBase(BaseSchema):
    subject_type_name: str


class SubjectTypeCreate(SubjectTypeBase):
    pass


class SubjectTypeUpdate(SubjectTypeBase):
    pass


class SubjectTypeOut(SubjectTypeBase):
    id_subject_type: int
