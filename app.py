from flask import Flask, render_template, request, jsonify
import together
import os

app = Flask(__name__)

# Đặt API Key từ biến môi trường
os.environ["TOGETHER_API_KEY"] = "5d014c761147a739fe900d696ae980ffe8e063fe2908632ef2fe3609b20dd35d"

# Dữ liệu nội bộ của công ty
company_data = {
    "giám đốc": "Tạ Quang Trực",
    "giờ làm việc": "Công ty làm việc từ 8h đến 17h.",
    "nghỉ phép": "Nhân viên được nghỉ 12 ngày phép/năm.",
    "hỗ trợ làm việc từ xa": "Có, công ty hỗ trợ tối đa 2 ngày/tuần."
}

def get_answer(question):
    """Xử lý câu hỏi và trả lời chỉ với thông tin cần thiết"""
    context = "\n".join([f"{key}: {value}" for key, value in company_data.items()])
    
    full_prompt = f"""Dưới đây là thông tin nội bộ của công ty:

{context}

Dựa vào dữ liệu trên, trả lời câu hỏi dưới đây một cách ngắn gọn, chính xác và không thêm thông tin thừa.

Câu hỏi: {question}
Trả lời:"""

    try:
        response = together.Complete.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            prompt=full_prompt,
            max_tokens=30,  # Giới hạn câu trả lời ngắn gọn
            stop=["Câu hỏi:", "Trả lời:"],  # Ngăn bot sinh câu hỏi tiếp theo
        )

        if isinstance(response, dict) and "choices" in response:
            return response["choices"][0]["text"].strip()

        return "Lỗi: Không thể lấy kết quả từ AI."
    except Exception as e:
        return f"Lỗi: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    response = get_answer(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
