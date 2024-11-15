var timeout;

    function handleClick(button) {
        var existingPopovers = document.querySelectorAll('.popover');
        existingPopovers.forEach(function (popover) {
            popover.style.display = 'none';
        });
        var buttonId = button.getAttribute('data-id');
        var popoverId = 'popover-' + buttonId;
        var popover = document.getElementById(popoverId);
        if (popover) {
            document.body.removeChild(popover);
        }
        popover = document.createElement('div');
        popover.classList.add('popover');
        popover.id = popoverId;
        document.body.appendChild(popover);
        popover.style.display = 'block';
        var buttonRect = button.getBoundingClientRect();
        var pageX = buttonRect.left + button.offsetWidth / 2;
        var pageY = buttonRect.top + button.offsetHeight / 2;
        popover.style.top = (pageY - popover.offsetHeight / 2) + 'px';
        popover.style.left = (pageX - popover.offsetWidth / 2) + 'px';
        var textarea = document.createElement('textarea');
        textarea.placeholder = '输入文本';
        popover.appendChild(textarea);
        var charCount = document.createElement('div');
        charCount.classList.add('char-count');
        charCount.textContent = '140字';
        textarea.addEventListener('input', function() {
            var textLength = textarea.value.length;
            if (textLength > 140) {
                textarea.value = textarea.value.substring(0, 140);
                textLength = 140;
            }
            charCount.textContent = (140 - textLength) + '字';
        });
        popover.appendChild(charCount);
        var cancelButton = document.createElement('button');
        cancelButton.textContent = '取消';
        cancelButton.classList.add('cancel-button');
        cancelButton.addEventListener('click', function () {
            popover.style.display = 'none';
        });
        var confirmButton = document.createElement('button');
        confirmButton.textContent = '确认';
        confirmButton.classList.add('confirm-button');
        var buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container1');
        popover.appendChild(buttonContainer);
        buttonContainer.appendChild(confirmButton);
        buttonContainer.appendChild(cancelButton);
        popover.appendChild(buttonContainer);
        confirmButton.addEventListener('click', function () {
            var text = textarea.value;
            var color = $('.color-picker').find('input').val();
            $.ajax({
                url: '/api/process_data/' + buttonId + '/',
                method: 'POST',
                data: {
                    'text': text,
                    'color': color,
                    'csrfmiddlewaretoken': '{{ csrf_token }}'
                },
                success: function (response) {
                    if (response.success) {
                        button.style.backgroundColor = color;
                    } else {
                        console.error('Error processing data:', response.error);
                    }
                },
                error: function (xhr, status, error) {
                    console.error('AJAX error:', error);
                }
            });
        });
        button.removeEventListener('mouseleave', function () {
            popover.style.display = 'none';
        });
        button.addEventListener('mouseleave', function () {
            clearTimeout(timeout);
        });
        popover.addEventListener('mouseover', function () {
            clearTimeout(timeout);
        });
    }
    document.body.addEventListener('mousemove', function (event) {
        var buttons = document.querySelectorAll('.button-grid button');
        var glowRadius = 20;
        buttons.forEach(function (button) {
            var buttonRect = button.getBoundingClientRect();
            var left = buttonRect.left;
            var top = buttonRect.top;
            var right = buttonRect.right;
            var bottom = buttonRect.bottom;
            if (event.clientX >= left - glowRadius && event.clientX <= right + glowRadius &&
                event.clientY >= top - glowRadius && event.clientY <= bottom + glowRadius) {
                button.classList.add('glow-button');
            } else {
                button.classList.remove('glow-button');
            }
        });
    });