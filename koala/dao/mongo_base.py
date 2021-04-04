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

from fastapi import HTTPException
from pymongo import ReturnDocument

from koala.db.mongodb import get_collection


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
        try:
            self.collection = get_collection(self.collection_name)
        except Exception as e:
            raise e

    async def insert_one(self, document: dict):
        try:
            result = await self.collection.insert_one(document)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Mongo base: Error while inserting document. Error: {e}")
            raise e

    async def find_one(
        self,
        finder: dict,
        projection: dict = None,
    ):
        try:
            result = await self.collection.find_one(
                filter=finder, projection=projection
            )
            return result
        except Exception as e:
            logging.error(f"Mongo base: Error while looking for a document. Error: {e}")
            raise e

    async def find(
        self,
        finder: dict,
        limit: int = None,
        sort: list = None,
        projection: [dict] = None,
        skip: int = None,
    ):
        try:
            if skip is None and limit is None:
                result = self.collection.find(
                    filter=finder,
                    projection=projection,
                    sort=sort,
                )
            elif skip is not None and limit is not None:
                result = self.collection.find(
                    filter=finder,
                    projection=projection,
                    sort=sort,
                    skip=skip,
                    limit=limit,
                )
            else:
                logging.error("Query not valid")
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while fetching all matching documents using find. Error: {e}"
            )
            raise e

    async def insert_many(self, document_list: list):
        try:
            result = await self.collection.insert_many(document_list, ordered=True)
            return result
        except Exception as e:
            raise e

    async def find_one_and_modify(
        self,
        finder: dict,
        update: dict,
        projection: [dict] = None,
        sort: list = None,
        upsert: bool = False,
        return_updated_document: bool = True,
    ):
        try:
            result = await self.collection.find_one_and_update(
                filter=finder,
                update=update,
                projection=projection,
                sort=sort,
                upsert=upsert,
                return_document=ReturnDocument.AFTER
                if return_updated_document
                else ReturnDocument.BEFORE,
            )
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while inserting/updating in collection. Error: {e}"
            )
            raise e

    async def find_one_and_replace(
        self,
        finder: dict,
        replacement: dict,
        projection: [dict] = None,
        sort: list = None,
        upsert: bool = False,
        return_updated_document: bool = True,
    ):
        try:
            result = await self.collection.find_one_and_replace(
                filter=finder,
                replacement=replacement,
                projection=projection,
                sort=sort,
                upsert=upsert,
                return_document=ReturnDocument.AFTER
                if return_updated_document
                else ReturnDocument.BEFORE,
            )
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while inserting/updating in collection. Error: {e}"
            )
            raise e

    async def update_one(
        self,
        finder: dict,
        update: dict,
        upsert: bool = False,
        bypass_document_validation: bool = False,
        array_filters: list = None,
    ):
        try:
            result = await self.collection.update_one(
                filter=finder,
                update=update,
                upsert=upsert,
                bypass_document_validation=bypass_document_validation,
                array_filters=array_filters,
            )
            return result
        except Exception as e:
            logging.error(
                f"Mongo base: Error while inserting/updating in collection. Error: {e}"
            )
            raise e
