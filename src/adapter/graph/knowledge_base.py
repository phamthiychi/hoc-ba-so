class StudentAssessments():
    def __init__(self):
        self.define = {
            "Phẩm chất chủ yếu": {
                "Yêu nước": [
                    "Yêu thiên nhiên và có những việc làm thiết thực bảo vệ thiên nhiên.",
                    "Yêu quê hương, yêu Tổ quốc, tôn trọng các biểu trưng của đất nước.",
                    "Kính trọng, biết ơn người lao động, người có công với quê hương, đất nước; tham gia các hoạt động đền ơn, đáp nghĩa đối với những người có công với quê hương, đất nước."
                ],
                "Nhân ái": [
                    "Yêu thương, quan tâm, chăm sóc người thân trong gia đình.",
                    "Yêu quý bạn bè, thầy cô; quan tâm, động viên, khích lệ bạn bè.",
                    "Tôn trọng người lớn tuổi; giúp đỡ người già, người ốm yếu, người khuyết tật; nhường nhịn và giúp đỡ em nhỏ.",
                    "Biết chia sẻ với những bạn có hoàn cảnh khó khăn, các bạn ở vùng sâu, vùng xa, người khuyết tật và đồng bào bị ảnh hưởng của thiên tai.",
                    "Tôn trọng sự khác biệt của bạn bè trong lớp về cách ăn mặc, tính nết và hoàn cảnh gia đình.",
                    "Không phân biệt đối xử, chia rẽ các bạn.","Sẵn sàng tha thứ cho những hành vi có lỗi của bạn."
                ],
                "Chăm chỉ": [
                    "Đi học đầy đủ, đúng giờ.",
                    "Thường xuyên hoàn thành nhiệm vụ học tập.",
                    "Ham học hỏi, thích đọc sách để mở rộng hiểu biết.",
                    "Có ý thức vận dụng kiến thức, kĩ năng học được ở nhà trường vào đời sống hằng ngày.",
                    " Thường xuyên tham gia các công việc của gia đình vừa sức với bản thân.",
                    "Thường xuyên tham gia các công việc của trường lớp, cộng đồng vừa sức với bản thân."
                ],
                "Trung thực": [
                    "Trung thực, thật thà, ngay thẳng trong học tập, lao động và sinh hoạt hằng ngày; mạnh dạn nói lên ý kiến của mình.",
                    "Luôn giữ lời hứa; mạnh dạn nhận lỗi, sửa lỗi và bảo vệ cái đúng, cái tốt.",
                    "Không tự tiện lấy đồ vật, tiền bạc của người thân, bạn bè, thầy cô và những người khác.",
                    "Không đồng tình với các hành vi thiếu trung thực trong học tập và trong cuộc sống."
                ],
                "Trách nhiệm": [
                    "Có ý thức giữ gìn vệ sinh, rèn luyện thân thể, chăm sóc sức khoẻ.",
                    "Có ý thức sinh hoạt nền nếp.",
                    "Có ý thức bảo quản, giữ gìn đồ dùng cá nhân và gia đình.",
                    "Không bỏ thừa đồ ăn, thức uống; có ý thức tiết kiệm tiền bạc, điện nước trong gia đình.",
                    "Tự giác thực hiện nghiêm túc nội quy của nhà trường và các quy định, quy ước của tập thể; giữ vệ sinh chung; bảo vệ của công.",
                    "Không gây mất trật tự, cãi nhau, đánh nhau.",
                    "Nhắc nhở bạn bè chấp hành nội quy trường lớp; nhắc nhở người thân chấp hành các quy định, quy ước nơi công cộng.",
                    "Có trách nhiệm với công việc được giao ở trường, ở lớp.",
                    "Tích cực tham gia các hoạt động tập thể, hoạt động xã hội phù hợp với lứa tuổi.",
                    "Có ý thức chăm sóc, bảo vệ cây xanh và các con vật có ích.",
                    "Có ý thức giữ vệ sinh môi trường, không xả rác bừa bãi.",
                    "Không đồng tình với những hành vi xâm hại thiên nhiên."
                ]
            },
            "Năng lực chung": {
                "Tự chủ và tự học": [
                    "Tự làm được những việc của mình ở nhà và ở trường theo sự phân công, hướng dẫn.",
                    "Có ý thức về quyền và mong muốn của bản thân; bước đầu biết cách trình bày và thực hiện một số quyền lợi và nhu cầu chính đáng.",
                    "Nhận biết và bày tỏ được tình cảm, cảm xúc của bản thân; biết chia sẻ tình cảm, cảm xúc của bản thân với người khác.",
                    "Hoà nhã với mọi người; không nói hoặc làm những điều xúc phạm người khác.",
                    "Thực hiện đúng kế hoạch học tập, lao động; không mải chơi, làm ảnh hưởng đến việc học và các việc khác.",
                    "Tìm được những cách giải quyết khác nhau cho cùng một vấn đề.",
                    "Thực hiện được các nhiệm vụ khác nhau với những yêu cầu khác nhau.",
                    "Bộc lộ được sở thích, khả năng của bản thân.",
                    "Biết tên, hoạt động chính và vai trò của một số nghề nghiệp; liên hệ được những hiểu biết đó với nghề nghiệp của người thân trong gia đình.",
                    "Có ý thức tổng kết và trình bày được những điều đã học.",
                    "Nhận ra và sửa chữa sai sót trong bài kiểm tra qua lời nhận xét của thầy cô.",
                    "Có ý thức học hỏi thầy cô, bạn bè và người khác để củng cố và mở rộng hiểu biết.",
                    "Có ý thức học tập và làm theo những gương người tốt."
                ],
                "Giao tiếp và hợp tác": [
                    "Nhận ra được ý nghĩa của giao tiếp trong việc đáp ứng các nhu cầu của bản thân.",
                    "Tiếp nhận được những văn bản về đời sống, tự nhiên và xã hội có sử dụng ngôn ngữ kết hợp với hình ảnh như truyện tranh, bài viết đơn giản.",
                    "Bước đầu biết sử dụng ngôn ngữ kết hợp với hình ảnh, cử chỉ để trình bày thông tin và ý tưởng.",
                    "Tập trung chú ý khi giao tiếp; nhận ra được thái độ của đối tượng giao tiếp.",
                    "Biết cách kết bạn và giữ gìn tình bạn.",
                    "Nhận ra được những bất đồng, xích mích giữa bản thân với bạn hoặc giữa các bạn với nhau; biết nhường bạn hoặc thuyết phục bạn.",
                    "Có thói quen trao đổi, giúp đỡ nhau trong học tập; biết cùng nhau hoàn thành nhiệm vụ học tập theo sự hướng dẫn của thầy cô.",
                    "Hiểu được nhiệm vụ của nhóm và trách nhiệm, hoạt động của bản thân trong nhóm sau khi được hướng dẫn, phân công.",
                    "Nhận biết được một số đặc điểm nổi bật của các thành viên trong nhóm để đề xuất phương án phân công công việc phù hợp.",
                    "Biết cố gắng hoàn thành phần việc mình được phân công và chia sẻ giúp đỡ thành viên khác cùng hoàn thành việc được phân công.",
                    "Báo cáo được kết quả thực hiện nhiệm vụ của cả nhóm; tự nhận xét được ưu điểm, thiếu sót của bản thân theo hướng dẫn của thầy cô.",
                    "Có hiểu biết ban đầu về một số nước trong khu vực và trên thế giới.",
                    "Biết tham gia một số hoạt động hội nhập quốc tế theo hướng dẫn của nhà trường."
                ],
                "Giải quyết vấn đề và sáng tạo": [
                    "Biết xác định và làm rõ thông tin, ý tưởng mới đối với bản thân từ các nguồn tài liệu cho sẵn theo hướng dẫn.",
                    "Biết thu nhận thông tin từ tình huống, nhận ra những vấn đề đơn giản và đặt được câu hỏi.",
                    "Dựa trên hiểu biết đã có, biết hình thành ý tưởng mới đối với bản thân và dự đoán được kết quả khi thực hiện.",
                    "Dựa trên hiểu biết đã có, biết hình thành ý tưởng mới đối với bản thân và dự đoán được kết quả khi thực hiện.",
                    "Xác định được nội dung chính và cách thức hoạt động để đạt mục tiêu đặt ra theo hướng dẫn.",
                    "Nhận xét được ý nghĩa của các hoạt động.",
                    "Nêu được thắc mắc về sự vật, hiện tượng xung quanh; không e ngại nêu ý kiến cá nhân trước các thông tin khác nhau về sự vật, hiện tượng; sẵn sàng thay đổi khi nhận ra sai sót."
                ]
            },
            "Năng lực đặc thù":{
                "Ngôn ngữ":[
                    "Có năng lực sử dụng tiếng Việt và năng lực sử dụng ngoại ngữ.",
                    "Có kỹ năng nghe, nói, đọc, viết tốt.",
                    "Có am hiểu môn Ngữ văn, môn Ngoại ngữ"
                ],
                "Tính toán": [
                    "Nhận thức kiến thức toán học;",
                    "Tư duy toán học, thực hiện tính đúng",
                    "Vận dụng kiến thức, kĩ năng tính toán đã học",
                    "Năng lực tính toán được hình thành, phát triển ở nhiều môn học",
                    "Có năng lực toán học, được hình thành và phát triển chủ yếu ở môn Toán."
                ],
                "Khoa học":[
                    "Nhận thức khoa học;",
                    "Tìm hiểu tự nhiên, tìm hiểu xã hội;",
                    "Vận dụng kiến thức, kĩ năng khoa học đã học",
                    "Năng lực khoa học được hình thành, phát triển ở nhiều môn học,"
                    "Có am hiểu về các môn học: Tự nhiên và Xã hội, Khoa học, Lịch sử và Địa lí."
                ],
                "Thẩm mĩ":[
                    "Có  năng lực âm nhạc, năng lực mĩ thuật, năng lực văn học",
                    "Nhận thức các yếu tố thẩm mĩ, yêu cái đẹp",
                    "Phân tích, đánh giá các yếu tố thẩm mĩ",
                    "Tái hiện, sáng tạo và ứng dụng các yếu tố thẩm mĩ."
                    "Có am hiểu về các môn Âm nhạc, Mĩ thuật, Ngữ văn"
                ],
                "Thể chất": [
                    "Chăm sóc sức khỏe;",
                    "Vận động cơ bản;",
                    "Hoạt động thể dục thể thao"
                ]
            }
        }

class KnowledgeBase:
    def __init__(self):
        self.student_assessments = StudentAssessments()