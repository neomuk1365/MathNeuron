class QuizEngine {
    constructor(mountId, topicId) {
        this.mountPoint = document.getElementById(mountId);
        this.topicId = topicId;
        this.questions = [];
        this.currentQuestionIndex = 0;
    }

    async init() {
        try {
            const response = await fetch(`/api/questions/${this.topicId}`);
            const data = await response.json();
            
            if (data.status === 'success' && data.questions.length > 0) {
                this.questions = data.questions;
                this.renderQuestion();
            } else {
                this.mountPoint.innerHTML = '<div class="text-center text-secondary">No questions for this topic yet.</div>';
            }
        } catch (e) {
            console.error('Error loading questions:', e);
            this.mountPoint.innerHTML = '<div class="text-error text-center">Failed to load questions.</div>';
        }
    }

    initPreloaded(questions) {
        if (questions && questions.length > 0) {
            this.questions = questions;
            this.renderQuestion();
        } else {
            this.mountPoint.innerHTML = '<div class="text-center text-secondary">No questions for this topic yet.</div>';
        }
    }

    renderQuestion() {
        const q = this.questions[this.currentQuestionIndex];
        
        let optionsHtml = q.options.map(opt => `
            <div class="quiz-option" data-id="${opt.id}">
                <div style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid var(--border-color); display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;">
                    ${opt.id}
                </div>
                <div>${opt.text}</div>
            </div>
        `).join('');

        const treeHtml = q.explanation.tree ? this.renderTree(q.explanation.tree) : '';

        this.mountPoint.innerHTML = `
            <div class="card">
                <div class="text-secondary" style="font-size: 0.875rem; margin-bottom: 1rem; font-weight: 600;">
                    INTUITION CHECK ${this.currentQuestionIndex + 1} OF ${this.questions.length}
                </div>
                <h3 style="font-family: var(--font-sans);">${q.question_text}</h3>
                
                <div class="quiz-options">
                    ${optionsHtml}
                </div>
                
                <div class="explanation-panel" id="exp-${q.id}">
                    <div class="explanation-header" id="exp-header-${q.id}"></div>
                    
                    <div id="mistake-analysis-${q.id}" style="display: none; margin-bottom: 1rem;" class="text-error"></div>
                    
                    <div class="callout intuition" style="font-size: 1.1rem; font-weight: 500; margin: 1.5rem 0; border-width: 0 0 0 4px; padding: 1rem 1.5rem; background: var(--warning-bg); color: var(--text-primary); border-radius: 0.5rem; border-color: var(--warning-color); border-style: solid;">
                        <strong style="color: var(--warning-color); font-size: 1.2rem; display: block; margin-bottom: 0.5rem;">🧠 Core Intuition:</strong>
                        ${q.explanation.intuition}
                    </div>
                    
                    ${treeHtml}
                    
                    <div class="mt-4 pt-4" style="border-top: 1px solid var(--border-color);">
                        <span style="font-weight: 700;">Step-by-Step:</span><br/>
                        <div style="white-space: pre-line; margin-top: 0.5rem;" class="text-secondary">
                            ${q.explanation.step_by_step}
                        </div>
                    </div>
                    
                    <button class="btn btn-primary mt-4" id="next-btn-${q.id}" style="display: none;">
                        ${this.currentQuestionIndex < this.questions.length - 1 ? 'Next Question' : 'Complete Topic'}
                    </button>
                </div>
            </div>
        `;

        this.attachEventListeners(q);
    }

    attachEventListeners(q) {
        const options = this.mountPoint.querySelectorAll('.quiz-option');
        const expPanel = this.mountPoint.querySelector(`#exp-${q.id}`);
        const expHeader = this.mountPoint.querySelector(`#exp-header-${q.id}`);
        const mistakePanel = this.mountPoint.querySelector(`#mistake-analysis-${q.id}`);
        const nextBtn = this.mountPoint.querySelector(`#next-btn-${q.id}`);

        options.forEach(opt => {
            opt.addEventListener('click', () => {
                // If already answered, ignore
                if (this.mountPoint.querySelector('.quiz-option.correct') || 
                    this.mountPoint.querySelector('.quiz-option.wrong')) {
                    return;
                }

                const selectedId = opt.getAttribute('data-id');
                const isCorrect = selectedId === q.correct_answer;

                // Send attempt to server
                fetch('/api/submit_attempt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question_id: q.id,
                        is_correct: isCorrect,
                        selected_answer: selectedId
                    })
                });

                options.forEach(o => o.classList.add('disabled'));
                opt.classList.remove('disabled');

                if (isCorrect) {
                    opt.classList.add('correct');
                    expHeader.textContent = '✨ Brilliant Intuition!';
                    expHeader.className = 'explanation-header correct';
                } else {
                    opt.classList.add('wrong');
                    expHeader.textContent = '🤔 Let\'s Check the Intuition';
                    expHeader.className = 'explanation-header wrong';
                    
                    if (q.explanation.common_mistakes && q.explanation.common_mistakes[selectedId]) {
                        mistakePanel.innerHTML = `<strong>Mistake Analysis:</strong> ${q.explanation.common_mistakes[selectedId]}`;
                        mistakePanel.style.display = 'block';
                    }
                    
                    // Highlight correct answer
                    const correctOpt = this.mountPoint.querySelector(`.quiz-option[data-id="${q.correct_answer}"]`);
                    correctOpt.classList.remove('disabled');
                    correctOpt.classList.add('correct');
                }

                expPanel.classList.add('show');
                nextBtn.style.display = 'inline-flex';
            });
        });

        nextBtn.addEventListener('click', () => {
            if (this.currentQuestionIndex < this.questions.length - 1) {
                this.currentQuestionIndex++;
                this.renderQuestion();
            } else {
                this.mountPoint.innerHTML = `
                    <div class="card text-center" style="background-color: var(--success-bg); border-color: var(--success-color);">
                        <h3 style="color: var(--success-color);">Topic Completed!</h3>
                        <p class="mt-2 text-secondary">You've successfully built intuition for this concept.</p>
                    </div>
                `;
            }
        });
    }

    renderTree(treeConfig) {
        if (!treeConfig) return '';
        
        let html = `<div class="visual-tree-container" style="transform: scale(0.85); transform-origin: top; margin: 1rem 0 0 0; padding: 1.5rem 1rem;">
            <div class="tree-root">${treeConfig.root}</div>
            <div class="tree-branches">`;
            
        treeConfig.level1.options.forEach(opt1 => {
            html += `<div class="tree-branch">
                <div class="tree-node level-1">${opt1}</div>`;
                
            if (treeConfig.level2) {
                html += `<div class="tree-sub-branches">`;
                treeConfig.level2.options.forEach(opt2 => {
                    html += `<div class="tree-sub-branch">
                        <div class="tree-node level-2">${opt2}</div>`;
                    if (treeConfig.level3) {
                        html += `<div class="tree-sub-branches">`;
                        treeConfig.level3.options.forEach(opt3 => {
                            html += `<div class="tree-sub-branch"><div class="tree-node level-3">${opt3}</div></div>`;
                        });
                        html += `</div>`;
                    }
                    html += `</div>`;
                });
                html += `</div>`;
            }
            html += `</div>`;
        });
        
        html += `</div></div>`;
        return html;
    }
}
