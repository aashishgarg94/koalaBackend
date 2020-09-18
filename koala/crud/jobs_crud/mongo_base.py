# This is the base class for all mongo queries.
# It will act as a wrapper on pyMongo.motor queries
# Purpose:
# Single place to query from everywhere in application
# Dealing with mongoID will be easier
# Will remove overhead of checking/changing common implementation


# NOTE:
# Will continue adding queries here.
# There should not be any model check. Will try to keep it pure.
# There should not be any transformation in return.
# Will return the complete set, independent modules have to handle specific transformation

import logging
from typing import List

from fastapi import HTTPException
from koala.constants import REQUEST_LIMIT, REQUEST_SKIP_DEFAULT
from koala.db.mongodb import get_collection
from pymongo import ReturnDocument


# Keeping is static for exceptional cases where we might need to transform the data explicitly
def return_id_transformation(extended_class_model, result):
    try:
        logging.info(f"Post flight operations. Performing transformations now...")
        is_list_type = isinstance(result, list)
        if is_list_type:
            data_list = []
            for document in result:
                data = extended_class_model.from_mongo(data=document)
                data_list.append(data)
            logging.info(f"Transformation successfully completed ;)")
            return data_list
        else:
            data = extended_class_model.from_mongo(data=result) if result else None
            logging.info(f"Transformation successfully completed ;)")
            return data
    except Exception as e:
        raise e


class MongoBase:
    def __init__(self, collection_name: str = None):
        self.collection_name = collection_name

    def __call__(self, collection_name: str = None):
        if collection_name is not None:
            self.collection_name = collection_name

        # check if collection name still None
        if self.collection_name is None:
            raise HTTPException(
                status_code=500,
                detail=f"Mongo base: Not callable. DB collection is not passed.",
            )

        logging.info(
            f"Yay... Collection name OK :). Trying to connect to collection..."
        )
        try:
            self.collection = get_collection(self.collection_name)
            logging.info(f"Connected to collection. Will try to perform operations now")
        except Exception as e:
            raise e

    @staticmethod
    def pre_flight_check(return_doc_id=False, extended_class_model=None):
        if return_doc_id and extended_class_model is None:
            raise ValueError(
                f"return_doc_id set to True. extended_class_model is required now"
            )
        elif not return_doc_id and extended_class_model is not None:
            raise ValueError(f"api model is provided, please set return_doc_id to True")
        elif return_doc_id and extended_class_model is not None:
            logging.info(
                f"Transformation required, will be performed on data in post flight operations..."
            )
        else:
            logging.info(f"Transformation not required, will skip it...")

    async def insert_one(
        self, document: dict, return_doc_id=False, extended_class_model=None
    ):
        try:
            self.pre_flight_check(return_doc_id, extended_class_model)
        except Exception as e:
            raise e
        logging.info(f"Pre flight operations looks good ;)")
        try:
            result = await self.collection.insert_one(document)
            logging.info(
                f"Mongo base: Item Created. Checking if transformation required..."
            )
            return result.inserted_id
        except Exception as e:
            logging.error(
                f"Mongo base: Error while fetching one from collection. Error: {e}"
            )
            raise e

    async def find_one(
        self, finder: dict, return_doc_id=False, extended_class_model=None
    ):
        try:
            self.pre_flight_check(return_doc_id, extended_class_model)
        except Exception as e:
            raise e
        logging.info(f"Pre flight operations looks good ;)")
        try:
            result = await self.collection.find_one(finder)
            logging.info(
                f"Mongo base: Item fetched. Checking if transformation required..."
            )
            if return_doc_id:
                transformed_result = return_id_transformation(
                    extended_class_model=extended_class_model, result=result
                )
                return transformed_result
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while fetching one from collection. Error: {e}"
            )
            raise e

    async def find_one_and_modify(
        self,
        find: dict,
        update: dict,
        return_updated_document: bool = True,
        return_doc_id=False,
        extended_class_model=None,
        insert_if_not_found: bool = False,
        array_filters=None,
    ):
        try:
            self.pre_flight_check(return_doc_id, extended_class_model)
        except Exception as e:
            raise e
        logging.info(f"Pre flight operations looks good ;)")
        try:
            result = await self.collection.find_one_and_update(
                find,
                update,
                return_document=ReturnDocument.AFTER
                if return_updated_document
                else ReturnDocument.BEFORE,
                upsert=insert_if_not_found,
                array_filters=array_filters,
            )
            logging.info(
                f"Mongo base: Item updated. Checking if transformation required..."
            )
            if return_doc_id:
                transformed_result = return_id_transformation(
                    extended_class_model=extended_class_model, result=result
                )
                return transformed_result
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while updating one in collection. Error: {e}"
            )
            raise e

    async def find(
        self,
        finder: dict,
        projection: dict = None,
        return_doc_id=False,
        extended_class_model=None,
        skip: int = REQUEST_SKIP_DEFAULT,
        limit: int = REQUEST_LIMIT,
        only_list_without_id: bool = False,
    ):
        try:
            self.pre_flight_check(return_doc_id, extended_class_model)
            if only_list_without_id:
                logging.warning(
                    f"only_list_without_id is provided, return_doc_id and extended_class_model will be skipped"
                )
        except Exception as e:
            raise e
        logging.info(f"Pre flight operations looks good ;)")
        try:
            result = (
                self.collection.find(filter=finder, projection=projection)
                .skip(skip)
                .limit(limit)
            )
            logging.info(
                f"Mongo base: Item fetched. Checking if transformation required..."
            )
            result_list = []
            if only_list_without_id:
                for document in await result.to_list(length=limit):
                    result_list.append(document["name"])
            else:
                for document in await result.to_list(length=limit):
                    result_list.append(document)
                if return_doc_id:
                    transformed_result = return_id_transformation(
                        extended_class_model=extended_class_model, result=result_list
                    )
                    return transformed_result
            return result_list
        except Exception as e:
            logging.error(
                f"Mongo base: Error while fetching one from collection. Error: {e}"
            )
            raise e

    async def count(
        self, filter_condition: dict,
    ):
        try:
            logging.info(f"Mongo base: Fetching count...")
            return await self.collection.count_documents(filter=filter_condition)
        except Exception as e:
            logging.error(
                f"Mongo base: Error while counting from collection. Error: {e}"
            )
            raise e

    async def aggregate(self, condition: List):
        try:
            result = self.collection.aggregate(condition)
            for document in await result.to_list(length=10):
                logging.info(document)
        except Exception as e:
            logging.error(f"Mongo base: Error while aggregating. Error {e}")
            raise e
