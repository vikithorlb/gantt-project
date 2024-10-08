from flask import Flask, render_template, request, redirect, url_for
import plotly.express as px
import pandas as pd

app = Flask(__name__)
tasks = []  # Lista para armazenar as tarefas temporariamente

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_id = request.form.get('task_id')
        task_name = request.form.get('task')
        start_date = pd.to_datetime(request.form.get('start_date'))
        duration = int(request.form.get('duration'))

        if task_id:
            for task in tasks:
                if task['ID'] == int(task_id):
                    task['Task'] = task_name
                    task['Start Date'] = start_date  # Mantém como datetime
                    task['Duration'] = duration
                    break
        else:
            task_id = len(tasks) + 1
            tasks.append({
                'ID': task_id,
                'Task': task_name,
                'Start Date': start_date,  # Mantém como datetime
                'Duration': duration
            })

        return redirect(url_for('index'))
    
    # Formatar a data como string antes de passar para o template
    formatted_tasks = []
    for task in tasks:
        formatted_task = task.copy()
        formatted_task['Start Date'] = task['Start Date'].strftime('%Y-%m-%d')  # Formatar a data como string
        formatted_tasks.append(formatted_task)

    return render_template('index.html', tasks=formatted_tasks)

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    task = next((task for task in tasks if task['ID'] == task_id), None)
    if request.method == 'POST':
        task_name = request.form.get('task')
        start_date = pd.to_datetime(request.form.get('start_date'))
        duration = int(request.form.get('duration'))
        
        if task:
            task['Task'] = task_name
            task['Start Date'] = start_date  # Mantém como datetime
            task['Duration'] = duration
        
        return redirect(url_for('index'))

    # Formatar a data como string para exibição no formulário
    if task:
        task['Start Date'] = task['Start Date'].strftime('%Y-%m-%d')  # Formatar a data como string para o template

    return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete(task_id):
    global tasks
    tasks = [task for task in tasks if task['ID'] != task_id]
    return redirect(url_for('index'))

@app.route('/gantt')
def gantt_chart():
    df = pd.DataFrame(tasks)
    if not df.empty:
        df['Finish Date'] = df['Start Date'] + pd.to_timedelta(df['Duration'], unit='D')

        fig = px.timeline(df, x_start='Start Date', x_end='Finish Date', y='Task', title='Diagrama de Gantt')
        fig.update_layout(xaxis_title='Data', yaxis_title='Tarefa')
        gantt_html = fig.to_html(full_html=False)
    else:
        gantt_html = "<p>Nenhuma tarefa adicionada ainda.</p>"
    
    return render_template('gantt.html', gantt_html=gantt_html)

if __name__ == '__main__':
    app.run(debug=True)

