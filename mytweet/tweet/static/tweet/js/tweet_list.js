function openTweetModal(id) {
    const card = document.querySelector('[data-id="' + id + '"]');
    if (!card) return;

    document.getElementById('modalImg').src = card.dataset.img;
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
        '<a href="#" class="btn btn-primary btn-sm" onclick="closeTweetModal(); openFormModal(\'' + card.dataset.editUrl + '?embed=1\'); return false;">Edit</a>' +
        '<a href="#" class="btn btn-danger btn-sm" onclick="closeTweetModal(); openFormModal(\'' + card.dataset.deleteUrl + '?embed=1\'); return false;">Delete</a>';
    }

    document.getElementById('tweetModalOverlay').classList.add('active');
    document.body.style.overflow = 'hidden';
}

