import logging

from koala.config.collections import (
    BENEFITS,
    DOCUMENTS,
    GIG_TYPE,
    HIRING_TYPES,
    JOB_TYPES,
    LANGUAGES,
    OP_AREAS,
    OP_CITIES,
    QUALIFICATIONS,
    SKILLS,
    TAGS,
)
from koala.models.jobs_models.master import (
    BaseNameModel,
    GigTypeModel,
    JobMasterModel,
    LanguageBaseNameModel,
    OpAreaModel,
    OpCityModel,
    SocialTagsModel,
)

from .mongo_base import MongoBase


class MasterCollections:
    def __init__(self):
        self.collection = MongoBase()

    async def get_all_gig_types(self) -> GigTypeModel:
        try:
            self.collection(GIG_TYPE)
            result = await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
            logging.info(f"gig types fetched successfully")
            return GigTypeModel(gig_types=result)
        except Exception as e:
            logging.error(f"Error: fetching gig type {e}")
            raise e

    async def get_op_cities(self) -> OpCityModel:
        try:
            self.collection(OP_CITIES)
            result = await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
            logging.info(f"op cities fetched successfully")
            return OpCityModel(op_cities=result)
        except Exception as e:
            logging.error(f"Error: fetching fetching op cities {e}")
            raise e

    async def get_op_areas(self) -> OpAreaModel:
        try:
            self.collection(OP_AREAS)
            result = await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
            logging.info(f"op area fetched successfully")
            return OpAreaModel(op_areas=result)
        except Exception as e:
            logging.error(f"Error: fetching op areas {e}")
            raise e

    async def get_benefits(self):
        try:
            self.collection(BENEFITS)
            logging.info(f"fetching benefits...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching benefits {e}")
            raise e

    async def get_documents(self):
        try:
            self.collection(DOCUMENTS)
            logging.info(f"fetching documents...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching documents {e}")
            raise e

    async def get_hiring_types(self):
        try:
            self.collection(HIRING_TYPES)
            logging.info(f"fetching hiring types...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching hiring types {e}")
            raise e

    async def get_job_types(self):
        try:
            self.collection(JOB_TYPES)
            logging.info(f"fetching job types...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching job types {e}")
            raise e

    async def get_languages(self):
        try:
            self.collection(LANGUAGES)
            logging.info(f"fetching languages...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=LanguageBaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching languages {e}")
            raise e

    async def get_qualifications(self):
        try:
            self.collection(QUALIFICATIONS)
            logging.info(f"fetching qualifications...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching qualifications {e}")
            raise e

    async def get_skills(self):
        try:
            self.collection(SKILLS)
            logging.info(f"fetching skills...")
            return await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
        except Exception as e:
            logging.error(f"Error: fetching skills {e}")
            raise e

    async def get_job_master(self) -> JobMasterModel:
        try:
            benefits = await self.get_benefits()
            documents = await self.get_documents()
            hiring_types = await self.get_hiring_types()
            job_types = await self.get_job_types()
            languages = await self.get_languages()
            qualifications = await self.get_qualifications()
            skills = await self.get_skills()
            job_master = JobMasterModel(
                benefits=benefits,
                documents=documents,
                hiring_types=hiring_types,
                job_types=job_types,
                languages=languages,
                qualifications=qualifications,
                skills=skills,
            )

            logging.info(f"Error: Job master assembled successfully")
            return job_master
        except Exception as e:
            logging.error(f"Error: Assembling job master {e}")
            raise e

    async def get_social_tags(self):
        try:
            self.collection(TAGS)
            logging.info(f"fetching tags...")
            result = await self.collection.find(
                finder={},
                return_doc_id=True,
                extended_class_model=BaseNameModel,
                only_list_without_id=False,
            )
            return SocialTagsModel(tags=result)
        except Exception as e:
            logging.error(f"Error: fetching skills {e}")
            raise e
