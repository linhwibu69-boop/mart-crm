# Mart CRM — Quản lí khách mua hàng tại siêu thị

Ứng dụng web chạy thật: FastAPI + SQLAlchemy ORM + SQLite, giao diện HTML/CSS/JavaScript.
Không cần tài khoản GitHub để chạy cục bộ. Toàn bộ khách hàng, số điện thoại, email và giao dịch trong bản bàn giao là dữ liệu kiểm thử do chương trình và phiên thao tác trình duyệt tạo ra, không phải dữ liệu của siêu thị đang kinh doanh.

## Chạy trên Windows

1. Cài **Python 3.12 64 bit** từ https://www.python.org/downloads/ (nếu chưa có).
2. Giải nén đầy đủ thư mục `mart-crm`.
3. Chạy `start.bat`. Lần đầu cần Internet để cài các gói từ PyPI.
4. Mở http://127.0.0.1:8000. Giữ cửa sổ máy chủ mở khi dùng ứng dụng.
5. Nếu trình duyệt mở trước lúc máy chủ sẵn sàng, tải lại trang.

Tài khoản **chỉ dùng cho dữ liệu kiểm thử**:

| Tài khoản | Mật khẩu thực hành | Vai trò |
|---|---|---|
| admin | MartDemo!2026 | Quản trị |
| cashier | Cashier!2026 | Thu ngân |

Bản bàn giao có `data/mart.sqlite3` đã chứa giao dịch thật của phiên demo. Khi cơ sở dữ liệu đã có, chương trình seed không ghi đè. Không xóa file để khắc phục lỗi nếu cần giữ dữ liệu.

Linux/macOS: dùng Python 3.12 rồi chạy `bash start.sh`.

## Kiểm thử

Sau khi cài phụ thuộc:

```text
.venv\Scripts\python.exe run_tests.py
```

Trên Linux: `.venv/bin/python run_tests.py`.
Test tạo SQLite tạm riêng; không làm mất dữ liệu đang sử dụng. Kết quả JSON và văn bản được ghi trong `evidence/`. Bộ kiểm thử có 9 ca đơn vị và 39 ca API/tích hợp. Kết quả đã thực thi khi bàn giao: 48 ca đạt, 0 lỗi, 0 bỏ qua. `static/verification.html` là bản trình bày của lần chạy đã chụp, không tự cập nhật sau mỗi lần chạy test.

## Chức năng

- Đăng nhập, đăng xuất, phiên 8 giờ; vai trò admin/thu ngân.
- CRUD khách hàng, kiểm tra điện thoại trùng, tìm kiếm và lọc trạng thái.
- CRUD sản phẩm cho admin, giá VND nguyên và tồn kho không âm.
- Lập hóa đơn nhiều dòng; giá đọc từ CSDL; trừ kho và cộng/đổi điểm trong cùng transaction.
- Cứ 10.000 VND thực trả được 1 điểm (lấy phần nguyên); 1 điểm đổi 1.000 VND, tối đa 20% tiền hàng.
- Chống tạo trùng qua request_key + request_hash; khóa ghi SQLite bằng BEGIN IMMEDIATE.
- Admin hủy hóa đơn: hoàn kho, hoàn điểm đã đổi, thu hồi điểm đã tích. Không cho hủy nếu số dư điểm thành âm.
- Hạng dựa trên chi tiêu của hóa đơn chưa hủy: thành viên dưới 2 triệu, Bạc từ 2 triệu, Vàng từ 5 triệu VND.
- Chi tiết khách, sổ điểm, báo cáo doanh thu, xuất CSV và nhật ký thao tác.
- Không xóa khách/sản phẩm đã có hóa đơn; có thể ngừng hoạt động thay thế.

## Cấu trúc

- `app/controllers/`: tiếp nhận HTTP và phân quyền.
- `app/schemas.py`: DTO Pydantic, từ chối trường ngoài hợp đồng.
- `app/services/`: nghiệp vụ, transaction, tính tiền và điểm.
- `app/repositories/`: truy vấn đối tượng và dữ liệu tổng hợp.
- `app/models.py`: 8 lớp ORM, khóa ngoại, UNIQUE và CHECK.
- `app/database.py`: kết nối, Session, SQLite FK/WAL.
- `static/`: giao diện gọi API thật; không lưu hồ sơ trong localStorage.
- `test/`: unit test và API integration test.
- `docs/diagrams/`: sơ đồ PNG, SVG và mã nguồn DOT có thể sửa.
- `evidence/screenshots/`: ảnh gốc lấy từ trình duyệt đang chạy ứng dụng.
- `data/mart.sql`: xuất SQL của đúng CSDL bàn giao.
- `docs/git-history.txt` và `mart-crm-history.bundle`: lịch sử Git thật, tác giả Codex.
- `evidence/browser-session.json`: kết quả phiên ảnh ban đầu (10 hóa đơn).
- `evidence/recording-session.json`: mốc thời gian của video liên tục.
- `evidence/video-final-database.json`: kết quả sau phiên quay và đúng CSDL bàn giao: 11 hóa đơn, 9 PAID, 2 CANCELLED, 16 dòng sổ điểm, 14 audit; doanh thu 11.830.000 đồng, KH0009 có 33 điểm và tồn gạo 63.

Tài liệu API tại `/api/docs`; đặc tả OpenAPI gốc tại `/api/openapi.json`. Giao diện Swagger sử dụng CDN, cần Internet; API và giao diện CRM sau cài đặt hoạt động cục bộ.

## Giới hạn hiện tại

Đây là sản phẩm thực hành chạy cục bộ, chưa triển khai thành dịch vụ Internet. Chưa tích hợp thanh toán thật, hóa đơn điện tử, email, SMS, nhiều chi nhánh, trả hàng một phần, đổi mật khẩu hoặc quản trị tài khoản trong UI. SQLite phù hợp bản thực hành, chưa được đo tải lớn. Bộ test không phải chứng nhận đã tìm hết mọi lỗi.

Trước triển khai thật: thay toàn bộ tài khoản thực hành, cấu hình HTTPS và MART_SECURE_COOKIE=1, đánh giá lại chi phí scrypt (bản này n=16384,r=8,p=1), cơ chế giới hạn tần suất dùng chung, lưu trữ dự phòng, migration lược đồ, xử lý yêu cầu dữ liệu cá nhân và kiểm thử bảo mật độc lập. `.env` không được đưa vào Git. `start.bat` chỉ bind localhost.

## Repository và lịch sử Git

- Đề chỉ nhắc tên ảnh `Screenshot 2026-07-16 at 8.05.43 AM.png`, không có ảnh nhúng trong file. Chưa thể xác nhận khớp bố cục riêng của giảng viên.
- Repository: https://github.com/linhwibu69-boop/mart-crm
- Lịch sử được tạo trong quá trình hỗ trợ có tác giả **Codex**. Không mạo danh thành viên, không tạo lại ngày giờ cũ. Câu 10 về commit của từng sinh viên cần đóng góp thực tế của sinh viên.
- Chưa có danh sách họ tên, MSSV, đóng góp thực tế. Không gán tên hoặc phần trăm tự đặt.
- Video MP4 được ghi liên tục từ trình duyệt trong phiên thao tác thật, dài 79,56 giây khi phát chậm 0,5x, có chú thích. Chưa có URL chia sẻ trực tuyến; cần đăng bằng tài khoản nhóm và cấp quyền xem cho giảng viên.
- Chưa có hướng dẫn trình bày chính thức của trường trong file đề. Word theo bố cục nội dung tham khảo và yêu cầu riêng của người dùng, không khẳng định đã được nhà trường duyệt định dạng.

Lịch sử phát triển gốc được giữ trong `mart-crm-history.bundle`, kèm danh sách tại `docs/git-history.txt`. Lịch sử trên GitHub ghi nhận các lần đưa tệp dự án lên repository. Hai loại lịch sử phản ánh đúng thao tác đã thực hiện; không thay đổi tác giả của các commit gốc.

Khôi phục lịch sử gốc vào một thư mục riêng để xem:

```text
git clone mart-crm-history.bundle mart-crm-history
git -C mart-crm-history log --oneline --all
```
