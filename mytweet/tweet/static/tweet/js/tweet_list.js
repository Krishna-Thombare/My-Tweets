function openTweetModal(id) {
    const card = document.querySelector('[data-id="' + id + '"]');
    if (!card) return;

    const modalImg = document.getElementById('modalImg');
        modalImg.src = card.dataset.img;
        if (!card.dataset.tweetHasPhoto || card.dataset.tweetHasPhoto === '0') {
            modalImg.classList.add('profile-fallback');
        } else {
            modalImg.classList.remove('profile-fallback');
        }
    const handleHtml = card.dataset.handle
        ? ' <span class="grid-card-handle">@' + card.dataset.handle + '</span>'
        : '';
    const profileHref = card.dataset.handle ? '/mytweets/profile/' + card.dataset.handle + '/' : '#';
    document.getElementById('modalUser').innerHTML =
        '<a href="' + profileHref + '" class="profile-link card-user-link">' +
        '<img src="' + card.dataset.avatar + '" class="card-avatar" alt="">' +
        '<span class="card-username-text">' + card.dataset.user + handleHtml + '</span>' +
        '</a>';
    document.getElementById('modalDate').textContent = card.dataset.date;
    document.getElementById('modalText').textContent = card.dataset.text;

    const actions = document.getElementById('modalActions');
    actions.innerHTML = '';
    if (card.dataset.owner === '1') {
        actions.innerHTML =
        '<a href="#" class="btn btn-outline-dark text-white" onclick="closeTweetModal(); openFormModal(\'' + card.dataset.editUrl + '?embed=1\'); return false;">Edit</a>' +
        '<a href="#" class="btn btn-outline-dark text-white" onclick="closeTweetModal(); openFormModal(\'' + card.dataset.deleteUrl + '?embed=1\'); return false;">Delete</a>';
    }

    document.getElementById('tweetModalOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeTweetModal() {
    document.getElementById('tweetModalOverlay').classList.remove('active');
    document.body.style.overflow = '';
}

function closeTweetModalOnOverlay(e) {
    if (e.target.id === 'tweetModalOverlay') closeTweetModal();
}

document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeTweetModal();
        closeFormModal();
    }
});

function openFormModal(url) {
    document.getElementById('formModalIframe').src = url;
    document.getElementById('formModalOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeFormModal() {
    document.getElementById('formModalOverlay').classList.remove('active');
    document.getElementById('formModalIframe').src = '';
    document.body.style.overflow = '';
}

function closeFormModalOnOverlay(e) {
    if (e.target.id === 'formModalOverlay') closeFormModal();
}

const newTweetBtn = document.getElementById('newTweetBtn');
if (newTweetBtn) {
    newTweetBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openFormModal(this.dataset.createUrl + '?embed=1');
    });
}

const emptyStateBtn = document.getElementById('emptyStateNewTweetBtn');
if (emptyStateBtn) {
    emptyStateBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openFormModal(this.dataset.createUrl + '?embed=1');
    });
}

const profileEditBtn = document.getElementById('profileEditBtn');
if (profileEditBtn) {
    profileEditBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openFormModal(this.dataset.createUrl + '?embed=1');
    });
}

const mobileFabBtn = document.getElementById('mobileFabBtn');
if (mobileFabBtn) {
    mobileFabBtn.addEventListener('click', function (e) {
        e.preventDefault();
        openFormModal(this.dataset.createUrl + '?embed=1');
    });
}