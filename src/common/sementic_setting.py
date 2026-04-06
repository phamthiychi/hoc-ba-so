import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    CONJUNCTION = [
        "trong trường hợp",
        "thế nhưng", "không những", "chẳng những", "bao nhiêu", "bấy nhiêu",
        "hay là", "cũng như", "thêm nữa", "tuy nhiên", "vậy mà", "thế nên",
        "do đó", "vì vậy", "bởi vậy", "bởi vì", "cho nên", "thành ra",
        "giá mà", "giả sử", "mặc dù", "trong khi", "trước khi", "sau khi",
        "giống như", "tựa như", "mà còn", "kể cả", "ngay cả",
        "vả lại", "huống chi", "miễn là", "chỉ cần", "thậm chí",
        "và", "hoặc", "nhưng", "song", "nên",
        "tuy", "dù", "dẫu", "thì"
]

settings = Settings()