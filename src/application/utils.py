import pandas as pd
import datetime

from typing import BinaryIO
from src.common.common_setting import settings

class Utils:
    def __init__(self):
        self.dif_log = settings.REPO_ROOT / "logs/debug.txt"

    def _log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.dif_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]: {message} \n")
        return None

    def verify(self, Value):
        return None if pd.isna(Value) else Value

    def extract_info_from_student_profile(self, file_xls: BinaryIO) -> dict:
        df =  pd.read_excel(file_xls)
        result =  []
        for _, row in df.iterrows():
            data =  {
                "class_name": self.verify(row.get("Mã lớp")),
                "name": self.verify(row.get("Họ tên")),
                "date_of_birth": pd.to_datetime(row.get("Ngày sinh"),
                                                errors = "coerce") \
                                .strftime("%Y-%m-%d") if self.verify(row.get("Ngày sinh")) else None,
                "gender": self.verify(row.get("Giới tính")),
                "ethnicity": self.verify(row.get("Dân tộc")),
                "nationality": self.verify(row.get("Quốc tịch")),
                "card_id": None if pd.isna(row.get("Số CCCD")) else str(row.get("Số CCCD")),
                "edu_id": None if pd.isna(row.get("Mã định danh Bộ GD&ĐT")) else str(row.get("Mã định danh Bộ GD&ĐT")),
                "status": self.verify(row.get("Trạng thái HS")),
                "phone": None if pd.isna(row.get("Số điện thoại liên hệ")) else f'0{str(row.get("Số điện thoại liên hệ"))}',
                "address": self.verify(row.get("Chỗ ở hiện nay chi tiết")),
                "father_name": self.verify(row.get("Họ tên cha")),
                "father_job": self.verify(row.get("Nghề nghiệp cha")),
                "father_card_id": None if pd.isna(row.get("Số CCCD/CMND/DDCN cha")) else str(row.get("Số CCCD/CMND/DDCN cha")).split(".")[0],
                "father_phone": None if pd.isna(row.get("Số điện thoại cha")) else f'0{str(row.get("Số điện thoại cha"))}'.split(".")[0],
                "mother_name": self.verify(row.get("Họ tên mẹ")),
                "mother_job": self.verify(row.get("Nghề nghiệp mẹ")),
                "mother_card_id": None if pd.isna(row.get("Số CCCD/CMND/DDCN mẹ")) else str(row.get("Số CCCD/CMND/DDCN mẹ")).split(".")[0],
                "mother_phone": None if pd.isna(row.get("Số điện thoại mẹ")) else f'0{str(row.get("Số điện thoại mẹ"))}'.split(".")[0],
                "guardian_name": self.verify(row.get("Họ tên người giám hộ")),
                "guardian_job": self.verify(row.get("Nghề nghiệp người giám hộ")),
                "guardian_card_id": None if pd.isna(row.get("Số CCCD/CMND/DDCN người giám hộ")) else str(row.get("Số CCCD/CMND/DDCN người giám hộ")).split(".")[0],
                "guardian_phone": None if pd.isna(row.get("Số điện thoại người giám hộ")) else f'0{str(row.get("Số điện thoại người giám hộ"))}'.split(".")[0],
                "place_of_birth": self.verify(row.get("Nơi sinh"))
            }
            if data:
                result.append(data)
        return result

    def flatten_props(self, data: dict, parent_key: str = "", sep: str = "_") -> dict:
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if v is None:
                continue  # ❌ bỏ None
            if isinstance(v, dict):
                items.extend(self.flatten_props(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)