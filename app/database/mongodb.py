import pymongo

from model.room import createRoomModel, updateRoomModel


class MongoDB:
    def __init__(self, host, port, user, password, auth_db, db, collection):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auth_db = auth_db
        self.db = db
        self.collection = collection
        self.connection = None

    def _connect(self):
        client = pymongo.MongoClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            authSource=self.auth_db,
            authMechanism="SCRAM-SHA-1",
        )
        db = client[self.db]
        self.connection = db[self.collection]

    def find(self, sort_by, order):
        mongo_results = self.connection.find({})
        if sort_by is not None and order is not None:
            mongo_results.sort(sort_by, self._get_sort_by(order))

        return list(mongo_results)

    def _get_sort_by(self, sort: str) -> int:
        return pymongo.DESCENDING if sort == "desc" else pymongo.ASCENDING

    def find_one(self, id):
        return self.connection.find_one({"_id": id})

    def create(self, room: createRoomModel):
        room_dict = room.dict(exclude_unset=True)

        insert_dict = {**room_dict, "_id": room_dict["room"]}

        inserted_result = self.connection.insert_one(insert_dict)
        room_id = str(inserted_result.inserted_id)

        return room_id

    def update(self, room_id, room: updateRoomModel):
        updated_result = self.connection.update_one(
            {"room": room_id}, {"$set": room.dict(exclude_unset=True)}
        )
        return [room_id, updated_result.modified_count]

    def delete(self, room_id):
        deleted_result = self.connection.delete_one({"room": room_id})
        return [room_id, deleted_result.deleted_count]
