from flask import Flask, render_template, request, redirect, url_for, send_file
import plotly.express as px
import pandas as pd
import json

app = Flask(__name__)
tasks = []  # Lista para armazenar as tarefas temporariamente

# Função para carregar tarefas do arquivo JSON
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função para salvar tarefas no arquivo JSON
def save_tasks():
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, default=str)

# Carregar as tarefas no início
tasks = load_tasks()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        task_name = request.form.get('task')
        start_date = pd.to_datetime(request.form.get('start_date'), errors='coerce')
        duration = int(request.form.get('duration'))

        if task_id:
            for task in tasks:
                if task['ID'] == int(task_id):
                    task['Task'] = task_name
                    task['Start Date'] = start_date
                    task['Duration'] = duration
                    break
        else:
            task_id = len(tasks) + 1
            tasks.append({
                'ID': task_id,
                'Task': task_name,
                'Start Date': start_date,
                'Duration': duration
            })

        save_tasks()
        return redirect(url_for('index'))
    
    formatted_tasks = []
    for task in tasks:
        formatted_task = task.copy()
        start_date = pd.to_datetime(task['Start Date'], errors='coerce')
        if pd.notna(start_date):
            formatted_task['Start Date'] = start_date.strftime('%Y-%m-%d')
        else:
            formatted_task['Start Date'] = ''
        formatted_tasks.append(formatted_task)

    return render_template('index.html', tasks=formatted_tasks)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = next((task for task in tasks if task['ID'] == task_id), None)
    if request.method == 'POST':
        task_name = request.form.get('task')
        start_date = pd.to_datetime(request.form.get('start_date'), errors='coerce')
        duration = int(request.form.get('duration'))
        
        if task:
            task['Task'] = task_name
            task['Start Date'] = start_date
            task['Duration'] = duration
        
        save_tasks()
        return redirect(url_for('index'))

    if task:
        start_date = pd.to_datetime(task['Start Date'], errors='coerce')
        if pd.notna(start_date):
            task['Start Date'] = start_date.strftime('%Y-%m-%d')
        else:
            task['Start Date'] = ''

    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task['ID'] != task_id]
    save_tasks()
    return redirect(url_for('index'))

@app.route('/gantt')
def gantt_chart():
    df = pd.DataFrame(tasks)
    if not df.empty:
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
        df = df.dropna(subset=['Start Date'])
        
        # Ordena pelo início das tarefas
        df = df.sort_values(by=['Start Date', 'Duration'])
        
        # Calcula a data de término com base no início e duração
        df['Finish Date'] = df['Start Date'] + pd.to_timedelta(df['Duration'], unit='D')

        # Ordena as tarefas de cima para baixo pela data de início
        ordered_tasks = df['Task'][::-1].tolist()  # Reverter a ordem para cima para baixo

        # Cria o gráfico de Gantt com Plotly
        fig = px.timeline(df, x_start='Start Date', x_end='Finish Date', y='Task', title='Diagrama de Gantt')
        
        # Configuração para exibir as tarefas de cima para baixo em ordem cronológica
        fig.update_yaxes(categoryorder='array', categoryarray=ordered_tasks)
        fig.update_layout(xaxis_title='Data', yaxis_title='Tarefa', height=300 + (len(df) * 20))
        
        gantt_html = fig.to_html(full_html=False)
    else:
        gantt_html = "<p>Nenhuma tarefa adicionada ainda.</p>"
    
    return render_template('gantt.html', gantt_html=gantt_html)

@app.route('/download-task')
def download_task():
    return send_file('tasks.json', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

