import enum
from datetime import datetime
from typing import Any

from fastapi import Query
from pydantic import BaseModel, Field, RootModel


class UserInput(BaseModel):
    username: str


class QuestionOrderSchema(str, enum.Enum):  # noqa: UP042 enum.StrEnum for 3.11
    id = "id"
    active = "active"
    updated_dt = "updated_dt"


class QuestionOrderEnum(str, enum.Enum):
    ID = "id"
    CREATED_AT = "created_at"
    TEXT = "text"


class QuestionListRequest(BaseModel):
    question_id: int | None = Field(description="id of a question", default=0)
    text: str | None = Field(description="search by text", default=None)
    active: int | None = Field(description="if question is active", default=1)
    # order: str | None = Field(
    #     default="id",
    #     description="order of results"
    # )
    # offset: int | None = Field(description="offset to show on page", default=0)
    # limit: int | None = Field(description="limit to show on page", default=50)

    @classmethod
    def as_query(
        cls,
        question_id: int | None = Query(None, description="id of a question"),
        text: str | None = Query(None, description="search by text"),
        active: int | None = Query(1, description="if question is active"),
        # order: str | None = Query(
        #     "id",
        #     description="order of results"
        # ),
        # offset: int | None = Query(0, description="offset to show on page"),
        # limit: int | None = Query(50, description="limit to show on page"),
    ):
        return cls(
            question_id=question_id,
            text=text,
            active=active,
            #    order=order, offset=offset, limit=limit
        )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "question",
                "active": 1,
                "id": None,
                "order": "updated_dt",
                "offset": 0,
                "limit": 50,
            }
        }


class QuestionGetOneRequest(BaseModel):
    question_id: int | None = Field(description="id of a question", default=0)
    tg_id: int = Field(description="tg_id of a player")


class QuestionAddRequest(BaseModel):
    text: str = Field(description="text", min_length=1, max_length=255)
    active: int | None = Field(description="if question is active", default=1)

    class Config:
        json_schema_extra = {
            "example": {
                "text": "question1",
                "active": 1,
            }
        }


class QuestionEditRequest(BaseModel):
    # id: int = Field(description="id of a question")
    text: str | None = Field(
        description="text", min_length=1, max_length=255, default=None
    )
    active: int | None = Field(
        description="if question is active", default=None
    )

    class Config:
        json_schema_extra = {
            "example": {
                "text": "question1",
                "active": 1,
                "id": 1,
            }
        }


class QuestionResponse(BaseModel):
    id: int = Field(description="id of a question")
    text: str = Field(description="text")
    active: int = Field(description="if question is active")
    updated_dt: datetime = Field(description="date")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "question1",
                "active": 1,
                "updated_dt": "2024-09-10T08:19:54.531503+00:00",
            }
        }


class QuizListResponse(BaseModel):
    id: int = Field(description="id of a question")
    text: str = Field(description="text")
    active: int = Field(description="if question is active")
    answers: list[Any]


class AnswerRequest(BaseModel):
    id: int | None = Field(description="id of an answer", default=None)
    text: str = Field(description="text", min_length=1, max_length=50)
    correct: bool = Field(description="if answer is correct")
    question_id: int = Field(description="id of a question")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "answer",
                "correct": True,
                "question_id": 1,
            }
        }


class AnswerAddRequest(BaseModel):
    text: str = Field(
        example="answer 1", description="text", min_length=1, max_length=50
    )
    correct: bool = Field(example=True, description="if answer is correct")
    question_id: int = Field(example=1, description="id of a question")

    class Config:
        json_schema_extra = {
            "example": {"text": "answer", "correct": True, "question_id": 1}
        }


class AnswerSubmitRequest(BaseModel):
    question_id: int = Field(description="id of a question")
    answer_ids: list[int] = Field(
        default_factory=list, min_length=0
    )  # AnswersList

    class Config:
        json_schema_extra = {"example": {"answer_ids": [1], "question_id": 1}}


class AnswerResponse(BaseModel):
    id: int = Field(description="id of an answer")
    text: str = Field(description="text")
    correct: bool = Field(description="if answer is correct")
    question_id: int = Field(description="id of a question")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "answer",
                "correct": True,
                "question_id": 1,
            }
        }


class TgPlayerIdRequest(BaseModel):
    tg_id: int = Field(description="tg_id")


class TgUpdateIdRequest(BaseModel):
    update_id: int = Field(description="update_id")

    class Config:
        json_schema_extra = {
            "example": {
                "update_id": 0,
            }
        }


class AnswerInResponse(BaseModel):
    id: int
    text: str
    correct: bool


class IsCorrectAnsResponse(BaseModel):
    correct: bool
    answers: list[AnswerInResponse]


class ScoreResponse(BaseModel):
    score: int


class QuestionIdResponse(BaseModel):
    question_id: int = Field(description="question_id")


class QuestionResponseInQuiz(BaseModel):
    id: int
    text: str
    active: int
    answers: list[AnswerInResponse]


class QuizResponse(RootModel):
    root: dict[int, QuestionResponseInQuiz]


class AnswerAddResponse(BaseModel):
    created: int = Field(description="id of created answer")

    class Config:
        json_schema_extra = {
            "example": {
                "created": 1,
            }
        }


class QuestionAddResponse(BaseModel):
    created: int = Field(description="id of created question")

    class Config:
        json_schema_extra = {
            "example": {
                "created": 1,
            }
        }
