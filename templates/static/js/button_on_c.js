$(document).ready(function () {
    $('.button-grid button').on('click', function () {
        var existingPopovers = $('.popover');
        existingPopovers.css('display', 'none');
        var buttonId = $(this).data('id');
        var labelData = '输入'
        console.log(buttonId)


        // 使用AJAX调用新的视图来获取与按钮ID关联的数据
        $.ajax({
            url: '/api/get_label_data/' + buttonId + '/', // 修改URL以匹配新的视图
            method: 'GET',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function (response) {
                if (response.success) {
                    // 使用返回的数据进行后续处理
                    labelData = response.data;
                    console.log(labelData)
                } else {
                    console.error('Error retrieving label data:', response.error);
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX error:', error);
            }
        });


        var popoverId = 'popover-' + buttonId;
        var popover = $('#' + popoverId);
        if (popover.length) {
            popover.remove();
        }
        popover = $('<div>').addClass('popover').attr('id', popoverId);
        $('body').append(popover);
        popover.css('display', 'block');
        var buttonRect = this.getBoundingClientRect();
        var pageX = buttonRect.left + this.offsetWidth ;
        var pageY = buttonRect.top + this.offsetHeight ;
        popover.css('top', (pageY - popover.outerHeight() / 2) + 'px');
        popover.css('left', (pageX - popover.outerWidth() / 2) + 'px');
        var textarea = $('<textarea>').text(labelData + '12s')
        // var textarea = $('<textarea>').attr('placeholder', '输入文本');
        popover.append(textarea);
        var charCount = $('<div>').addClass('char-count').text('140字');
        textarea.on('input', function () {
            var textLength = textarea.val().length;
            if (textLength > 140) {
                textarea.val(textarea.val().substring(0, 140));
                textLength = 140;
            }
            charCount.text((140 - textLength) + '字');
        });
        popover.append(charCount);
        var cancelButton = $('<button>').text('取消').addClass('cancel-button');
        cancelButton.on('click', function () {
            popover.css('display', 'none');
        });
        var confirmButton = $('<button>').text('确认').addClass('confirm-button');
        var buttonContainer = $('<div>').addClass('button-container1');
        // 创建颜色选择器元素
        var colorPicker = document.createElement('input');
        colorPicker.type = 'color';
        colorPicker.value = '#ffffff'; // 默认颜色为白色

        buttonContainer.append(confirmButton);
        buttonContainer.append(cancelButton);
        buttonContainer.append(colorPicker);

        popover.append(buttonContainer);

        confirmButton.on('click', function () {
            var text = textarea.val();
            var color = colorPicker.value; // 获取颜色选择器的值
            console.log(text)
            console.log(color)
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
                        $('#' + popoverId).css('display', 'none');
                        $('#' + buttonId).css('backgroundColor', color);
                    } else {
                        console.error('Error processing data:', response.error);
                    }
                },
                error: function (xhr, status, error) {
                    console.error('AJAX error:', error);
                }
            });
        });
    });

    $(document).on('mousemove', function (event) {
        var glowRadius = 20;
        $('.button-grid button').each(function () {
            var button = $(this);
            var buttonRect = this.getBoundingClientRect();
            var left = buttonRect.left;
            var top = buttonRect.top;
            var right = buttonRect.right;
            var bottom = buttonRect.bottom;
            if (event.clientX >= left - glowRadius && event.clientX <= right + glowRadius &&
                event.clientY >= top - glowRadius && event.clientY <= bottom + glowRadius) {
                button.addClass('glow-button');
            } else {
                button.removeClass('glow-button');
            }
        });
    });
});
