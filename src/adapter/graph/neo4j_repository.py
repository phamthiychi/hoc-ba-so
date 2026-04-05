from typing import Any, Dict, List, Optional
from src.application.utils import Utils

utils = Utils()
class BaseNeo4jRepository:
    label: str = ""
    id_field: str = "id"
    allowed_fields: set = set()

    def __init__(self, manager):
        self.manager = manager

    def validate_field(self, field: str):
        if self.allowed_fields and field not in self.allowed_fields:
            return utils._log(f"{self.label} said: Invalid field {field}")

    def _record_to_dict(self, record, key: str = "n") -> Dict[str, Any]:
        node = record[key]
        return dict(node)

    def _relation_to_dict(self, record, rel_key: str = "r", from_key: str = "a", to_key: str = "b") -> Dict[str, Any]:
        rel = record[rel_key]
        from_node = record[from_key]
        to_node = record[to_key]

        return {
            "relation_type": rel.type,
            "relation_props": dict(rel),
            "from_node": dict(from_node),
            "to_node": dict(to_node),
        }

    # =========================
    # NODE CRUD
    # =========================
    def create(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.manager.execute_write(self._create, data)

    def get_by_id(self, value: Any) -> Optional[Dict[str, Any]]:
        return self.manager.execute_read(self._get_by_field, self.id_field, value)

    def update_by_id(self, value: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.manager.execute_write(self._update_by_id, value, data)

    def delete_by_id(self, value: Any) -> bool:
        return self.manager.execute_write(self._delete_by_id, value)

    def _create(self, tx, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self.get_by_id(data[self.id_field]):
            return ("Exist", data[self.id_field])
        query = f"""
        CREATE (n:{self.label})
        SET n = $props
        RETURN n
        """
        record = tx.run(query, props=data).single()
        return self._record_to_dict(record) if record else None

    def _get_by_field(self, tx, field: str, value: Any) -> Optional[Dict[str, Any]]:
        self.validate_field(field)

        query = f"""
        MATCH (n:{self.label})
        WHERE n.{field} = $value
        RETURN n
        LIMIT 1
        """
        record = tx.run(query, value=value).single()
        return self._record_to_dict(record) if record else None

    def _update_by_id(self, tx, value: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        query = f"""
        MATCH (n:{self.label})
        WHERE n.{self.id_field} = $id_value
        SET n += $props
        RETURN n
        """
        record = tx.run(query, id_value=value, props=data).single()
        return self._record_to_dict(record) if record else None

    def _delete_by_id(self, tx, value: Any) -> bool:
        query = f"""
        MATCH (n:{self.label})
        WHERE n.{self.id_field} = $id_value
        WITH n, COUNT(n) AS cnt
        DETACH DELETE n
        RETURN cnt > 0 AS deleted
        """
        record = tx.run(query, id_value=value).single()
        return record["deleted"] if record else False

    # =========================
    # RELATION CRUD
    # =========================

    def create_relationship(
        self,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        relation_props: Optional[Dict[str, Any]] = None,
        from_id_field: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        return self.manager.execute_write(
            self._create_relationship,
            from_value,
            to_label,
            to_id_field,
            to_value,
            relation_type,
            relation_props or {},
            from_id_field or self.id_field,
        )

    def update_relationship(
        self,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        relation_props: Dict[str, Any],
        from_id_field: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        return self.manager.execute_write(
            self._update_relationship,
            from_value,
            to_label,
            to_id_field,
            to_value,
            relation_type,
            relation_props,
            from_id_field or self.id_field,
        )

    def delete_relationship(
        self,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        from_id_field: Optional[str] = None,
    ) -> bool:
        return self.manager.execute_write(
            self._delete_relationship,
            from_value,
            to_label,
            to_id_field,
            to_value,
            relation_type,
            from_id_field or self.id_field,
        )

    def get_relationships(
        self,
        from_value: Any,
        to_label: Optional[str] = None,
        relation_type: Optional[str] = None,
        from_id_field: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        return self.manager.execute_read(
            self._get_relationships,
            from_value,
            to_label,
            relation_type,
            from_id_field or self.id_field,
        )

    def _create_relationship(
        self,
        tx,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        relation_props: Dict[str, Any],
        from_id_field: str,
    ) -> Optional[Dict[str, Any]]:
        if self.get_relationships(from_value, to_label, relation_type, from_id_field):
            return ("Exist")
        query = f"""
        MATCH (a:{self.label}), (b:{to_label})
        WHERE a.{from_id_field} = $from_value
          AND b.{to_id_field} = $to_value
        MERGE (a)-[r:{relation_type}]->(b)
        SET r += $relation_props
        RETURN a, r, b
        """
        record = tx.run(
            query,
            from_value=from_value,
            to_value=to_value,
            relation_props=relation_props,
        ).single()
        return self._relation_to_dict(record) if record else None

    def _update_relationship(
        self,
        tx,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        relation_props: Dict[str, Any],
        from_id_field: str,
    ) -> Optional[Dict[str, Any]]:
        query = f"""
        MATCH (a:{self.label})-[r:{relation_type}]->(b:{to_label})
        WHERE a.{from_id_field} = $from_value
          AND b.{to_id_field} = $to_value
        SET r += $relation_props
        RETURN a, r, b
        """
        record = tx.run(
            query,
            from_value=from_value,
            to_value=to_value,
            relation_props=relation_props,
        ).single()
        return self._relation_to_dict(record) if record else None

    def _delete_relationship(
        self,
        tx,
        from_value: Any,
        to_label: str,
        to_id_field: str,
        to_value: Any,
        relation_type: str,
        from_id_field: str,
    ) -> bool:
        query = f"""
        MATCH (a:{self.label})-[r:{relation_type}]->(b:{to_label})
        WHERE a.{from_id_field} = $from_value
          AND b.{to_id_field} = $to_value
        WITH r, COUNT(r) AS cnt
        DELETE r
        RETURN cnt > 0 AS deleted
        """
        record = tx.run(
            query,
            from_value=from_value,
            to_value=to_value,
        ).single()
        return record["deleted"] if record else False

    def _get_relationships(
        self,
        tx,
        from_value: Any,
        to_label: Optional[str],
        relation_type: Optional[str],
        from_id_field: str,
    ) -> List[Dict[str, Any]]:
        rel_part = f"[r:{relation_type}]" if relation_type else "[r]"
        to_label_part = f":{to_label}" if to_label else ""

        query = f"""
        MATCH (a:{self.label})-{rel_part}->(b{to_label_part})
        WHERE a.{from_id_field} = $from_value
        RETURN a, r, b
        """
        result = tx.run(query, from_value=from_value)
        records = list(result)
        if not records:
            return None
        return [self._relation_to_dict(record) for record in records]

class Neo4jThingRepository(BaseNeo4jRepository):
    label = "Thing"
    id_field = "code"
    allowed_fields = {"code", "name"}

    def __init__(self, manager):
        super().__init__(manager)
        self.create({
            "code": "thing",
            "name": "Thực thể"
        })

class Neo4jStudentQualityRepository(BaseNeo4jRepository):
    label = "StudentQuality"
    id_field = "code"
    allowed_fields = {"code", "name"}

    def __init__(self, manager):
        super().__init__(manager)
        self.create({
            "code": "student_quality",
            "name": "Phẩm chất chủ yếu của học sinh"
        })

class Neo4jStudentGeneralAbilitiesRepository(BaseNeo4jRepository):
    label = "StudentGeneralAbilities"
    id_field = "code"
    allowed_fields = {"code", "name"}

    def __init__(self, manager):
        super().__init__(manager)
        self.create({
            "code": "student_general_abilities",
            "name": "Năng lực chung của học sinh"
        })

class Neo4jStudentSpecialAbilitiesRepository(BaseNeo4jRepository):
    label = "StudentSpecialAbilities"
    id_field = "code"
    allowed_fields = {"code", "name"}

    def __init__(self, manager):
        super().__init__(manager)
        self.create({
            "code": "student_special_abilities",
            "name": "Năng lực đặc thù của học sinh"
        })

class Neo4jStudentRepository(BaseNeo4jRepository):
    label = "Student"
    id_field = "code"
    allowed_fields = {"code", "name", "car_id", "edu_id"}

class Neo4jStudentContactInfosRepository(BaseNeo4jRepository):
    label = "StudentContactInfos"
    id_field = "code"
    allowed_fields = {"code", "url"}

class Neo4jStudentSubjectAssessmentsRepository(BaseNeo4jRepository):
    label = "StudentSubjectAssessments"
    id_field = "code"
    allowed_fields = {"code", "url"}

