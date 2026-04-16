from pydantic import BaseModel


class SubjectTypeBase(BaseModel):
    subject_type_name: str


class SubjectTypeCreate(SubjectTypeBase):
    pass


class SubjectTypeUpdate(SubjectTypeBase):
    pass


class SubjectTypeOut(SubjectTypeBase):
    id_subject_type: int

    model_config = {"from_attributes": True}
