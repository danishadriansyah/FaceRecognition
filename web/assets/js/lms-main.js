// ===========================
// LMS Main JavaScript
// ===========================

// Toggle Sidebar for Mobile
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}

// Close sidebar when clicking outside (mobile)
document.addEventListener('click', function(event) {
    const sidebar = document.querySelector('.sidebar');
    const menuToggle = document.querySelector('.menu-toggle');
    
    if (sidebar && menuToggle) {
        if (!sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
            sidebar.classList.remove('open');
        }
    }
});

// ===========================
// Progress Tracking System
// ===========================
const STORAGE_KEY = 'face_recognition_lms_progress';

// Initialize progress from localStorage
function loadProgress() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
        return JSON.parse(saved);
    }
    
    // Default progress structure
    return {
        weeks: {
            1: { completed: 0, total: 5, lessons: {} },
            2: { completed: 0, total: 4, lessons: {} },
            3: { completed: 0, total: 3, lessons: {} },
            4: { completed: 0, total: 3, lessons: {} },
            5: { completed: 0, total: 2, lessons: {} },
            6: { completed: 0, total: 3, lessons: {} },
            7: { completed: 0, total: 2, lessons: {} },
            8: { completed: 0, total: 3, lessons: {} }
        },
        totalLessons: 25,
        completedLessons: 0,
        badges: [],
        lastAccessed: null
    };
}

// Save progress to localStorage
function saveProgress(progress) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
}

// Get current progress
let progress = loadProgress();

// Mark lesson as completed
function markLessonCompleted(week, lesson) {
    if (!progress.weeks[week].lessons[lesson]) {
        progress.weeks[week].lessons[lesson] = {
            completed: true,
            completedAt: new Date().toISOString()
        };
        
        progress.weeks[week].completed++;
        progress.completedLessons++;
        
        saveProgress(progress);
        updateProgressUI();
        
        // Check for week completion badge
        if (progress.weeks[week].completed === progress.weeks[week].total) {
            awardBadge(`week${week}_complete`);
        }
    }
}

// Check if lesson is completed
function isLessonCompleted(week, lesson) {
    return progress.weeks[week].lessons[lesson]?.completed || false;
}

// Award badge
function awardBadge(badgeId) {
    if (!progress.badges.includes(badgeId)) {
        progress.badges.push(badgeId);
        saveProgress(progress);
        showBadgeNotification(badgeId);
    }
}

// Show badge notification
function showBadgeNotification(badgeId) {
    const badges = {
        week1_complete: { icon: '🎉', title: 'Week 1 Complete!', desc: 'Python & OpenCV mastered' },
        week2_complete: { icon: '🔍', title: 'Week 2 Complete!', desc: 'Face Detection expert' },
        week3_complete: { icon: '👤', title: 'Week 3 Complete!', desc: 'Face Recognition unlocked' },
        week4_complete: { icon: '📊', title: 'Week 4 Complete!', desc: 'Dataset Master' },
        week5_complete: { icon: '⚙️', title: 'Week 5 Complete!', desc: 'System Integration Pro' },
        week6_complete: { icon: '🗄️', title: 'Week 6 Complete!', desc: 'Database Expert' },
        week7_complete: { icon: '🖥️', title: 'Week 7 Complete!', desc: 'GUI Developer' },
        week8_complete: { icon: '🏆', title: 'Course Complete!', desc: 'All modules mastered!' }
    };
    
    const badge = badges[badgeId];
    if (badge) {
        showNotification(badge.icon, badge.title, badge.desc);
    }
}

// Show notification
function showNotification(icon, title, message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `
        <div class="notification-icon">${icon}</div>
        <div class="notification-content">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Update progress UI
function updateProgressUI() {
    // Update overall progress
    const overallPercentage = Math.round((progress.completedLessons / progress.totalLessons) * 100);
    
    // Update dashboard stats if on dashboard
    const statsElement = document.querySelector('.welcome-stats');
    if (statsElement) {
        statsElement.innerHTML = `
            <div class="stat-item">
                <div class="stat-icon">📚</div>
                <div class="stat-info">
                    <h3>25</h3>
                    <p>Total Lessons</p>
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">⏱️</div>
                <div class="stat-info">
                    <h3>8</h3>
                    <p>Weeks</p>
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">🎯</div>
                <div class="stat-info">
                    <h3>${overallPercentage}%</h3>
                    <p>Progress</p>
                </div>
            </div>
            <div class="stat-item">
                <div class="stat-icon">🏆</div>
                <div class="stat-info">
                    <h3>${progress.badges.length}</h3>
                    <p>Badges</p>
                </div>
            </div>
        `;
    }
    
    // Update mini progress bar
    const miniProgressFill = document.querySelector('.mini-progress-fill');
    if (miniProgressFill) {
        miniProgressFill.style.width = `${overallPercentage}%`;
    }
    
    // Update week progress cards
    Object.keys(progress.weeks).forEach(weekNum => {
        const week = progress.weeks[weekNum];
        const percentage = Math.round((week.completed / week.total) * 100);
        
        const progressCard = document.querySelector(`.week-progress-card[data-week="${weekNum}"]`);
        if (progressCard) {
            const progressFill = progressCard.querySelector('.progress-fill');
            const progressInfo = progressCard.querySelector('.progress-info');
            
            if (progressFill) {
                progressFill.style.width = `${percentage}%`;
            }
            
            if (progressInfo) {
                progressInfo.innerHTML = `
                    <span>${week.completed}/${week.total} Lessons Completed</span>
                    <span>${percentage}%</span>
                `;
            }
            
            // Remove locked state if previous week completed
            if (weekNum > 1) {
                const prevWeek = progress.weeks[weekNum - 1];
                if (prevWeek.completed === prevWeek.total) {
                    progressCard.classList.remove('locked');
                    const lockMsg = progressCard.querySelector('.lock-msg');
                    if (lockMsg) lockMsg.remove();
                }
            }
        }
    });
}

// ===========================
// Open Lesson (Navigate to lesson detail page)
// ===========================
function openLesson(week, lesson) {
    // Navigate to lesson detail page (all lessons unlocked)
    window.location.href = `lessons/week${week}-lesson${lesson}.html`;
}

// ===========================
// Quiz System
// ===========================
let currentQuiz = null;
let quizAnswers = {};

function loadQuiz(quizData) {
    currentQuiz = quizData;
    quizAnswers = {};
}

function submitQuiz() {
    let correct = 0;
    let total = currentQuiz.questions.length;
    
    currentQuiz.questions.forEach((q, index) => {
        if (quizAnswers[index] === q.correct) {
            correct++;
        }
    });
    
    const percentage = Math.round((correct / total) * 100);
    
    if (percentage >= 70) {
        showNotification('✅', 'Quiz Passed!', `You scored ${percentage}%`);
        return true;
    } else {
        showNotification('❌', 'Quiz Failed', `You scored ${percentage}%. Try again!`);
        return false;
    }
}

// ===========================
// Search Functionality
// ===========================
function searchLessons(query) {
    // Search through all lessons
    // This would be implemented with a proper search index
    console.log('Searching for:', query);
}

// ===========================
// Initialize on Page Load
// ===========================
document.addEventListener('DOMContentLoaded', function() {
    // Update progress UI
    updateProgressUI();
    
    // Set last accessed
    progress.lastAccessed = new Date().toISOString();
    saveProgress(progress);
    
    // Add notification styles if not exists
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                padding: 1rem 1.5rem;
                border-radius: 0.75rem;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
                display: flex;
                gap: 1rem;
                align-items: center;
                z-index: 10000;
                transform: translateX(400px);
                opacity: 0;
                transition: all 0.3s ease;
                max-width: 350px;
            }
            
            .notification.show {
                transform: translateX(0);
                opacity: 1;
            }
            
            .notification-icon {
                font-size: 2rem;
            }
            
            .notification-content h4 {
                font-size: 1rem;
                color: var(--text-primary);
                margin-bottom: 0.25rem;
            }
            
            .notification-content p {
                font-size: 0.875rem;
                color: var(--text-secondary);
                margin: 0;
            }
        `;
        document.head.appendChild(style);
    }
    
    console.log('🎓 LMS Initialized');
    console.log('Progress:', progress);
});

// ===========================
// Export Functions
// ===========================
window.toggleSidebar = toggleSidebar;
window.openLesson = openLesson;
window.markLessonCompleted = markLessonCompleted;
window.isLessonCompleted = isLessonCompleted;
window.showNotification = showNotification;
window.searchLessons = searchLessons;
window.progress = progress;
