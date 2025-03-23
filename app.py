from flask import Flask, render_template, request, jsonify
import together
import os

app = Flask(__name__)

# Đặt API Key từ biến môi trường
os.environ["TOGETHER_API_KEY"] = "5d014c761147a739fe900d696ae980ffe8e063fe2908632ef2fe3609b20dd35d"

MAXTOKEN = 500 # Liên quan tới số từ trả lời trong 1 câu hỏi 


# Dữ liệu nội bộ của công ty
company_data = {
    "hỗ trợ làm việc từ xa": "Có, công ty hỗ trợ tối đa 2 ngày/tuần.",
    "Portland hỗn hợp PCB40": {
        "Tiêu chuẩn sản phẩm": "TCVN 6260: 2009 (PCB40)",
        "Mô tả": "Xi măng Vicem Hà Tiên PCB40 là hỗn hợp bột mịn chứa nhiều thành phần khoáng chất. Được sản xuất bằng cách khai thác và tuyển chọn các khoáng vật từ đá vôi và đất sét chứa silica và alumina, nung ở nhiệt độ 1450°C, làm lạnh nhanh hình thành Clinker. Clinker sau đó được nghiền mịn với thạch cao và các phụ gia hoạt tính khác như Puzzolan, đá vôi,…",
        "Chỉ tiêu cơ lý (Physical characteristic)": {
            "Độ mịn (Fineness test)": {
                "Lượng sót sàng (Residue on sieve 0.09mm)": {
                    "Đơn vị": "%",
                    "Phương pháp thử": "TCVN 4030: 2003",
                    "Yêu cầu kỹ thuật": "≤ 10",
                    "Kết quả thử nghiệm": "0.2"
                },
                "Bề mặt riêng (Specific surface - Blain method)": {
                    "Đơn vị": "cm²/g",
                    "Yêu cầu kỹ thuật": "≥ 2800",
                    "Kết quả thử nghiệm": "4210"
                }
            },
            "Thời gian ninh kết (Time of setting)": {
                "Phương pháp thử": "TCVN 6017: 2015",
                "Bắt đầu (Initial set)": {
                     "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≥ 45",
                    "Kết quả thử nghiệm": "195"
                },
                "Kết thúc (Final set)": {
                    "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≤ 420",
                    "Kết quả thử nghiệm": "245"
                }
            },
            "Cường độ xi măng (Compressive strength)": {
                "Phương pháp thử": "TCVN 6016: 2011",
                "3 ngày (3 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 18",
                    "Kết quả thử nghiệm": "22.0"
                },
                "28 ngày (28 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 40",
                    "Kết quả thử nghiệm": "43.5"
                }
             },
            "Độ ổn định thể tích (Soundness - Lechatelier method)": {
                "Đơn vị": "mm",
                "Phương pháp thử": "TCVN 6017: 2015",
                "Yêu cầu kỹ thuật": "≤ 10",
                "Kết quả thử nghiệm": "0.5"
            }
        },
        "Chỉ tiêu thành phần hóa (Chemical characteristic)": {
            "Hàm lượng SO₃ (Sulfur trioxide content)": {
                "Đơn vị": "%",
                "Phương pháp thử": "TCVN 141: 2008",
                "Yêu cầu kỹ thuật": "≤ 3.5",
                "Kết quả thử nghiệm": "2.06"
            }
        }
    },
    "Xi măng Vicem Hà Tiên Xây Tô": {
        "Tiêu chuẩn sản phẩm": "TCVN 9202: 2012 (MC25)",
        "Mô tả": "Xi măng Vicem Hà Tiên Xây Tô là loại xi măng chuyên dụng cho công tác xây và tô hoàn thiện công trình, được sản xuất theo tiêu chuẩn TCVN 9202:2012. Sản phẩm có độ dẻo cao, chống thấm tốt, thời gian ninh kết hợp lý, và cường độ vượt trội, giúp tiết kiệm chi phí và đảm bảo thẩm mỹ cho công trình.",
        "Chỉ tiêu cơ lý (Physical characteristic)": {
            "Độ mịn (Fineness test)": {
                "Lượng sót sàng (Residue on sieve 0.09mm)": {
                    "Đơn vị": "%",
                    "Phương pháp thử": "TCVN 4030: 2003",
                    "Yêu cầu kỹ thuật": "≤ 12",
                    "Kết quả thử nghiệm": "0.35"
                }
            },
            "Thời gian ninh kết (Time of setting)": {
                "Phương pháp thử": "TCVN 6017: 1995, ISO 9597: 1989 (E)",
                "Bắt đầu (Initial set)": {
                    "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≥ 60",
                    "Kết quả thử nghiệm": "140"
                },
                "Kết thúc (Final set)": {
                    "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≤ 600",
                    "Kết quả thử nghiệm": "195"
                }
            },
            "Cường độ xi măng (Compressive strength)": {
                "Phương pháp thử": "TCVN 6016: 2011",
                "7 ngày (7 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 15",
                    "Kết quả thử nghiệm": "20.5"
                },
                "28 ngày (28 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 25",
                    "Kết quả thử nghiệm": "30.5"
                }
            },
            "Độ ổn định thể tích (Soundness - Lechatelier method)": {
                "Đơn vị": "mm",
                "Phương pháp thử": "TCVN 6017: 1995",
                "Yêu cầu kỹ thuật": "≤ 10",
                "Kết quả thử nghiệm": "0.60"
            }
        },
        "Chỉ tiêu thành phần hóa (Chemical characteristic)": {
            "Hàm lượng SO₃ (Sulfur trioxide content)": {
                "Đơn vị": "%",
                "Phương pháp thử": "TCVN 141: 2008",
                "Yêu cầu kỹ thuật": "≤ 3.0",
                "Kết quả thử nghiệm": "2.06"
            },
            "Hàm lượng clorua (Cl⁻) (Chloride content)": {
                "Đơn vị": "%",
                "Phương pháp thử": "TCVN 141: 2008",
                "Yêu cầu kỹ thuật": "≤ 0.1",
                "Kết quả thử nghiệm": "-"
            }
        }
    },
    "Xi măng Vicem Hà Tiên Đa Dụng": {
        "Tiêu chuẩn sản phẩm": "TCVN 6260: 2009",
        "Mô tả": "Xi măng Vicem Hà Tiên Đa Dụng là hỗn hợp nghiền mịn của clinker, thạch cao và các phụ gia khoáng hoạt tính khác như Puzzolan, đá vôi,… giúp cải thiện các tính chất vật lý của xi măng và bê tông như: rút ngắn thời gian đông kết, tạo cường độ cao, vữa dẻo. Sản phẩm được sử dụng cho nhiều mục đích như đổ bê tông móng, sàn, cột, đà, trộn vữa xây, vữa tô, ốp gạch đá hoặc cán nền, phù hợp cho các công trình dân dụng và dự án công nghiệp.",
        "Chỉ tiêu cơ lý (Physical characteristic)": {
            "Độ mịn (Fineness test)": {
                "Lượng sót sàng (Residue on sieve 0.09mm)": {
                    "Đơn vị": "%",
                    "Phương pháp thử": "TCVN 4030: 2003",
                    "Yêu cầu kỹ thuật": "≤ 10",
                    "Kết quả thử nghiệm": "5.2"
                },
                "Bề mặt riêng (Specific surface - Blain method)": {
                    "Đơn vị": "cm²/g",
                    "Phương pháp thử": "TCVN 4030: 2003",
                    "Yêu cầu kỹ thuật": "≥ 2800",
                    "Kết quả thử nghiệm": "4215"
                }
            },
            "Thời gian ninh kết (Time of setting)": {
                "Phương pháp thử": "TCVN 6017: 2015",
                "Bắt đầu (Initial set)": {
                    "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≥ 45",
                    "Kết quả thử nghiệm": "175"
                },
                "Kết thúc (Final set)": {
                    "Đơn vị": "phút (minute)",
                    "Yêu cầu kỹ thuật": "≤ 420",
                    "Kết quả thử nghiệm": "225"
                }
            },
            "Cường độ xi măng (Compressive strength)": {
                "Phương pháp thử": "TCVN 6016: 2011",
                "3 ngày (3 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 18",
                    "Kết quả thử nghiệm": "22.0"
                },
                "28 ngày (28 days)": {
                    "Đơn vị": "N/mm²",
                    "Yêu cầu kỹ thuật": "≥ 40",
                    "Kết quả thử nghiệm": "43.0"
                }
            },
            "Độ ổn định thể tích (Soundness - Lechatelier method)": {
                "Đơn vị": "mm",
                "Phương pháp thử": "TCVN 6017: 2015",
                "Yêu cầu kỹ thuật": "≤ 10",
                "Kết quả thử nghiệm": "0.5"
            }
        },
        "Chỉ tiêu thành phần hóa (Chemical characteristic)": {
            "Hàm lượng SO₃ (Sulfur trioxide content)": {
                "Đơn vị": "%",
                "Phương pháp thử": "TCVN 141: 2008",
                "Yêu cầu kỹ thuật": "≤ 3.5",
                "Kết quả thử nghiệm": "2.06"
            }
        }
    }
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
            max_tokens=MAXTOKEN,  # Giới hạn câu trả lời ngắn gọn
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
