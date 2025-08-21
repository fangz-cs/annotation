
document.addEventListener('DOMContentLoaded', () => {
    const problemsData = JSON.parse(document.getElementById('problem-data').textContent);
    let annotations = JSON.parse(localStorage.getItem('annotations')) || {};
    let currentIndex = 0;
    let currentAnnotationIndex = -1; // -1表示正在新建, >=0 表示正在编辑

    // 获取DOM元素... (省略以保持简洁)
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
            // 使用标注创建时间作为标识
            item.textContent = `标注 #${index + 1} (${new Date(anno.timestamp).toLocaleString()})`;
            if (index === currentAnnotationIndex) {
                item.classList.add('active');
            }
            item.addEventListener('click', () => {
                currentAnnotationIndex = index;
                renderAnnotationList(); // 重新渲染列表以更新高亮
                clearAndLoadForm();
            });
            ui.annotationList.appendChild(item);
        });
    }

    function clearAndLoadForm() {
        // 清空表单
        ui.keywordsForm.querySelectorAll('input').forEach(i => i.checked = false);
        ui.modifiedContent.value = '';
        [ui.q1, ui.a1, ui.q2, ui.a2, ui.q3, ui.a3].forEach(el => el.value = '');

        const problemId = problemsData[currentIndex].question_id;
        const problemAnnotations = annotations[problemId] || [];

        if (currentAnnotationIndex !== -1 && problemAnnotations[currentAnnotationIndex]) {
            const data = problemAnnotations[currentAnnotationIndex];
            // 加载 keywords
            data.keywords.forEach(kw => {
                const cb = ui.keywordsForm.querySelector(`input[value="${kw}"]`);
                if (cb) cb.checked = true;
            });
            // 加载其他字段
            ui.modifiedContent.value = data.modified_content || '';
            data.qa_pairs.forEach((pair, i) => {
                if (i < 3) {
                    ui[`q${i+1}`].value = pair.question || '';
                    ui[`a${i+1}`].value = pair.answer || '';
                }
            });
        }
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

        if (currentAnnotationIndex === -1) { // 新建
            annotations[problemId].push(annotationData);
            currentAnnotationIndex = annotations[problemId].length - 1; // 自动选中新建的这个
        } else { // 更新
            annotations[problemId][currentAnnotationIndex] = annotationData;
        }

        localStorage.setItem('annotations', JSON.stringify(annotations));
        alert(`标注已保存！`);
        renderAnnotationList(); // 保存后刷新列表
    }
    
    ui.newAnnotationBtn.addEventListener('click', () => {
        currentAnnotationIndex = -1; // 设置为“新建”模式
        clearAndLoadForm();
        renderAnnotationList(); // 取消列表中所有项的高亮
        ui.modifiedContent.focus();
    });

    ui.submitBtn.addEventListener('click', saveCurrentAnnotation);

    ui.prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            currentAnnotationIndex = -1; // 切换问题时重置
            renderProblem(currentIndex);
        }
    });

    ui.nextBtn.addEventListener('click', () => {
        if (currentIndex < problemsData.length - 1) {
            currentIndex++;
            currentAnnotationIndex = -1; // 切换问题时重置
            renderProblem(currentIndex);
        }
    });

    ui.downloadBtn.addEventListener('click', () => {
        const allAnnotationsList = Object.values(annotations).flat();
        if (allAnnotationsList.length === 0) {
            alert("没有可下载的标注！");
            return;
        }
        const content = allAnnotationsList.map(anno => JSON.stringify(anno)).join('\n');
        const blob = new Blob([content], { type: 'application/jsonl' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'annotations_multiple.jsonl';
        a.click();
        URL.revokeObjectURL(a.href);
    });

    // 初始加载
    renderProblem(currentIndex);
});
