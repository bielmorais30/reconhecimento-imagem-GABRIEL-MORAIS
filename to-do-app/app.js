/**
 * TaskFlow — To-Do App
 * Stack: HTML + Tailwind CDN + Vanilla JS + localStorage
 *
 * Storage schema (simulates db.json):
 *   localStorage["tf_db"] = { users: User[], todos: Todo[] }
 *
 * User  : { id, name, email, password }
 * Todo  : { id, userId, title, type, description, done }
 */

/* ─────────────────────────────────────────
   DB HELPERS — read / write localStorage
───────────────────────────────────────── */

const DB_KEY      = 'tf_db';
const SESSION_KEY = 'currentUser';

function getDB() {
  const raw = localStorage.getItem(DB_KEY);
  if (raw) return JSON.parse(raw);
  const initial = { users: [], todos: [] };
  localStorage.setItem(DB_KEY, JSON.stringify(initial));
  return initial;
}

function saveDB(db) {
  localStorage.setItem(DB_KEY, JSON.stringify(db));
}

function getSession() {
  const raw = localStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : null;
}

function setSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

/* ─────────────────────────────────────────
   UI HELPERS
───────────────────────────────────────── */

function showEl(id)  { document.getElementById(id).classList.remove('hidden'); }
function hideEl(id)  { document.getElementById(id).classList.add('hidden'); }
function setText(id, text) { document.getElementById(id).textContent = text; }

function showError(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.classList.add('visible');
}
function clearError(id) {
  const el = document.getElementById(id);
  el.textContent = '';
  el.classList.remove('visible');
}

function showSuccess(id, msg) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.classList.add('visible');
}
function clearSuccess(id) {
  const el = document.getElementById(id);
  el.textContent = '';
  el.classList.remove('visible');
}

/* ─────────────────────────────────────────
   SCREENS
───────────────────────────────────────── */

function showAuthScreen() {
  showEl('screen-auth');
  hideEl('screen-dashboard');
}

function showDashboard(user) {
  hideEl('screen-auth');
  showEl('screen-dashboard');
  setText('greeting-name', user.name);
  renderTasks();
}

/* ─────────────────────────────────────────
   TAB SWITCHER (Login / Register)
───────────────────────────────────────── */

const TAB_ACTIVE   = ['bg-white/10', 'text-white', 'shadow-sm'];
const TAB_INACTIVE = ['text-slate-500'];

function applyTabStyle(btn, active) {
  if (active) {
    btn.classList.remove(...TAB_INACTIVE);
    btn.classList.add(...TAB_ACTIVE);
  } else {
    btn.classList.remove(...TAB_ACTIVE);
    btn.classList.add(...TAB_INACTIVE);
  }
}

/* ─────────────────────────────────────────
   APP OBJECT — public surface
───────────────────────────────────────── */

const App = {

  /** Switch between login / register tabs */
  showTab(tab) {
    const isLogin = tab === 'login';

    applyTabStyle(document.getElementById('tab-login'),    isLogin);
    applyTabStyle(document.getElementById('tab-register'), !isLogin);

    if (isLogin) {
      showEl('form-login');
      hideEl('form-register');
      showEl('swap-hint-login');
      hideEl('swap-hint-register');
    } else {
      hideEl('form-login');
      showEl('form-register');
      hideEl('swap-hint-login');
      showEl('swap-hint-register');
    }

    // clear messages on switch
    clearError('login-error');
    clearError('reg-error');
    clearSuccess('reg-success');
  },

  /* ── REGISTER ── */
  handleRegister(e) {
    e.preventDefault();
    clearError('reg-error');
    clearSuccess('reg-success');

    const name     = document.getElementById('reg-name').value.trim();
    const email    = document.getElementById('reg-email').value.trim().toLowerCase();
    const password = document.getElementById('reg-password').value;

    // validation
    if (!name || !email || !password) {
      showError('reg-error', 'Preencha todos os campos obrigatórios.');
      return;
    }
    if (!email.includes('@') || !email.includes('.')) {
      showError('reg-error', 'Informe um e-mail válido.');
      return;
    }
    if (password.length < 6) {
      showError('reg-error', 'A senha deve ter no mínimo 6 caracteres.');
      return;
    }

    const db = getDB();
    const exists = db.users.find(u => u.email === email);
    if (exists) {
      showError('reg-error', 'Este e-mail já está cadastrado.');
      return;
    }

    const newUser = { id: Date.now(), name, email, password };
    db.users.push(newUser);
    saveDB(db);

    // reset form + feedback
    document.getElementById('form-register').reset();
    showSuccess('reg-success', '✓ Conta criada! Faça login para continuar.');

    // auto-switch to login after a moment
    setTimeout(() => App.showTab('login'), 1400);
  },

  /* ── LOGIN ── */
  handleLogin(e) {
    e.preventDefault();
    clearError('login-error');

    const email    = document.getElementById('login-email').value.trim().toLowerCase();
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
      showError('login-error', 'Preencha e-mail e senha.');
      return;
    }

    const db   = getDB();
    const user = db.users.find(u => u.email === email);

    if (!user) {
      showError('login-error', 'E-mail não encontrado. Crie uma conta primeiro.');
      return;
    }
    if (user.password !== password) {
      showError('login-error', 'Senha incorreta. Tente novamente.');
      return;
    }

    setSession(user);
    document.getElementById('form-login').reset();
    showDashboard(user);
  },

  /* ── LOGOUT ── */
  handleLogout() {
    clearSession();
    showAuthScreen();
    App.showTab('login');
  },

  /* ── ADD TASK ── */
  handleAddTask(e) {
    e.preventDefault();
    clearError('task-error');

    const user = getSession();
    if (!user) { App.handleLogout(); return; }

    const title = document.getElementById('task-title').value.trim();
    const type  = document.getElementById('task-type').value;
    const desc  = document.getElementById('task-desc').value.trim();

    if (!title) {
      showError('task-error', 'O título da tarefa é obrigatório.');
      return;
    }

    const db = getDB();
    const todo = {
      id: Date.now(),
      userId: user.email,
      title,
      type,
      description: desc,
      done: false,
    };
    db.todos.push(todo);
    saveDB(db);

    document.getElementById('form-task').reset();
    renderTasks();
  },

  /* ── COMPLETE TASK ── */
  completeTask(id) {
    const db   = getDB();
    const todo = db.todos.find(t => t.id === id);
    if (!todo) return;
    todo.done = true;
    saveDB(db);
    renderTasks();
  },
};

/* ─────────────────────────────────────────
   RENDER TASK LIST
───────────────────────────────────────── */

const BADGE_CLASS = {
  'Trabalho': 'badge-trabalho',
  'Pessoal':  'badge-pessoal',
  'Estudos':  'badge-estudos',
};

function renderTasks() {
  const user = getSession();
  if (!user) return;

  const db    = getDB();
  const mine  = db.todos.filter(t => t.userId === user.email);

  // pending first, done after
  const pending   = mine.filter(t => !t.done);
  const completed = mine.filter(t =>  t.done);
  const ordered   = [...pending, ...completed];

  const container = document.getElementById('task-list');
  const countEl   = document.getElementById('task-count');

  countEl.textContent = `${pending.length} pendente${pending.length !== 1 ? 's' : ''} · ${completed.length} concluída${completed.length !== 1 ? 's' : ''}`;

  if (ordered.length === 0) {
    container.innerHTML = `
      <div class="glass rounded-2xl p-8 text-center">
        <p class="text-4xl mb-3">📋</p>
        <p class="text-slate-500 text-sm">Nenhuma tarefa cadastrada ainda.</p>
        <p class="text-slate-600 text-xs mt-1">Adicione sua primeira tarefa acima.</p>
      </div>`;
    return;
  }

  container.innerHTML = ordered.map(todo => {
    const badgeCls = BADGE_CLASS[todo.type] || 'badge-trabalho';
    const isDone   = todo.done;

    return `
      <div class="glass rounded-2xl p-5 task-card ${isDone ? 'done-card' : ''}" id="task-${todo.id}"
        style="animation: fadeSlideUp 0.35s cubic-bezier(.22,1,.36,1) both;">
        <div class="flex items-start justify-between gap-3">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap mb-1.5">
              <span class="badge ${badgeCls}">${escapeHtml(todo.type)}</span>
              ${isDone ? `<span class="text-xs text-emerald-400 font-semibold">✓ Concluída</span>` : ''}
            </div>
            <p class="task-title font-semibold text-white text-sm leading-snug truncate">
              ${escapeHtml(todo.title)}
            </p>
            ${todo.description
              ? `<p class="text-slate-400 text-xs mt-1.5 leading-relaxed line-clamp-2">${escapeHtml(todo.description)}</p>`
              : ''}
          </div>
          <button
            class="btn-done flex-shrink-0"
            onclick="App.completeTask(${todo.id})"
            ${isDone ? 'disabled' : ''}
            aria-label="Marcar tarefa como concluída">
            ${isDone ? '✓ Feito' : 'Concluir'}
          </button>
        </div>
      </div>`;
  }).join('');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/* ─────────────────────────────────────────
   BOOT — check session on page load
───────────────────────────────────────── */

(function boot() {
  // ensure DB exists
  getDB();

  // set default tab styles
  App.showTab('login');

  const session = getSession();
  if (session) {
    showDashboard(session);
  } else {
    showAuthScreen();
  }
})();
