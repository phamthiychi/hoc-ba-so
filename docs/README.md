# Description
- `src/model/`: Định nghĩa cấu trúc dữ liệu và các thực thể trong hệ thống Học bạ số. Đây là nơi mô tả “Hệ thống có những gì”. Ví dụ: Student, Subject
- `src/interface/`: Định nghĩa các tương tác (thêm, xóa, sửa) giữa hệ thống (application) với các thành phần khác (adapter).
- `src/application`: Chứa logic xử lý nghiệp vụ chính của hệ thống.
- `src/adapter`: Chứa phần kết nối hệ thống với các thành phần ngoài hệ thống (framework, database, api, ...).

# Setup env
- Require python version `> 3.11.9`. Check with `python --version`
- Open command port, run a command `python -m venv .venv` to create virtual environment
- Run a command `.venv\Scripts\activate.bat` to active the virtual environment
- Upgrade pip `python -m pip install --upgrade pip`
- Install the packages with `python -m pip install -r requirements.txt`

# Run
- uvicorn src.adapter.api.main:app --host 0.0.0.0 --port 8000 --reload

- `http://127.0.0.1:8000/docs` to using API

# Test with postman
- Dowload postman at: `https://www.postman.com/downloads/` and sign in with Google account.
- Go to `Workspace > My workspace > Collections`
- Import file from `\common\postman\hocbaso.postman_collection` in repo project.
- Have fun !!!!

# Kill fastapi process:
- netstat -ano | findstr :8000
# -> (TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       17232 (&PID))
- taskkill /PID  &PID /F
