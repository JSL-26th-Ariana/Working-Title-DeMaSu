/* ============================================
   デマス 共通ヘッダー JS
   ============================================ */

// ログアウト後（?logout=true）はページロード時にモーダルを自動で開かない
// ただし、ユーザーが手動でログインボタンを押した場合はモーダルを開く
// → URLから ?logout=true を除去してからモーダルを表示する
if (window.location.search && window.location.search.includes('logout')) {
    window.openLoginModal = function() {
        // URLのクエリパラメータを除去してブラウザ履歴を更新（リロードなし）
        history.replaceState(null, '', window.location.pathname);
        // 元の openLoginModal を呼び出すため、app.js の実装を直接実行
        var modal = document.getElementById('loginModal');
        if (modal) {
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    };
}

// ======= パスワードを忘れた: 모달 단계 전환 =======

/**
 * 1단계 → 2단계: 로그인 폼 숨기고 본인 확인 폼 표시
 * 「パスワードを忘れた」링크 클릭 시 호출
 */
function showForgotStep() {
    // 로그인 폼 숨기기
    var loginForm = document.querySelector('#loginModal .login-form');
    var loginTitle = document.querySelector('#loginModal .modal-title');
    var loginSubtitle = document.querySelector('#loginModal .modal-subtitle');
    if (loginForm) loginForm.style.display = 'none';
    if (loginTitle) loginTitle.style.display = 'none';
    if (loginSubtitle) loginSubtitle.style.display = 'none';

    // 2단계 표시 + 입력값 초기화
    var step2 = document.getElementById('forgotStep2');
    if (step2) {
        step2.style.display = 'block';
        document.getElementById('forgot-username').value = '';
        document.getElementById('forgot-email').value = '';
        document.getElementById('forgot-error').style.display = 'none';
    }
}

/**
 * 2단계 → 1단계: 로그인 폼으로 돌아가기
 * 「← ログインに戻る」링크 클릭 시 호출
 */
function showLoginStep() {
    // 2단계, 3단계 숨기기
    var step2 = document.getElementById('forgotStep2');
    var step3 = document.getElementById('forgotStep3');
    if (step2) step2.style.display = 'none';
    if (step3) step3.style.display = 'none';

    // 로그인 폼 다시 표시
    var loginForm = document.querySelector('#loginModal .login-form');
    var loginTitle = document.querySelector('#loginModal .modal-title');
    var loginSubtitle = document.querySelector('#loginModal .modal-subtitle');
    if (loginForm) loginForm.style.display = 'block';
    if (loginTitle) loginTitle.style.display = 'block';
    if (loginSubtitle) loginSubtitle.style.display = 'block';
}

/**
 * 2단계: 본인 확인 API 호출
 * POST /api/users/verify-identity?username=...&email=...
 * 성공 시 3단계(새 비밀번호 입력) 표시
 */
function verifyIdentity() {
    var username = document.getElementById('forgot-username').value.trim();
    var email = document.getElementById('forgot-email').value.trim();
    var errorEl = document.getElementById('forgot-error');

    // 입력값 검증
    if (!username || !email) {
        errorEl.textContent = 'IDとメールアドレスを入力してください';
        errorEl.style.display = 'block';
        return;
    }

    errorEl.style.display = 'none';

    fetch('/api/users/verify-identity?username=' + encodeURIComponent(username) + '&email=' + encodeURIComponent(email), {
        method: 'POST'
    })
    .then(function(r) { return r.json(); })
    .then(function(res) {
        if (!res.success) {
            // 일치하는 계정 없음
            errorEl.textContent = 'IDまたはメールアドレスが正しくありません';
            errorEl.style.display = 'block';
            return;
        }
        // 확인 성공 → 2단계 숨기고 3단계 표시
        document.getElementById('forgotStep2').style.display = 'none';
        var step3 = document.getElementById('forgotStep3');
        if (step3) {
            step3.style.display = 'block';
            document.getElementById('forgot-newpw').value = '';
            document.getElementById('forgot-newpw-confirm').value = '';
            document.getElementById('forgot-reset-error').style.display = 'none';
        }
    })
    .catch(function() {
        errorEl.textContent = 'エラーが発生しました。もう一度お試しください';
        errorEl.style.display = 'block';
    });
}

/**
 * 3단계: 새 비밀번호로 변경 API 호출
 * POST /api/users/reset-password?username=...&email=...&newPassword=...
 * 성공 시 로그인 폼으로 복귀 + 성공 토스트 표시
 */
function resetPassword() {
    var username = document.getElementById('forgot-username').value.trim();
    var email = document.getElementById('forgot-email').value.trim();
    var newpw = document.getElementById('forgot-newpw').value;
    var confirm = document.getElementById('forgot-newpw-confirm').value;
    var errorEl = document.getElementById('forgot-reset-error');

    // 비밀번호 확인 일치 검증
    if (newpw !== confirm) {
        errorEl.textContent = 'パスワードが一致しません';
        errorEl.style.display = 'block';
        return;
    }
    // 최소 8자 검증
    if (newpw.length < 8) {
        errorEl.textContent = 'パスワードは8文字以上で入力してください';
        errorEl.style.display = 'block';
        return;
    }

    errorEl.style.display = 'none';

    fetch('/api/users/reset-password?username=' + encodeURIComponent(username) +
          '&email=' + encodeURIComponent(email) +
          '&newPassword=' + encodeURIComponent(newpw), {
        method: 'POST'
    })
    .then(function(r) { return r.json(); })
    .then(function(res) {
        if (!res.success) {
            errorEl.textContent = res.message || 'パスワード変更に失敗しました';
            errorEl.style.display = 'block';
            return;
        }
        // 성공: 모달 닫고 로그인 폼으로 복귀 + 토스트
        document.getElementById('forgotStep3').style.display = 'none';
        showLoginStep();
        // 모달 닫기
        var modal = document.getElementById('loginModal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
        // 성공 토스트 표시
        showToast('パスワードが変更されました', 'success');
    })
    .catch(function() {
        errorEl.textContent = 'エラーが発生しました。もう一度お試しください';
        errorEl.style.display = 'block';
    });
}

// ======= ユーザードロップダウン =======
function toggleUserMenu(event) {
    event.stopPropagation();
    var dropdown = document.getElementById('userDropdown');
    var chevron = document.querySelector('.chevron-icon');
    if (!dropdown) return;
    var isOpen = dropdown.classList.contains('open');
    if (isOpen) {
        dropdown.classList.remove('open');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    } else {
        dropdown.classList.add('open');
        if (chevron) chevron.style.transform = 'rotate(180deg)';
    }
}

// 外部クリックでドロップダウンを閉じる
document.addEventListener('click', function(e) {
    var wrapper = document.getElementById('userMenuWrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        var dropdown = document.getElementById('userDropdown');
        var chevron = document.querySelector('.chevron-icon');
        if (dropdown) dropdown.classList.remove('open');
        if (chevron) chevron.style.transform = 'rotate(0deg)';
    }
});

// ======= トースト通知 =======
function showToast(msg, type) {
    var toast = document.getElementById('dmsToast');
    if (!toast || !msg) return;
    toast.textContent = msg;
    toast.className = 'dms-toast ' + (type || 'success');
    void toast.offsetWidth; // reflow for animation reset
    toast.classList.add('show');
    setTimeout(function() {
        toast.classList.remove('show');
    }, 3000);
}

// ======= トースト初期化 (body末尾で実行するのでDOM準備済み) =======
(function() {
    var msg = '';
    var type = 'success';
    var toastType = window._toastType || '';

    if (toastType === 'logout') {
        sessionStorage.removeItem('splashShown');
        msg = 'ログアウトしました';
    } else if (toastType === 'register') {
        msg = '会員登録が完了しました！';
    } else if (toastType === 'loginError') {
        sessionStorage.removeItem('justLoggedIn');
        msg = 'IDまたはパスワードが正しくありません';
        type = 'error';
    } else if (sessionStorage.getItem('justLoggedIn')) {
        sessionStorage.removeItem('justLoggedIn');
        msg = 'ログインしました';
    }

    if (msg) {
        setTimeout(function() { showToast(msg, type); }, 300);
    }
})();
