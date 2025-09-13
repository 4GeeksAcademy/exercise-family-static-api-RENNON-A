"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # Internal list of members
        self._members = []

        # Seed data (el test espera que el primero sea "Tommy")
        self.add_member({
            "first_name": "Tommy",
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        self.add_member({
            "first_name": "Jane",
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        self.add_member({
            "first_name": "Jimmy",
            "age": 5,
            "lucky_numbers": [1]
        })

    def _generateId(self):
        # En un proyecto real usar UUID y chequear colisiones
        return randint(1, 99999999)

    def add_member(self, member: dict) -> dict:
        """
        Crea un miembro nuevo con last_name de la familia y un id si no viene.
        Campos esperados: first_name (str), age (int), lucky_numbers (list[int])
        """
        if not isinstance(member, dict):
            raise ValueError("member must be a dict")

        data = {
            "id": member.get("id") or self._generateId(),
            "first_name": member.get("first_name"),
            "last_name": self.last_name,  # siempre el apellido de la familia
            "age": member.get("age"),
            "lucky_numbers": member.get("lucky_numbers") if member.get("lucky_numbers") is not None else [],
        }

        # Validaciones básicas
        if not data["first_name"]:
            raise ValueError("first_name is required")
        if data["age"] is None:
            raise ValueError("age is required")
        if not isinstance(data["lucky_numbers"], list):
            raise ValueError("lucky_numbers must be a list")

        # Evitar IDs duplicados
        if any(m["id"] == data["id"] for m in self._members):
            raise ValueError("id already exists")

        self._members.append(data)
        return data

    def delete_member(self, id: int) -> bool:
        """
        Elimina un miembro por id. Devuelve True si lo eliminó, False si no existe.
        """
        for index, m in enumerate(self._members):
            if m["id"] == id:
                self._members.pop(index)
                return True
        return False

    def update_member(self, id: int, updates: dict):
        """
        Actualiza campos del miembro por id. Devuelve el miembro actualizado o None si no existe.
        Permitimos actualizar: first_name, age, lucky_numbers. (id y last_name no se tocan)
        """
        member = self.get_member(id)
        if member is None:
            return None

        if "first_name" in updates:
            if not updates["first_name"]:
                raise ValueError("first_name cannot be empty")
            member["first_name"] = updates["first_name"]

        if "age" in updates:
            if updates["age"] is None:
                raise ValueError("age cannot be None")
            member["age"] = updates["age"]

        if "lucky_numbers" in updates:
            if not isinstance(updates["lucky_numbers"], list):
                raise ValueError("lucky_numbers must be a list")
            member["lucky_numbers"] = updates["lucky_numbers"]

        return member

    def get_member(self, id: int):
        """
        Retorna el miembro por id o None si no existe.
        """
        for m in self._members:
            if m["id"] == id:
                return m
        return None

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

