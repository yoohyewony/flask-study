from flask import Flask, render_template
import subprocess

app = Flask(__name__)

def get_gpu_info():
    try:
        # nvidia-smi 실행 및 결과 파싱
        nvidia_smi_output = subprocess.check_output(["nvidia-smi", "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu", "--format=csv,noheader,nounits"], encoding='utf-8')

        # 각 줄을 리스트로 변환
        gpu_info_lines = nvidia_smi_output.strip().split('\n')
        gpu_data = []

        # 각 GPU 정보를 딕셔너리 형태로 저장
        for line in gpu_info_lines:
            fields = line.split(', ')
            gpu_data.append({
                'id': fields[0],
                'name': fields[1],
                'memory_total': f"{fields[2]} MB",
                'memory_used': f"{fields[3]} MB",    # 사용 중 메모리
                'memory_free': f"{fields[4]} MB",    # 남은 메모리
                'utilization': f"{fields[5]}%",      # 사용률
                'temperature': f"{fields[6]} °C"     # 온도
            })

        return gpu_data
    except Exception as e:
        return [{"id": "N/A", "name": "NVIDIA-SMI Error", "memory_total": "N/A", "memory_used": "N/A", "memory_free": "N/A", "utilization": "N/A", "temperature": "N/A"}]
    
@app.route('/')
def home():
    gpu_data = get_gpu_info()
    return render_template('index.html', gpu_data=gpu_data)

if __name__ == '__main__':
    app.run(debug=True)