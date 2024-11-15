var timeout;

// 为每个选项卡绑定点击事件
document.querySelectorAll('.tab-button').forEach(function(tab) {
    tab.addEventListener('click', function() {
        // 移除所有选项卡的激活状态
        document.querySelectorAll('.tab-button').forEach(function(tab) {
            tab.classList.remove('active');
        });
        // 移除所有内容的激活状态
        document.querySelectorAll('.tab-content').forEach(function(content) {
            content.classList.remove('active');
        });

        // 添加激活状态到当前点击的选项卡和对应的内容
        var tabId = this.id.replace('tab-', '');
        console.log(tabId)
        document.getElementById('content-' + tabId).classList.add('active');
        this.classList.add('active');
    });
});
$(document).ready(function(){
    $('#searchForm').submit(function(e){
        e.preventDefault(); // 防止表单提交
        var query = $('#searchInput').val();
        var csrftoken = $('input[name=csrfmiddlewaretoken]').val(); // 获取CSRF令牌
        $.ajax({
            url: '/search/', // 替换为你的搜索视图URL
            type: 'POST',
            data: { 'q': query },
            headers: {
                // 'csrfmiddlewaretoken': '{{ csrf_token }}',
                'X-CSRFToken': csrftoken
                 },
            success: function(data){
                $('#searchResults').empty();
                $.each(data, function(index, item){
                    $('#searchResults').append($('<li>').text(item.name));
                });
            }
        });
    });
});



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
        popover.style.top = (pageY - 170 ) + 'px';
        popover.style.left = (pageX) + 'px';
        var colorPicker = document.getElementById('colorPicker');
        var color = colorPicker.value;
        var textarea = document.createElement('textarea');
        var count_c = document.createElement('div');
        // count_c.id = buttonId + '-count'
        var count_cc = document.createElement('div');
        count_cc.textContent = '图层:';

        $.ajax({
            url: '/api/get_label_data/' + buttonId + '/',
            method: 'GET',
            data: {
                'buttonId': buttonId,
                // 'color': color,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.success) {
                    if (response.data[0]) {
                        textarea.placeholder = response.data[0];
                        count_c.textContent = response.data[1];
                        // count_c.id = buttonId + response.data[1];
                    }else {
                        count_c.textContent = response.data[1];
                        textarea.placeholder = '输入文本';
                        // count_c.id = buttonId + response.data[1];
                    }
                    if (response.data[1] >= 3) {
                        // 如果返回值大于等于3，禁用确认按钮
                        confirmButton.disabled = true;
                        confirmButton.classList.add('cancel-button');
                        textarea.disabled = true
                        textarea.readOnly = true;
                    } else {
                        // 如果返回值小于3，启用确认按钮
                        // confirmButton.disabled = false;
                        confirmButton.classList.add('confirm-button');
                    }
                } else {

                    console.error('Error get_label_data:', response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });


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

        var buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container1');
        count_c.classList.add('count-text');
        count_cc.classList.add('count-text');
        popover.appendChild(buttonContainer);
        buttonContainer.appendChild(confirmButton);
        buttonContainer.appendChild(cancelButton);
        buttonContainer.appendChild(count_cc);
        buttonContainer.appendChild(count_c);


        popover.appendChild(buttonContainer);
        confirmButton.addEventListener('click', function () {
        var text = textarea.value;
        var colorPicker = document.getElementById('colorPicker');
        var color = colorPicker.value;
        console.log('Selected color: ', color);
        var csrftoken = document.querySelector('input[name=csrfmiddlewaretoken]').value;

        $.ajax({
            url: '/api/process_data/' + buttonId + '/',
            method: 'POST',
            data: {
                'text': text,
                'color': color,
                // 'csrfmiddlewaretoken': '{{ csrf_token }}'
                'csrfmiddlewaretoken': csrftoken

            },
            success: function (response) {
                if (response.success) {
                    button.style.backgroundColor = color;
                    popover.style.display = 'none';
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
