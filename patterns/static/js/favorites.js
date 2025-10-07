(function () {
    function getCookie(name) {
        const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return m ? m.pop() : '';
    }
    const csrftoken = getCookie('csrftoken');

    document.addEventListener('submit', function (e) {
        const form = e.target.closest('.fav-form');
        if (!form) return;
        e.preventDefault();

        const url = form.action;
        const patternId = form.dataset.pattern;
        const btn = form.querySelector('button');
        const icon = btn.querySelector('i');
        const next = form.querySelector('input[name="next"]')?.value || window.location.href;

        btn.disabled = true;
        btn.setAttribute('aria-busy', 'true');

        fetch(url, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken, 'X-Requested-With': 'XMLHttpRequest' },
        body: new FormData(form)
        })
        .then(async (resp) => {
        if (resp.redirected) {            // not logged in or login required
            window.location.href = resp.url;
            return null;
        }
        if (!(resp.headers.get('content-type') || '').includes('application/json')) {
            window.location.href = next;     // unexpected -> hard fallback
            return null;
        }
        return resp.json();
        })
        .then((data) => {
        if (!data) return;

        // Expect { ok: true, favorited: bool, count: int }
        if (data.favorited) {
            icon.classList.remove('fa-regular');
            icon.classList.add('fa-solid');
            btn.setAttribute('aria-pressed', 'true');
            btn.title = 'Remove from favorites';
        } else {
            icon.classList.remove('fa-solid');
            icon.classList.add('fa-regular');
            btn.setAttribute('aria-pressed', 'false');
            btn.title = 'Add to favorites';
        }

        const countEl = document.querySelector(`.fav-count[data-pattern="${patternId}"]`);
        if (countEl) countEl.textContent = data.count;
        })
        .catch(() => { window.location.href = next; })
        .finally(() => {
        btn.disabled = false;
        btn.removeAttribute('aria-busy');
        });
    });
})();
