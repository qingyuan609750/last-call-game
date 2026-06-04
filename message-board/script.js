document.addEventListener('DOMContentLoaded', function () {
    var nicknameInput = document.getElementById('nickname');
    var contentInput = document.getElementById('content');
    var publishBtn = document.getElementById('publishBtn');
    var messageList = document.getElementById('messageList');
    var messageCount = document.getElementById('messageCount');
    var errorTip = document.getElementById('errorTip');

    function updateCount() {
        messageCount.textContent = messageList.children.length;
    }

    function createMessageItem(nickname, content) {
        var li = document.createElement('li');
        li.className = 'message-item';

        var divContent = document.createElement('div');
        divContent.className = 'message-content';

        var nameDiv = document.createElement('div');
        nameDiv.className = 'message-nickname';
        nameDiv.textContent = nickname;

        var textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = content;

        divContent.appendChild(nameDiv);
        divContent.appendChild(textDiv);

        var actionsDiv = document.createElement('div');
        actionsDiv.className = 'message-actions';

        var likeBtn = document.createElement('button');
        likeBtn.className = 'like-btn';
        likeBtn.textContent = '点赞 (0)';
        likeBtn.dataset.liked = 'false';
        likeBtn.dataset.count = '0';

        var deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.textContent = '删除';

        actionsDiv.appendChild(likeBtn);
        actionsDiv.appendChild(deleteBtn);

        li.appendChild(divContent);
        li.appendChild(actionsDiv);

        return li;
    }

    function showError(msg) {
        errorTip.textContent = msg;
    }

    function clearError() {
        errorTip.textContent = '';
    }

    publishBtn.addEventListener('click', function (e) {
        e.preventDefault();
        clearError();

        var nickname = nicknameInput.value.trim();
        var content = contentInput.value.trim();

        if (!nickname || !content) {
            showError('昵称和留言内容不能为空！');
            return;
        }

        var item = createMessageItem(nickname, content);
        messageList.insertBefore(item, messageList.firstChild);

        nicknameInput.value = '';
        contentInput.value = '';
        updateCount();
    });

    messageList.addEventListener('click', function (e) {
        var target = e.target;

        if (target.classList.contains('delete-btn')) {
            e.stopPropagation();
            var item = target.closest('.message-item');
            if (item) {
                messageList.removeChild(item);
                updateCount();
            }
        } else if (target.classList.contains('like-btn')) {
            e.stopPropagation();
            var liked = target.dataset.liked === 'true';
            var count = parseInt(target.dataset.count, 10);

            if (liked) {
                count--;
                target.dataset.liked = 'false';
                target.classList.remove('liked');
            } else {
                count++;
                target.dataset.liked = 'true';
                target.classList.add('liked');
            }

            target.dataset.count = count;
            target.textContent = '点赞 (' + count + ')';
        }
    });

    [nicknameInput, contentInput].forEach(function (input) {
        input.addEventListener('focus', clearError);
    });

    updateCount();
});
