from flask import Flask, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def form():
    return '''
    <html>
    <head><title>Состав преступления</title></head>
    <body>
        <h2>Форма: Ввод данных о преступлении</h2>
        <form action="/generate" method="post">
            <label>Объект преступления:</label><br>
            <input type="text" name="object"><br><br>

            <label>Деяние:</label><br>
            <input type="text" name="act"><br><br>

            <label>Последствия:</label><br>
            <input type="text" name="consequence"><br><br>

            <label>Причинно-следственная связь:</label><br>
            <input type="text" name="causal"><br><br>

            <label>Факультативные признаки:</label><br>
            <input type="text" name="optional"><br><br>

            <label>Субъект преступления:</label><br>
            <input type="text" name="subject"><br><br>

            <label>Возраст субъекта:</label><br>
            <input type="number" name="age"><br><br>

            <label>Вменяемость:</label><br>
            <select name="sanity">
                <option value="вменяем">вменяем</option>
                <option value="невменяем">невменяем</option>
            </select><br><br>

            <label>Форма вины:</label><br>
            <select name="guilt">
                <option value="прямой умысел">прямой умысел</option>
                <option value="косвенный умысел">косвенный умысел</option>
                <option value="неосторожность">неосторожность</option>
            </select><br><br>

            <label>Мотив:</label><br>
            <input type="text" name="motive"><br><br>

            <label>Цель:</label><br>
            <input type="text" name="goal"><br><br>

            <label>Предполагаемая статья:</label><br>
            <input type="text" name="article"><br><br>

            <input type="submit" value="Сформировать PDF-оглашение">
        </form>
    </body>
    </html>
    '''

@app.route('/generate', methods=['POST'])
def generate():
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    date = datetime.now().strftime("%d.%m.%Y")

    data = {
        'object': request.form.get('object'),
        'act': request.form.get('act'),
        'consequence': request.form.get('consequence'),
        'causal': request.form.get('causal'),
        'optional': request.form.get('optional'),
        'subject': request.form.get('subject'),
        'age': request.form.get('age'),
        'sanity': request.form.get('sanity'),
        'guilt': request.form.get('guilt'),
        'motive': request.form.get('motive'),
        'goal': request.form.get('goal'),
        'article': request.form.get('article')
    }

    y = 800
    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Оглашение по делу от {date}")
    y -= 40

    text = f"На основании представленных данных установлено, что объектом преступного посягательства являются {data['object']}. " \
           f"Объективная сторона преступления выражается в следующем деянии: {data['act']}, повлекшем последствия в виде {data['consequence']}. " \
           f"Между деянием и наступившими последствиями имеется причинно-следственная связь: {data['causal']}. " \
           f"Дополнительно установлены следующие факультативные признаки: {data['optional']}. " \
           f"Субъектом преступления является {data['subject']}, возраст {data['age']}, {data['sanity']}. " \
           f"Субъективная сторона выражается в форме вины — {data['guilt']}, при наличии мотива: {data['motive']} и цели: {data['goal']}. " \
           f"Данные обстоятельства позволяют квалифицировать содеянное по статье {data['article']}."

    for line in text.split(". "):
        p.drawString(50, y, line.strip() + ("." if not line.strip().endswith(".") else ""))
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="oglashenie_prestupleniya.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
