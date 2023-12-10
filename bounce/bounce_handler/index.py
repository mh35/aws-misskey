"""."""
from __future__ import annotations

import json
import os
import time
from typing import TYPE_CHECKING, Literal, NotRequired, TypedDict

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import SNSEvent, event_source
from boto3 import Session

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


class _MailHeaderItem(TypedDict):
    """mail headers element."""

    name: str
    value: str


class _MailDict(TypedDict):
    """mail element."""

    timestamp: str
    messageId: str  # noqa: N815
    source: str
    sourceArn: str  # noqa: N815
    sendingAccountId: str  # noqa: N815
    destination: list[str]
    headersTruncated: bool  # noqa: N815
    headers: list[_MailHeaderItem]
    commonHeaders: dict[str, str | list[str]]  # noqa: N815
    tags: dict[str, list[str]]


class _BounceRecepientItem(TypedDict):
    """bounceRecipents item element."""

    emailAddress: str  # noqa: N815
    action: NotRequired[str]
    status: NotRequired[str]
    diagnosticCode: NotRequired[str]  # noqa: N815


class _BounceDict(TypedDict):
    """bounce element."""

    bounceType: Literal["Undetermined", "Permanent", "Transient"]  # noqa: N815
    bounceSubType: str  # noqa: N815
    bouncedRecipients: list[_BounceRecepientItem]  # noqa: N815
    timestamp: str
    feedbackId: str  # noqa: N815
    reportingMTA: NotRequired[str]  # noqa: N815


class _BounceRecord(TypedDict):
    """Bounce record."""

    eventType: Literal["Bounce"]  # noqa: N815
    mail: _MailDict
    bounce: _BounceDict


class _ComplaintRecepient(TypedDict):
    """complainedRecipients item element."""

    emailAddress: str  # noqa: N815


class _ComplaintDict(TypedDict):
    """complaint element."""

    complainedRecipients: list[_ComplaintRecepient]  # noqa: N815
    timestamp: str
    feedbackId: str  # noqa: N815
    complaintSubType: NotRequired[  # noqa: N815
        Literal["OnAccountSuppressionList"] | None
    ]
    userAgent: NotRequired[str]  # noqa: N815
    complaintFeedbackType: NotRequired[  # noqa: N815
        Literal["abuse", "auth-failure", "fraud", "not-spam", "other", "virus"]
    ]
    arrivalDate: NotRequired[str]  # noqa: N815


class _ComplaintRecord(TypedDict):
    """Complaint record."""

    eventType: Literal["Complaint"]  # noqa: N815
    mail: _MailDict
    complaint: _ComplaintDict


@logger.inject_lambda_context(log_event=True)
@event_source(data_class=SNSEvent)
def handler(event: SNSEvent, context: "LambdaContext") -> None:
    """Event handler."""
    sess = Session()
    table = sess.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    ct = int(time.time())
    for record in event.records:
        data: _BounceRecord | _ComplaintRecord = json.loads(record.sns.message)
        if data["eventType"] == "Bounce":
            if data["bounce"]["bounceType"] == "Permanent":
                with table.batch_writer() as batch:
                    for target in data["bounce"]["bouncedRecipients"]:
                        email = target["emailAddress"]
                        batch.put_item(
                            Item={
                                "email": email,
                                "category": "Bounce_Info",
                                "ttl": ct + 86400 * 7,
                                "reason": "Bounce",
                            }
                        )
                        batch.put_item(
                            Item={
                                "email": email,
                                "category": "Bounce_#" + str(ct),
                                "reason": "Bounce",
                            }
                        )
        elif data["eventType"] == "Complaint":
            if data["complaint"].get("complaintFeedbackType") not in [
                "not-spam",
                "virus",
            ]:
                with table.batch_writer() as batch:
                    for ctarget in data["complaint"]["complainedRecipients"]:
                        email = ctarget["emailAddress"]
                        batch.put_item(
                            Item={
                                "email": email,
                                "category": "Bounce_Info",
                                "ttl": ct + 86400 * 7,
                                "reason": "Complaint",
                            }
                        )
                        batch.put_item(
                            Item={
                                "email": email,
                                "category": "Bounce_#" + str(ct),
                                "reason": "Complaint",
                                "subType": data["complaint"].get(
                                    "complaintFeedbackType"
                                ),
                            }
                        )
