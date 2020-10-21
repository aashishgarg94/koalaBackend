# function getSequenceNextValue(seqName) {
#   var seqDoc = db.student.findAndModify({
#     query: { _id: seqName },
#     update: { $inc: { seqValue: 1 } },
#     new: true
#   });
#
#   return seqDoc.seqValue;
# }
import logging

from koala.models.jobs_models.master import GlobalSequenceIn
from pymongo import ReturnDocument

from ..config.collections import SEQUENCE
from ..db.mongodb import db

# TODO: Do I need to add decrement also for failed cases ???


async def get_seq_next_value(collection_name: GlobalSequenceIn):
    seq_collection = db.client["koala-backend"][SEQUENCE]
    result = await seq_collection.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    logging.info(result.get("seq"))
    return result.get("seq")
