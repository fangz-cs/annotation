import json
import os

def create_pro_annotation_tool():
    """
    生成一个具有专业字体、支持多次标注且包含删除功能的静态网站工具。
    """
    project_dir = './'
    jsonl_file_path = '/home/fangz/project/require/test6_20.jsonl'

    # 定义歧义类型
    ambiguity_keywords = [
        "Lexical Ambiguity (词义歧义)", "Syntactic Ambiguity (语法歧义)",
        "Semantic Ambiguity (语义歧义)", "Scope Ambiguity (范围歧义)",
        "Anaphora Ambiguity (指代不清)", "Incomplete Information (信息不全)",
        "Implied Context (隐含上下文)", "Contradictory Statements (描述矛盾)",
        "Vague Quantification (量化模糊)", "Unclear Constraints (约束不明)",
        "Formatting Issues (格式问题)", "Example-Problem Mismatch (示例与题目不符)",
        "Edge Case Unspecified (边界情况未定义)", "Typographical Error (拼写或打字错误)",
        "Cultural/Domain-specific Jargon (文化/领域术语)"
    ]
    
    # 读取原始问题数据
    try:
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        all_questions = [json.loads(line) for line in lines]
        questions_json_string = json.dumps(all_questions, indent=2)
    except FileNotFoundError:
        print(f"错误：找不到文件 '{jsonl_file_path}'。")
        return

    # --- HTML 模板 ---
    checkboxes_html = "\\n".join([f'            <label><input type="checkbox" name="ambiguity" value="{kw}"> {kw}</label>' for kw in ambiguity_keywords])

    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>专业版问题标注工具</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="main-container">
        <aside class="left-panel">
            <h2>已有标注</h2>
            <div id="annotation-list" class="form-section"></div>
            <button id="new-annotation-btn">新建标注</button>
            <hr>
            <h2>歧义类型</h2>
            <div id="keywords-form" class="form-section">{checkboxes_html}</div>
            <h2>当前问题信息</h2>
            <div id="info-box" class="form-section"></div>
        </aside>

        <main class="main-content">
            <header>
                <h1 id="question-title"></h1>
                <p id="problem-counter"></p>
            </header>
            <div id="question-content" class="content-box"></div>
        </main>

        <aside class="right-panel">
            <h2>标注输入</h2>
            <div class="form-section">
                <label for="modified-content">修改后的题面:</label>
                <textarea id="modified-content" rows="10"></textarea>
            </div>
            <h3>问答对 (Q&A Pairs)</h3>
            <div id="qa-pairs">
                <div class="qa-pair">
                    <label for="question1">Question 1:</label> <textarea id="question1" rows="3"></textarea>
                    <label for="answer1">Answer 1:</label> <textarea id="answer1" rows="3"></textarea>
                </div>
                <div class="qa-pair">
                    <label for="question2">Question 2:</label> <textarea id="question2" rows="3"></textarea>
                    <label for="answer2">Answer 2:</label> <textarea id="answer2" rows="3"></textarea>
                </div>
                <div class="qa-pair">
                    <label for="question3">Question 3:</label> <textarea id="question3" rows="3"></textarea>
                    <label for="answer3">Answer 3:</label> <textarea id="answer3" rows="3"></textarea>
                </div>
            </div>
        </aside>
    </div>

    <footer class="footer-controls">
        <button id="prev-btn">← 上一个</button>
        <button id="submit-btn">保存/更新标注</button>
        <button id="download-btn">下载所有标注</button>
        <button id="next-btn">下一个 →</button>
    </footer>

    <script id="problem-data" type="application/json">{questions_json_string}</script>
    <script src="script.js"></script>
</body>
</html>
"""

    # --- CSS 样式 (增加了字体设置) ---
    css_content = """
body { 
    /* --- 字体设置 --- */
    font-family: Arial, 'Heiti', 'Microsoft YaHei', sans-serif;
    background-color: #f0f2f5; 
    margin: 0; 
}
.main-container { display: flex; padding: 15px; gap: 15px; min-height: calc(100vh - 100px); }
.left-panel, .right-panel { flex: 1; min-width: 280px; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow-y: auto; }
.main-content { flex: 2; min-width: 400px; background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
h1, h2, h3 { color: #333; }
hr { border: 0; border-top: 1px solid #eee; margin: 20px 0; }
.form-section { margin-bottom: 20px; }
.form-section label { display: block; margin-bottom: 8px; font-weight: bold; }
#keywords-form label { font-weight: normal; margin-bottom: 10px; }
#info-box p { margin: 5px 0; }
.content-box { white-space: pre-wrap; word-wrap: break-word; background-color: #f9f9f9; border: 1px solid #ddd; padding: 15px; border-radius: 4px; line-height: 1.7; }
textarea, input { font-family: Arial, 'Heiti', 'Microsoft YaHei', sans-serif; }
textarea { width: 100%; padding: 8px; border-radius: 4px; border: 1px solid #ccc; box-sizing: border-box; margin-bottom: 10px; }
.qa-pair { border-top: 1px solid #eee; padding-top: 15px; margin-top: 15px; }
.footer-controls { background: #fff; padding: 15px; text-align: center; box-shadow: 0 -2px 5px rgba(0,0,0,0.1); position: sticky; bottom: 0; z-index: 10; }
button { font-family: Arial, 'Heiti', 'Microsoft YaHei', sans-serif; padding: 10px 20px; border: none; border-radius: 5px; color: white; cursor: pointer; font-size: 1em; margin: 0 10px; transition: background-color 0.2s; }
#prev-btn, #next-btn { background-color: #1890ff; }
#submit-btn { background-color: #52c41a; }
#download-btn { background-color: #faad14; }
#new-annotation-btn { width: 100%; background-color: #08979c; margin-top: 10px;}
button:hover { opacity: 0.8; }
button:disabled { background-color: #ccc; cursor: not-allowed; }
.annotation-item { display: flex; justify-content: space-between; align-items: center; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 5px; cursor: pointer; }
.annotation-item.active { border-color: #1890ff; background-color: #e6f7ff; }
.delete-btn { background-color: #f5222d; color: white; border: none; border-radius: 4px; padding: 4px 8px; cursor: pointer; font-size: 0.8em; }
"""

    # --- JavaScript 逻辑 (包含删除功能) ---
    js_content = """
document.addEventListener('DOMContentLoaded', () => {
    const problemsData = JSON.parse(document.getElementById('problem-data').textContent);
    let annotations = JSON.parse(localStorage.getItem('annotations')) || {};
    let currentIndex = 0;
    let currentAnnotationIndex = -1; // -1 表示新建, >=0 表示编辑

    const ui = {
        keywordsForm: document.getElementById('keywords-form'),
        infoBox: document.getElementById('info-box'),
        title: document.getElementById('question-title'),
        counter: document.getElementById('problem-counter'),
        content: document.getElementById('question-content'),
        modifiedContent: document.getElementById('modified-content'),
        q1: document.getElementById('question1'), a1: document.getElementById('answer1'),
        q2: document.getElementById('question2'), a2: document.getElementById('answer2'),
        q3: document.getElementById('question3'), a3: document.getElementById('answer3'),
        prevBtn: document.getElementById('prev-btn'),
        nextBtn: document.getElementById('next-btn'),
        submitBtn: document.getElementById('submit-btn'),
        downloadBtn: document.getElementById('download-btn'),
        newAnnotationBtn: document.getElementById('new-annotation-btn'),
        annotationList: document.getElementById('annotation-list')
    };

    function renderProblem(index) {
        const problem = problemsData[index];
        ui.title.textContent = problem.question_title;
        ui.counter.textContent = `问题 ${index + 1} / ${problemsData.length}`;
        ui.content.textContent = problem.question_content;
        ui.infoBox.innerHTML = `<p><strong>ID:</strong> ${problem.question_id}</p><p><strong>Platform:</strong> ${problem.platform}</p>`;
        
        renderAnnotationList();
        clearAndLoadForm();

        ui.prevBtn.disabled = index === 0;
        ui.nextBtn.disabled = index === problemsData.length - 1;
    }
    
    function renderAnnotationList() {
        const problemId = problemsData[currentIndex].question_id;
        const problemAnnotations = annotations[problemId] || [];
        ui.annotationList.innerHTML = '';

        if (problemAnnotations.length === 0) {
            ui.annotationList.innerHTML = '<p>暂无标注</p>';
            return;
        }

        problemAnnotations.forEach((anno, index) => {
            const item = document.createElement('div');
            item.className = 'annotation-item';
            
            const text = document.createElement('span');
            text.textContent = `标注 #${index + 1} (${new Date(anno.timestamp).toLocaleTimeString()})`;
            
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-btn';
            deleteBtn.textContent = '删除';
            
            item.appendChild(text);
            item.appendChild(deleteBtn);

            if (index === currentAnnotationIndex) {
                item.classList.add('active');
            }

            text.addEventListener('click', () => {
                currentAnnotationIndex = index;
                renderAnnotationList();
                clearAndLoadForm();
            });

            deleteBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (confirm(`确定要删除“标注 #${index + 1}”吗？此操作无法撤销。`)) {
                    deleteAnnotation(index);
                }
            });

            ui.annotationList.appendChild(item);
        });
    }

    function clearAndLoadForm() {
        ui.keywordsForm.querySelectorAll('input').forEach(i => i.checked = false);
        ui.modifiedContent.value = '';
        [ui.q1, ui.a1, ui.q2, ui.a2, ui.q3, ui.a3].forEach(el => el.value = '');

        const problemId = problemsData[currentIndex].question_id;
        const problemAnnotations = annotations[problemId] || [];

        if (currentAnnotationIndex !== -1 && problemAnnotations[currentAnnotationIndex]) {
            const data = problemAnnotations[currentAnnotationIndex];
            data.keywords.forEach(kw => {
                const cb = ui.keywordsForm.querySelector(`input[value="${kw}"]`);
                if (cb) cb.checked = true;
            });
            ui.modifiedContent.value = data.modified_content || '';
            data.qa_pairs.forEach((pair, i) => {
                if (i < 3) {
                    ui[`q${i+1}`].value = pair.question || '';
                    ui[`a${i+1}`].value = pair.answer || '';
                }
            });
        }
    }
    
    function deleteAnnotation(indexToDelete) {
        const problemId = problemsData[currentIndex].question_id;
        annotations[problemId].splice(indexToDelete, 1);

        if (annotations[problemId].length === 0) {
            delete annotations[problemId];
        }

        localStorage.setItem('annotations', JSON.stringify(annotations));
        
        if (currentAnnotationIndex === indexToDelete) {
            currentAnnotationIndex = -1;
            clearAndLoadForm();
        } else if (currentAnnotationIndex > indexToDelete) {
            currentAnnotationIndex--;
        }

        renderAnnotationList();
    }
    
    function saveCurrentAnnotation() {
        const problemId = problemsData[currentIndex].question_id;
        if (!annotations[problemId]) {
            annotations[problemId] = [];
        }

        const qa_pairs = [];
        for (let i = 1; i <= 3; i++) {
            const q = ui[`q${i}`].value.trim();
            const a = ui[`a${i}`].value.trim();
            if (q && a) qa_pairs.push({ question: q, answer: a });
        }

        const annotationData = {
            timestamp: new Date().toISOString(),
            question_id: problemId,
            keywords: Array.from(ui.keywordsForm.querySelectorAll('input:checked')).map(cb => cb.value),
            modified_content: ui.modifiedContent.value.trim(),
            qa_pairs: qa_pairs
        };

        if (currentAnnotationIndex === -1) {
            annotations[problemId].push(annotationData);
            currentAnnotationIndex = annotations[problemId].length - 1;
        } else {
            annotations[problemId][currentAnnotationIndex] = annotationData;
        }

        localStorage.setItem('annotations', JSON.stringify(annotations));
        alert(`标注已保存！`);
        renderAnnotationList();
    }
    
    ui.newAnnotationBtn.addEventListener('click', () => {
        currentAnnotationIndex = -1;
        clearAndLoadForm();
        renderAnnotationList();
        ui.modifiedContent.focus();
    });

    ui.submitBtn.addEventListener('click', saveCurrentAnnotation);

    ui.prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            currentAnnotationIndex = -1;
            renderProblem(currentIndex);
        }
    });

    ui.nextBtn.addEventListener('click', () => {
        if (currentIndex < problemsData.length - 1) {
            currentIndex++;
            currentAnnotationIndex = -1;
            renderProblem(currentIndex);
        }
    });

    ui.downloadBtn.addEventListener('click', () => {
        const allAnnotationsList = Object.values(annotations).flat();
        if (allAnnotationsList.length === 0) {
            alert("没有可下载的标注！");
            return;
        }
        const content = allAnnotationsList.map(anno => JSON.stringify(anno)).join('\\n');
        const blob = new Blob([content], { type: 'application/jsonl' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'annotations_final.jsonl';
        a.click();
        URL.revokeObjectURL(a.href);
    });

    renderProblem(currentIndex);
});
"""
    # 5. 创建文件和目录
    os.makedirs(project_dir, exist_ok=True)
    with open(os.path.join(project_dir, 'index.html'), 'w', encoding='utf-8') as f: f.write(html_content)
    with open(os.path.join(project_dir, 'style.css'), 'w', encoding='utf-8') as f: f.write(css_content)
    with open(os.path.join(project_dir, 'script.js'), 'w', encoding='utf-8') as f: f.write(js_content)
        
    print(f"✓ 专业版标注工具网站已成功生成在 '{project_dir}' 文件夹中！")
    print(f"  请在浏览器中打开 '{os.path.join(project_dir, 'index.html')}' 文件开始标注。")

if __name__ == "__main__":
    create_pro_annotation_tool()